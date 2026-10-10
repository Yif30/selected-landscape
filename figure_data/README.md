# 图 1–3 直接绘图数据

本目录包含用于定量面板的直接数值输入，均由公开场景、环境和行为表计算。每个图目录内的 README 分别说明具体文件、每行单位、所有字段及统计定义。

| 文件或目录 | 用途与内容 | 形式 |
| --- | --- | --- |
| [Fig1/](Fig1/README.md) | 场景组成、地理分布、代表元素、嵌套词表分类与等深度相似度 | 10 个 CSV 与 README |
| [Fig2/](Fig2/README.md) | 环境集中度、类别重加权、省际环境组成与相似度 | 9 个 CSV 与 README |
| [Fig3/](Fig3/README.md) | 角色行为、环境与场景模型效应、角色转移及省际行为相似度 | 9 个 CSV 与 README |
| [README.md](README.md) | 图面板映射、通用单位和计算关系 | Markdown 文本 |

## 图面板与数值内容

| 图面板 | 文件名前缀与用途 |
| --- | --- |
| Fig. 1a | Fig1a：总体四类场景的时长与条目份额 |
| Fig. 1b | Fig1b：街区场景组成、经纬度剖面、省际场景相似度及展示连线 |
| Fig. 1c | Fig1c：代表性环境元素的均衡出现比例与 log2 比值 |
| Fig. 1d | Fig1d：累计暴露词表规模与街区外分类表现 |
| Fig. 1e | Fig1e：等深度街区元素集合 Jaccard 相似度 |
| Fig. 2a | Fig2a：各环境类别的累计暴露曲线、Gini 和类别内部 H80 |
| Fig. 2b | Fig2b：全局 H80 与完整词表的环境类别组成差 |
| Fig. 2c | Fig2c：省级街区平均 Gini 节点及词项相似度展示连线 |
| Fig. 2d | Fig2d：两种尺度的最大差异省份对及其七类环境组成 |
| Fig. 2e | Fig2e：七类环境尺度的完整省际相似度 |
| Fig. 2f | Fig2f：完整环境词项尺度的完整省际相似度 |
| Fig. 3a | Fig3a：角色行为组成与媒介导向功能份额 |
| Fig. 3b | Fig3b：环境份额 AME 和场景标准化概率偏差 |
| Fig. 3c | Fig3c：主要视觉焦点与背景人物的六类行为转移矩阵 |
| Fig. 3d | Fig3d：省内街区 focal 媒介导向份额的等权均值与六类行为组成相似度 |

文件名的开头标识对应图面板，其余部分说明估计量。例如 Fig2b_functional_reweighting.csv 保存环境类别份额重加权。

CSV 为带 BOM 的 UTF-8 文本。时长单位为秒；份额和概率为 0–1；percent 字段为百分比；percentage_points 字段为百分点。地理坐标为度，投影坐标为米。q025–q975 为重复抽样经验区间；cluster_ci 为研究视频聚类的 95% 模型区间；q25–q75 为街区间四分位距。

TVD 为归一化组成之差的绝对值之和除以 2，省际 similarity = 1 − TVD。H80 为达到 80% 累计元素暴露的最小词表。角色回归及重复抽样的完整输入与逐次结果见 [results/README.md](../results/README.md)。

绘图命令为 `python code/run_all.py --figures-only`，代码及输出形式见 [code/README.md](../code/README.md)。视频示例与行政边界素材独立于这些数值输入。
