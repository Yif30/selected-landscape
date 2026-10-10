# 分析设计、估计量与模型结果

本目录保存由公开数据表计算的回归输入、元素暴露排序、环境组成、统计模型系数及概率对比、行为转移分母和重复抽样结果。直接用于图 1–3 的汇总表位于 [figure_data/](../figure_data/README.md)。

CSV 使用带 BOM 的 UTF-8 编码；JSON 为 UTF-8 文本。数据编号按字符串读取。角色数据值为 focal、background，模型展示标签为 Focal、Background，内部 role_code 的 main 对应 focal。

环境类别份额使用场景内不同词项数量计算。category_share_1–7 依次对应 Architecture、Natural features、Street infrastructure、Landscape decoration、Commercial signage、Consumption interfaces、Display facilities；无环境元素时七项均为零。模型观测为去重 (scene_id, role, function) 组合，is_media 为媒介导向标记。

角色回归为未加权 Logistic 模型，按研究视频编号聚类协方差。beta 和其区间采用 log odds；标准化概率采用 0–1；概率差同样采用比例差，乘 100 为百分点。p_holm 在各角色的六个场景概率对比内校正。cluster_ci 是视频聚类 95% 区间。

元素均衡抽样使用具有四类有元素场景的街区，每类配额为四类可用场景数的最小值与 50 的较小者。元素出现比例与优势稳定性汇总 100 次重复。分类器按街区划分训练测试，暴露排序使用公开整体语料。Jaccard 抽样使用全部 S1–S4 场景，包括没有公开环境元素的场景；每街区每类场景均至少满足最大抽样深度 20，汇总 50 次重复，环境并集为空时相似度取 0。重复区间采用经验百分位数。

相邻角色观测转移分配集合对总质量 1，再归并六类行为。outgoing_weight 为矩阵行归一化前的分母。估计定义、实际样本设计及各字段见下文。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [classifier_block_splits.csv](classifier_block_splits.csv) | 每次重复的街区级训练与测试划分，以及该街区每类场景的抽样配额。街区在一次重复内仅属于一个集合。 | CSV 表格 |
| [classifier_repeat_metrics.csv](classifier_repeat_metrics.csv) | 每次重复与累计暴露阈值下的街区外分类结果，含训练测试样本数及分类指标。 | CSV 表格 |
| [element_exposure_ranking.csv](element_exposure_ranking.csv) | 全体环境词项按累计场景暴露时长降序的排序及累计份额，是 H80 和嵌套词表的共同来源。 | CSV 表格 |
| [element_present_block_design.csv](element_present_block_design.csv) | 街区内各场景形式含至少一个公开环境元素的场景数，以及均衡抽样配额。四类场景都有可用记录的街区进入分类与元素表示计算。 | CSV 表格 |
| [environment_concentration.json](environment_concentration.json) | 整体元素暴露集中度与 H80 的 JSON 汇总。 | JSON 对象 |
| [environment_model_coefficients.csv](environment_model_coefficients.csv) | 七个单类别环境回归模型在两类人物角色下的环境份额系数。模型分别调整场景形式与对数时长。 | CSV 表格 |
| [equal_depth_element_representation.csv](equal_depth_element_representation.csv) | 全局 H80 元素在四类场景中的均衡抽样出现比例及 log2 比值，汇总 100 次重复。 | CSV 表格 |
| [jaccard_rarefaction_replicates.csv](jaccard_rarefaction_replicates.csv) | 每次等深度抽样得到的街区元素集合平均 Jaccard。合格街区在四类场景中均至少具有最大深度的可用场景。 | CSV 表格 |
| [province_behavior_composition.csv](province_behavior_composition.csv) | 省级六类行为的记录时长组成，合并两个角色并归一化；为 Fig3d TVD 的计算输入。 | CSV 表格 |
| [rarefaction_block_design.csv](rarefaction_block_design.csv) | 全部已分类场景的街区与场景数量及 Jaccard 抽样合格标记。 | CSV 表格 |
| [province_environment_composition.csv](province_environment_composition.csv) | 省级七类环境累计元素暴露组成，省内所有场景与元素关联合并后按总量归一化。 | CSV 表格 |
| [province_role_function_composition.csv](province_role_function_composition.csv) | 省级四种角色与功能组合的行为记录时长加权组成，四列合计为 1。 | CSV 表格 |
| [resampling_design.json](resampling_design.json) | 实际分类与等深度抽样设计的 JSON 对象。 | JSON 对象 |
| [role_function_composition.csv](role_function_composition.csv) | 每类视觉角色的两类行为功能时长加权组成。 | CSV 表格 |
| [role_model_input.csv](role_model_input.csv) | 角色回归设计表，行为数据按 scene_id、role、function 去重后关联场景、街区和环境份额。同一场景角色同时存在两类功能时保留两行。 | CSV 表格 |
| [scene_adjusted_probabilities.csv](scene_adjusted_probabilities.csv) | 场景形式回归模型的媒介导向标准化概率。各场景预测平均于该角色全部观测记录的对数时长分布，概率区间截于 0–1。 | CSV 表格 |
| [scene_environment_shares.csv](scene_environment_shares.csv) | 回归用场景环境组成。每类份额使用该类不同词项数除以场景内全部不同词项数，无环境词项时各份额为零。 | CSV 表格 |
| [scene_model_coefficients.csv](scene_model_coefficients.csv) | 角色分层场景形式 Logistic 模型的系数，S1 为参照，模型调整对数时长。 | CSV 表格 |
| [scene_omnibus_tests.csv](scene_omnibus_tests.csv) | 场景形式模型中 S2–S4 三个系数联合为零的总体 Wald 检验。 | CSV 表格 |
| [scene_pairwise_contrasts.csv](scene_pairwise_contrasts.csv) | 每个视觉角色下，四类场景标准化概率的六个成对差异及 Holm 多重比较校正。 | CSV 表格 |
| [stable_element_candidates.csv](stable_element_candidates.csv) | 代表性元素选择表；每类场景保留最多 15 个符合出现比例和优势稳定性条件的元素，绘图从每类取前三个。 | CSV 表格 |
| [transition_support.csv](transition_support.csv) | 角色分层行为转移矩阵的起点权重与视频内相邻角色观测连接数，供理解六类转移矩阵的归一化分母。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## scene_environment_shares.csv

