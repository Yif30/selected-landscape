# 场景研究核心数据

本目录包含视频清单、街区登记、最终场景、环境和行为表，以及按场景关联的 JSON Lines 数据。分析单位为研究视频中的场景。

CSV 使用带 BOM 的 UTF-8 编码，首行为字段名。编号按文本读取，保留前导零及平台长整数。布尔字段在视频表中为 True/False，在场景人物存在标记中为 0/1。空白来源编号或链接表示元数据缺失。

研究视频编号标识街区检索记录；同一平台视频可能对应不同街区的研究记录。场景通过 video_id 关联 videos.csv，通过 block_id 关联 blocks.csv。环境与行为通过 scene_id 关联 scenes.csv。环境元素通过 element_id 关联最终元素字典，行为功能使用 (behavior_code, behavior_subtype) 关联功能映射表。

场景类别为 S1 Local scenes、S2 Curated local scenes、S3 Glocal scenes、S4 Global scenes。人物角色为 focal、background。行为采用整数 1–6 和两类功能 media_oriented、everyday_practice。分类定义见 [dictionaries/README.md](../dictionaries/README.md)。

场景时长用于暴露与行为组成的加权。同一元素在一个场景内仅计一次；多个环境元素或行为可以共享同一场景时长，因此元素或行为的累计加权时长可以超过视频场景总时长。

## 文件内容

| 文件 | 用途与内容 | 形式 |
| --- | --- | --- |
| [behaviors.csv](behaviors.csv) | 最终人物行为表，按视觉角色记录一级行为、二级标签及映射得到的功能。一个场景或角色可包含多个行为。 | CSV 表格 |
| [blocks.csv](blocks.csv) | 采样街区登记表，包含行政区划、WGS84 坐标及采样批次。 | CSV 表格 |
| [dataset_summary.json](dataset_summary.json) | 核心数据规模的单个 JSON 汇总对象。 | JSON 对象 |
| [environment.csv](environment.csv) | 最终环境关联表，同一场景与同一元素仅保留一行，类别来自最终环境元素字典。 | CSV 表格 |
| [scenes.csv](scenes.csv) | 最终 S1–S4 场景表，提供视频内时间位置、持续时间、场景形式及人物存在标记。 | CSV 表格 |
| [scenes.jsonl.gz](scenes.jsonl.gz) | 按场景关联环境与行为的压缩 JSON Lines。 | gzip 压缩 JSON Lines |
| [videos.csv](videos.csv) | 视频清单；每行对应一个街区检索或归档中的研究视频记录，包含来源链接、归档状态和公开场景数量。 | CSV 表格 |
| [README.md](README.md) | 目录用途、文件关系和字段定义 | Markdown 文本 |

## videos.csv

视频清单；每行对应一个街区检索或归档中的研究视频记录，包含来源链接、归档状态和公开场景数量。

每行单位：研究视频记录。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `video_id` | 字符串；八位研究视频编号，所属街区检索记录的标识，保留前导零。 |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `source_video_id` | 字符串；来源平台的视频编号，作为文本保存长整数；空白表示来源索引元数据缺失。 |
| `source_url` | 字符串；来源平台视频链接；空白表示来源索引元数据缺失。 |
| `collection_month_reported` | 字符串，YYYY-MM；稿件报告的采集月份，精度为月。 |
| `has_structured_scene` | 布尔值，True/False；归档结构化场景表中是否存在该研究视频的场景。 |
| `classified_scene_count` | 整数；当前公开 scenes.csv 中属于该研究视频的 S1–S4 场景数。 |
| `has_archived_translation` | 布尔值，True/False；该研究编号是否存在归档视频解析文件。 |
| `in_retrieval_index` | 布尔值，True/False；该研究视频编号是否出现在可用检索索引中。 |

## blocks.csv

采样街区登记表，包含行政区划、WGS84 坐标及采样批次。

每行单位：街区。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `block_name` | 字符串；采样街区名称。 |
| `province` | 字符串；省级行政单元名称。 |
| `city` | 字符串；采样登记中的城市名称。 |
| `district` | 字符串；采样登记中的区县名称。 |
| `longitude_wgs84` | 数值，东经度；WGS84 经度。 |
| `latitude_wgs84` | 数值，北纬度；WGS84 纬度。 |
| `collection_batch` | 字符串；采样街区批次标签。 |

## scenes.csv

最终 S1–S4 场景表，提供视频内时间位置、持续时间、场景形式及人物存在标记。

