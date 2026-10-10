"""Compute exposure, provincial compositions and role-observation transitions."""
from itertools import combinations
import json
import numpy as np
import pandas as pd
from pyproj import Transformer
from common import *

def main():
    s,e,b,blocks=load()
    e=enrich(e,s,blocks);b=enrich(b,s,blocks)
    sp=s.merge(blocks[["block_id","province"]],on="block_id",validate="many_to_one")
    overall=s.groupby("scene").duration_seconds.agg(["sum","size"]).reindex(SCENES)
    overall["duration_share"]=overall["sum"]/overall["sum"].sum()
    overall["count_share"]=overall["size"]/overall["size"].sum()
    save(overall.reset_index().rename(columns={"scene":"scene_type"}),"figure_data/Fig1/Fig1a_overall_scene_duration_share.csv")
    block_scene=composition(s,"block_id","scene",SCENES)
    coords=blocks.rename(columns={"longitude_wgs84":"lon","latitude_wgs84":"lat"})
    points=coords[["block_id","province","lon","lat"]].merge(block_scene.reset_index(),on="block_id",validate="one_to_one")
    projection=Transformer.from_crs("EPSG:4326","+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +ellps=GRS80 +units=m +no_defs",always_xy=True)
    points["x_aea_m"],points["y_aea_m"]=projection.transform(points.lon.to_numpy(),points.lat.to_numpy())
    save(points,"figure_data/Fig1/Fig1b_projected_blocks.csv")
    for direction,width in [("longitude",4),("latitude",3)]:
        coordinate="lon" if direction=="longitude" else "lat"
        v=points.copy();v["bin"]=np.floor(v[coordinate]/width)*width+width/2
        rows=[]
        for form in SCENES:
            for center,z in v.groupby("bin",sort=True):
                rows.append({"scene":form,"bin":center,"mean":z[form].mean(),"q25":z[form].quantile(.25),"q75":z[form].quantile(.75),"n":len(z),"projected_position":z["x_aea_m" if direction=="longitude" else "y_aea_m"].median()})
        save(pd.DataFrame(rows),f"figure_data/Fig1/Fig1b_{direction}_scene_profiles.csv")
    scene_pairs=pairs(composition(sp,"province","scene",SCENES),"Scene")
    save(scene_pairs,"figure_data/Fig1/Fig1b_province_scene_tvd_all_pairs.csv")
    save(edges(scene_pairs,nearest=2,farthest=2),"figure_data/Fig1/Fig1b_province_extreme_edges.csv")
    ranking=rank(e);save(ranking,"results/element_exposure_ranking.csv")
    hn=n_features(ranking,.8);heads=set(ranking.head(hn).element_id)
    curve=pd.DataFrame({"cumulative_exposure":np.linspace(0,1,201)})
    curve["n_features"]=[n_features(ranking,q) for q in curve.cumulative_exposure]
    save(curve,"figure_data/Fig1/Fig1d_cumulative_vocabulary_curve.csv")
    summaries=[];curves=[]
    for category in CATEGORIES:
        r=rank(e[e.category.eq(category)])
        h=n_features(r,.8)
        summaries.append({"category":category,"n":len(r),"n80":h,"head_share":h/len(r),"gini":gini(r.duration)})
        r["category"]=category
        sampled=np.unique(np.rint(np.geomspace(1,len(r),120)).astype(int)-1)
        curves.append(r.iloc[sampled])
    save(pd.DataFrame(summaries),"figure_data/Fig2/Fig2a_category_gini_h80.csv")
    save(pd.concat(curves,ignore_index=True),"figure_data/Fig2/Fig2a_category_curve_samples.csv")
    full=e.groupby("category").duration_seconds.sum().reindex(CATEGORIES,fill_value=0)
    head=e[e.element_id.isin(heads)].groupby("category").duration_seconds.sum().reindex(CATEGORIES,fill_value=0)
    fdi=pd.DataFrame({"category":CATEGORIES,"full_share":(full/full.sum()).values,"head_share":(head/head.sum()).values})
    fdi["fdi"]=fdi.head_share-fdi.full_share
    save(fdi,"figure_data/Fig2/Fig2b_functional_reweighting.csv")
    category_comp=composition(e,"province","category",CATEGORIES)
    category_pairs=pairs(category_comp,"Environment")
    item_comp=composition(e,"province","element_id",ranking.element_id.tolist())
    item_pairs=pairs(item_comp,"Element items")
    save(category_comp.reset_index(),"results/province_environment_composition.csv")
    save(category_pairs,"figure_data/Fig2/Fig2e_category_pair_similarity.csv")
    save(item_pairs,"figure_data/Fig2/Fig2f_item_pair_similarity.csv")
    save(edges(item_pairs),"figure_data/Fig2/Fig2c_displayed_item_similarity_edges.csv")
    selections=[];rings=[]
    for resolution,pr in [("seven_categories",category_pairs),("all_items",item_pairs)]:
        row=pr.loc[pr.tvd.idxmax()]
        selections.append({"selection_resolution":resolution,"province_a":row.province_a,"province_b":row.province_b,"similarity":row.similarity,"tvd":row.tvd,"display_resolution":"seven_categories"})
        for province in [row.province_a,row.province_b]:
            for cat in CATEGORIES:
                rings.append({"selection_resolution":resolution,"selection_tvd":row.tvd,"province":province,"category":cat,"share":category_comp.loc[province,cat]})
    save(pd.DataFrame(selections),"figure_data/Fig2/Fig2d_selected_pair_summary.csv")
    save(pd.DataFrame(rings),"figure_data/Fig2/Fig2d_selected_pair_category_compositions.csv")
    block_gini=e.groupby(["block_id","element_id"]).duration_seconds.sum().groupby(level=0).agg(gini)
    nodes=points.groupby("province",as_index=False).agg(lon=("lon","mean"),lat=("lat","mean"),block_count=("block_id","size"))
    nodes["mean_gini"]=nodes.province.map(points.assign(gini=points.block_id.map(block_gini)).groupby("province").gini.mean())
    nodes["x_aea_m"],nodes["y_aea_m"]=projection.transform(nodes.lon,nodes.lat)
    save(nodes,"figure_data/Fig2/Fig2c_province_nodes.csv")
    bc=b.groupby(["role","behavior_code"]).duration_seconds.sum().rename("duration").reset_index()
    bc["share"]=bc.duration/bc.groupby("role").duration.transform("sum")
    save(bc.rename(columns={"role":"analysis_role","behavior_code":"behaviour_code"}),"figure_data/Fig3/Fig3a_role_behaviour_composition.csv")
    fn=b.groupby(["role","function"]).duration_seconds.sum().rename("duration").reset_index()
    fn["share"]=fn.duration/fn.groupby("role").duration.transform("sum")
    save(fn,"results/role_function_composition.csv")
    output=[]
    for role in ["focal","background"]:
        for measure,cur in [("count",b),("duration",b)]:
            z=cur[cur.role.eq(role)]
            val=z.function.eq("media_oriented").mean() if measure=="count" else z.loc[z.function.eq("media_oriented"),"duration_seconds"].sum()/z.duration_seconds.sum()
            output.append({"role":role,"measure":measure,"media_oriented_share":val})
    save(pd.DataFrame(output),"figure_data/Fig3/Fig3a_role_function_composition.csv")
    b["state"]=b.behavior_code.astype(str)
    mask=b.behavior_code.isin([1,2])
    b.loc[mask,"state"]=b.loc[mask,"state"]+"_"+b.loc[mask,"function"]
    transition_support=[]
    for role in ["focal","background"]:
        z=b[b.role.eq(role)]
        groups=z.groupby(["video_id","start_seconds","scene_id"],sort=True).state.agg(lambda x:sorted(set(x))).reset_index(name="states")
        mass=np.zeros((6,6));n=0
        for _,video in groups.groupby("video_id",sort=True):
            seq=video.sort_values(["start_seconds","scene_id"]).states.tolist()
            for a,c in zip(seq[:-1],seq[1:]):
                n+=1
                for source in a:
                    for target in c:mass[int(source[0])-1,int(target[0])-1]+=1/(len(a)*len(c))
        outgoing=mass.sum(axis=1)
        probability=np.divide(mass,outgoing[:,None],out=np.zeros_like(mass),where=outgoing[:,None]>0)
        assert np.isclose(mass.sum(),n)
        tab=pd.DataFrame(probability,index=range(1,7),columns=range(1,7))
        save(tab.reset_index(names="origin"),f"figure_data/Fig3/Fig3c_{role}_transition.csv")
        for i in range(6):transition_support.append({"role":role,"behavior_code":i+1,"outgoing_weight":outgoing[i],"role_observation_pairs":n})
    save(pd.DataFrame(transition_support),"results/transition_support.csv")
    b["role_function"]=b.role+"_"+b.function
    role_comp=composition(b,"province","role_function",["focal_media_oriented","focal_everyday_practice","background_media_oriented","background_everyday_practice"])
    behavior_comp=composition(b,"province","behavior_code",list(range(1,7)))
    behavior_comp.columns=["behavior_share_"+str(i) for i in range(1,7)]
    save(behavior_comp.reset_index(),"results/province_behavior_composition.csv")
    behavior_pairs=pairs(behavior_comp,"Human")
    save(role_comp.reset_index(),"results/province_role_function_composition.csv")
    save(behavior_pairs,"figure_data/Fig3/Fig3d_province_pair_behaviour_similarity.csv")
    save(edges(behavior_pairs,nearest=1,farthest=1),"figure_data/Fig3/Fig3d_displayed_behaviour_similarity_edges.csv")
    main=b[b.role.eq("focal")]
    main_total=main.groupby("block_id").duration_seconds.sum()
    main_media=main[main.function.eq("media_oriented")].groupby("block_id").duration_seconds.sum()
    block_media=(main_media/main_total).fillna(0)
    province_media=blocks.assign(focal_media_share=blocks.block_id.map(block_media)).groupby("province").focal_media_share.mean()
    nodes3=nodes.drop(columns="mean_gini").copy()
    nodes3["focal_media_share"]=nodes3.province.map(province_media)
    save(nodes3,"figure_data/Fig3/Fig3d_province_nodes.csv")
    scientific={"environment_vocabulary":len(ranking),"environment_exposure_seconds":e.duration_seconds.sum(),"global_gini":gini(ranking.duration),"head80_elements":hn,"head80_vocabulary_share":hn/len(ranking),"head80_exposure_share":ranking.iloc[hn-1].cum_exposure_share}
    (ROOT/"results/environment_concentration.json").write_text(json.dumps(scientific,indent=2),encoding="utf-8")
    print("Duration-weighted descriptive estimates completed.",flush=True)
if __name__=="__main__":main()