回归用场景环境组成。每类份额使用该类不同词项数除以场景内全部不同词项数，无环境词项时各份额为零。

每行单位：场景。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene_id` | 字符串；研究视频编号、连字符与场景开始秒数组成的唯一场景标识。 |
| `category_share_1` | 比例 0–1；场景内属于 Architecture 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_2` | 比例 0–1；场景内属于 Natural features 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_3` | 比例 0–1；场景内属于 Street infrastructure 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_4` | 比例 0–1；场景内属于 Landscape decoration 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_5` | 比例 0–1；场景内属于 Commercial signage 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_6` | 比例 0–1；场景内属于 Consumption interfaces 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_7` | 比例 0–1；场景内属于 Display facilities 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |

## role_model_input.csv

角色回归设计表，行为数据按 scene_id、role、function 去重后关联场景、街区和环境份额。同一场景角色同时存在两类功能时保留两行。

每行单位：场景、角色与功能的唯一组合。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene_id` | 字符串；研究视频编号、连字符与场景开始秒数组成的唯一场景标识。 |
| `role` | 枚举字符串；focal 为主要视觉焦点人物，background 为可见背景人物。 |
| `function` | 枚举字符串；media_oriented 或 everyday_practice，按一级行为与二级标签的组合确定。 |
| `video_id` | 字符串；八位研究视频编号，所属街区检索记录的标识，保留前导零。 |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `scene` | 枚举字符串；S1、S2、S3 或 S4。 |
| `start_seconds` | 数值，秒；场景开始时间。 |
| `duration_seconds` | 数值，秒；场景持续时间，非负。 |
| `province` | 字符串；省级行政单元名称。 |
| `category_share_1` | 比例 0–1；场景内属于 Architecture 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_2` | 比例 0–1；场景内属于 Natural features 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_3` | 比例 0–1；场景内属于 Street infrastructure 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_4` | 比例 0–1；场景内属于 Landscape decoration 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_5` | 比例 0–1；场景内属于 Commercial signage 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_6` | 比例 0–1；场景内属于 Consumption interfaces 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `category_share_7` | 比例 0–1；场景内属于 Display facilities 的不同元素数 / 场景全部不同环境元素数；无环境元素的场景取 0。 |
| `log_duration` | 数值；ln(1 + duration_seconds)，用于回归时长调整。 |
| `is_media` | 0/1；function 为 media_oriented 时取 1，为 everyday_practice 时取 0。 |

## element_exposure_ranking.csv

全体环境词项按累计场景暴露时长降序的排序及累计份额，是 H80 和嵌套词表的共同来源。

每行单位：环境词项。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `element_id` | 字符串；最终元素字典中的唯一环境词项编号。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `duration` | 数值，秒；同一词项所有场景关联的场景持续时间之和。 |
| `rank` | 整数，从 1 开始；按元素累计暴露时长降序排列的名次。 |
| `element_share` | 比例 0–1；rank / 该排序范围内的元素总数，表示累计词表份额。 |
| `exposure_share` | 比例 0–1；该元素累计暴露时长 / 该排序范围内所有元素的累计暴露时长之和。 |
| `cum_exposure_share` | 比例 0–1；从排序首项到当前元素的 exposure_share 累计和。 |

## environment_model_coefficients.csv

七个单类别环境回归模型在两类人物角色下的环境份额系数。模型分别调整场景形式与对数时长。

每行单位：视觉角色与环境模型变量。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，模型输出展示标签。 |
| `term` | 字符串；回归变量名称，category_share_1–7 为环境份额，scene_S2–S4 为以 S1 作参照的场景哑变量，const 为截距，log_duration 为对数时长。 |
| `beta` | 数值；Logistic 回归系数，单位为 log odds。 |
| `cluster_se` | 数值，log odds；环境份额回归系数的视频聚类标准误。 |
| `cluster_ci_low` | 数值，log odds；环境份额回归系数的 95% 区间下界。 |
| `cluster_ci_high` | 数值，log odds；环境份额回归系数的 95% 区间上界。 |
| `cluster_p` | 数值 0–1；采用视频聚类协方差的双侧 Wald 检验 p 值。 |

## scene_model_coefficients.csv

角色分层场景形式 Logistic 模型的系数，S1 为参照，模型调整对数时长。

每行单位：视觉角色与模型变量。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，模型输出展示标签。 |
| `term` | 字符串；回归变量名称，category_share_1–7 为环境份额，scene_S2–S4 为以 S1 作参照的场景哑变量，const 为截距，log_duration 为对数时长。 |
| `beta` | 数值；Logistic 回归系数，单位为 log odds。 |
| `cluster_se` | 数值，log odds；回归系数的视频聚类标准误。 |
| `cluster_ci_low` | 数值，log odds；回归系数的 95% 区间下界。 |
| `cluster_ci_high` | 数值，log odds；回归系数的 95% 区间上界。 |
| `cluster_p` | 数值 0–1；采用视频聚类协方差的双侧 Wald 检验 p 值。 |

## scene_adjusted_probabilities.csv

场景形式回归模型的媒介导向标准化概率。各场景预测平均于该角色全部观测记录的对数时长分布，概率区间截于 0–1。

每行单位：视觉角色与场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，模型输出展示标签。 |
| `role_code` | 枚举字符串；模型内部角色名称 main 对应公开数据中的 focal，background 对应 background。 |
| `scene_form` | 枚举字符串；S1–S4 场景形式。 |
| `adjusted_probability` | 概率 0–1；在该角色全部记录的观测时长分布上平均的场景标准化媒介导向概率。 |
| `adjusted_probability_percent` | 百分比；adjusted_probability × 100。 |
| `cluster_se` | 数值，概率；标准化媒介导向概率的视频聚类 delta method 标准误。 |
| `cluster_ci_low` | 概率 0–1；标准化概率的 95% 区间下界。 |
| `cluster_ci_high` | 概率 0–1；标准化概率的 95% 区间上界。 |
| `cluster_ci_low_percent` | 百分比；标准化概率的 95% 区间下界 × 100。 |
| `cluster_ci_high_percent` | 百分比；标准化概率的 95% 区间上界 × 100。 |
| `n_records` | 整数；模型拟合使用的去重场景与角色及功能记录数。 |
| `n_videos` | 整数；模型拟合使用的不同研究视频编号数。 |
| `standardisation` | 字符串；标准化概率所采用的时长分布。 |

## scene_pairwise_contrasts.csv

每个视觉角色下，四类场景标准化概率的六个成对差异及 Holm 多重比较校正。

每行单位：视觉角色与场景对比。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，模型输出展示标签。 |
| `contrast` | 字符串；场景概率差的方向，例如 S2 - S1。 |
| `probability_difference` | 概率差；contrast 中前一场景的标准化概率减后一场景的标准化概率。 |
| `difference_percentage_points` | 数值，百分点；probability_difference × 100。 |
| `cluster_se` | 数值，概率差；成对场景概率差的视频聚类 delta method 标准误。 |
| `cluster_ci_low` | 数值，概率差；成对概率差的 95% 区间下界。 |
| `cluster_ci_high` | 数值，概率差；成对概率差的 95% 区间上界。 |
| `cluster_ci_low_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间下界 × 100。 |
| `cluster_ci_high_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间上界 × 100。 |
| `p_raw` | 数值 0–1；场景成对差异的未校正双侧 p 值。 |
| `p_holm` | 数值 0–1；同一角色六个成对场景对比的 Holm 校正 p 值。 |

## scene_omnibus_tests.csv

场景形式模型中 S2–S4 三个系数联合为零的总体 Wald 检验。

每行单位：视觉角色。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，模型输出展示标签。 |
| `wald_chi_square` | 数值；S2–S4 场景系数联合为零的 Wald 卡方统计量。 |
| `df` | 整数；联合场景检验的自由度，为 3。 |
| `cluster_p` | 数值 0–1；采用视频聚类协方差的双侧 Wald 检验 p 值。 |
| `n_records` | 整数；模型拟合使用的去重场景与角色及功能记录数。 |
| `n_videos` | 整数；模型拟合使用的不同研究视频编号数。 |

## equal_depth_element_representation.csv

全局 H80 元素在四类场景中的均衡抽样出现比例及 log2 比值，汇总 100 次重复。

每行单位：H80 环境词项与场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `depth` | 整数或字符串；抽样深度；cap_50 表示每个合格街区每类场景抽样数上限为 50。 |
| `n_per_scene_form` | 整数；每次重复中，所有合格街区合计的每类场景样本数。 |
| `repeats` | 整数；用于该汇总的重复抽样或分类次数。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `scene_type` | 枚举字符串；S1–S4 场景形式。 |
| `prevalence_median` | 比例 0–1；等深度抽样中，该环境词项在该类场景内出现比例的重复中位数。 |
| `prevalence_q025` | 比例 0–1；上述出现比例的重复分布第 2.5 百分位数。 |
| `prevalence_q975` | 比例 0–1；上述出现比例的重复分布第 97.5 百分位数。 |
| `log2_prevalence_ratio_median` | 数值；该类相对其余三类场景合并的平滑出现比例比值的 log2，重复中位数。 |
| `log2_prevalence_ratio_q025` | 数值；上述 log2 比值的重复分布第 2.5 百分位数。 |
| `log2_prevalence_ratio_q975` | 数值；上述 log2 比值的重复分布第 97.5 百分位数。 |
| `modal_dominant_scene` | S1–S4；重复抽样中最常成为该元素出现比例最高类别的场景形式。 |
| `dominant_scene_stability` | 比例 0–1；modal_dominant_scene 成为最高出现比例类别的重复次数份额。 |

## stable_element_candidates.csv

代表性元素选择表；每类场景保留最多 15 个符合出现比例和优势稳定性条件的元素，绘图从每类取前三个。

每行单位：候选词项与优势场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `depth` | 整数或字符串；抽样深度；cap_50 表示每个合格街区每类场景抽样数上限为 50。 |
| `n_per_scene_form` | 整数；每次重复中，所有合格街区合计的每类场景样本数。 |
| `repeats` | 整数；用于该汇总的重复抽样或分类次数。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `scene_type` | 枚举字符串；S1–S4 场景形式。 |
| `prevalence_median` | 比例 0–1；等深度抽样中，该环境词项在该类场景内出现比例的重复中位数。 |
| `prevalence_q025` | 比例 0–1；上述出现比例的重复分布第 2.5 百分位数。 |
| `prevalence_q975` | 比例 0–1；上述出现比例的重复分布第 97.5 百分位数。 |
| `log2_prevalence_ratio_median` | 数值；该类相对其余三类场景合并的平滑出现比例比值的 log2，重复中位数。 |
| `log2_prevalence_ratio_q025` | 数值；上述 log2 比值的重复分布第 2.5 百分位数。 |
| `log2_prevalence_ratio_q975` | 数值；上述 log2 比值的重复分布第 97.5 百分位数。 |
| `modal_dominant_scene` | S1–S4；重复抽样中最常成为该元素出现比例最高类别的场景形式。 |
| `dominant_scene_stability` | 比例 0–1；modal_dominant_scene 成为最高出现比例类别的重复次数份额。 |
| `pooled_prevalence` | 比例 0–1；四类场景 prevalence_median 的等权均值，用于候选元素筛选。 |

## element_present_block_design.csv

街区内各场景形式含至少一个公开环境元素的场景数，以及均衡抽样配额。四类场景都有可用记录的街区进入分类与元素表示计算。

每行单位：街区。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `S1` | 整数；该街区 S1 场景中至少具有一个公开环境元素的数量。 |
| `S2` | 整数；该街区 S2 场景中至少具有一个公开环境元素的数量。 |
| `S3` | 整数；该街区 S3 场景中至少具有一个公开环境元素的数量。 |
| `S4` | 整数；该街区 S4 场景中至少具有一个公开环境元素的数量。 |
| `used_per_form` | 整数；min(该街区四类有元素场景的最小数量, 50)，0 表示不进入均衡四类抽样。 |

## classifier_block_splits.csv

每次重复的街区级训练与测试划分，以及该街区每类场景的抽样配额。街区在一次重复内仅属于一个集合。

每行单位：重复编号与街区。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `repeat` | 整数，从 1 开始；分类器的重复抽样与拟合编号。 |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `set` | 枚举字符串；train 为训练街区，test 为独立保留的测试街区。 |
| `scenes_per_form` | 整数；该街区每类场景在本次重复中的抽样数。 |

## classifier_repeat_metrics.csv

每次重复与累计暴露阈值下的街区外分类结果，含训练测试样本数及分类指标。

每行单位：重复编号与累计暴露阈值。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `repeat` | 整数，从 1 开始；分类器的重复抽样与拟合编号。 |
| `cumulative_exposure` | 比例 0–1；按环境元素累计暴露时长排序后，截取词表的目标累计暴露份额。 |
| `n_features` | 整数；达到目标累计暴露份额所需的最小环境词项数，100% 时使用全部词项。 |
| `n_train` | 整数；本次分类器拟合的训练场景数。 |
| `n_test` | 整数；本次分类器评估的测试场景数。 |
| `accuracy` | 比例 0–1；测试场景整体分类正确率。 |
| `balanced_accuracy` | 比例 0–1；四类场景召回率的等权平均。 |
| `macro_f1` | 比例 0–1；四类场景 F1 的等权平均。 |
| `chance_corrected_f1_recovery` | 数值；(当前词表 macro_f1 − 0.25) / (同次重复完整词表 macro_f1 − 0.25)，可为负值。 |

## jaccard_rarefaction_replicates.csv

每次等深度抽样得到的街区元素集合平均 Jaccard。合格街区在四类场景中均至少具有最大深度的可用场景。

每行单位：重复编号、抽样深度与场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `replicate` | 整数，从 0 开始；Jaccard 等深度重复抽样编号。 |
| `depth` | 整数；每街区每场景形式无放回抽取的场景数。 |
| `scene_type` | 枚举字符串；S1–S4 场景形式。 |
| `mean_jaccard` | 数值 0–1；同一类场景的街区元素集合之间，所有无序街区对 Jaccard 相似度的均值。 |

## province_environment_composition.csv

省级七类环境累计元素暴露组成，省内所有场景与元素关联合并后按总量归一化。

每行单位：省级行政单元。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `province` | 字符串；省级行政单元名称。 |
| `Architecture` | 比例 0–1；该省 Architecture 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Natural features` | 比例 0–1；该省 Natural features 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Street infrastructure` | 比例 0–1；该省 Street infrastructure 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Landscape decoration` | 比例 0–1；该省 Landscape decoration 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Commercial signage` | 比例 0–1；该省 Commercial signage 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Consumption interfaces` | 比例 0–1；该省 Consumption interfaces 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |
| `Display facilities` | 比例 0–1；该省 Display facilities 元素累计场景暴露时长占该省全部环境元素累计暴露的份额。 |

