"""Grouped-block classification, balanced element representation and rarefaction."""
import json
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score,balanced_accuracy_score,f1_score
from joblib import Parallel,delayed
from common import *

def design(s,X):
    block=s.block_id.to_numpy()
    code=pd.Categorical(s.scene,categories=SCENES).codes
    present=X.getnnz(axis=1)>0
    pools={}
    rows=[]
    for name,idx in s.groupby("block_id",sort=True).indices.items():
        idx=np.asarray(idx);idx=idx[present[idx]]
        counts=[]
        for k in range(4):
            pools[(name,k)]=idx[code[idx]==k]
            counts.append(len(pools[(name,k)]))
        rows.append({"block_id":name,**dict(zip(SCENES,counts)),"used_per_form":min(min(counts),CONFIG["classifier_cap_per_form"])})
    availability=pd.DataFrame(rows)
    eligible=availability.loc[availability.used_per_form.gt(0),"block_id"].tolist()
    save(availability,"results/element_present_block_design.csv")
    return block,code,pools,availability,eligible

def summarize(frame,metrics):
    rows=[]
    for (q,n),z in frame.groupby(["cumulative_exposure","n_features"],sort=True):
        row={"cumulative_exposure":q,"n_features":n,"repeats":len(z)}
        for metric in metrics:
            x=z[metric].to_numpy(float)
            row.update({metric+"_mean":x.mean(),metric+"_sd":x.std(ddof=1),metric+"_q025":np.quantile(x,.025),metric+"_median":np.median(x),metric+"_q975":np.quantile(x,.975)})
        rows.append(row)
    return pd.DataFrame(rows)

def classifier(s,X,r,block,code,pools,eligible):
    repeats=CONFIG["classifier_repeats"];seed=CONFIG["classifier_seed"]
    threshold_counts={float(q):n_features(r,q) for q in CONFIG["thresholds"]}
    quota={b:min(min(len(pools[(b,k)]) for k in range(4)),CONFIG["classifier_cap_per_form"]) for b in eligible}
    ntrain=int(np.floor(CONFIG["train_block_share"]*len(eligible)))
    metrics=[];splits=[]
    for repeat in range(1,repeats+1):
        rng=np.random.default_rng(seed+repeat)
        shuffled=rng.permutation(np.asarray(eligible))
        train_blocks=set(shuffled[:ntrain])
        sampled=np.concatenate([rng.choice(pools[(b,k)],size=quota[b],replace=False) for b in eligible for k in range(4)])
        train=sampled[np.isin(block[sampled],list(train_blocks))]
        test=sampled[~np.isin(block[sampled],list(train_blocks))]
        assert not(set(block[train])&set(block[test]))
        assert np.unique(np.bincount(code[train],minlength=4)).size==1
        assert np.unique(np.bincount(code[test],minlength=4)).size==1
        def fit_one(q,n):
            model=SGDClassifier(loss="log_loss",penalty="l2",alpha=1e-5,max_iter=300,tol=1e-4,average=True,random_state=seed+repeat)
            model.fit(X[train,:n],code[train])
            pred=model.predict(X[test,:n])
            return {"repeat":repeat,"cumulative_exposure":q,"n_features":n,"n_train":len(train),"n_test":len(test),
                    "accuracy":accuracy_score(code[test],pred),"balanced_accuracy":balanced_accuracy_score(code[test],pred),
                    "macro_f1":f1_score(code[test],pred,average="macro",zero_division=0)}
        metrics.extend(Parallel(n_jobs=CONFIG["jobs"],prefer="threads")(delayed(fit_one)(q,n) for q,n in threshold_counts.items()))
        splits.extend({"repeat":repeat,"block_id":b,"set":"train" if b in train_blocks else "test","scenes_per_form":quota[b]} for b in eligible)
        if repeat==1 or repeat%5==0:
            save(pd.DataFrame(metrics),"results/classifier_repeat_metrics.csv")
            print(f"Classifier repeat {repeat}/{repeats}",flush=True)
    repeated=pd.DataFrame(metrics)
    full=repeated[repeated.cumulative_exposure.eq(1)].set_index("repeat").macro_f1
    repeated["chance_corrected_f1_recovery"]=(repeated.macro_f1-.25)/(repeated["repeat"].map(full)-.25)
    save(repeated,"results/classifier_repeat_metrics.csv")
    save(pd.DataFrame(splits),"results/classifier_block_splits.csv")
    save(summarize(repeated,["accuracy","balanced_accuracy","macro_f1","chance_corrected_f1_recovery"]),"figure_data/Fig1/Fig1d_equal_depth_element_present_sensitivity.csv")
    return {"eligible_blocks":len(eligible),"train_blocks":ntrain,"test_blocks":len(eligible)-ntrain,"repeats":repeats,"cap":CONFIG["classifier_cap_per_form"],"seed":seed}

