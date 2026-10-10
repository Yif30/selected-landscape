# 图 3 直接绘图数据

本目录提供图 3a–d 的数值输入：角色行为组成、媒介导向概率的环境与场景效应、行为转移，以及省际角色功能相似度网络。

CSV 使用带 BOM 的 UTF-8 编码。数据表的 role 或 analysis_role 使用 focal、background；模型输出展示标签为 Focal、Background，role_code 中 main 对应 focal。行为代码 1–6 依次为 Digital production、Performance、Consumption、Social interaction、Rest、Movement。

角色行为组成按每条行为记录关联的场景时长加权。角色功能的 count 使用去重 (scene_id, role, function) 观测，duration 使用角色与行为记录时长。两种分母在字段 measure 中区分。

环境模型每次仅纳入一个环境类别份额，调整场景形式与 ln(1 + duration_seconds)，协方差按研究视频聚类。AME 为局部平均边际导数乘 0.10，并非两个有限变化预测概率的差。场景偏差使用四类时长标准化预测概率的等权均值作参照。cluster_ci 为 95% delta method 区间；带 percentage_points 的字段使用百分点，其余概率变化字段使用比例差。

行为转移连接同一视频内该角色的相邻行为观测，未记录该角色的场景可被跳过。每个状态集合对贡献总权重 1，再汇总为六类并按起点行归一化；无出发权重时该行取零。转移统计不追踪个人身份。

省际行为相似度使用六类行为的时长加权组成，合并 focal 与 background 记录。网络节点的 focal_media_share 为省内各采样街区 focal 媒介导向时长份额的等权均值；各街区分母限于 focal 行为。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [Fig3a_role_behaviour_composition.csv](Fig3a_role_behaviour_composition.csv) | 图 3a：focal、background 两类角色各自的六类行为时长加权组成。 | CSV 表格 |
| [Fig3a_role_function_composition.csv](Fig3a_role_function_composition.csv) | 图 3a：各角色的媒介导向行为份额，分别按角色与行为记录计数和行为记录时长计算。 | CSV 表格 |
| [Fig3b_environment_ame_10pp.csv](Fig3b_environment_ame_10pp.csv) | 图 3b：环境类别份额增加 10 个百分点时，媒介导向概率的局部平均边际变化。各类别单独建模，调整场景形式与对数时长，协方差按研究视频聚类。 | CSV 表格 |
| [Fig3b_scene_adjusted_probability_deviation.csv](Fig3b_scene_adjusted_probability_deviation.csv) | 图 3b：四类场景的时长标准化媒介导向概率相对于四类等权均值的偏差，协方差按研究视频聚类。 | CSV 表格 |
| [Fig3c_background_transition.csv](Fig3c_background_transition.csv) | 图 3c：背景人物的六类行为行归一化转移矩阵。视频内连接相邻同角色行为观测，场景中未记录该角色的片段可被跳过。 | CSV 表格 |
| [Fig3c_focal_transition.csv](Fig3c_focal_transition.csv) | 图 3c：主要视觉焦点人物的六类行为行归一化转移矩阵。视频内连接相邻同角色行为观测，场景中未记录该角色的片段可被跳过。 | CSV 表格 |
| [Fig3d_displayed_behaviour_similarity_edges.csv](Fig3d_displayed_behaviour_similarity_edges.csv) | 图 3d：六类行为组成尺度的展示连线；每省保留最相似的一对和差异最大的一对，随后去重。 | CSV 表格 |
| [Fig3d_province_nodes.csv](Fig3d_province_nodes.csv) | 图 3d：省际行为网络节点，节点值为该省采样街区 focal 媒介导向时长份额的等权均值。地理位置来自样本街区经纬度的均值。 | CSV 表格 |
| [Fig3d_province_pair_behaviour_similarity.csv](Fig3d_province_pair_behaviour_similarity.csv) | 图 3d：所有无序省份对的六类行为的时长加权组成相似度。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## Fig3a_role_behaviour_composition.csv