## province_role_function_composition.csv

省级四种角色与功能组合的行为记录时长加权组成，四列合计为 1。

每行单位：省级行政单元。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `province` | 字符串；省级行政单元名称。 |
| `focal_media_oriented` | 比例 0–1；该省所有角色与行为记录时长中，focal 媒介导向记录的份额。 |
| `focal_everyday_practice` | 比例 0–1；该省所有角色与行为记录时长中，focal 日常实践记录的份额。 |
| `background_media_oriented` | 比例 0–1；该省所有角色与行为记录时长中，background 媒介导向记录的份额。 |
| `background_everyday_practice` | 比例 0–1；该省所有角色与行为记录时长中，background 日常实践记录的份额。 |

## role_function_composition.csv

每类视觉角色的两类行为功能时长加权组成。

每行单位：视觉角色与功能。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；focal 为主要视觉焦点人物，background 为可见背景人物。 |
| `function` | 枚举字符串；media_oriented 或 everyday_practice，按一级行为与二级标签的组合确定。 |
| `duration` | 数值，秒；该角色与功能的行为记录所关联场景时长之和。 |
| `share` | 比例 0–1；该角色该功能时长加权量 / 该角色所有行为记录时长加权量。 |

## transition_support.csv

角色分层行为转移矩阵的起点权重与视频内相邻角色观测连接数，供理解六类转移矩阵的归一化分母。