def representation(s,X,r,pools,eligible):
    h=n_features(r,.8);X=X[:,:h];names=r.head(h).element.to_numpy()
    quota={b:min(min(len(pools[(b,k)]) for k in range(4)),CONFIG["classifier_cap_per_form"]) for b in eligible}
    per_form=sum(quota.values());repeats=CONFIG["representation_repeats"]
    prevalence=np.empty((repeats,4,h),dtype=np.float32)
    logratio=np.empty_like(prevalence)
    dominant=np.empty((repeats,h),dtype=np.int8)
    for repeat in range(repeats):
        rng=np.random.default_rng(CONFIG["representation_seed"]+repeat)
        counts=np.empty((4,h),dtype=float)
        for k in range(4):
            sample=np.concatenate([rng.choice(pools[(b,k)],size=quota[b],replace=False) if quota[b]<len(pools[(b,k)]) else pools[(b,k)] for b in eligible])
            counts[k]=np.asarray(X[sample].sum(axis=0)).ravel()
        prevalence[repeat]=counts/per_form
        smooth=(counts+.5)/(per_form+1)
        for k in range(4):
            other=(counts.sum(axis=0)-counts[k]+.5)/(3*per_form+1)
            logratio[repeat,k]=np.log2(smooth[k]/other)
        dominant[repeat]=np.argmax(prevalence[repeat],axis=0)
    mode=[];stability=[]
    for j in range(h):
        tally=np.bincount(dominant[:,j],minlength=4);m=int(np.argmax(tally));mode.append(SCENES[m]);stability.append(tally[m]/repeats)
    rows=[]
    for k,form in enumerate(SCENES):
        rows.append(pd.DataFrame({"depth":"cap_50","n_per_scene_form":per_form,"repeats":repeats,"element":names,"scene_type":form,
             "prevalence_median":np.median(prevalence[:,k,:],axis=0),"prevalence_q025":np.quantile(prevalence[:,k,:],.025,axis=0),"prevalence_q975":np.quantile(prevalence[:,k,:],.975,axis=0),
             "log2_prevalence_ratio_median":np.median(logratio[:,k,:],axis=0),"log2_prevalence_ratio_q025":np.quantile(logratio[:,k,:],.025,axis=0),"log2_prevalence_ratio_q975":np.quantile(logratio[:,k,:],.975,axis=0),
             "modal_dominant_scene":mode,"dominant_scene_stability":stability}))
    summary=pd.concat(rows,ignore_index=True)
    save(summary,"results/equal_depth_element_representation.csv")
    pooled=summary.pivot(index="element",columns="scene_type",values="prevalence_median").mean(axis=1)
    candidates=[];anchors=[]
    for form in SCENES:
        z=summary[summary.scene_type.eq(form)].copy()
        z["pooled_prevalence"]=z.element.map(pooled)
        z=z[z.modal_dominant_scene.eq(form)&z.pooled_prevalence.ge(.005)&z.dominant_scene_stability.ge(.8)]
        z=z.sort_values(["log2_prevalence_ratio_median","pooled_prevalence","element"],ascending=[False,False,True])
        candidates.append(z.head(15));anchors.extend(z.head(3).element)
    save(pd.concat(candidates),"results/stable_element_candidates.csv")
    panel=summary[summary.element.isin(anchors)].copy()
    panel["element_order"]=pd.Categorical(panel.element,categories=anchors,ordered=True).codes
    panel["scene_order"]=pd.Categorical(panel.scene_type,categories=SCENES,ordered=True).codes
    save(panel.sort_values(["element_order","scene_order"]),"figure_data/Fig1/Fig1c_anchor_element_matrix.csv")
    print("Balanced element representation completed.",flush=True)

