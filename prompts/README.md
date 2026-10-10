# 提示词与分类格式

模板版本：依据 `Selected_landscape_1009.docx` 投稿版及公开分类字典修订。P1–P5 使用四类场景、七类环境、六类行为和两类行为功能。二级行为标签保留公开映射表的原文。

| 文件 | 用途与输入 | 输出形式 |
| --- | --- | --- |
| [P1_primary_video_interpretation_Chinese.txt](P1_primary_video_interpretation_Chinese.txt) | 从视频提取场景边界、物理环境和人物行为；输入视频、研究编号及字典内容 | 含 `scene_analysis` 与 `video_summary` 的 JSON 对象 |
| [P2_video_review_Chinese.txt](P2_video_review_Chinese.txt) | 依据视频和 P1 分类定义完善已有结构化记录 | 与 P1 完全相同的完整 JSON 对象 |
| [P3_behavior_classification_Chinese.txt](P3_behavior_classification_Chinese.txt) | 将带场景编号和视觉角色的动作描述归入六类行为，关联二级标签与功能 | 行为条目的 JSON 数组 |
| [P4_environment_classification_Chinese.txt](P4_environment_classification_Chinese.txt) | 将可见物理元素词项归入七类环境，匹配最终元素字典 | 环境条目的 JSON 数组 |
| [P5_behavior_function_mapping_Chinese.md](P5_behavior_function_mapping_Chinese.md) | 按一级行为与二级标签的组合赋予功能，内含完整公开映射表 | 带 `function` 的行为条目 JSON 数组 |
| [README.md](README.md) | 模板用途、字段定义及分类关系 | Markdown 文本 |

字典内容须随标注任务提供给模型。文件名或路径不代表模型已读取对应内容。数值分析脚本直接读取公开结构化表；运行统计计算不需要调用视频模型。

## 分类值

| 维度 | 合法非空值 |
| --- | --- |
| 场景 `scene` | S1 Local scenes；S2 Curated local scenes；S3 Glocal scenes；S4 Global scenes |
| 环境 `category` | Architecture；Natural features；Street infrastructure；Landscape decoration；Commercial signage；Consumption interfaces；Display facilities |
| 人物角色 `role` | `focal`：主要视觉焦点；`background`：可见但未构成主要视觉焦点 |
| 一级行为 `behavior_code` | 1 Digital production；2 Performance；3 Consumption；4 Social interaction；5 Rest；6 Movement |
| 行为功能 `function` | `media_oriented`：媒介导向行为；`everyday_practice`：日常实践 |

分类定义见 [classification_codebook.csv](../dictionaries/classification_codebook.csv)。功能映射键为 `(behavior_code, behavior_subtype)`，完整映射见 [behavior_subtype_function.csv](../dictionaries/behavior_subtype_function.csv)。一级行为代码不能独立确定功能。

## P1 与 P2 字段

| 字段或路径 | 类型 | 含义 |
| --- | --- | --- |
| `video_id` | 字符串 | 外部提供的研究视频编号，保留前导零 |
| `block_id` | 字符串 | 外部提供的采样街区编号 |
| `scene_analysis` | 对象数组 | 按时间排列的场景记录 |
| `scene_analysis[].scene_id` | 字符串 | 视频编号与场景开始秒数构成的唯一场景标识 |
| `scene_analysis[].video_id`、`block_id` | 字符串 | 当前场景所属视频和街区 |
| `scene_analysis[].start_seconds` | 数值，秒 | 当前场景开始时间 |
| `scene_analysis[].duration_seconds` | 数值，秒 | 当前场景持续时间，非负 |
| `scene_analysis[].scene` | S1–S4 或 null | 场景类别；null 表示缺少分类依据 |
| `scene_analysis[].has_focal`、`has_background` | 布尔值 | 两类视觉角色是否可见；人物存在与行为是否可判断分别记录 |
| `scene_analysis[].scene_description` | 字符串 | 可见环境和活动的简要描述 |
| `scene_analysis[].cinematography` | 对象 | 辅助拍摄描述 |
| `cinematography.shot_scale` | 字符串或 null | 景别 |
| `cinematography.framing` | 字符串或 null | 构图及主体位置 |
| `cinematography.perspective` | 字符串或 null | 拍摄视角 |
| `cinematography.camera_movement` | 字符串或 null | 镜头移动 |
| `cinematography.lighting` | 字符串或 null | 可见照明条件 |
| `scene_analysis[].text_content` | 对象 | 可辨认文字 |
| `text_content.signboards` | 字符串数组 | 标识文字 |
| `text_content.subtitles` | 字符串数组 | 视频字幕 |
| `scene_analysis[].environment` | 对象数组 | 去重的可见物理环境元素 |
| `environment[].element_id` | 字符串或 null | 最终元素字典编号；新词项尚无字典编号时为 null |
| `environment[].element` | 字符串 | 中文环境词项 |
| `environment[].category` | 枚举字符串 | 七类环境中的一项 |
| `scene_analysis[].behavior` | 对象数组 | 按视觉角色记录的可观察行为 |
| `behavior[].role` | 枚举字符串 | focal 或 background |
| `behavior[].behavior_code` | 整数 | 六类行为中的 1–6 |
| `behavior[].behavior_subtype` | 字符串 | 中文二级行为标签，与功能映射表精确匹配 |
| `behavior[].function` | 枚举字符串或 null | 两类功能之一；映射表中没有该组合时为 null |
| `behavior[].action_description` | 字符串 | 支持行为编码的可见动作及语境 |
| `video_summary` | 对象 | 视频总体描述 |
| `video_summary.scene_count` | 整数 | scene_analysis 数组长度 |
| `video_summary.overall_theme` | 字符串 | 可见主题 |
| `video_summary.overall_style` | 字符串 | 视频呈现风格 |

## P3、P4 与 P5 字段

| 模板 | 字段 | 含义 |
| --- | --- | --- |
| P3 | `id` | 输入描述的标识；一个输入包含多个行为时可对应多个输出 |
| P3 | `scene_id`、`role`、`text` | 输入的场景、视觉角色和动作描述；输出保留场景及角色 |
| P3 | `behavior_code`、`behavior_subtype`、`function`、`action_description` | 六类行为编码、二级标签、功能及可见动作依据 |
| P4 | `id`、`element`、`context` | 输入词项标识、中文名称及空间语境 |
| P4 | `element_id`、`element`、`category` | 输出的字典编号、词项及七类环境归属；输出保留 id |
| P5 | `id`、`scene_id`、`role` | 可选的输入关联信息，提供时原样保留 |
| P5 | `behavior_code`、`behavior_subtype` | 必需的复合匹配键 |
| P5 | `function` | 按映射表赋值的两类功能之一，未匹配时为 null |
| P5 映射表 | `behavior_label` | 便于阅读的一级行为英文名称，实际匹配使用数字代码 |

JSON `null` 表示缺失值，`[]` 表示没有条目，二者均不构成新增类别。公开分析表记录 S1–S4 场景、已有字典元素及具有功能映射的行为。辅助拍摄、文字和动作描述属于标注格式；公开场景文件保留用于计算的场景、环境及行为字段，结构见 [data/README.md](../data/README.md)。