每行单位：角色与起点行为类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；focal 为主要视觉焦点人物，background 为可见背景人物。 |
| `behavior_code` | 整数 1–6；Digital production、Performance、Consumption、Social interaction、Rest、Movement。 |
| `outgoing_weight` | 数值；从该一级行为类别出发的转移总权重，归一化前的行和。 |
| `role_observation_pairs` | 整数；该角色在视频内相邻可见行为观测之间的连接总数，同一角色各行重复记录该总数。 |

## environment_concentration.json：总体元素暴露集中度

单个 JSON 对象，统计范围为完整公开环境词表。

| 字段 | 形式与含义 |
| --- | --- |
| `environment_vocabulary` | 整数；不同环境词项数量 |
| `environment_exposure_seconds` | 数值，秒；全部场景与环境元素关联的累计时长 |
| `global_gini` | 0–1；全体词项暴露分布的 Gini |
| `head80_elements` | 整数；全局累计暴露达到 80% 的最小词项数 |
| `head80_vocabulary_share` | 0–1；head80_elements / environment_vocabulary |
| `head80_exposure_share` | 0–1；上述最小词表的实际累计暴露份额，可略高于 0.80 |

## resampling_design.json：实际抽样设计

顶层包含 classifier 和 rarefaction 两个对象，记录本次数据计算实际采用的设计。

