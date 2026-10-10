# 数据计算与绘图代码

本目录包含 Python 3.10 分析模块，计算输入为公开场景、环境、行为及街区表。数据字段见 [data/README.md](../data/README.md)，模型及抽样输出字段见 [results/README.md](../results/README.md)，各图件输入字段见 [figure_data/README.md](../figure_data/README.md)。

| 文件 | 功能与输入 | 输出与形式 |
| --- | --- | --- |
| [01_prepare_analysis.py](01_prepare_analysis.py) | 计算场景内七类环境的不同词项数量份额；行为表按场景、角色、功能去重并关联时长与街区 | results/scene_environment_shares.csv、role_model_input.csv；CSV 设计表 |
| [02_descriptive.py](02_descriptive.py) | 计算场景和行为时长组成、元素暴露、集中度、类别重加权、省际 TVD、地理剖面及角色转移 | 图 1–3 的描述性输入；results/ 中的排序、组成、集中度与转移分母；CSV 与 JSON |
| [03_role_models.py](03_role_models.py) | 从 role_model_input.csv 拟合角色分层 Logistic 模型，计算视频聚类系数、AME、标准化概率及场景对比 | Fig3b 的两个直接绘图 CSV；results/ 的模型系数、概率、总体检验与成对对比 CSV |
| [04_scene_element_models.py](04_scene_element_models.py) | 从二元场景与元素矩阵计算均衡元素表示、等深度 Jaccard，以及街区外场景分类 | Fig1c–e 的 CSV；抽样设计、重复指标、街区划分、候选元素等 results/ 文件 |
| [05_plot_figures.py](05_plot_figures.py) | 读取 figure_data/ 中的直接数值输入，生成定量图面板 | 15 组图件，每组 PNG、PDF、SVG 三种格式 |
| [run_all.py](run_all.py) | 按计算依赖依次调用 01–05，或仅调用绘图模块 | 完整数值与绘图工作流 |
| [common.py](common.py) | 定义分类及配置，加载数据，计算累计暴露、Gini、组成、TVD 与稀疏二元矩阵 | 供其他模块调用的共享 Python 函数 |
| [README.md](README.md) | 模块关系、参数、计算定义及执行方式 | Markdown 文本 |

## 执行方式

工作目录为公开包根目录。

```powershell
python -m pip install -r requirements.txt
python code/run_all.py
```

各模块按 01_prepare_analysis、02_descriptive、03_role_models、04_scene_element_models、05_plot_figures 的顺序执行。CSV 输出使用带 BOM 的 UTF-8 编码，JSON 使用 UTF-8。

```powershell
python code/run_all.py --figures-only
python code/run_all.py --figures-only --output "F:/plot_output"
```

| 命令参数 | 类型 | 功能 |
| --- | --- | --- |
| `run_all.py --figures-only` | 布尔开关 | 从已有 figure_data/ 生成图件 |
| `run_all.py --output PATH` | 目录路径 | 设置图件输出目录，可与完整计算或 figures-only 组合使用 |
| `05_plot_figures.py --output PATH` | 目录路径 | 单独绘图时指定输出目录，默认包根目录下的 figures/ |

参数配置见 [config/README.md](../config/README.md)。数值结果写入 results/ 和 figure_data/，重新执行相应模块会覆盖同名输出。统计计算读取已公开结构化表，运行时不需要模型服务凭据。

## 计算定义

环境份额为场景内某类不同元素数除以该场景不同元素总数，无元素场景的份额取零。回归观测为唯一 (scene_id, role, function) 组合。同一场景与角色可能对应两类功能记录。

角色模型分别拟合 focal 和 background，因变量 is_media 表示媒介导向功能，协方差按研究视频编号聚类。每个环境模型仅包含一类环境份额，并调整 S2–S4 场景哑变量与 ln(1 + duration_seconds)。环境 AME 为局部平均边际导数乘 0.10。场景模型以 S1 为参照，标准化概率平均于该角色全部观测的对数时长分布；场景偏差的参照为四类标准化概率的等权均值。各角色六个场景对比分别执行 Holm 校正。

