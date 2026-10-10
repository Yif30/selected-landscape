# 图 1 直接绘图数据

本目录提供图 1a–e 的数值输入：场景组成与空间分布、代表性环境元素、累计暴露词表与场景分类表现，以及等深度街区元素相似度。

CSV 使用带 BOM 的 UTF-8 编码。时长单位为秒，比例为 0–1，经纬度为度，投影坐标为米。q25、q75 表示街区间四分位数；q025、q975 表示重复估计的第 2.5 和第 97.5 百分位数。

环境词表按所有场景的元素累计暴露排序。H80 为达到 80% 累计暴露的最小词表。分类器在包含环境元素的场景上，按街区保持四类场景数量一致，每类每街区上限为 50；训练与测试按街区划分。完整分类指标见 [results/README.md](../../results/README.md)。

元素出现比例使用四类等量场景。log2 比值比较当前类与其余三类合并，出现次数使用 0.5 平滑。代表元素要求四类中位出现比例的等权均值至少为 0.005、优势类别稳定性至少为 0.8；每类按 log2 比值与出现比例排序选取前三项。

投影定义：+proj=aea +lat_1=25 +lat_2=47 +lat_0=0 +lon_0=105 +ellps=GRS80 +units=m +no_defs，来源坐标为 EPSG:4326。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [Fig1a_overall_scene_duration_share.csv](Fig1a_overall_scene_duration_share.csv) | 图 1a：四类场景的总体时长与条目组成。 | CSV 表格 |
| [Fig1b_latitude_scene_profiles.csv](Fig1b_latitude_scene_profiles.csv) | 图 1b：按 3° 纬度分组的街区场景时长份额剖面，区间为街区间四分位距。 | CSV 表格 |
| [Fig1b_longitude_scene_profiles.csv](Fig1b_longitude_scene_profiles.csv) | 图 1b：按 4° 经度分组的街区场景时长份额剖面，区间为街区间四分位距。 | CSV 表格 |
| [Fig1b_projected_blocks.csv](Fig1b_projected_blocks.csv) | 图 1b：街区地理位置、四类场景的街区时长份额及 Albers 等积投影坐标。 | CSV 表格 |
| [Fig1b_province_extreme_edges.csv](Fig1b_province_extreme_edges.csv) | 图 1b：从完整省际场景比较表中选择的展示连线；每省保留最相似的两对和差异最大的两对，随后去重。 | CSV 表格 |
| [Fig1b_province_scene_tvd_all_pairs.csv](Fig1b_province_scene_tvd_all_pairs.csv) | 图 1b：所有无序省份对在四类场景时长组成上的 TVD 与相似度。省内采用全部场景时长合并归一化。 | CSV 表格 |
| [Fig1c_anchor_element_matrix.csv](Fig1c_anchor_element_matrix.csv) | 图 1c：代表性环境词项在四类场景中的等深度出现比例、log2 比值及重复抽样区间。 | CSV 表格 |
| [Fig1d_cumulative_vocabulary_curve.csv](Fig1d_cumulative_vocabulary_curve.csv) | 图 1d：从 0 到 100% 累计元素暴露阈值对应的最小词表规模，阈值步长为 0.005。 | CSV 表格 |
| [Fig1d_equal_depth_element_present_sensitivity.csv](Fig1d_equal_depth_element_present_sensitivity.csv) | 图 1d：不同累计暴露词表下，100 次街区外测试分类表现的汇总。输入场景包含至少一个公开环境元素，抽样保持四类均衡。 | CSV 表格 |
| [Fig1e_equal_depth_jaccard.csv](Fig1e_equal_depth_jaccard.csv) | 图 1e：同一场景形式下等深度抽样的街区元素集合 Jaccard 相似度，汇总 50 次重复。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## Fig1a_overall_scene_duration_share.csv

图 1a：四类场景的总体时长与条目组成。

