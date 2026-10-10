# 场景研究数据与代码

对应研究题目：Selected landscapes in short-video representations of urban places。

公开数据包括视频清单、街区信息、场景表、环境元素表、人物行为表，以及同时包含 scene、environment、behavior 的压缩场景文件。图 1–3 的直接绘图数据位于 `figure_data/`；计算代码位于 `code/`；提示词位于 `prompts/`。

| 数据 | 文件 | 数据单位 |
| --- | --- | --- |
| 视频清单 | `data/videos.csv` | 街区检索中的视频记录 |
| 街区信息 | `data/blocks.csv` | 采样街区 |
| 场景数据 | `data/scenes.csv` | 视频内场景 |
| 环境数据 | `data/environment.csv` | 场景与环境元素的唯一关联 |
| 行为数据 | `data/behaviors.csv` | 角色与行为记录 |
| 完整场景记录 | `data/scenes.jsonl.gz` | 按场景关联的环境与行为 |
| 分类与字段定义 | `dictionaries/` | 分类定义、元素类别、行为功能及字段说明 |
| 绘图数据 | `figure_data/Fig1–Fig3/` | 对应图件的直接数值输入 |

研究视频编号由街区编号和街区内视频序号组成，同一平台视频可能出现在不同街区的检索结果中。统计分析保留这些检索记录的独立研究编号。平台视频编号、研究视频编号、街区编号均按文本读取，避免长整数截断和前导零丢失。

场景分类采用 S1–S4；环境分类采用文中的七类物理环境定义；行为采用六类行为及两类功能。行为功能由一级行为与二级行为的组合确定，完整映射保存在 `behavior_subtype_function.csv`。环境词项通过最终元素字典确定类别，人物词项、移动个人物件及缺少物理环境归属的词项不属于环境词汇范围。

时长加权统计、环境集中度、省际比较、人物角色回归、行为转移、场景分类和重复抽样均从公开表计算。绘图数据使用这些计算结果。原视频画面和行政边界文件不属于数值绘图输入。

完整运行命令为 `python code/run_all.py`；使用已提供的绘图数据生成图件，运行 `python code/run_all.py --figures-only`。运行环境及安装命令见英文 README。数据文件为带 BOM 的 UTF-8 CSV；压缩场景文件为 UTF-8 JSON Lines。

数据、字典、提示词和数值结果采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)；计算代码采用 [MIT](https://opensource.org/license/mit)。来源视频保留相应权利。P1–P5 为与最终投稿版分类一致的修订提示词，字段与示例使用同一分类体系；P5 内含完整二级行为功能映射。

## 目录与文件说明

各目录均包含 README，说明文件用途、内容形式、关联关系及全部数据字段。

| 目录 | 功能与内容形式 |
| --- | --- |
| [data/](data/README.md) | 视频、街区、场景、环境和行为 CSV；关联场景的 gzip JSON Lines；数据规模 JSON |
| [dictionaries/](dictionaries/README.md) | 分类、元素、行为功能、字段及转移状态的 CSV 字典 |
| [figure_data/](figure_data/README.md) | 图面板与文件的映射，以及通用单位说明 |
| [figure_data/Fig1/](figure_data/Fig1/README.md) | 图 1a–e 的 10 个直接绘图 CSV 及所有字段定义 |
| [figure_data/Fig2/](figure_data/Fig2/README.md) | 图 2a–f 的 9 个直接绘图 CSV 及所有字段定义 |
| [figure_data/Fig3/](figure_data/Fig3/README.md) | 图 3a–d 的 9 个直接绘图 CSV 及所有字段定义 |
| [results/](results/README.md) | 模型输入、回归估计、组成与排序、重复抽样指标及实际设计；CSV 与 JSON |
| [prompts/](prompts/README.md) | 五份投稿版分类提示词及输入输出字段；TXT 与 Markdown |
| [code/](code/README.md) | 七个 Python 计算及绘图模块，模块作用与参数说明 |
| [config/](config/README.md) | analysis.json 的全部配置字段、当前取值及抽样规则 |

比例默认范围为 0–1；时长为秒；经纬度为度；投影坐标为米；模型字段中的 percent 表示百分比，percentage_points 表示百分点。重复抽样百分位区间与视频聚类模型区间分别定义。场景、环境和行为的具体字段见各目录 README。

| 根目录文件 | 作用与内容形式 |
| --- | --- |
| [README.md](README.md) | 英文总说明、统计定义和运行命令；Markdown |
| [README_zh.md](README_zh.md) | 中文总说明与目录导航；Markdown |
| [requirements.txt](requirements.txt) | Python 依赖与固定版本，每行采用 package==version |
| [CITATION.cff](CITATION.cff) | 数据包引用信息；CFF/YAML 格式，包含格式版本、说明、题目、资源类型、数据版本、作者及许可证 |
| [LICENSE_DATA.md](LICENSE_DATA.md) | 数据、字典、提示词和数值结果的许可范围及署名信息；Markdown |
| [LICENSE_CODE.txt](LICENSE_CODE.txt) | 计算代码的 MIT 许可文本 |
| [.gitignore](.gitignore) | Python 缓存及生成图件的 Git 忽略规则；逐行文本 |

CITATION.cff 的 cff-version 表示引用文件格式版本，version 表示数据包版本，type 表示资源类型；authors 中 family-names 为姓、given-names 为名，license 为许可标识。

抽样定义：元素表示和场景分类仅使用包含公开环境元素的场景；Jaccard 稀释抽样使用全部 S1–S4 场景，每街区每类场景至少 20 条，当前设计包含 187 个街区和 17,391 个无序街区对，重复 50 次。两组环境标签并集为空时 Jaccard 取 0。

行为记录计数与时长组成采用角色与行为条目；角色回归使用去重的场景、角色、功能组合。省际行为 TVD 使用六类行为的时长组成；省级 focal 节点值为省内街区媒介导向时长份额的等权均值。
