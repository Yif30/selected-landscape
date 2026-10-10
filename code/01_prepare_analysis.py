"""Derive scene-category shares and scene-role-function regression observations."""
import numpy as np
import pandas as pd
from common import ROOT,SCENES,CATEGORIES,load,enrich,save

def main():
    s,e,b,blocks=load()
    counts=pd.crosstab(e.scene_id,e.category).reindex(index=s.scene_id,columns=CATEGORIES,fill_value=0).fillna(0)
    total=counts.sum(axis=1)
    shares=counts.div(total.replace(0,np.nan),axis=0).fillna(0)
    shares.columns=["category_share_"+str(i) for i in range(1,8)]
    shares=shares.reset_index()
    save(shares,"results/scene_environment_shares.csv")
    regression=b.drop_duplicates(["scene_id","role","function"])[["scene_id","role","function"]]
    regression=enrich(regression,s,blocks).merge(shares,on="scene_id",validate="many_to_one")
    regression["log_duration"]=np.log1p(regression.duration_seconds)
    regression["is_media"]=regression.function.eq("media_oriented").astype(int)
    save(regression,"results/role_model_input.csv")
    print(f"Prepared {len(regression):,} scene-role-function records.",flush=True)
if __name__=="__main__":main()