每行单位：场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene_type` | 枚举字符串；S1–S4 场景形式。 |
| `sum` | 数值，秒；场景持续时间之和。 |
| `size` | 整数；场景条目数。 |
| `duration_share` | 比例 0–1；该类场景时长占全部场景时长的份额。 |
| `count_share` | 比例 0–1；该类场景条目占全部场景条目的份额。 |

## Fig1b_projected_blocks.csv

图 1b：街区地理位置、四类场景的街区时长份额及 Albers 等积投影坐标。

每行单位：街区。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `province` | 字符串；省级行政单元名称。 |
| `lon` | 数值，东经度；WGS84 经度。 |
| `lat` | 数值，北纬度；WGS84 纬度。 |
| `S1` | 比例 0–1；Local scenes 的街区场景时长份额。 |
| `S2` | 比例 0–1；Curated local scenes 的街区场景时长份额。 |
| `S3` | 比例 0–1；Glocal scenes 的街区场景时长份额。 |
| `S4` | 比例 0–1；Global scenes 的街区场景时长份额。 |
| `x_aea_m` | 数值，米；Albers 等积投影的横坐标。 |
| `y_aea_m` | 数值，米；Albers 等积投影的纵坐标。 |

## Fig1b_longitude_scene_profiles.csv

图 1b：按 4° 经度分组的街区场景时长份额剖面，区间为街区间四分位距。

每行单位：场景形式与经度区间。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene` | 枚举字符串；S1、S2、S3 或 S4。 |
| `bin` | 数值，东经度；4° 经度分组区间中心。 |
| `mean` | 比例 0–1；该经度区间内街区场景时长份额的等权均值。 |
| `q25` | 数值；组内观测的第 25 百分位数。 |
| `q75` | 数值；组内观测的第 75 百分位数。 |
| `n` | 整数；该经度区间的街区数量。 |
| `projected_position` | 数值，米；分组街区投影坐标的中位数，经度剖面用 x，纬度剖面用 y。 |

## Fig1b_latitude_scene_profiles.csv

图 1b：按 3° 纬度分组的街区场景时长份额剖面，区间为街区间四分位距。

