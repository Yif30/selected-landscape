"""Shared data loading and duration-weighted estimators."""
from pathlib import Path
from itertools import combinations
import json
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parents[1]
SCENES=["S1","S2","S3","S4"]
CATEGORIES=["Architecture","Natural features","Street infrastructure","Landscape decoration","Commercial signage","Consumption interfaces","Display facilities"]
BEHAVIORS=["Digital production","Performance","Consumption","Social interaction","Rest","Movement"]
CONFIG=json.loads((ROOT/"config/analysis.json").read_text(encoding="utf-8"))
def read(path,**kw):
    return pd.read_csv(ROOT/path,encoding="utf-8-sig",**kw)
def save(df,path,index=False):
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(target,index=index,encoding="utf-8-sig")
def load():
    s=read("data/scenes.csv",dtype={"scene_id":str,"video_id":str,"block_id":str})
    e=read("data/environment.csv",dtype={"scene_id":str,"element_id":str})
    b=read("data/behaviors.csv",dtype={"scene_id":str,"behavior_id":str})
    blocks=read("data/blocks.csv",dtype={"block_id":str})
    videos=read("data/videos.csv",dtype={"video_id":str,"source_video_id":str,"block_id":str})
    assert s.video_id.isin(videos.video_id).all() and videos.video_id.is_unique
    assert s.scene_id.is_unique and blocks.block_id.is_unique
    assert s.scene.isin(SCENES).all()
    assert s.duration_seconds.ge(0).all()
    assert e.category.isin(CATEGORIES).all()
    assert not e.duplicated(["scene_id","element_id"]).any()
    assert e.scene_id.isin(s.scene_id).all() and b.scene_id.isin(s.scene_id).all()
    assert b.role.isin(["focal","background"]).all()
    assert b.behavior_code.isin(range(1,7)).all()
    presence=s.set_index("scene_id")
    for role,column in [("focal","has_focal"),("background","has_background")]:
        role_scenes=b.loc[b.role.eq(role),"scene_id"].unique()
        assert presence.loc[role_scenes,column].eq(1).all()
    return s,e,b,blocks
def enrich(d,s,blocks):
    d=d.merge(s[["scene_id","video_id","block_id","scene","start_seconds","duration_seconds"]],on="scene_id",validate="many_to_one")
    return d.merge(blocks[["block_id","province"]],on="block_id",validate="many_to_one")
def rank(e):
    r=e.groupby(["element_id","element"],as_index=False).duration_seconds.sum()
    r=r.sort_values(["duration_seconds","element_id"],ascending=[False,True]).reset_index(drop=True)
    r=r.rename(columns={"duration_seconds":"duration"})
    r["rank"]=np.arange(1,len(r)+1)
    r["element_share"]=r["rank"]/len(r)
    r["exposure_share"]=r.duration/r.duration.sum()
    r["cum_exposure_share"]=r.exposure_share.cumsum()
    return r
def n_features(r,q):
    if q>=1:return len(r)
    if q<=0:return 0
    return min(len(r),int(np.searchsorted(r.cum_exposure_share.to_numpy(),q))+1)
def gini(x):
    x=np.sort(np.asarray(x,float));n=len(x)
    return float(np.dot(2*np.arange(1,n+1)-n-1,x)/(n*x.sum())) if n and x.sum()>0 else np.nan
def composition(d,group,key,columns):
    p=d.groupby([group,key]).duration_seconds.sum().unstack(fill_value=0).reindex(columns=columns,fill_value=0)
    return p.div(p.sum(axis=1),axis=0)
def pairs(p,domain):
    rows=[]
    for a,b in combinations(p.index,2):
        tvd=float(np.abs(p.loc[a].to_numpy()-p.loc[b].to_numpy()).sum()/2)
        rows.append({"domain":domain,"province_a":a,"province_b":b,"similarity":1-tvd,"tvd":tvd})
    return pd.DataFrame(rows)
def edges(p,nearest=2,farthest=1):
    rows=[]
    for province in sorted(set(p.province_a)|set(p.province_b)):
        local=p[p.province_a.eq(province)|p.province_b.eq(province)]
        rows.extend([local.nsmallest(nearest,"tvd").assign(edge_type="similar"),local.nlargest(farthest,"tvd").assign(edge_type="dissimilar")])
    return pd.concat(rows,ignore_index=True).drop_duplicates(["province_a","province_b","edge_type"]).sort_values(["edge_type","province_a","province_b"])
def matrix(s,e,r):
    scene_index=pd.Series(np.arange(len(s)),index=s.scene_id)
    column_index=pd.Series(np.arange(len(r)),index=r.element_id)
    rows=e.scene_id.map(scene_index).to_numpy()
    cols=e.element_id.map(column_index).to_numpy()
    return coo_matrix((np.ones(len(e),dtype=np.float32),(rows,cols)),shape=(len(s),len(r))).tocsr()