场景分类使用元素存在的二元稀疏矩阵。合格街区四类场景数量保持一致，每类街区配额上限为 50；训练与测试按街区划分。暴露排序来自整个公开语料。分类器为 SGD Logistic，L2 penalty，alpha=1e-5，max_iter=300，tol=1e-4，average=True。分类种子为 classifier_seed + repeat，repeat 从 1 开始。chance_corrected_f1_recovery 为 (当前 macro_f1 − 0.25) / (同次完整词表 macro_f1 − 0.25)。

均衡元素表示使用 representation_seed + repeat，repeat 从 0 开始。出现比例比较四类等量抽样；log2 比值比较当前类与其余三类合并，出现次数加 0.5 平滑。Jaccard 抽样使用一个由 rarefaction_seed 初始化的生成器，重复区间为经验第 2.5–97.5 百分位数。

行为时长组成按角色与行为条目的场景时长加权；计数型功能组成按角色与行为原始记录计算。行为转移连接同一视频内相邻角色观测中的状态集合；每个集合对贡献总权重 1，汇总六类后按起点行归一化。

## 共享函数及参数

| 函数 | 参数与含义 | 返回内容 |
| --- | --- | --- |
| `read(path, **kw)` | path 为包内 CSV 路径，kw 为 pandas 读取选项 | DataFrame |
| `save(df, path, index=False)` | df 为结果表，path 为包内目标路径，index 控制索引输出 | 写入 UTF-8 BOM CSV |
| `load()` | 读取核心公开表并检查结构约束 | 场景、环境、行为、街区四个 DataFrame |
| `enrich(d, s, blocks)` | d 为环境或行为记录，s 为场景表，blocks 为街区表 | 关联视频、场景形式、时间及省份的表 |
| `rank(e)` | e 为含场景持续时间的元素关联表 | 累计暴露排序、单项份额及累计份额 |
| `n_features(r, q)` | r 为暴露排序，q 为累计暴露阈值 | 达到阈值的最小词项数 |
| `gini(x)` | x 为非负暴露量向量 | Gini 系数 |
| `composition(d, group, key, columns)` | 按 group 分组，key 为组成类别，columns 指定列顺序 | 时长归一化组成矩阵 |
| `pairs(p, domain)` | p 为省份组成矩阵，domain 标识比较域 | 无序省份对 TVD 与相似度表 |
| `edges(p, nearest=2, farthest=1)` | p 为完整省际比较表；nearest、farthest 分别为每省保留的最近与最远邻居数 | 合并并去重的展示连线；Fig1b 为 2/2，Fig2c 为 2/1，Fig3d 为 1/1 |
| `matrix(s, e, r)` | s 为场景表，e 为元素关联，r 为暴露排序 | 行为场景、列为环境元素的二元 CSR 稀疏矩阵 |

ROOT 为脚本所在包的根目录，CONFIG 来自 config/analysis.json。SCENES、CATEGORIES、BEHAVIORS 的类别顺序与公开分类字典一致。

## 图件形式

PNG 为 300 dpi 栅格图；PDF 为矢量文档；SVG 为可编辑矢量图。文件名由图号与定量内容组成，例如 Fig1d_classifier.png、Fig3b_adjusted_associations.pdf。图面板根据公开数值表生成，视频示例画面和行政边界图形另需对应图形素材。

Jaccard 抽样使用全部已分类场景，包括没有公开环境元素的场景。合格街区四类场景数均至少为最大深度 20；场景抽样无放回，环境集合并集为空时该街区对相似度取 0。分母为全部合格街区的无序对数。实际街区设计见 results/rarefaction_block_design.csv。

省际行为 TVD 由六类行为的省级时长组成计算；四种角色与功能组合另存为组成表。省级 focal 媒介导向节点值为省内街区时长份额的等权均值。分类曲线使用 accuracy_mean、macro_f1_mean 作为线条，使用 q025–q975 作为区间。