每行单位：场景形式与纬度区间。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene` | 枚举字符串；S1、S2、S3 或 S4。 |
| `bin` | 数值，北纬度；3° 纬度分组区间中心。 |
| `mean` | 比例 0–1；该纬度区间内街区场景时长份额的等权均值。 |
| `q25` | 数值；组内观测的第 25 百分位数。 |
| `q75` | 数值；组内观测的第 75 百分位数。 |
| `n` | 整数；该纬度区间的街区数量。 |
| `projected_position` | 数值，米；分组街区投影坐标的中位数，经度剖面用 x，纬度剖面用 y。 |

## Fig1b_province_scene_tvd_all_pairs.csv

图 1b：所有无序省份对在四类场景时长组成上的 TVD 与相似度。省内采用全部场景时长合并归一化。

每行单位：无序省份对。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |

## Fig1b_province_extreme_edges.csv

图 1b：从完整省际场景比较表中选择的展示连线；每省保留最相似的两对和差异最大的两对，随后去重。

每行单位：省份对与连线类型。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |
| `edge_type` | 枚举字符串；similar 为近似组成连线，dissimilar 为差异较大连线。 |

## Fig1c_anchor_element_matrix.csv

图 1c：代表性环境词项在四类场景中的等深度出现比例、log2 比值及重复抽样区间。

每行单位：代表性环境词项与场景形式。

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
| `element_order` | 整数，从 0 开始；环境词项在绘图矩阵中的展示顺序。 |
| `scene_order` | 整数，从 0 开始；场景形式在绘图矩阵中的顺序，0–3 对应 S1–S4。 |

## Fig1d_cumulative_vocabulary_curve.csv

图 1d：从 0 到 100% 累计元素暴露阈值对应的最小词表规模，阈值步长为 0.005。

每行单位：累计暴露阈值。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `cumulative_exposure` | 比例 0–1；按环境元素累计暴露时长排序后，截取词表的目标累计暴露份额。 |
| `n_features` | 整数；达到目标累计暴露份额所需的最小环境词项数，100% 时使用全部词项。 |

## Fig1d_equal_depth_element_present_sensitivity.csv

图 1d：不同累计暴露词表下，100 次街区外测试分类表现的汇总。输入场景包含至少一个公开环境元素，抽样保持四类均衡。

每行单位：累计暴露阈值与词表规模。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `cumulative_exposure` | 比例 0–1；按环境元素累计暴露时长排序后，截取词表的目标累计暴露份额。 |
| `n_features` | 整数；达到目标累计暴露份额所需的最小环境词项数，100% 时使用全部词项。 |
| `repeats` | 整数；用于该汇总的重复抽样或分类次数。 |
| `accuracy_mean` | 数值；整体分类正确率的重复均值。 |
| `accuracy_sd` | 数值；整体分类正确率的重复样本标准差。 |
| `accuracy_q025` | 数值；整体分类正确率的重复分布第 2.5 百分位数。 |
| `accuracy_median` | 数值；整体分类正确率的重复中位数。 |
| `accuracy_q975` | 数值；整体分类正确率的重复分布第 97.5 百分位数。 |
| `balanced_accuracy_mean` | 数值；四类召回率等权均值的重复均值。 |
| `balanced_accuracy_sd` | 数值；四类召回率等权均值的重复样本标准差。 |
| `balanced_accuracy_q025` | 数值；四类召回率等权均值的重复分布第 2.5 百分位数。 |
| `balanced_accuracy_median` | 数值；四类召回率等权均值的重复中位数。 |
| `balanced_accuracy_q975` | 数值；四类召回率等权均值的重复分布第 97.5 百分位数。 |
| `macro_f1_mean` | 数值；四类 F1 等权均值的重复均值。 |
| `macro_f1_sd` | 数值；四类 F1 等权均值的重复样本标准差。 |
| `macro_f1_q025` | 数值；四类 F1 等权均值的重复分布第 2.5 百分位数。 |
| `macro_f1_median` | 数值；四类 F1 等权均值的重复中位数。 |
| `macro_f1_q975` | 数值；四类 F1 等权均值的重复分布第 97.5 百分位数。 |
| `chance_corrected_f1_recovery_mean` | 数值；相对完整词表的机会水平校正 F1 恢复值的重复均值。 |
| `chance_corrected_f1_recovery_sd` | 数值；相对完整词表的机会水平校正 F1 恢复值的重复样本标准差。 |
| `chance_corrected_f1_recovery_q025` | 数值；相对完整词表的机会水平校正 F1 恢复值的重复分布第 2.5 百分位数。 |
| `chance_corrected_f1_recovery_median` | 数值；相对完整词表的机会水平校正 F1 恢复值的重复中位数。 |
| `chance_corrected_f1_recovery_q975` | 数值；相对完整词表的机会水平校正 F1 恢复值的重复分布第 97.5 百分位数。 |

## Fig1e_equal_depth_jaccard.csv

图 1e：同一场景形式下等深度抽样的街区元素集合 Jaccard 相似度，汇总 50 次重复。

每行单位：每街区每类场景抽样深度与场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `depth` | 整数；每个合格街区每类场景无放回抽取的场景数。 |
| `scene_type` | 枚举字符串；S1–S4 场景形式。 |
| `mean` | 数值 0–1；每次重复的省内外全部合格街区无序对平均 Jaccard 的重复均值。 |
| `sd` | 数值；重复估计值的样本标准差。 |
| `q025` | 数值；重复估计值的第 2.5 百分位数。 |
| `q975` | 数值；重复估计值的第 97.5 百分位数。 |

Jaccard 的抽样池为全部已分类 S1–S4 场景，包括没有公开环境元素的场景；各街区四类场景数均至少为 20。实际设计包含 187 个街区、每次 17,391 个无序街区对。标签并集为空时相似度取 0。抽样池及合格标记见 results/rarefaction_block_design.csv。

Fig1d 曲线展示重复均值 accuracy_mean、macro_f1_mean，区间为 q025–q975。元素表示与分类使用包含环境元素的场景，抽样池定义见 results/element_present_block_design.csv。
