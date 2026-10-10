# 分类及字段字典

本目录定义最终投稿版的分类、核心数据字段、物理环境词项、二级行为功能及转移状态。CSV 使用带 BOM 的 UTF-8 编码。

环境元素字典提供 42,874 个词项的固定归属，环境表通过 element_id 连接该字典。功能映射表包含 265 个 (behavior_code, behavior_subtype) 组合；同名二级行为在不同一级代码下分别匹配，一级行为代码不能独立决定功能。二级标签保留中文原文。

分类代码在不同维度下有不同含义：scene 使用 S1–S4；environment 的数字 1–7 对应七类环境；behavior 使用整数 1–6；role 与 function 使用字符串。公开环境表的 category 保存英文类别名称。人物存在标记不表示某种行为必然可见。

转移状态采用八个编码：1_media_oriented、1_everyday_practice、2_media_oriented、2_everyday_practice、3、4、5、6。相邻角色观测中的状态集合分配总质量为 1 的转移权重，再合并为六类行为。具体行为是否具有某种功能由公开功能映射及实际记录确定。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [behavior_subtype_function.csv](behavior_subtype_function.csv) | 完整行为功能映射表，包含 265 个一级行为代码与二级标签组合。功能由复合键匹配确定。 | CSV 表格 |
| [classification_codebook.csv](classification_codebook.csv) | 投稿版分类定义，涵盖四类场景、七类环境、六类行为、两类人物角色和两类行为功能。 | CSV 表格 |
| [data_fields.csv](data_fields.csv) | 核心 CSV 数据表的字段字典，记录逻辑类型、单位和定义。 | CSV 表格 |
| [element_dictionary.csv](element_dictionary.csv) | 最终物理环境词项字典，连接元素编号、中文名称及七类环境归属。 | CSV 表格 |
| [transition_states.csv](transition_states.csv) | 行为转移状态编码规则。行为 1、2 按两类功能拆分，行为 3–6 合并为一级代码，共八个状态。转移图再汇总为六类行为。表内编码规则不表示每个组合均在观察数据中出现。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## classification_codebook.csv

投稿版分类定义，涵盖四类场景、七类环境、六类行为、两类人物角色和两类行为功能。

每行单位：分类维度与代码。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `dimension` | 枚举字符串；scene、environment、behavior、role 或 function，标识分类维度。 |
| `code` | 文本或数字代码；具体取值依据 dimension，角色及功能使用字符串。 |
| `label` | 字符串；分类的英文名称。 |
| `definition` | 字符串；分类或数据字段的定义。 |

## data_fields.csv

核心 CSV 数据表的字段字典，记录逻辑类型、单位和定义。

每行单位：文件与字段。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `file` | 字符串；字段所属数据文件名。 |
| `field` | 字符串；数据列名。 |
| `type` | 字符串；字段的逻辑数据类型。 |
| `unit` | 字符串；字段单位；空白表示无适用物理单位。 |
| `definition` | 字符串；分类或数据字段的定义。 |

## element_dictionary.csv

最终物理环境词项字典，连接元素编号、中文名称及七类环境归属。

每行单位：环境词项。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `element_id` | 字符串；最终元素字典中的唯一环境词项编号。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |

## behavior_subtype_function.csv

完整行为功能映射表，包含 265 个一级行为代码与二级标签组合。功能由复合键匹配确定。

每行单位：一级行为与二级标签组合。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `behavior_code` | 整数 1–6；Digital production、Performance、Consumption、Social interaction、Rest、Movement。 |
| `behavior_subtype` | 字符串；中文二级行为标签，是功能映射复合键的一部分。 |
| `function` | 枚举字符串；media_oriented 或 everyday_practice，按一级行为与二级标签的组合确定。 |

## transition_states.csv

行为转移状态编码规则。行为 1、2 按两类功能拆分，行为 3–6 合并为一级代码，共八个状态。转移图再汇总为六类行为。表内编码规则不表示每个组合均在观察数据中出现。

每行单位：一级行为与功能组合。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `behavior_code` | 整数 1–6；Digital production、Performance、Consumption、Social interaction、Rest、Movement。 |
| `function` | 枚举字符串；media_oriented 或 everyday_practice，按一级行为与二级标签的组合确定。 |
| `transition_state` | 字符串；行为转移计算中的状态代码，1、2 按功能拆分，3–6 使用一级行为代码。 |

## 分类定义

四类场景、七类环境、六类行为与角色、功能定义均由 classification_codebook.csv 提供。中文解释如下。

| 维度 | 代码或名称 | 含义 |
| --- | --- | --- |
| 场景 | S1 Local scenes | 地方特征体现在日常环境与使用中 |
| 场景 | S2 Curated local scenes | 地方特征经过布置、装饰与展示导向的组织 |
| 场景 | S3 Glocal scenes | 地方性特征与标准化商业形式结合 |
| 场景 | S4 Global scenes | 通用商业环境为主，地方特征有限 |
| 环境 | 1 Architecture | 建筑形态、立面及结构构件 |
| 环境 | 2 Natural features | 植被及其他自然环境内容 |
| 环境 | 3 Street infrastructure | 铺地、通行及街道服务设施 |
| 环境 | 4 Landscape decoration | 装饰与景观布景元素 |
| 环境 | 5 Commercial signage | 商业标识、标志及商业识别内容 |
| 环境 | 6 Consumption interfaces | 商品、食物及服务接触界面 |
| 环境 | 7 Display facilities | 舞台与支撑表演、展览的设施 |
| 行为 | 1 Digital production | 现场摄影与数字内容创作 |
| 行为 | 2 Performance | 风格化摆姿与主题化公共展示 |
| 行为 | 3 Consumption | 日常购物与服务消费 |
| 行为 | 4 Social interaction | 交谈、互动、共在及共同观看 |
| 行为 | 5 Rest | 功能性停留及面向景观的停留 |
| 行为 | 6 Movement | 日常通行及休闲漫游 |
| 角色 | focal | 构成场景主要视觉焦点的可见人物 |
| 角色 | background | 可见但未构成主要视觉焦点的人物 |
| 功能 | media_oriented | 身体作为影像生产、展示或传播的视觉材料 |
| 功能 | everyday_practice | 身体参与通行、消费、互动、停留、工作或使用活动 |

CSV 逻辑类型 string 对应文本，integer 对应整数，float 对应数值，boolean 对应真假标记，enum 对应有限分类。编号保持文本格式。数据文件中的空白来源字段表示缺失来源元数据；unit 为空表示没有适用物理单位。