图 3a：focal、background 两类角色各自的六类行为时长加权组成。

每行单位：角色与一级行为类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `analysis_role` | 枚举字符串；focal 或 background，人物的视觉角色。 |
| `behaviour_code` | 整数 1–6；英式拼写的行为列名，与 behavior_code 的分类一致。 |
| `duration` | 数值，秒；该角色与一级行为的所有行为记录所关联场景时长之和。 |
| `share` | 比例 0–1；该类行为时长加权量 / 该角色全部行为记录时长加权量。 |

## Fig3a_role_function_composition.csv

图 3a：各角色的媒介导向行为份额，分别按角色与行为记录计数和行为记录时长计算。

每行单位：角色与加权方式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；focal 为主要视觉焦点人物，background 为可见背景人物。 |
| `measure` | 枚举字符串；count 为角色与行为条目的记录计数，duration 为角色与行为记录的场景时长加权。 |
| `media_oriented_share` | 比例 0–1；该角色中媒介导向行为按 measure 指定分母计算的份额。 |

## Fig3b_environment_ame_10pp.csv

图 3b：环境类别份额增加 10 个百分点时，媒介导向概率的局部平均边际变化。各类别单独建模，调整场景形式与对数时长，协方差按研究视频聚类。

每行单位：视觉角色与环境类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，为模型输出展示标签。 |
| `role_code` | 枚举字符串；模型内部角色名称 main 对应公开数据中的 focal，background 对应 background。 |
| `environment_category` | 枚举字符串；七类环境之一。 |
| `term` | 字符串；回归变量名称，category_share_1–7 为环境份额，scene_S2–S4 为以 S1 作参照的场景哑变量，const 为截距，log_duration 为对数时长。 |
| `increment_in_share` | 数值；环境类别份额增量，0.10 表示增加 10 个百分点。 |
| `average_marginal_probability_change` | 概率差；对环境类别份额增加 0.10 的局部平均边际效应。 |
| `change_percentage_points` | 数值，百分点；average_marginal_probability_change × 100。 |
| `cluster_se` | 数值，概率差；平均边际概率变化的视频聚类 delta method 标准误。 |
| `cluster_ci_low` | 数值，概率差；平均边际变化的 95% delta method 区间下界。 |
| `cluster_ci_high` | 数值，概率差；平均边际变化的 95% delta method 区间上界。 |
| `cluster_ci_low_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间下界 × 100。 |
| `cluster_ci_high_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间上界 × 100。 |
| `cluster_p` | 数值 0–1；采用视频聚类协方差的双侧 Wald 检验 p 值。 |
| `n_records` | 整数；模型拟合使用的去重场景与角色及功能记录数。 |
| `n_videos` | 整数；模型拟合使用的不同研究视频编号数。 |
| `estimand` | 字符串；估计量定义。 |

## Fig3b_scene_adjusted_probability_deviation.csv

图 3b：四类场景的时长标准化媒介导向概率相对于四类等权均值的偏差，协方差按研究视频聚类。