| 字段路径 | 形式与含义 |
| --- | --- |
| `classifier.eligible_blocks` | 整数；四类均具有有元素场景的合格街区数 |
| `classifier.train_blocks` | 整数；每次重复的训练街区数量 |
| `classifier.test_blocks` | 整数；每次重复的测试街区数量 |
| `classifier.repeats` | 整数；分类重复次数 |
| `classifier.cap` | 整数；每街区每类场景抽样上限 |
| `classifier.seed` | 整数；分类抽样及模型随机种子基数 |
| `rarefaction.eligible_blocks` | 整数；四类可用场景数均满足最大深度的街区数量 |
| `rarefaction.pairs_per_repeat` | 整数；每个深度与场景形式中比较的无序街区对数量 |
| `rarefaction.depths` | 整数数组；每街区每类场景的抽样深度 |
| `rarefaction.repeats` | 整数；等深度相似度重复次数 |
| `rarefaction.seed` | 整数；Jaccard 抽样随机数生成器的初始种子 |

## province_behavior_composition.csv

每行单位：省级行政单元。省内所有角色与行为记录按场景时长加权后汇总六类行为，六列之和为 1。分类顺序与 classification_codebook.csv 一致；省际 TVD 与 similarity 由这些组成计算。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `province` | 字符串；省级行政单元名称。 |
| `behavior_share_1` | 比例 0–1；Digital production 的时长份额。 |
| `behavior_share_2` | 比例 0–1；Performance 的时长份额。 |
| `behavior_share_3` | 比例 0–1；Consumption 的时长份额。 |
| `behavior_share_4` | 比例 0–1；Social interaction 的时长份额。 |
| `behavior_share_5` | 比例 0–1；Rest 的时长份额。 |
| `behavior_share_6` | 比例 0–1；Movement 的时长份额。 |

## rarefaction_block_design.csv

每行单位：采样街区。S1–S4 数量为全部已分类场景的数量，包括没有公开环境元素的场景；每类数量均不小于 20 时 eligible 为 True。当前设计包含 187 个合格街区。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `S1` | 非负整数；Local scenes 场景数。 |
| `S2` | 非负整数；Curated local scenes 场景数。 |
| `S3` | 非负整数；Glocal scenes 场景数。 |
| `S4` | 非负整数；Global scenes 场景数。 |
| `eligible` | 布尔值；四类场景数均达到最大深度 20 时为 True，否则为 False。 |