每行单位：场景。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene_id` | 字符串；研究视频编号、连字符与场景开始秒数组成的唯一场景标识。 |
| `video_id` | 字符串；八位研究视频编号，所属街区检索记录的标识，保留前导零。 |
| `block_id` | 字符串；四位采样街区编号，保留前导零。 |
| `start_seconds` | 数值，秒；场景开始时间。 |
| `duration_seconds` | 数值，秒；场景持续时间，非负。 |
| `scene` | 枚举字符串；S1、S2、S3 或 S4。 |
| `has_focal` | 0/1；主要视觉焦点人物的存在指示；场景存在编码或 focal 行为记录任一为阳性时取 1。 |
| `has_background` | 0/1；背景人物的存在指示；场景存在编码或 background 行为记录任一为阳性时取 1。 |

## environment.csv

最终环境关联表，同一场景与同一元素仅保留一行，类别来自最终环境元素字典。

每行单位：场景与环境元素的唯一关联。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `scene_id` | 字符串；研究视频编号、连字符与场景开始秒数组成的唯一场景标识。 |
| `element_id` | 字符串；最终元素字典中的唯一环境词项编号。 |
| `element` | 字符串；标准化中文物理环境词项。 |
| `category` | 枚举字符串；七类环境之一，英文名称与分类字典一致。 |

## behaviors.csv

最终人物行为表，按视觉角色记录一级行为、二级标签及映射得到的功能。一个场景或角色可包含多个行为。

每行单位：角色与行为记录。

| 字段 | 形式、单位与含义 |
| --- | --- |
| `behavior_id` | 字符串；公开角色与行为记录的唯一编号。 |
| `scene_id` | 字符串；研究视频编号、连字符与场景开始秒数组成的唯一场景标识。 |
| `role` | 枚举字符串；focal 为主要视觉焦点人物，background 为可见背景人物。 |
| `behavior_code` | 整数 1–6；Digital production、Performance、Consumption、Social interaction、Rest、Movement。 |
| `behavior_subtype` | 字符串；中文二级行为标签，是功能映射复合键的一部分。 |
| `function` | 枚举字符串；media_oriented 或 everyday_practice，按一级行为与二级标签的组合确定。 |

## scenes.jsonl.gz：关联场景记录

内容为 gzip 压缩的 UTF-8 JSON Lines，每行一个场景对象。解压后按行读取即可获得 scene、environment 和 behavior 的关联记录。

| 字段或路径 | 形式 | 含义 |
| --- | --- | --- |
| `scene_id`、`video_id`、`block_id` | 字符串 | 场景、所属研究视频及街区标识 |
| `start_seconds`、`duration_seconds` | 数值，秒 | 场景开始时间及持续时间 |
| `scene` | 枚举字符串 | S1–S4 场景形式 |
| `environment` | 对象数组 | 当前场景不同物理环境元素；无元素时为 [] |
| `environment[].element_id` | 字符串 | 最终元素字典编号 |
| `environment[].element` | 字符串 | 中文环境词项 |
| `environment[].category` | 枚举字符串 | 七类环境中的归属 |
| `behavior` | 对象数组 | 当前场景的角色与行为；无可用行为时为 [] |
| `behavior[].role` | 枚举字符串 | focal 或 background |
| `behavior[].behavior_code` | 整数 1–6 | 一级行为 |
| `behavior[].behavior_subtype` | 字符串 | 中文二级行为标签 |
| `behavior[].function` | 枚举字符串 | media_oriented 或 everyday_practice |

JSON Lines 同时包含 `has_focal`、`has_background` 布尔值，与 scenes.csv 的 0/1 标记一致；场景存在编码或对应角色行为记录任一为阳性时取 true。行为唯一编号 `behavior_id` 见 behaviors.csv。

```python
import gzip
import json

with gzip.open("data/scenes.jsonl.gz", "rt", encoding="utf-8") as stream:
    for line in stream:
        scene_record = json.loads(line)
        # scene_record["environment"] 和 scene_record["behavior"] 为对象数组
```

## dataset_summary.json：数据规模

单个 JSON 对象，各字段为整数计数，scene_duration_seconds 为数值秒数。

| 字段 | 含义 |
| --- | --- |
| `street_blocks` | 采样街区数量 |
| `provinces` | 涉及省级行政单元数量 |
| `retrieval_records` | 可用检索索引中的研究视频记录数量 |
| `unique_source_video_ids` | 来源索引中不同平台视频编号数量 |
| `structured_research_videos` | 归档结构化场景表中具有场景记录的研究视频数量 |
| `classified_research_videos` | 当前公开表中具有 S1–S4 场景的研究视频数量 |
| `scenes` | 公开场景数量 |
| `scene_duration_seconds` | 公开场景持续时间之和，单位为秒 |
| `scene_element_rows` | 场景与环境元素的唯一关联数量 |
| `environment_elements` | 最终环境字典中不同元素数量 |
| `behavior_records` | 公开角色与行为记录数量 |
| `archived_research_translations` | 归档视频解析文件数量 |
| `video_inventory_records` | videos.csv 的研究视频记录总数 |

videos.csv 的归档状态字段描述可用源记录。公开分类场景数量由 classified_scene_count 和 scenes.csv 定义，归档场景存在标记可对应零个公开分类场景。
