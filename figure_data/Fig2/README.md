# 图 2 直接绘图数据

本目录提供图 2a–f 的数值输入：环境暴露集中度、H80 的类别重加权、省际词项相似度网络、最大差异省份对，以及七类环境和完整词项两种尺度的省际比较。

CSV 使用带 BOM 的 UTF-8 编码。时长单位为秒，份额为 0–1。fdi 是比例差，绘图乘 100 后表示百分点。

元素暴露等于该元素所有场景关联的持续时间之和，同一场景同一元素只计一次。类别内部 H80 与全局 H80 具有不同的排序范围：图 2a 在每一环境类别内部计算，图 2b 使用全局词表。Gini 由词项累计暴露计算。

省份组成使用省内全部元素暴露合并归一化。TVD 为两个组成向量之差的绝对值之和除以 2；similarity = 1 − TVD。网络连线来自每省相似度最高的两对和相似度最低的一对，合并后按省份对与连线类型去重。节点位置是样本街区坐标的省级均值。

投影定义及场景分类见 [Fig1/README.md](../Fig1/README.md)；七类环境定义见 [dictionaries/README.md](../../dictionaries/README.md)。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [Fig2a_category_curve_samples.csv](Fig2a_category_curve_samples.csv) | 图 2a：七类环境各自内部的累计暴露曲线，按近似对数间隔抽取排名位置以形成直接绘图点。 | CSV 表格 |
| [Fig2a_category_gini_h80.csv](Fig2a_category_gini_h80.csv) | 图 2a：每类环境内部的暴露集中度与达到 80% 暴露所需的词项规模。 | CSV 表格 |
| [Fig2b_functional_reweighting.csv](Fig2b_functional_reweighting.csv) | 图 2b：全局 H80 词表与完整词表的七类环境组成差。H80 是整体暴露排序的头部词表。 | CSV 表格 |
| [Fig2c_displayed_item_similarity_edges.csv](Fig2c_displayed_item_similarity_edges.csv) | 图 2c：完整环境词项尺度的展示连线；每省保留最相似的两对和差异最大的一对，随后去重。 | CSV 表格 |
| [Fig2c_province_nodes.csv](Fig2c_province_nodes.csv) | 图 2c：省际环境词项网络的节点，节点值为省内街区暴露 Gini 的等权均值。地理位置来自该省样本街区经纬度的均值。 | CSV 表格 |
| [Fig2d_selected_pair_category_compositions.csv](Fig2d_selected_pair_category_compositions.csv) | 图 2d：所选省份对的七类环境暴露组成，供环形组成图使用。 | CSV 表格 |
| [Fig2d_selected_pair_summary.csv](Fig2d_selected_pair_summary.csv) | 图 2d：分别在七类环境和完整词项尺度选择 TVD 最大的省份对，展示均采用七类环境组成。 | CSV 表格 |
| [Fig2e_category_pair_similarity.csv](Fig2e_category_pair_similarity.csv) | 图 2e：所有无序省份对在七类环境暴露组成上的相似度。 | CSV 表格 |
| [Fig2f_item_pair_similarity.csv](Fig2f_item_pair_similarity.csv) | 图 2f：所有无序省份对在完整环境词项暴露组成上的相似度。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## Fig2a_category_curve_samples.csv

图 2a：七类环境各自内部的累计暴露曲线，按近似对数间隔抽取排名位置以形成直接绘图点。

每行单位：环境类别内选定排名位置的词项。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `element_id` | 字符串；最终元素字典中的唯一环境词项编号。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `duration` | 数值，秒；该词项所有场景关联的持续时间之和。 |
| `rank` | 整数，从 1 开始；该环境类别内部累计暴露降序名次。 |
| `element_share` | 比例 0–1；rank / 当前环境类别的词项总数。 |
| `exposure_share` | 比例 0–1；该词项暴露时长占当前类别全部词项累计暴露的份额。 |
| `cum_exposure_share` | 比例 0–1；从排序首项到当前元素的 exposure_share 累计和。 |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |

## Fig2a_category_gini_h80.csv

图 2a：每类环境内部的暴露集中度与达到 80% 暴露所需的词项规模。

每行单位：环境类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |
| `n` | 整数；该类别不同环境词项的总数。 |
| `n80` | 整数；该环境类别内，达到 80% 累计暴露所需的最小词项数。 |
| `head_share` | 比例 0–1；n80 / n，类别内部 H80 词表占该类别全部词项的份额。 |
| `gini` | 数值 0–1；元素累计暴露时长分布的 Gini 系数。 |

## Fig2b_functional_reweighting.csv

图 2b：全局 H80 词表与完整词表的七类环境组成差。H80 是整体暴露排序的头部词表。

每行单位：环境类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |
| `full_share` | 比例 0–1；某环境类别在完整元素词表累计暴露中的份额。 |
| `head_share` | 比例 0–1；该类别暴露时长占全局 H80 词表全部累计暴露的份额。 |
| `fdi` | 比例差；全局 H80 内类别份额减完整词表类别份额，乘 100 为百分点。 |

## Fig2c_province_nodes.csv

图 2c：省际环境词项网络的节点，节点值为省内街区暴露 Gini 的等权均值。地理位置来自该省样本街区经纬度的均值。

每行单位：省级行政单元。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `province` | 字符串；省级行政单元名称。 |
| `lon` | 数值，东经度；该省样本街区经度的均值。 |
| `lat` | 数值，北纬度；该省样本街区纬度的均值。 |
| `block_count` | 整数；该省样本中具有公开场景组成的街区数。 |
| `mean_gini` | 数值 0–1；该省采样街区的元素暴露 Gini 系数的等权均值。 |
| `x_aea_m` | 数值，米；Albers 等积投影的横坐标。 |
| `y_aea_m` | 数值，米；Albers 等积投影的纵坐标。 |

## Fig2c_displayed_item_similarity_edges.csv

图 2c：完整环境词项尺度的展示连线；每省保留最相似的两对和差异最大的一对，随后去重。

每行单位：省份对与连线类型。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |
| `edge_type` | 枚举字符串；similar 为近似组成连线，dissimilar 为差异较大连线。 |

## Fig2d_selected_pair_summary.csv

图 2d：分别在七类环境和完整词项尺度选择 TVD 最大的省份对，展示均采用七类环境组成。

每行单位：省份对选择尺度。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `selection_resolution` | 枚举字符串；seven_categories 为七类环境尺度，all_items 为完整词项尺度，用于选择最大 TVD 省份对。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |
| `display_resolution` | 枚举字符串；展示组成的尺度，seven_categories 表示七类环境。 |

## Fig2d_selected_pair_category_compositions.csv

图 2d：所选省份对的七类环境暴露组成，供环形组成图使用。

每行单位：选择尺度、省份与环境类别。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `selection_resolution` | 枚举字符串；seven_categories 为七类环境尺度，all_items 为完整词项尺度，用于选择最大 TVD 省份对。 |
| `selection_tvd` | 数值 0–1；在 selection_resolution 指定尺度上，所选省份对的 TVD。 |
| `province` | 字符串；省级行政单元名称。 |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |
| `share` | 比例 0–1；该省该环境类别累计元素暴露占该省全部环境元素暴露的份额。 |

## Fig2e_category_pair_similarity.csv

图 2e：所有无序省份对在七类环境暴露组成上的相似度。

每行单位：无序省份对。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |

## Fig2f_item_pair_similarity.csv

图 2f：所有无序省份对在完整环境词项暴露组成上的相似度。

每行单位：无序省份对。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `domain` | 字符串；比较域：Scene 为四类场景，Environment 为七类环境，Element items 为完整环境词项，Human 为六类行为组成。 |
| `province_a` | 字符串；省份对的一个省级行政单元。 |
| `province_b` | 字符串；省份对的另一个省级行政单元。 |
| `similarity` | 数值 0–1；1 − TVD，数值越大表示组成越相近。 |
| `tvd` | 数值 0–1；总变差距离，两个归一化组成向量之差的绝对值之和除以 2。 |

