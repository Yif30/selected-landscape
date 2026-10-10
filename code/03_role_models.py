"""Video-clustered role models and delta-method probability contrasts."""
import math
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from common import read,save,SCENES,CATEGORIES
ROLES=["main","background"]
ROLE_LABEL={"main":"Focal","background":"Background"}
ENV_TERMS=["category_share_"+str(i) for i in range(1,8)]
ENV_LABELS=dict(zip(ENV_TERMS,CATEGORIES))

def fit_cluster_logit(y: pd.Series, x: pd.DataFrame, groups: pd.Series):
    x = sm.add_constant(x.astype(float), has_constant="add")
    model = sm.Logit(y.astype(float), x)
    result = model.fit(
        disp=False,
        maxiter=200,
        cov_type="cluster",
        cov_kwds={"groups": groups.astype(str)},
    )
    if not bool(result.mle_retvals.get("converged", False)):
        raise RuntimeError("Logit model did not converge")
    return result, x


def delta_summary(estimate: float, gradient: np.ndarray, covariance: np.ndarray) -> tuple[float, float, float, float]:
    variance = float(gradient @ covariance @ gradient)
    se = math.sqrt(max(variance, 0.0))
    low = estimate - 1.96 * se
    high = estimate + 1.96 * se
    p = float(2 * st.norm.sf(abs(estimate / se))) if se > 0 else float("nan")
    return se, low, high, p


def environmental_models(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    coefficient_rows = []
    for role in ROLES:
        d = data.loc[data["analysis_role"].eq(role)].copy()
        scene_dummies = pd.get_dummies(d["scene_type_clean"], prefix="scene", dtype=float)
        for col in ["scene_S2", "scene_S3", "scene_S4"]:
            if col not in scene_dummies:
                scene_dummies[col] = 0.0
        controls = scene_dummies[["scene_S2", "scene_S3", "scene_S4"]]
        for term in ENV_TERMS:
            xraw = pd.concat(
                [d[[term]].rename(columns={term: "env_share"}), controls, d[["log_duration"]]],
                axis=1,
            )
            result, x = fit_cluster_logit(d["is_media"], xraw, d["video_id"])
            params = result.params.to_numpy(float)
            cov = result.cov_params().to_numpy(float)
            p = result.predict(x).to_numpy(float)
            q = p * (1 - p)
            j = list(x.columns).index("env_share")
            step = 0.10
            estimate = float(step * params[j] * q.mean())
            grad = step * (
                np.eye(len(params))[j] * q.mean()
                + params[j] * np.mean((q * (1 - 2 * p))[:, None] * x.to_numpy(float), axis=0)
            )
            se, low, high, pvalue = delta_summary(estimate, grad, cov)
            beta = float(result.params["env_share"])
            rows.append({
                "role": ROLE_LABEL[role], "role_code": role,
                "environment_category": ENV_LABELS[term], "term": term,
                "increment_in_share": step,
                "average_marginal_probability_change": estimate,
                "change_percentage_points": estimate * 100,
                "cluster_se": se,
                "cluster_ci_low": low,
                "cluster_ci_high": high,
                "cluster_ci_low_percentage_points": low * 100,
                "cluster_ci_high_percentage_points": high * 100,
                "cluster_p": pvalue,
                "n_records": len(d), "n_videos": d["video_id"].nunique(),
                "estimand": "Average local marginal change for a +0.10 category-share increment",
            })
            coefficient_rows.append({
                "role": ROLE_LABEL[role], "term": term, "beta": beta,
                "cluster_se": float(result.bse["env_share"]),
                "cluster_ci_low": beta - 1.96 * float(result.bse["env_share"]),
                "cluster_ci_high": beta + 1.96 * float(result.bse["env_share"]),
                "cluster_p": float(result.pvalues["env_share"]),
            })
            print(f"Environment model complete: {ROLE_LABEL[role]} / {ENV_LABELS[term]}", flush=True)
    return pd.DataFrame(rows), pd.DataFrame(coefficient_rows)


def standardised_probability(result, duration: np.ndarray, scene: str) -> tuple[float, np.ndarray]:
    columns = list(result.params.index)
    xcf = pd.DataFrame(0.0, index=np.arange(len(duration)), columns=columns)
    xcf["const"] = 1.0
    xcf["log_duration"] = duration
    if scene != "S1":
        xcf[f"scene_{scene}"] = 1.0
    eta = xcf.to_numpy(float) @ result.params.to_numpy(float)
    p = 1 / (1 + np.exp(-eta))
    gradient = np.mean((p * (1 - p))[:, None] * xcf.to_numpy(float), axis=0)
    return float(p.mean()), gradient


def scene_models(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    probability_rows = []
    deviation_rows = []
    contrast_rows = []
    omnibus_rows = []
    coefficient_rows = []
    for role in ROLES:
        d = data.loc[data["analysis_role"].eq(role)].copy()
        scene_dummies = pd.get_dummies(d["scene_type_clean"], prefix="scene", dtype=float)
        for col in ["scene_S2", "scene_S3", "scene_S4"]:
            if col not in scene_dummies:
                scene_dummies[col] = 0.0
        xraw = pd.concat([scene_dummies[["scene_S2", "scene_S3", "scene_S4"]], d[["log_duration"]]], axis=1)
        result, _ = fit_cluster_logit(d["is_media"], xraw, d["video_id"])
        cov = result.cov_params().to_numpy(float)
        estimates = {}
        gradients = {}
        for scene in SCENES:
            estimate, gradient = standardised_probability(result, d["log_duration"].to_numpy(float), scene)
            se, low, high, _ = delta_summary(estimate, gradient, cov)
            estimates[scene] = estimate
            gradients[scene] = gradient
            probability_rows.append({
                "role": ROLE_LABEL[role], "role_code": role, "scene_form": scene,
                "adjusted_probability": estimate, "adjusted_probability_percent": estimate * 100,
                "cluster_se": se, "cluster_ci_low": max(0.0, low), "cluster_ci_high": min(1.0, high),
                "cluster_ci_low_percent": max(0.0, low) * 100,
                "cluster_ci_high_percent": min(1.0, high) * 100,
                "n_records": len(d), "n_videos": d["video_id"].nunique(),
                "standardisation": "All role-specific records' observed log-duration distribution",
            })
        equal_weight_mean = float(np.mean([estimates[s] for s in SCENES]))
        equal_weight_gradient = np.mean(np.vstack([gradients[s] for s in SCENES]), axis=0)
        for scene in SCENES:
            estimate = estimates[scene] - equal_weight_mean
            gradient = gradients[scene] - equal_weight_gradient
            se, low, high, pvalue = delta_summary(estimate, gradient, cov)
            deviation_rows.append({
                "role": ROLE_LABEL[role], "role_code": role, "scene_form": scene,
                "equal_weight_adjusted_mean": equal_weight_mean,
                "equal_weight_adjusted_mean_percent": equal_weight_mean * 100,
                "probability_deviation": estimate,
                "deviation_percentage_points": estimate * 100,
                "cluster_se": se, "cluster_ci_low": low, "cluster_ci_high": high,
                "cluster_ci_low_percentage_points": low * 100,
                "cluster_ci_high_percentage_points": high * 100,
                "cluster_p": pvalue,
                "reference": "Equal-weighted mean of the four duration-standardised scene-form probabilities",
            })
        pair_start = len(contrast_rows)
        for i, a in enumerate(SCENES):
            for b in SCENES[i + 1:]:
                estimate = estimates[b] - estimates[a]
                gradient = gradients[b] - gradients[a]
                se, low, high, pvalue = delta_summary(estimate, gradient, cov)
                contrast_rows.append({
                    "role": ROLE_LABEL[role], "contrast": f"{b} - {a}",
                    "probability_difference": estimate,
                    "difference_percentage_points": estimate * 100,
                    "cluster_se": se, "cluster_ci_low": low, "cluster_ci_high": high,
                    "cluster_ci_low_percentage_points": low * 100,
                    "cluster_ci_high_percentage_points": high * 100,
                    "p_raw": pvalue,
                })
        role_ix = list(range(pair_start, len(contrast_rows)))
        adjusted = multipletests([contrast_rows[i]["p_raw"] for i in role_ix], method="holm")[1]
        for i, padj in zip(role_ix, adjusted):
            contrast_rows[i]["p_holm"] = float(padj)

        names = list(result.params.index)
        idx = [names.index("scene_S2"), names.index("scene_S3"), names.index("scene_S4")]
        beta = result.params.to_numpy(float)[idx]
        vcov = cov[np.ix_(idx, idx)]
        stat = float(beta @ np.linalg.inv(vcov) @ beta)
        omnibus_rows.append({
            "role": ROLE_LABEL[role], "wald_chi_square": stat, "df": 3,
            "cluster_p": float(st.chi2.sf(stat, 3)),
            "n_records": len(d), "n_videos": d["video_id"].nunique(),
        })
        for name in names:
            coefficient_rows.append({
                "role": ROLE_LABEL[role], "term": name,
                "beta": float(result.params[name]), "cluster_se": float(result.bse[name]),
                "cluster_ci_low": float(result.params[name] - 1.96 * result.bse[name]),
                "cluster_ci_high": float(result.params[name] + 1.96 * result.bse[name]),
                "cluster_p": float(result.pvalues[name]),
            })
        print(f"Unified scene-form model complete: {ROLE_LABEL[role]}", flush=True)
    return (
        pd.DataFrame(probability_rows), pd.DataFrame(deviation_rows), pd.DataFrame(contrast_rows),
        pd.DataFrame(omnibus_rows), pd.DataFrame(coefficient_rows),
    )

def main():
    data=read("results/role_model_input.csv",dtype={"video_id":str,"scene_id":str})
    data=data.rename(columns={"role":"analysis_role","scene":"scene_type_clean","is_media":"is_media"})
    data["analysis_role"]=data.analysis_role.replace({"focal":"main"})
    env,coef=environmental_models(data)
    save(env,"figure_data/Fig3/Fig3b_environment_ame_10pp.csv")
    save(coef,"results/environment_model_coefficients.csv")
    prob,deviation,contrasts,omnibus,coef=scene_models(data)
    save(deviation,"figure_data/Fig3/Fig3b_scene_adjusted_probability_deviation.csv")
    for frame,name in [(prob,"scene_adjusted_probabilities"),(contrasts,"scene_pairwise_contrasts"),(omnibus,"scene_omnibus_tests"),(coef,"scene_model_coefficients")]:
        save(frame,"results/"+name+".csv")
if __name__=="__main__":main()