def rarefaction(s,X,pools,availability):
    depths=CONFIG["rarefaction_depths"]
    counts=pd.crosstab(s.block_id,s.scene).reindex(columns=SCENES,fill_value=0)
    eligible=counts.loc[counts.min(axis=1).ge(max(depths))].index.tolist()
    role_free_design=counts.reset_index()
    role_free_design["eligible"]=role_free_design.block_id.isin(eligible)
    save(role_free_design,"results/rarefaction_block_design.csv")
    all_pools={}
    scene_codes=pd.Categorical(s.scene,categories=SCENES).codes
    for name,idx in s.groupby("block_id",sort=True).indices.items():
        idx=np.asarray(idx)
        for k in range(4):
            all_pools[(name,k)]=idx[scene_codes[idx]==k]
    n=len(eligible);upper=np.triu_indices(n,1)
    rng=np.random.default_rng(CONFIG["rarefaction_seed"]);rows=[]
    # Sparse binary union vectors give exact set-intersection and set-union counts.
    for repeat in range(CONFIG["rarefaction_repeats"]):
        for depth in depths:
            for k,form in enumerate(SCENES):
                rr=[];cc=[]
                for i,b in enumerate(eligible):
                    selected=rng.choice(all_pools[(b,k)],size=depth,replace=False)
                    items=np.unique(X[selected].indices)
                    rr.extend([i]*len(items));cc.extend(items)
                unions=csr_matrix((np.ones(len(cc),dtype=np.int32),(rr,cc)),shape=(n,X.shape[1]))
                sizes=np.asarray(unions.getnnz(axis=1))
                intersection=(unions@unions.T).toarray()
                denom=sizes[:,None]+sizes[None,:]-intersection
                jaccard=np.divide(intersection,denom,out=np.zeros_like(intersection,dtype=float),where=denom>0)
                rows.append({"replicate":repeat,"depth":depth,"scene_type":form,"mean_jaccard":jaccard[upper].mean()})
        if (repeat+1)%10==0:print(f"Rarefaction repeat {repeat+1}/{CONFIG['rarefaction_repeats']}",flush=True)
    repeated=pd.DataFrame(rows)
    save(repeated,"results/jaccard_rarefaction_replicates.csv")
    summary=repeated.groupby(["depth","scene_type"]).mean_jaccard.agg(mean="mean",sd="std",q025=lambda x:x.quantile(.025),q975=lambda x:x.quantile(.975)).reset_index()
    save(summary,"figure_data/Fig1/Fig1e_equal_depth_jaccard.csv")
    return {"eligible_blocks":n,"pairs_per_repeat":n*(n-1)//2,"depths":depths,"repeats":CONFIG["rarefaction_repeats"],"seed":CONFIG["rarefaction_seed"]}

def main():
    s,e,b,blocks=load()
    e=enrich(e,s,blocks);r=rank(e)
    X=matrix(s,e,r)
    block,code,pools,availability,eligible=design(s,X)
    representation(s,X,r,pools,eligible)
    rare=rarefaction(s,X,pools,availability)
    cls=classifier(s,X,r,block,code,pools,eligible)
    (ROOT/"results/resampling_design.json").write_text(json.dumps({"classifier":cls,"rarefaction":rare},indent=2),encoding="utf-8")
if __name__=="__main__":main()
