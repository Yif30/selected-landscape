"""Plot quantitative panels from figure_data without video frames or boundary files."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from common import ROOT,SCENES,CATEGORIES,BEHAVIORS,read
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Microsoft YaHei","Arial","DejaVu Sans"],"font.size":9,"axes.spines.top":False,"axes.spines.right":False,"pdf.fonttype":42,"svg.fonttype":"none"})
SC=["#4B799B","#AB6848","#71865A","#8C759C"]
CC=["#9B8F86","#A8B48A","#8FA1B3","#C3A6A0","#D1A36F","#B99174","#8E7E95"]
BC=["#B78274","#A56A6E","#C8A47A","#92A58F","#A79F96","#7E98A6"]
def frame(figure,file):return read(f"figure_data/{figure}/{file}.csv")
def store(fig,name,out):
    fig.tight_layout()
    for ext in ["png","pdf","svg"]:fig.savefig(out/f"{name}.{ext}",dpi=300)
    plt.close(fig)
def network(nodes,edges,value,ax):
    lookup=nodes.set_index("province")
    for r in edges.itertuples():
        a,c=lookup.loc[r.province_a],lookup.loc[r.province_b]
        ax.plot([a.lon,c.lon],[a.lat,c.lat],color="#B66B44" if r.edge_type=="similar" else "#476E99",alpha=.28,lw=.7,zorder=0)
    image=ax.scatter(nodes.lon,nodes.lat,c=nodes[value],s=15+nodes.block_count*5,cmap="viridis",edgecolors="white",linewidth=.5)
    ax.set(xlabel="Longitude (°E)",ylabel="Latitude (°N)")
    return image
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=ROOT/"figures")
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    d=frame("Fig1","Fig1a_overall_scene_duration_share")
    fig,ax=plt.subplots(figsize=(5,3));ax.bar(d.scene_type,d.duration_share,color=SC);ax.set(ylabel="Scene-duration share")
    store(fig,"Fig1a_scene_composition",out)
    d=frame("Fig1","Fig1b_projected_blocks")
    fig,axes=plt.subplots(2,2,figsize=(8,6))
    for form,ax in zip(SCENES,axes.flat):
        sc=ax.scatter(d.lon,d.lat,c=d[form],s=14,cmap="viridis",vmin=0,vmax=1);ax.set(title=form,xlabel="Longitude (°E)",ylabel="Latitude (°N)");fig.colorbar(sc,ax=ax,label="Duration share")
    store(fig,"Fig1b_block_scene_locations",out)
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    for direction,ax in zip(["longitude","latitude"],axes):
        d=frame("Fig1",f"Fig1b_{direction}_scene_profiles")
        for form,color in zip(SCENES,SC):
            z=d[d.scene.eq(form)].sort_values("bin");ax.fill_between(z.bin.to_numpy(float),z.q25.to_numpy(float),z.q75.to_numpy(float),color=color,alpha=.12);ax.plot(z.bin,z["mean"],color=color,label=form)
        ax.set(xlabel=direction.title()+" (degrees)",ylabel="Block scene-duration share");ax.legend()
    store(fig,"Fig1b_geographic_profiles",out)
    d=frame("Fig1","Fig1c_anchor_element_matrix")
    names=d.sort_values("element_order").element.drop_duplicates().tolist()
    fig,ax=plt.subplots(figsize=(6,max(4,len(names)*.3)))
    for row in d.itertuples():
        ax.scatter(SCENES.index(row.scene_type),names.index(row.element),s=20+700*row.prevalence_median,c=[row.log2_prevalence_ratio_median],cmap="RdBu_r",norm=TwoSlopeNorm(vcenter=0,vmin=-4,vmax=4),edgecolors="white",linewidth=.3)
    ax.set_xticks(range(4),SCENES);ax.set_yticks(range(len(names)),names);ax.invert_yaxis();ax.set(xlabel="Scene form")
    fig.colorbar(plt.cm.ScalarMappable(norm=TwoSlopeNorm(vcenter=0,vmin=-4,vmax=4),cmap="RdBu_r"),ax=ax,label="log2 prevalence ratio")
    store(fig,"Fig1c_element_representation",out)
    d=frame("Fig1","Fig1d_equal_depth_element_present_sensitivity");v=frame("Fig1","Fig1d_cumulative_vocabulary_curve")
    fig,ax=plt.subplots(figsize=(6,4))
    for metric,color in [("accuracy","#2F6F91"),("macro_f1","#9A6B2F")]:
        x=100*d.cumulative_exposure;ax.fill_between(x.to_numpy(float),d[metric+"_q025"].to_numpy(float),d[metric+"_q975"].to_numpy(float),color=color,alpha=.12);ax.plot(x,d[metric+"_mean"],"o-",ms=3,color=color,label=metric)
    ax.axhline(.25,color="gray",ls="--",lw=.6);ax.set(xlabel="Cumulative element exposure (%)",ylabel="Out-of-block performance",xlim=(0,100));ax.legend(loc="upper left")
    other=ax.twinx();v=v[v.n_features.gt(0)];other.plot(100*v.cumulative_exposure,v.n_features,"--",color="gray");other.set(yscale="log",ylabel="Element vocabulary size")
    store(fig,"Fig1d_classifier",out)
    d=frame("Fig1","Fig1e_equal_depth_jaccard")
    fig,ax=plt.subplots(figsize=(5,3.5))
    for form,color in zip(SCENES,SC):
        z=d[d.scene_type.eq(form)];ax.fill_between(z.depth.to_numpy(float),z.q025.to_numpy(float),z.q975.to_numpy(float),color=color,alpha=.12);ax.plot(z.depth,z["mean"],"o-",color=color,label=form)
    ax.set(xlabel="Scenes per block and form",ylabel="Mean pairwise Jaccard");ax.legend()
    store(fig,"Fig1e_rarefaction",out)
    d=frame("Fig2","Fig2a_category_curve_samples");g=frame("Fig2","Fig2a_category_gini_h80")
    fig,axes=plt.subplots(2,4,figsize=(12,6))
    for category,color,ax in zip(CATEGORIES,CC,axes.flat):
        z=d[d.category.eq(category)];ax.plot(100*z.element_share,z.cum_exposure_share,color=color);ax.axhline(.8,color="gray",ls="--",lw=.6);ax.set(title=category,xscale="log",xlabel="Elements retained (%)",ylabel="Exposure share")
    ax=axes.flat[-1];ax.barh(g.category,g.gini,color=CC);ax.set(xlabel="Gini",xlim=(0,1))
    store(fig,"Fig2a_category_concentration",out)
    d=frame("Fig2","Fig2b_functional_reweighting")
    fig,ax=plt.subplots(figsize=(7,4));ax.barh(d.category,100*d.fdi,color=CC);ax.axvline(0,color="gray",lw=.8);ax.set(xlabel="Head − full category share (pp)")
    store(fig,"Fig2b_functional_reweighting",out)
    fig,ax=plt.subplots(figsize=(7,4))
    n=frame("Fig2","Fig2c_province_nodes");e=frame("Fig2","Fig2c_displayed_item_similarity_edges");im=network(n,e,"mean_gini",ax);fig.colorbar(im,ax=ax,label="Province mean block exposure Gini")
    store(fig,"Fig2c_province_item_network",out)
    d=frame("Fig2","Fig2d_selected_pair_category_compositions")
    groups=list(d.groupby(["selection_resolution","province"],sort=False))
    fig,axes=plt.subplots(1,len(groups),figsize=(12,3.5))
    for ((resolution,province),z),ax in zip(groups,axes):
        z=z.set_index("category").reindex(CATEGORIES);ax.pie(z.share,colors=CC,wedgeprops={"width":.35},startangle=90);ax.set_title(province+"\n"+resolution)
    store(fig,"Fig2d_selected_province_pairs",out)
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    for name,title,ax in zip(["Fig2e_category_pair_similarity","Fig2f_item_pair_similarity"],["Seven categories","Element items"],axes):
        z=frame("Fig2",name);ax.hist(z.similarity,bins=24,color="#7898AE",edgecolor="white");ax.axvline(z.similarity.median(),color="gray");ax.set(title=title,xlabel="Province-pair similarity (1 − TVD)",ylabel="Province pairs")
    store(fig,"Fig2ef_similarity_distributions",out)
    d=frame("Fig3","Fig3a_role_behaviour_composition");f=frame("Fig3","Fig3a_role_function_composition")
    fig,axes=plt.subplots(1,2,figsize=(10,3))
    for role,y in [("focal",1),("background",0)]:
        z=d[d.analysis_role.eq(role)].set_index("behaviour_code");left=0
        for k,color,label in zip(range(1,7),BC,BEHAVIORS):
            width=z.loc[k,"share"];axes[0].barh(y,width,left=left,color=color,label=label if role=="focal" else None);left+=width
        value=float(f[f.role.eq(role)&f.measure.eq("duration")].media_oriented_share.iloc[0]);axes[1].barh(y,value,color="#0072B2",label="Media-oriented" if role=="focal" else None);axes[1].barh(y,1-value,left=value,color="#C3C5BC",label="Everyday practice" if role=="focal" else None)
    for ax in axes:ax.set_yticks([1,0],["Focal","Background"]);ax.set(xlabel="Behaviour-record duration share",xlim=(0,1));ax.legend(fontsize=7,loc="upper center",bbox_to_anchor=(.5,-.25),ncol=2)
    store(fig,"Fig3a_role_compositions",out)
    fig,axes=plt.subplots(1,2,figsize=(11,5))
    d=frame("Fig3","Fig3b_environment_ame_10pp")
    z=frame("Fig3","Fig3b_scene_adjusted_probability_deviation")
    for role,color,offset in [("Focal","#0072B2",-.12),("Background","#D55E00",.12)]:
        a=d[d.role.eq(role)].set_index("environment_category").reindex(CATEGORIES)
        y=np.arange(7)+offset;mid=a.change_percentage_points.to_numpy();low=a.cluster_ci_low_percentage_points.to_numpy();hi=a.cluster_ci_high_percentage_points.to_numpy();axes[0].errorbar(mid,y,xerr=np.array([mid-low,hi-mid]),fmt="o",ms=4,color=color,label=role)
        a=z[z.role.eq(role)].set_index("scene_form").reindex(SCENES)
        y=np.arange(4)+offset;mid=a.deviation_percentage_points.to_numpy();low=a.cluster_ci_low_percentage_points.to_numpy();hi=a.cluster_ci_high_percentage_points.to_numpy();axes[1].errorbar(mid,y,xerr=np.array([mid-low,hi-mid]),fmt="o",ms=4,color=color,label=role)
    axes[0].set_yticks(range(7),CATEGORIES);axes[0].set(xlabel="AME for +10 pp category share (pp)")
    axes[1].set_yticks(range(4),SCENES);axes[1].set(xlabel="Adjusted scene probability deviation (pp)")
    for ax in axes:ax.axvline(0,color="gray",ls="--",lw=.6);ax.invert_yaxis();ax.legend()
    store(fig,"Fig3b_adjusted_associations",out)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for role,ax in zip(["focal","background"],axes):
        z=frame("Fig3",f"Fig3c_{role}_transition").set_index("origin");im=ax.imshow(z.to_numpy(),cmap="Blues",vmin=0,vmax=1);ax.set_xticks(range(6),BEHAVIORS,rotation=40,ha="right");ax.set_yticks(range(6),BEHAVIORS);ax.set(title=role.title(),xlabel="Destination",ylabel="Origin");fig.colorbar(im,ax=ax,label="Transition probability")
    store(fig,"Fig3c_role_transitions",out)
    n=frame("Fig3","Fig3d_province_nodes");e=frame("Fig3","Fig3d_displayed_behaviour_similarity_edges");z=frame("Fig3","Fig3d_province_pair_behaviour_similarity")
    fig,axes=plt.subplots(1,2,figsize=(10,4));im=network(n,e,"focal_media_share",axes[0]);fig.colorbar(im,ax=axes[0],label="Province mean block focal media share");axes[1].hist(z.similarity,bins=24,color="#B48465",edgecolor="white");axes[1].set(xlabel="Province-pair similarity (1 − TVD)",ylabel="Province pairs")
    store(fig,"Fig3d_province_behaviour_network",out)
    print(f"Quantitative panel plots saved in {out}",flush=True)
if __name__=="__main__":main()
