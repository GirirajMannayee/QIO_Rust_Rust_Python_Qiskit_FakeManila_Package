import numpy as np, pandas as pd, json, warnings
warnings.filterwarnings('ignore')
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit_aer import AerSimulator
from qiskit.quantum_info import hellinger_fidelity
B=FakeManilaV2();noisy=AerSimulator.from_backend(B);ideal=AerSimulator()
SH=4096;NS=20
def run(qc,sim,shots,seed):
    return sim.run(qc,shots=shots,seed_simulator=seed).result().get_counts()
def tp(qc,layout=None,opt=1):
    pm=generate_preset_pass_manager(backend=B,optimization_level=opt,initial_layout=layout,seed_transpiler=7);return pm.run(qc)
def bell(psi=False):
    qc=QuantumCircuit(2);qc.h(0);qc.cx(0,1)
    if psi:qc.x(1)
    qc.measure_all();return qc
def norm(c):
    t=sum(c.values());return {k.replace(' ',''):v/t for k,v in c.items()}
def tvd(p,q):
    ks=set(p)|set(q);return 0.5*sum(abs(p.get(k,0)-q.get(k,0)) for k in ks)
out={}
# E1: pair placement, Phi+ and Psi+
rows=[]
for psi in [False,True]:
    good=['01','10'] if psi else ['00','11']
    for pair in [(0,1),(1,2),(2,3),(3,4)]:
        t=tp(bell(psi),list(pair),1)
        ops=t.count_ops();pc=[]
        for s in range(NS):
            c=norm(run(t,noisy,SH,100+s));pc.append(sum(c.get(k,0) for k in good))
        idl={k:(0.5 if k in good else 0) for k in ['00','01','10','11']}
        # mean dist for hellinger
        agg={}
        for s in range(NS):
            for k,v in norm(run(t,noisy,SH,500+s)).items():agg[k]=agg.get(k,0)+v/NS
        rows.append(dict(state='Psi+' if psi else 'Phi+',pair=f'{pair[0]}-{pair[1]}',depth=t.depth(),cx=ops.get('cx',0),sx=ops.get('sx',0),rz=ops.get('rz',0),
            p_mean=np.mean(pc),p_sd=np.std(pc,ddof=1),p_lo=np.mean(pc)-2.093*np.std(pc,ddof=1)/np.sqrt(NS),p_hi=np.mean(pc)+2.093*np.std(pc,ddof=1)/np.sqrt(NS),
            hf=hellinger_fidelity(agg,{k:v for k,v in idl.items() if v>0})))
e1=pd.DataFrame(rows);e1.to_csv('qk_e1.csv',index=False);print(e1.round(4).to_string())
# E2: opt levels on default layout
rows=[]
for opt in [0,1,2,3]:
    t=tp(bell(),None,opt);ops=t.count_ops();pc=[]
    for s in range(NS):
        c=norm(run(t,noisy,SH,900+s));pc.append(c.get('00',0)+c.get('11',0))
    rows.append(dict(opt=opt,depth=t.depth(),cx=ops.get('cx',0),size=t.size(),layout=str([t.layout.final_index_layout()[i] for i in range(2)] if t.layout else None),p_mean=np.mean(pc),p_sd=np.std(pc,ddof=1)))
e2=pd.DataFrame(rows);e2.to_csv('qk_e2.csv',index=False);print(e2.round(4).to_string())
# E3: shots convergence TVD vs ideal (pair 3-4 best? use default opt1 layout)
t=tp(bell(),[3,4],1);rows=[]
ref=norm(run(t,noisy,2_000_000,1))
for sh in [64,128,256,512,1024,2048,4096,8192,16384]:
    v=[tvd(norm(run(t,noisy,sh,2000+s)),ref) for s in range(NS)];vi=[tvd(norm(run(bell(),ideal,sh,2000+s)),{'00':.5,'11':.5}) for s in range(NS)]
    rows.append(dict(shots=sh,tvd_noisy=np.mean(v),sd_noisy=np.std(v,ddof=1),tvd_ideal=np.mean(vi),sd_ideal=np.std(vi,ddof=1)))
e3=pd.DataFrame(rows);e3.to_csv('qk_e3.csv',index=False);print(e3.round(4).to_string());print('ref',ref)
# E4: 5-qubit grasp circuit (x,y,z,roll,pitch); H, Ry(0.5 rad), CX(1,3),CX(2,4), measure -- ideal probs from statevector
from qiskit.quantum_info import Statevector
def grasp5(theta):
    qc=QuantumCircuit(5)
    for q in range(5):qc.h(q)
    for q in range(5):qc.ry(theta,q)
    qc.cx(1,3);qc.cx(2,4)
    return qc
rows=[]
for th in [0.05,0.5,1.0]:
    base=grasp5(th);sv=Statevector(base).probabilities_dict()
    m=base.copy();m.measure_all();t=tp(m,[0,1,2,3,4],1);ops=t.count_ops()
    hf=[];tv=[]
    for s in range(NS):
        c=norm(run(t,noisy,SH,3000+s));hf.append(hellinger_fidelity(c,sv));tv.append(tvd(c,sv))
    # ideal sampling baseline (finite shot only)
    mi=base.copy();mi.measure_all()
    hfi=[hellinger_fidelity(norm(run(mi,ideal,SH,3000+s)),sv) for s in range(NS)];tvi=[tvd(norm(run(mi,ideal,SH,3000+s)),sv) for s in range(NS)]
    rows.append(dict(theta=th,depth=t.depth(),cx=ops.get('cx',0),hf_noisy=np.mean(hf),hf_sd=np.std(hf,ddof=1),tvd_noisy=np.mean(tv),tvd_sd=np.std(tv,ddof=1),hf_ideal=np.mean(hfi),tvd_ideal=np.mean(tvi)))
e4=pd.DataFrame(rows);e4.to_csv('qk_e4.csv',index=False);print(e4.round(4).to_string())
# E5: single-qubit amplitude calibration: Ry(phi) -> P(1)=sin^2(phi/2), each physical qubit
phis=np.linspace(0,np.pi,13);rows=[]
for q in range(5):
    for phi in phis:
        qc=QuantumCircuit(1);qc.ry(phi,0);qc.measure_all();t=tp(qc,[q],1)
        v=[norm(run(t,noisy,SH,4000+s)).get('1',0) for s in range(10)]
        rows.append(dict(qubit=q,phi=phi,p_target=np.sin(phi/2)**2,p_noisy=np.mean(v),sd=np.std(v,ddof=1)))
e5=pd.DataFrame(rows);e5.to_csv('qk_e5.csv',index=False)
e5['err']=e5.p_noisy-e5.p_target
print(e5.groupby('qubit').apply(lambda g:pd.Series(dict(mae=g.err.abs().mean(),bias0=g[g.phi==0].p_noisy.iloc[0],bias1=1-g[g.phi==np.pi].p_noisy.iloc[0]))).round(4))
# E6 six qubit: ideal only, show cannot map to 5q backend
try:
    qc=QuantumCircuit(6);qc.measure_all();tp(qc,None,1)
except Exception as e:print('6q error:',type(e).__name__,str(e)[:120])