每行单位：视觉角色与场景形式。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `role` | 枚举字符串；Focal 或 Background，为模型输出展示标签。 |
| `role_code` | 枚举字符串；模型内部角色名称 main 对应公开数据中的 focal，background 对应 background。 |
| `scene_form` | 枚举字符串；S1–S4 场景形式。 |
| `equal_weight_adjusted_mean` | 概率 0–1；四类场景时长标准化概率的等权平均值。 |
| `equal_weight_adjusted_mean_percent` | 百分比；equal_weight_adjusted_mean × 100。 |
| `probability_deviation` | 概率差；当前场景的标准化概率减四类场景标准化概率的等权均值。 |
| `deviation_percentage_points` | 数值，百分点；probability_deviation × 100。 |
| `cluster_se` | 数值，概率差；场景概率偏差的视频聚类 delta method 标准误。 |
| `cluster_ci_low` | 数值，概率差；场景概率偏差的 95% 区间下界。 |
| `cluster_ci_high` | 数值，概率差；场景概率偏差的 95% 区间上界。 |
| `cluster_ci_low_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间下界 × 100。 |
| `cluster_ci_high_percentage_points` | 数值，百分点；概率差或概率变化的 95% 区间上界 × 100。 |
| `cluster_p` | 数值 0–1；采用视频聚类协方差的双侧 Wald 检验 p 值。 |
| `reference` | 字符串；概率偏差所使用的参照定义。 |

## Fig3c_focal_transition.csv

图 3c：主要视觉焦点人物的六类行为行归一化转移矩阵。视频内连接相邻同角色行为观测，场景中未记录该角色的片段可被跳过。

每行单位：起点行为类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `origin` | 整数 1–6；转移的起点行为类别。 |
| `1` | 概率 0–1；从 origin 行的行为类别转向行为类别 1 的行归一化概率。 |
| `2` | 概率 0–1；从 origin 行的行为类别转向行为类别 2 的行归一化概率。 |
| `3` | 概率 0–1；从 origin 行的行为类别转向行为类别 3 的行归一化概率。 |
| `4` | 概率 0–1；从 origin 行的行为类别转向行为类别 4 的行归一化概率。 |
| `5` | 概率 0–1；从 origin 行的行为类别转向行为类别 5 的行归一化概率。 |
| `6` | 概率 0–1；从 origin 行的行为类别转向行为类别 6 的行归一化概率。 |

## Fig3c_background_transition.csv

图 3c：背景人物的六类行为行归一化转移矩阵。视频内连接相邻同角色行为观测，场景中未记录该角色的片段可被跳过。

每行单位：起点行为类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `origin` | 整数 1–6；转移的起点行为类别。 |
| `1` | 概率 0–1；从 origin 行的行为类别转向行为类别 1 的行归一化概率。 |
| `2` | 概率 0–1；从 origin 行的行为类别转向行为类别 2 的行归一化概率。 |
| `3` | 概率 0–1；从 origin 行的行为类别转向行为类别 3 的行归一化概率。 |
| `4` | 概率 0–1；从 origin 行的行为类别转向行为类别 4 的行归一化概率。 |
| `5` | 概率 0–1；从 origin 行的行为类别转向行为类别 5 的行归一化概率。 |
| `6` | 概率 0–1；从 origin 行的行为类别转向行为类别 6 的行归一化概率。 |

## Fig3d_province_nodes.csv

图 3d：省际行为网络节点，节点值为该省采样街区 focal 媒介导向时长份额的等权均值。地理位置来自样本街区经纬度的均值。

每行单位：省级行政单元。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `province` | 字符串；省级行政单元名称。 |
| `lon` | 数值，东经度；该省样本街区经度的均值。 |
| `lat` | 数值，北纬度；该省样本街区纬度的均值。 |
| `block_count` | 整数；该省样本中具有公开场景组成的街区数。 |
| `x_aea_m` | 数值，米；Albers 等积投影的横坐标。 |
| `y_aea_m` | 数值，米；Albers 等积投影的纵坐标。 |
| `focal_media_share` | 比例 0–1；省内采样街区 focal 媒介导向时长份额的等权均值。每街区份额为媒介导向 focal 行为时长 / 全部 focal 行为时长。 |

## Fig3d_displayed_behaviour_similarity_edges.csv

图 3d：六类行为组成尺度的展示连线；每省保留最相似的一对和差异最大的一对，随后去重。

每行单位：省份对与连线类型。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |
| `edge_type` | 枚举字符串；similar 为近似组成连线，dissimilar 为差异较大连线。 |

## Fig3d_province_pair_behaviour_similarity.csv

图 3d：所有无序省份对的六类行为的时长加权组成相似度。

每行单位：无序省份对。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |
