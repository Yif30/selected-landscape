# 分析配置

本目录保存统计计算的随机种子、重复次数、抽样配额、词表阈值及并行参数。配置由 code/common.py 读取，改变配置后重新运行相应计算模块即可形成对应的数值结果。

| 文件 | 用途 | 内容形式 |
| --- | --- | --- |
| [analysis.json](analysis.json) | 分类、元素表示及等深度相似度计算的参数 | 单个 UTF-8 JSON 对象 |
| [README.md](README.md) | 参数含义及随机抽样规则 | Markdown 文本 |

## analysis.json 字段

| 字段 | 类型与当前值 | 含义 |
| --- | --- | --- |
| `classifier_repeats` | 整数，100 | 场景分类的重复抽样与训练次数 |
| `classifier_seed` | 整数，20260916 | 分类抽样及分类器随机种子基数，第 r 次使用基数 + r，r 为 1–100 |
| `classifier_cap_per_form` | 整数，50 | 每个合格街区每类场景的抽样数量上限，同时用于均衡元素表示 |
| `train_block_share` | 数值，0.8 | 训练街区份额，训练街区数为 floor(份额 × 合格街区数)，其余街区进入测试集 |
| `thresholds` | 数值数组，0–1 | 嵌套环境词表的目标累计暴露份额，每个阈值对应达到该份额的最小词表 |
| `representation_repeats` | 整数，100 | 四类场景均衡抽样的元素出现比例与优势稳定性重复次数 |
| `representation_seed` | 整数，20290916 | 元素表示抽样种子基数，第 r 次使用基数 + r，r 从 0 开始 |
| `rarefaction_repeats` | 整数，50 | 街区元素集合等深度 Jaccard 相似度的重复次数 |
| `rarefaction_seed` | 整数，20260903 | Jaccard 抽样随机数生成器的初始种子，同一生成器依次产生全部抽样 |
| `rarefaction_depths` | 整数数组，[2, 5, 10, 15, 20] | 每个街区每类场景抽取的场景数量，使用同一组满足最大深度的合格街区 |
| `jobs` | 整数，4 | 同一次分类重复中，各词表阈值模型的并行线程数 |

thresholds 当前为 [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 1.0]。阈值 1.0 使用完整环境词表。抽样限于含至少一个公开环境元素的场景，四类场景数量在每个街区内保持一致。

实际合格街区数、训练测试数量及重复设计见 [results/resampling_design.json](../results/resampling_design.json)，字段定义见 [results/README.md](../results/README.md)。
