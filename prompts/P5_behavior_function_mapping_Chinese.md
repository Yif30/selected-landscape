# 行为功能映射提示词

模板版本：最终投稿版分类。

任务：根据输入条目的 behavior_code 与 behavior_subtype，匹配下方完整映射表，为行为赋予功能。

输入为 JSON 数组。behavior_code 为整数 1–6，behavior_subtype 为公开二级标签原文；id、scene_id、role 可作为关联字段提供。已有 function 可由映射表值替换，其他输入字段原样保留。

## 六类行为

| behavior_code | behavior_label | 定义 |
| --- | --- | --- |
| 1 | Digital production | 现场摄影与数字内容创作 |
| 2 | Performance | 风格化摆姿与主题化公共展示 |
| 3 | Consumption | 日常购物与服务消费 |
| 4 | Social interaction | 交谈、互动、共在与共同观看 |
| 5 | Rest | 功能性停留与面向景观的停留 |
| 6 | Movement | 日常通行与休闲漫游 |

## 两类功能

media_oriented：身体作为影像生产、展示或传播的视觉材料。
everyday_practice：身体参与通行、消费、互动、停留、工作或使用活动。

功能匹配使用 (behavior_code, behavior_subtype) 两个字段。相同二级标签出现在不同一级代码下时，分别按对应行处理；不根据一级代码单独赋值，不改写输入标签以获得匹配。
映射表中的二级标签保留公开数据原文。behavior_label 是一级行为的英文阅读标签，匹配键使用整数代码。
匹配到表中条目时 function 使用该条目的值。无法匹配时 function 为 null；null 表示缺失，不构成第三类功能，也不能凭缺少证据将条目归入某一功能。

仅输出合法 JSON 数组，保留输入关联字段并添加或替换 function，不附带 Markdown 或解释文本。

输入示例
[{"id":"EX01","behavior_code":1,"behavior_subtype":"数字沉浸"},{"id":"EX02","behavior_code":6,"behavior_subtype":"打卡/摄影"}]
输出示例
[{"id":"EX01","behavior_code":1,"behavior_subtype":"数字沉浸","function":"everyday_practice"},{"id":"EX02","behavior_code":6,"behavior_subtype":"打卡/摄影","function":"media_oriented"}]

## 完整功能映射表

表中 265 个组合与 dictionaries/behavior_subtype_function.csv 一致。

| behavior_code | behavior_label | behavior_subtype | function |
| --- | --- | --- | --- |
| 1 | Digital production | 视频创作/直播 | media_oriented |
| 1 | Digital production | 打卡/摄影 | media_oriented |
| 1 | Digital production | 视频创作 | media_oriented |
| 1 | Digital production | 打卡 | media_oriented |
| 1 | Digital production | 摄影 | media_oriented |
| 1 | Digital production | 数字沉浸 | everyday_practice |
| 1 | Digital production | 自拍 | media_oriented |
| 1 | Digital production | 展示 | media_oriented |
| 1 | Digital production | 直播 | media_oriented |
| 1 | Digital production | 观看表演 | media_oriented |
| 1 | Digital production | 观看屏幕 | media_oriented |
| 1 | Digital production | 拍照 | media_oriented |
| 1 | Digital production | 其他 | media_oriented |
| 1 | Digital production | 艺术创作 | media_oriented |
| 1 | Digital production | 展示动作 | media_oriented |
| 1 | Digital production | 引导视线 | media_oriented |
| 1 | Digital production | 指导拍摄 | media_oriented |
| 1 | Digital production | 展示物品 | media_oriented |
| 1 | Digital production | 打电话 | everyday_practice |
| 1 | Digital production | 放风筝 | media_oriented |
| 1 | Digital production | 展示照片 | media_oriented |
| 1 | Digital production | 展示道具 | media_oriented |
| 1 | Digital production | 查看手机 | everyday_practice |
| 1 | Digital production | 环境描写 | media_oriented |
| 1 | Digital production | 观察 | media_oriented |
| 1 | Digital production | 观看 | media_oriented |
| 1 | Digital production | 互动 | media_oriented |
| 1 | Digital production | 互动屏幕 | media_oriented |
| 1 | Digital production | 参观 | media_oriented |
| 1 | Digital production | 展示自己 | media_oriented |
| 1 | Digital production | 指向商铺 | media_oriented |
| 1 | Digital production | 查看时间表 | everyday_practice |
| 1 | Digital production | 浏览 | everyday_practice |
| 1 | Digital production | 观景 | media_oriented |
| 2 | Performance | 身体展演 | media_oriented |
| 2 | Performance | 观看表演 | media_oriented |
| 2 | Performance | 艺术创作 | media_oriented |
| 2 | Performance | NPC互动 | media_oriented |
| 2 | Performance | 视频创作/直播 | media_oriented |
| 2 | Performance | 表演 | media_oriented |
| 2 | Performance | 宗教活动 | everyday_practice |
| 2 | Performance | 喂鸽子 | media_oriented |
| 2 | Performance | 参观 | media_oriented |
| 2 | Performance | 视频创作 | media_oriented |
| 2 | Performance | 宗教仪式 | everyday_practice |
| 2 | Performance | 介绍景点 | media_oriented |
| 2 | Performance | 文化表演 | media_oriented |
| 2 | Performance | 展示 | media_oriented |
| 2 | Performance | 放风筝 | media_oriented |
| 2 | Performance | 围观 | media_oriented |
| 2 | Performance | 演讲 | media_oriented |
| 2 | Performance | 介绍 | media_oriented |
| 2 | Performance | 观看 | media_oriented |
| 2 | Performance | 舞台表演 | media_oriented |
| 2 | Performance | 展示菜品 | media_oriented |
| 2 | Performance | 推介 | media_oriented |
| 2 | Performance | 放孔明灯 | everyday_practice |
| 2 | Performance | 观看展示 | media_oriented |
| 2 | Performance | 观看展览 | media_oriented |
| 2 | Performance | 说话 | media_oriented |
| 2 | Performance | 互动 | media_oriented |
| 2 | Performance | 发言 | media_oriented |
| 2 | Performance | 展示拍立得照片 | media_oriented |
| 2 | Performance | 展示文物 | media_oriented |
| 2 | Performance | 巡游表演 | media_oriented |
| 2 | Performance | 游戏/娱乐 | media_oriented |
| 2 | Performance | 观察 | media_oriented |
| 2 | Performance | 观景性停留 | media_oriented |
| 2 | Performance | 触摸雕像 | media_oriented |
| 2 | Performance | 许愿 | everyday_practice |
| 2 | Performance | 主持 | media_oriented |
| 2 | Performance | 参观展示 | media_oriented |
| 2 | Performance | 参观展览 | media_oriented |
| 2 | Performance | 合影 | media_oriented |
| 2 | Performance | 喂锦鲤 | media_oriented |
| 2 | Performance | 喂鱼 | media_oriented |
| 2 | Performance | 展示体验 | media_oriented |
| 2 | Performance | 展示商品 | media_oriented |
| 2 | Performance | 展示小花 | media_oriented |
| 2 | Performance | 展示工艺品 | media_oriented |
| 2 | Performance | 展示手工艺品 | media_oriented |
| 2 | Performance | 展示服装 | media_oriented |
| 2 | Performance | 展示老相册 | media_oriented |
| 2 | Performance | 展示陶瓷器皿 | media_oriented |
| 2 | Performance | 展示香薰产品 | media_oriented |
| 2 | Performance | 巡游 | media_oriented |
| 2 | Performance | 开幕仪式 | media_oriented |
| 2 | Performance | 总结 | media_oriented |
| 2 | Performance | 挂祈福牌 | everyday_practice |
| 2 | Performance | 指示 | media_oriented |
| 2 | Performance | 指认 | media_oriented |
| 2 | Performance | 操作 | media_oriented |
| 2 | Performance | 烹饪 | media_oriented |
| 2 | Performance | 祈福 | everyday_practice |
| 2 | Performance | 纪念活动 | everyday_practice |
| 2 | Performance | 街头表演 | media_oriented |
| 2 | Performance | 观察细节 | media_oriented |
| 2 | Performance | 观看装饰 | media_oriented |
| 2 | Performance | 观赏 | media_oriented |
| 2 | Performance | 触摸建筑 | media_oriented |
| 2 | Performance | 讲解 | media_oriented |
| 3 | Consumption | 饮食 | everyday_practice |
| 3 | Consumption | 购物/体验 | everyday_practice |
| 3 | Consumption | 游戏/娱乐 | everyday_practice |
| 3 | Consumption | 体验 | everyday_practice |
| 3 | Consumption | 购物 | everyday_practice |
| 3 | Consumption | 喂鸽子 | everyday_practice |
| 3 | Consumption | 其他 | everyday_practice |
| 3 | Consumption | 服务 | everyday_practice |
| 3 | Consumption | 艺术创作 | everyday_practice |
| 3 | Consumption | 制作食物 | everyday_practice |
| 3 | Consumption | 劳动 | everyday_practice |
| 3 | Consumption | 工作 | everyday_practice |
| 3 | Consumption | 清理 | everyday_practice |
| 3 | Consumption | 娱乐 | everyday_practice |
| 3 | Consumption | 展示 | everyday_practice |
| 3 | Consumption | 参观 | everyday_practice |
| 3 | Consumption | 搬运 | everyday_practice |
| 3 | Consumption | 放风筝 | everyday_practice |
| 3 | Consumption | 展示菜品 | everyday_practice |
| 3 | Consumption | 喂动物 | everyday_practice |
| 3 | Consumption | 展示商品 | everyday_practice |
| 3 | Consumption | 钓鱼 | everyday_practice |
| 3 | Consumption | 互动 | everyday_practice |
| 3 | Consumption | 喂养 | everyday_practice |
| 3 | Consumption | 处理食材 | everyday_practice |
| 3 | Consumption | 排队 | everyday_practice |
| 3 | Consumption | 游戏 | everyday_practice |
| 3 | Consumption | 维修 | everyday_practice |
| 3 | Consumption | 观光 | everyday_practice |
| 3 | Consumption | 乘船 | everyday_practice |
| 3 | Consumption | 理发 | everyday_practice |
| 3 | Consumption | 观察餐车 | everyday_practice |
| 3 | Consumption | 阅读 | everyday_practice |
| 3 | Consumption | 介绍 | everyday_practice |
| 3 | Consumption | 家务 | everyday_practice |
| 3 | Consumption | 展示食物 | everyday_practice |
| 3 | Consumption | 指导 | everyday_practice |
| 3 | Consumption | 洗衣 | everyday_practice |
| 3 | Consumption | 划船 | everyday_practice |
| 3 | Consumption | 包饺子 | everyday_practice |
| 3 | Consumption | 展示美食 | everyday_practice |
| 3 | Consumption | 教育 | everyday_practice |
| 3 | Consumption | 体验服务 | everyday_practice |
| 3 | Consumption | 劳作 | everyday_practice |
| 3 | Consumption | 包粽子 | everyday_practice |
| 3 | Consumption | 品尝 | everyday_practice |
| 3 | Consumption | 喂鱼 | everyday_practice |
| 3 | Consumption | 清淤 | everyday_practice |
| 3 | Consumption | 观看表演 | everyday_practice |
| 3 | Consumption | 采摘 | everyday_practice |
| 3 | Consumption | 制作 | everyday_practice |
| 3 | Consumption | 喂锦鲤 | everyday_practice |
| 3 | Consumption | 垂钓 | everyday_practice |
| 3 | Consumption | 处理 | everyday_practice |
| 3 | Consumption | 宗教活动 | everyday_practice |
| 3 | Consumption | 操作 | everyday_practice |
| 3 | Consumption | 操作设备 | everyday_practice |
| 3 | Consumption | 放牧 | everyday_practice |
| 3 | Consumption | 救助 | everyday_practice |
| 3 | Consumption | 整理 | everyday_practice |
| 3 | Consumption | 整理商品 | everyday_practice |
| 3 | Consumption | 祈福 | everyday_practice |
| 3 | Consumption | 等待购买 | everyday_practice |
| 3 | Consumption | 观察 | everyday_practice |
| 3 | Consumption | 观看 | everyday_practice |
| 3 | Consumption | 观看电影 | everyday_practice |
| 3 | Consumption | 购物/体验, 饮食 | everyday_practice |
| 3 | Consumption | 购物/娱乐 | everyday_practice |
| 3 | Consumption | 运动 | everyday_practice |
| 3 | Consumption | 饮食/购物/体验 | everyday_practice |
| 3 | Consumption | 下棋 | everyday_practice |
| 3 | Consumption | 体检 | everyday_practice |
| 3 | Consumption | 体验智能设备 | everyday_practice |
| 3 | Consumption | 使用洗衣机 | everyday_practice |
| 3 | Consumption | 停车 | everyday_practice |
| 3 | Consumption | 准备食物 | everyday_practice |
| 3 | Consumption | 制作咖啡 | everyday_practice |
| 3 | Consumption | 制作饮品 | everyday_practice |
| 3 | Consumption | 功能性停留 | everyday_practice |
| 3 | Consumption | 化妆 | everyday_practice |
| 3 | Consumption | 参与活动 | everyday_practice |
| 3 | Consumption | 取水 | everyday_practice |
| 3 | Consumption | 喂养动物 | everyday_practice |
| 3 | Consumption | 喂山羊 | everyday_practice |
| 3 | Consumption | 喂海鸥 | everyday_practice |
| 3 | Consumption | 喂羊驼 | everyday_practice |
| 3 | Consumption | 喂骆驼 | everyday_practice |
| 3 | Consumption | 喂鸭子 | everyday_practice |
| 3 | Consumption | 学习 | everyday_practice |
| 3 | Consumption | 展示啤酒 | everyday_practice |
| 3 | Consumption | 展示海鲜 | everyday_practice |
| 3 | Consumption | 展示烤肉 | everyday_practice |
| 3 | Consumption | 手工 | everyday_practice |
| 3 | Consumption | 手工制作 | everyday_practice |
| 3 | Consumption | 抢险救灾 | everyday_practice |
| 3 | Consumption | 排队购买 | everyday_practice |
| 3 | Consumption | 揉面团 | everyday_practice |
| 3 | Consumption | 搬运食材 | everyday_practice |
| 3 | Consumption | 收摊 | everyday_practice |
| 3 | Consumption | 救援 | everyday_practice |
| 3 | Consumption | 整理蔬菜 | everyday_practice |
| 3 | Consumption | 文化展演与被凝视 | media_oriented |
| 3 | Consumption | 检查 | everyday_practice |
| 3 | Consumption | 浇酱汁 | everyday_practice |
| 3 | Consumption | 游泳 | everyday_practice |
| 3 | Consumption | 游船 | everyday_practice |
| 3 | Consumption | 烹饪 | everyday_practice |
| 3 | Consumption | 照顾盆栽 | everyday_practice |
| 3 | Consumption | 煮饺子 | everyday_practice |
| 3 | Consumption | 结束动作 | everyday_practice |
| 3 | Consumption | 结账 | everyday_practice |
| 3 | Consumption | 被救助 | everyday_practice |
| 3 | Consumption | 观景性停留 | everyday_practice |
| 3 | Consumption | 购物/用餐 | everyday_practice |
| 3 | Consumption | 运送食物 | everyday_practice |
| 3 | Consumption | 饮食/购物 | everyday_practice |
| 4 | Social interaction | 强社交 | everyday_practice |
| 4 | Social interaction | 弱社交 | everyday_practice |
| 4 | Social interaction | 交谈 | everyday_practice |
| 4 | Social interaction | 围观 | everyday_practice |
| 4 | Social interaction | 互动 | everyday_practice |
| 4 | Social interaction | 并肩 | everyday_practice |
| 4 | Social interaction | 游戏/娱乐 | everyday_practice |
| 4 | Social interaction | 欢送 | everyday_practice |
| 4 | Social interaction | 站在一起 | everyday_practice |
| 5 | Rest | 功能性停留 | everyday_practice |
| 5 | Rest | 观景性停留 | everyday_practice |
| 6 | Movement | 穿行 | everyday_practice |
| 6 | Movement | 漫游 | everyday_practice |
| 6 | Movement | 功能性停留 | everyday_practice |
| 6 | Movement | 参观 | everyday_practice |
| 6 | Movement | 双向流动 | everyday_practice |
| 6 | Movement | 引导 | everyday_practice |
| 6 | Movement | 聚集 | everyday_practice |
| 6 | Movement | 跑步 | everyday_practice |
| 6 | Movement | 观景性停留 | everyday_practice |
| 6 | Movement | 排队 | everyday_practice |
| 6 | Movement | 活动 | everyday_practice |
| 6 | Movement | 走向 | everyday_practice |
| 6 | Movement | 强社交 | everyday_practice |
| 6 | Movement | 并肩 | everyday_practice |
| 6 | Movement | 散步 | everyday_practice |
| 6 | Movement | 漫步 | everyday_practice |
| 6 | Movement | 行走 | everyday_practice |
| 6 | Movement | 运动 | everyday_practice |
| 6 | Movement | 马车 | everyday_practice |
| 6 | Movement | 准备活动 | everyday_practice |
| 6 | Movement | 攀登 | everyday_practice |
| 6 | Movement | 观光火车 | everyday_practice |
| 6 | Movement | 进出 | everyday_practice |
| 6 | Movement | 骑自行车 | everyday_practice |
| 6 | Movement | 乘船 | everyday_practice |
| 6 | Movement | 列队行进 | everyday_practice |
| 6 | Movement | 弱社交 | everyday_practice |
| 6 | Movement | 打卡/摄影 | media_oriented |
| 6 | Movement | 指路 | everyday_practice |
| 6 | Movement | 有序流动 | everyday_practice |
| 6 | Movement | 移动 | everyday_practice |
| 6 | Movement | 站立 | everyday_practice |
| 6 | Movement | 等待 | everyday_practice |
| 6 | Movement | 走动 | everyday_practice |
| 6 | Movement | 进入 | everyday_practice |
| 6 | Movement | 驾驶 | everyday_practice |
| 6 | Movement | 骑行 | everyday_practice |
