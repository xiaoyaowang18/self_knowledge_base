---
title: "Palantir 的“本体论”骗局"
source: "https://zhuanlan.zhihu.com/p/2008601762047746162"
author:
  - "[[冯若航]]"
published:
created: 2026-08-27
description: "Ontology 就是数据库建模。“本体论” 这个词唯一的作用，就是让不懂数据库的人觉得这是个新东西，然后心甘情愿地为旧东西付出一千倍的价格。 一、两种表情2025 年末，Palantir 市值冲上 4000 亿美元，在两年间翻…"
tags:
  - "clippings"
---
[收录于 · 数据系统那些事](https://www.zhihu.com/column/data-system)

航海家 王之葵托利 等 352 人赞同

[Ontology](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Ontology&zhida_source=entity) 就是 [数据库建模](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E5%BA%93%E5%BB%BA%E6%A8%A1&zhida_source=entity) 。“本体论” 这个词唯一的作用，就是让不懂数据库的人觉得这是个新东西，然后心甘情愿地为旧东西付出一千倍的价格。

## 一、两种表情

2025 年末， [Palantir](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Palantir&zhida_source=entity) 市值冲上 4000 亿美元，在两年间翻了二十多倍。 这家公司每次路演、每篇白皮书、每个技术博客，都在反复念叨同一个词： **Ontology** （本体论）。

这个词被包装成 Palantir 的核心 [技术壁垒](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E5%A3%81%E5%9E%92&zhida_source=entity) 、护城河与灵魂。 投资人听了肃然起敬， [五角大楼](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BA%94%E8%A7%92%E5%A4%A7%E6%A5%BC&zhida_source=entity) 的将军听了觉得这是 [信息战](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BF%A1%E6%81%AF%E6%88%98&zhida_source=entity) 的未来， [企业高管](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BC%81%E4%B8%9A%E9%AB%98%E7%AE%A1&zhida_source=entity) 听了觉得自己如果不买就会被时代淘汰。

*在一次面向企业 CXO 的 [AI](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=AI&zhida_source=entity) 峰会上，Palantir 的销售副总裁打出一页印着 “Ontology” 大字的 PPT。 台下的高管们微微点头，露出那种“我不太懂但感觉很厉害”的表情。旁边几位被拉来陪会的 [架构师](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E5%B8%88&zhida_source=entity) 面面相觑，其中一位低声说了一句：*

*“他说的是表和 [存储过程](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%AD%98%E5%82%A8%E8%BF%87%E7%A8%8B&zhida_source=entity) 吗？”*

*同事看了一眼 PPT 上的 [架构图](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E5%9B%BE&zhida_source=entity) ，沉默了三秒：“……是的。”*

![](https://pic2.zhimg.com/v2-32824fe57b4a4d59a456cdf1584957b5_1440w.jpg)

这就是 Palantir 最精妙的商业手法：用一个自带 2300 年哲学史威压的术语， 让不懂技术的决策者觉得这是某种前沿突破，同时让懂技术的工程师在会议室里找不到合适的方式去反驳。 因为你总不能当着 VP 的面说“老板，他们卖给我们的其实就是建表”。

最近老是有人故弄玄虚吹捧这个东西，所以今天老冯就把这件皇帝的新衣给拆穿。

---

## 二、罗塞塔石碑

先把事实摆到桌面上。Palantir Ontology 有四个核心概念： **Object Type** （对象类型）、 **[Property](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Property&zhida_source=entity)** （属性）、 **Link** （关联）、 **Action** （操作）。 翻遍他们所有的文档、白皮书、路演材料，这四个概念是一切的起点。

现在，请看这张表：

| 概念      | 哲学             | 数据库       | 面向对象            | Palantir    |
| ------- | -------------- | --------- | --------------- | ----------- |
| 事物的类型   | 范畴（Category）   | 表（Table）  | 类（Class）        | Object Type |
| 事物的特征   | 属性（Property）   | 列（Column） | 字段（Field）       | Property    |
| 事物之间的关联 | 关系（Relation）   | 外键（FK）    | 关联（Association） | Link        |
| 对事物的操作  | —              | 存储过程（SP）  | 方法（Method）      | Action      |
| 一个具体事物  | 个体（Individual） | 行（Row）    | 对象（Object）      | Object      |

四列。四种术语体系。同一件事。不是“可以类比”，不是“有点像”，而是完全重叠，严格同构。 Palantir 在文档里定义了 Interface（接口多态）、Function（ [代码逻辑](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BB%A3%E7%A0%81%E9%80%BB%E8%BE%91&zhida_source=entity) ）、 Virtual Table（ [虚拟表](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E8%99%9A%E6%8B%9F%E8%A1%A8&zhida_source=entity) ）等子概念 —— 翻译过来就是 View、UDF 和 Materialized View。

![](https://pic4.zhimg.com/v2-c18f08cf7437778161a4f9c159968067_1440w.jpg)

如果你学过数据库建模，你就已经完整掌握了 Palantir 所谓的“本体论”。 从来没有人告诉你，你会的这些东西可以套一个哲学名词，卖出每年几百万到几千万美元的合同价。

Palantir 2025 年年报披露：头部 20 个客户平均每家每年贡献 **9390 万美元** 。 全部 954 个客户平均每家贡献约 **470 万美元/年** ，这就是“表和存储过程”的标价。

---

## 三、同一个想法被卖了五次

Palantir 不是第一个“发明”这套东西的。同一个核心思想在 2300 年里被反复包装，每次换一个名字，每次都有一批人觉得这是全新的突破。

**第一次：公元前 350 年， [亚里士多德](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BA%9A%E9%87%8C%E5%A3%AB%E5%A4%9A%E5%BE%B7&zhida_source=entity) 。** 在 [《范畴篇》](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E3%80%8A%E8%8C%83%E7%95%B4%E7%AF%87%E3%80%8B&zhida_source=entity) 中提出：世界由实体（substance）组成，实体有属性，实体之间有关系。 翻译成 [SQL](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=SQL&zhida_source=entity) 就是 `CREATE TABLE person (height INTEGER); teacher_id REFERENCES person(id)` 。 这不是类比，这是同一种思维操作的不同记法。

**第二次：1976 年， [Peter Chen](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Peter+Chen&zhida_source=entity) 。** 发表 ER（实体-关系）模型，实体、属性、关系。 和亚里士多德说的完全一样，只不过从 [希腊语](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%B8%8C%E8%85%8A%E8%AF%AD&zhida_source=entity) 散文变成了矩形和菱形。这篇论文催生了整个关系数据库产业。 全世界每一个会写 `CREATE TABLE` 的程序员都在日常实践“本体论”，只是没人告诉他们这件事有哲学名。

**第三次：1990 年代，面向对象浪潮。** 类、属性、关联、方法。同一套东西加了“行为”维度。这一波里数据库也跟风搞了 [对象关系模型](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%AF%B9%E8%B1%A1%E5%85%B3%E7%B3%BB%E6%A8%A1%E5%9E%8B&zhida_source=entity) 。 PostgreSQL 里面那堆 [面向对象](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=3&q=%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1&zhida_source=entity) 的设计就是这时候跟风加进来的，这也是为啥 [数据表](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E8%A1%A8&zhida_source=entity) 的目录名字叫 `pg_class` 而不是 `pg_table` 的原因。

**第四次：2001 年， [语义网](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E8%AF%AD%E4%B9%89%E7%BD%91&zhida_source=entity) 。** [Tim Berners-Lee](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Tim+Berners-Lee&zhida_source=entity) 的愿景，OWL [本体语言](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%9C%AC%E4%BD%93%E8%AF%AD%E8%A8%80&zhida_source=entity) 的核心概念：类、属性、关系、实例，和 [ER 模型](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=ER+%E6%A8%A1%E5%9E%8B&zhida_source=entity) 完全同构。“Ontology” 这个词正式进入计算机领域就是在这一波。

**第五次：2016 年至今，Palantir [Foundry](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Foundry&zhida_source=entity) 。** Object Type、Property、Link、Action。  
注意规律： **每一次“重新发明”都伴随着一波市场狂热。** ER 模型催生了 [关系数据库](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=2&q=%E5%85%B3%E7%B3%BB%E6%95%B0%E6%8D%AE%E5%BA%93&zhida_source=entity) 市场， [OOP](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=OOP&zhida_source=entity) 催生了 Java 的狂潮，语义网催生了一波学术和创业泡沫然后破灭。 现在 Palantir 的 Ontology 搭上了 AI 叙事，公司市值在两年多里从不到 200 亿涨到超过 4000 亿美元。

这不是技术演进。这是概念轮回。每一轮周期里真正变化的不是思想，而是套在外面的包装纸和愿意为包装纸买单的人。

---

## 四、哲学名词的认知税

现在聊聊那层包装纸本身。

“Ontology”，本体论，来自希腊语 *on* （存在）+ *logos* （学问），字面意思是“关于存在的学问”。 亚里士多德研究过它， [康德](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%BA%B7%E5%BE%B7&zhida_source=entity) 讨论过它， [海德格尔](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%B5%B7%E5%BE%B7%E6%A0%BC%E5%B0%94&zhida_source=entity) 写了一整本《存在与时间》来重新定义它。你光读完维基百科上本体论的条目就需要半小时和一杯浓咖啡。

![](https://picx.zhimg.com/v2-5427ef72a17318d075fd482c138c60bf_1440w.jpg)

**这就是这个词的真正威力：它制造了 [知识不对称](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%9F%A5%E8%AF%86%E4%B8%8D%E5%AF%B9%E7%A7%B0&zhida_source=entity) 。**

当 Palantir 的销售跟一位制造业 VP 说 “我们用本体论来构建贵公司的数字孪生”时， VP 的内心活动大概是： “本体论？听起来像某种很深的学问。这一定是某种我不理解的 [前沿技术](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%89%8D%E6%B2%BF%E6%8A%80%E6%9C%AF&zhida_source=entity) 。”

如果把同样的话翻译成 [工程语言](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%B7%A5%E7%A8%8B%E8%AF%AD%E8%A8%80&zhida_source=entity) ，“我们帮你建表、定义字段、设外键、写存储过程”， VP 的反应会变成：“这不就是 IT 部门一直在做的事吗？为什么要花几千万请你来？”

**同一件事，换一个名字，价格差三个 [数量级](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E9%87%8F%E7%BA%A7&zhida_source=entity) 。** 这就是哲学名词的认知税。

![](https://pic1.zhimg.com/v2-41fef33803db47231364ba294fa13ef0_1440w.jpg)

而且这里有一个深层讽刺：Palantir 对“本体论”的使用方式恰恰是 **反哲学的** 。 真正的本体论探索的是开放性问题：“存在的边界在哪里？”“范畴能否穷尽？”这些问题的答案是流动的、不确定的。

但 Palantir 的 Ontology 做的恰恰相反。把业务实体固化成刚性的 Object Type，把关系固化成预定义的 Link， 把操作固化成审批流驱动的 Action。这不是在探索存在的本质， **这是在给现实浇模具** 。

数据分析师 Donald Farmer 在 [Substack](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Substack&zhida_source=entity) 上讲过一个真实案例： 九十年代他为一家 [美国](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%BE%8E%E5%9B%BD&zhida_source=entity) 汽车信贷公司建了一套完整的 [元数据](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%85%83%E6%95%B0%E6%8D%AE&zhida_source=entity) 本体。几个月内，业务团队换了新的分析工具，改了 [信用风险评估](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BF%A1%E7%94%A8%E9%A3%8E%E9%99%A9%E8%AF%84%E4%BC%B0&zhida_source=entity) 流程。 等本体团队赶上进度时，业务又变了。他的结论是： **一个不完整的本体论不仅仅是滞后的，它是错误的。而一个错误的本体论比没有本体论更危险。**

这是所有刚性 Schema 的宿命。但对 Palantir 来说，这不是问题， **这是 [商业模式](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%95%86%E4%B8%9A%E6%A8%A1%E5%BC%8F&zhida_source=entity)** 。模型过时了？花几百万更新。 业务变了？再买一轮咨询服务。Ontology 的刚性不是缺陷，而是锁定客户的机制。

---

## 五、几十行 SQL vs. 三千万美元

让我们从概念层下沉到工程层面。Palantir Ontology 的全部核心原语，在 PostgreSQL 用几行代码就能实现。

Object Type、Property、Link、Action、 [权限控制](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%9D%83%E9%99%90%E6%8E%A7%E5%88%B6&zhida_source=entity) 、审计日志、跨源联邦（FDW）。 Ontology 文档中吹嘘的每一个核心能力，PostgreSQL **全部原生支持** ，零许可费。

![](https://pic2.zhimg.com/v2-40f86c3072fe9e82cb4a09b6f12a699f_1440w.jpg)

我能想到反驳：“几十行 SQL 能设计一个 [schema](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=schema&zhida_source=entity) ，但能交付一个让 [供应链](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BE%9B%E5%BA%94%E9%93%BE&zhida_source=entity) 经理直接用的 [端到端](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%AB%AF%E5%88%B0%E7%AB%AF&zhida_source=entity) 平台吗？”

当然不能。但这恰恰说明： **Palantir 的价值不在 Ontology 这个概念里，而在 Ontology 之外的东西。** 在给非技术用户做 GUI 包装，在客户现场蹲点几个月理解业务流程，在搞定五角大楼的采购合同。

这些事情和“本体论”毫无关系，它们是 [产品工程](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BA%A7%E5%93%81%E5%B7%A5%E7%A8%8B&zhida_source=entity) 、咨询服务和政商关系。把苦力活包装成哲学概念，这是 Palantir 最核心的能力，也是最大的骗局。

---

## 六、挣钱后自有大儒辩经

讲到这里我们必须回答一个问题：如果技术这么平庸，Palantir 凭什么做到 3000 多亿市值、44.8 亿美元年营收、56% 的年增长率？

答案不在技术里。 **答案在 [华盛顿](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%8D%8E%E7%9B%9B%E9%A1%BF&zhida_source=entity) 。**

Palantir 由 Peter [Thiel](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Thiel&zhida_source=entity) 在 2003 年联合创办。Thiel 不是一般的 [硅谷](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%A1%85%E8%B0%B7&zhida_source=entity) 投资人。 他是特朗普最早期和最重要的科技界支持者之一，是 2016 年共和党全国代表大会的演讲嘉宾。 Palantir 的第一笔外部投资来自 CIA 的 [风险投资](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E9%A3%8E%E9%99%A9%E6%8A%95%E8%B5%84&zhida_source=entity) 部门 [In-Q-Tel](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=In-Q-Tel&zhida_source=entity) 。从成立第一天起，这家公司的 [基因](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%9F%BA%E5%9B%A0&zhida_source=entity) 就不是技术驱动，而是 **政商关系驱动** 。

2025 年的 Palantir 年报白纸黑字地写着： **54% 的收入来自政府客户** 。 美国陆军给了 Palantir 一笔 4.58 亿美元的战场情报合同。国防部签了 13 亿美元上限的 Project Maven AI 合同。 [ICE](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=ICE&zhida_source=entity) （移民和海关执法局）自 2011 年起累计拨款承诺超过 2.48 亿美元。2025 年，在特朗普政府的推动下，Palantir 拿到了为 ICE 建造 [ImmigrationOS](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=ImmigrationOS&zhida_source=entity) 的 3000 万美元合同，一个用来追踪无证移民的跨部门数据库。

这些合同是怎么拿到的？靠“本体论”的技术优越性？还是靠 Peter Thiel 在特朗普身边的位置？—— Palantir 每年在 [政治游说](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%94%BF%E6%B2%BB%E6%B8%B8%E8%AF%B4&zhida_source=entity) 上砸五百万美元。 但 Palantir 不会在路演里告诉 [投资人](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=3&q=%E6%8A%95%E8%B5%84%E4%BA%BA&zhida_source=entity) ：“我们的核心竞争力是 Peter Thiel 的政治关系网。” 它会说：“我们的核心竞争力是 **Ontology** 。”

![](https://pic3.zhimg.com/v2-2f9a3e9d6592bc213b0030db07607118_1440w.jpg)

**这就是“本体论”的真正功能：它不是技术架构，它是叙事架构。** 它让一家本质上靠政商关系拿单、靠驻场工程师堆人力交付的公司，看起来像一家拥有不可替代技术壁垒的软件平台公司。这就是典型的美国版“ [数据中台](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E4%B8%AD%E5%8F%B0&zhida_source=entity) ”与驻场外包。

---

## 七、披着 SaaS 皮的咨询公司

Palantir 有一种独特的角色叫 **FDE** ，Forward Deployed Engineer（前线 [部署工程师](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E9%83%A8%E7%BD%B2%E5%B7%A5%E7%A8%8B%E5%B8%88&zhida_source=entity) ）。 客户签约后，Palantir 会派一支工程师团队常驻客户现场，帮助梳理业务流程、建 [数据模型](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%A8%A1%E5%9E%8B&zhida_source=entity) 、开发应用、培训用户。  
这就是咨询，或者更直白的说 —— “ [人力外包](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BA%BA%E5%8A%9B%E5%A4%96%E5%8C%85&zhida_source=entity) ”。只不过 Palantir 坚称自己是软件公司而非咨询公司。 因为软件公司的 [估值倍数](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BC%B0%E5%80%BC%E5%80%8D%E6%95%B0&zhida_source=entity) 可以是营收的 70 倍，而咨询公司能拿到 2-3 倍就不错了。

[做空](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%81%9A%E7%A9%BA&zhida_source=entity) Palantir 的 [Michael Burry](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Michael+Burry&zhida_source=entity) 精准地抓住了这一点。他指出 Palantir 把 FDE 的 [人力成本](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E4%BA%BA%E5%8A%9B%E6%88%90%E6%9C%AC&zhida_source=entity) 归类为“研发”或“ [销售与市场](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E9%94%80%E5%94%AE%E4%B8%8E%E5%B8%82%E5%9C%BA&zhida_source=entity) ”费用， 而非 [营收成本](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E8%90%A5%E6%94%B6%E6%88%90%E6%9C%AC&zhida_source=entity) （cost of revenue）。如果按 [Accenture](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Accenture&zhida_source=entity) 的会计准则来算，Palantir 引以为傲的高 [毛利率](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%AF%9B%E5%88%A9%E7%8E%87&zhida_source=entity) 将大幅缩水。

一位前 FDE 对 Burry 说了一句话： **“Foundry 不是 [永久许可证](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%B0%B8%E4%B9%85%E8%AE%B8%E5%8F%AF%E8%AF%81&zhida_source=entity) 。你必须经过培训才能用它。即便如此，你还是需要大量的持续支持。”**  
那些 FDE 在客户现场实际做的事情是什么？写 [ETL](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=ETL&zhida_source=entity) 管道把数据从 [SAP](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=SAP&zhida_source=entity) 搬到 Foundry，调试 [Kafka](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Kafka&zhida_source=entity) 连接器，处理 [Oracle](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Oracle&zhida_source=entity) 和 [Snowflake](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Snowflake&zhida_source=entity) 的 schema 不兼容， 给业务用户解释为什么某个 Link 定义需要修改。 **这些工作的本质就是 [数据集成](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E6%88%90&zhida_source=entity) 和胶水代码** ，是 [软件工程](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B&zhida_source=entity) 里最最消耗人力、最依赖蹲点理解业务的苦力活。

每一个做过企业 [数据仓库](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E4%BB%93%E5%BA%93&zhida_source=entity) 项目的工程师都知道这种活：累、琐碎、 [没有银弹](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E6%B2%A1%E6%9C%89%E9%93%B6%E5%BC%B9&zhida_source=entity) 。全世界有成千上万的 SI（ [系统集成商](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%B3%BB%E7%BB%9F%E9%9B%86%E6%88%90%E5%95%86&zhida_source=entity) ）在做同样的事情。 [埃森哲](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%9F%83%E6%A3%AE%E5%93%B2&zhida_source=entity) 在做， [德勤](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%BE%B7%E5%8B%A4&zhida_source=entity) 在做， [Infosys](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=Infosys&zhida_source=entity) 在做，中国的各种数据中台厂商也在做。区别在于，他们没有把这些人力活包装成“本体论”，所以他们的估值倍数只有 Palantir 的百分之一。

**Ontology 的概念复杂度恰恰服务于这种商业模式。** 如果你把 Object Type 叫做“表”，把 Action 叫做“存储过程”，客户的 IT 部门会说“这个我们自己能干”。 但如果你把它叫做“本体论”，引入 semantic layer、kinetic layer、dynamic layer 三层架构术语，让整个建模过程需要在专有 GUI 里手动点击几十分钟才能完成。 那么客户就永远离不开你的 FDE 了。

![](https://pica.zhimg.com/v2-fc8597f1ec00e143f08cc89cbb036f1c_1440w.jpg)

**系统越难用，客户越依赖。概念越晦涩，FDE 越不可替代。这不是 bug，这是 feature。**

Palantir 自己的数据也在印证这一点：2025 年客户数量增长了 34%，但头部 20 客户的平均年贡献增长了 45%。 [CEO](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=CEO&zhida_source=entity) Alex Karp 在财报电话会上说了一句意味深长的话： **“未来会有无法解释的收入增长，但不会有无法解释的客户数量增长。”** 翻译成白话：我们不打算赢得更多客户，我们打算从已有的客户身上榨取更多的钱。

这是咨询公司的增长模型，不是软件平台的增长模型。

---

## 八、Ontology 买家画像

谁在买 Palantir？

看看客户名单你就明白了。美国陆军、ICE、CDC、 [NHS](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=NHS&zhida_source=entity) （英国 [国民医疗服务体系](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E5%9B%BD%E6%B0%91%E5%8C%BB%E7%96%97%E6%9C%8D%E5%8A%A1%E4%BD%93%E7%B3%BB&zhida_source=entity) ）、空客、 [BP](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=BP&zhida_source=entity) 。这些组织有几个共同特征：

**第一，决策者不懂技术。** 五角大楼的采购官不知道什么是外键。 NHS 的管理层不关心 ETL 管道怎么写。 他们需要的是一个听起来高级的概念， 来证明自己几千万的采购决策是“战略性”的。 “我们引入了 Palantir 的本体论驱动的数字孪生平台”， 这句话写在任何一份汇报 PPT 里， 都比“我们请了一个外包团队帮我们建了几张表”好看一万倍。

**第二，花的是公家的钱。** 政府合同的特点是预算充裕但缺乏技术审计能力。 没有人会因为花了三千万买 Palantir 而丢工作。 但如果你提议用开源方案自建，出了问题就是你的责任。 这是经典的“没人因为买 [IBM](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=IBM&zhida_source=entity) 而被开除”的现代翻版。 只不过 IBM 换成了 Palantir，大型机换成了“本体论”。

**第三， [路径依赖](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E8%B7%AF%E5%BE%84%E4%BE%9D%E8%B5%96&zhida_source=entity) 一旦形成就极难逆转。** 一旦你的业务模型被编码进 Palantir 的 Ontology， 你的团队被训练成只会用 Palantir 术语思考， 你的 Object Type 不是标准 SQL 表， 你的 Action 不是标准 [REST API](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=REST+API&zhida_source=entity) ， 你的整个语义层被锁在专有平台里。 迁出成本就变得高到不可承受。 这就是 Palantir 净收入留存率高达 134% 的秘密。 不是因为产品好到客户主动加购， 而是因为 **锁定效应** 让客户除了加购之外别无选择。

---

## 九、总结

**Ontology 是什么？** 一种有 2300 年历史的建模方法。对事物、属性、关系和操作进行形式化描述。 它的每一个核心概念都可以一对一映射为数据库原语。任何一本数据库教科书的前三章就能覆盖其全部内容。Palantir 没有发明任何新东西。

**Palantir 的真正竞争力是什么？** 不是 Ontology，而是 Peter Thiel 的政治关系网、FDE 驻场服务的人力密集模式，以及在政府和大企业中制造路径依赖的能力。 这三样东西，政商关系、咨询外包、锁定效应，没有一样跟“本体论”这个概念有半毛钱关系。

**“本体论”的真正功能是什么？** 叙事工具。它让一家实质上是政商关系 + 咨询外包的公司，能够在资本市场上享受顶级 SaaS 的估值倍数。 它让非技术决策者相信自己在购买某种深不可测的“核心技术”，而不是在签一份高价的系统集成外包合同。

说穿了，Palantir 做的事情就是： **把写 ETL、建表、配权限这些每天都有成千上万工程师在做的苦力活，套了一个亚里士多德的名词，卖了一个 AI 时代的估值。**

这就像一个米其林厨师在菜单上写 “分子重构 [碳水化合物](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=%E7%A2%B3%E6%B0%B4%E5%8C%96%E5%90%88%E7%89%A9&zhida_source=entity) 结晶配有机蛋白质凝胶”。端上来其实是蛋炒饭。 蛋炒饭可以做得很好吃，但你不能说“分子重构”是核心技术壁垒。尤其是当这盘蛋炒饭年收费九千万，且由 Peter Thiel 亲自端上桌的时候。

这套概念，与中国盛行的 “数据中台” 炒作有异曲同工之妙。下次你要是看见有乙方在 PPT 里大谈 “本体论”，留个心眼，十有八九是大忽悠。

---

*注：本文引用的财务数据来自 Palantir 2025 年 10-K 年报（ [SEC](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=SEC&zhida_source=entity) Filing）、 [MacroTrends](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=MacroTrends&zhida_source=entity) ，以及 [OpenSecrets](https://zhida.zhihu.com/search?content_id=270498788&content_type=Article&match_order=1&q=OpenSecrets&zhida_source=entity) 公开数据。 Michael Burry 做空信息来自其 2025 年 11 月 SEC 披露及后续 Substack 文章。*

还没有人送礼物，鼓励一下作者吧

发布于 2026-02-21 18:08・上海[Qwen3.8-Max首发尝鲜，个企双版超值优惠低至39元/月起](https://click.aliyun.com/m/20000000945/?cb=https%3A%2F%2Fsugar.zhihu.com%2Fplutus_adreaper_callback%3Fsi%3D1248bacc-a3a9-484a-9dd4-667d7a5f5704%26os%3D3%26zid%3D1629%26zaid%3D3785795%26zcid%3D3805795%26cid%3D3805795%26event%3D__EVENTTYPE__%26value%3D__EVENTVALUE__%26score%3D__EVENTSCORE__%26ts%3D__TIMESTAMP__%26cts%3D__TS__%26mh%3D5349c1beea4fd8c65e24c488f9b8ddcb%26adv%3D645640%26ocg%3D0%26cp%3D0%26ocs%3D0%26aic%3D0%26atp%3D0%26ct%3D0%26ed%3DGiBNJgVzfCMmUW9XFyEvRA8xBGxJICwkOhh0FlwxKw1ZY0gnWzUoISkYf1UXISFcCiIEeh4yNyw9GGJBRCUlVFZ0DHMIc2h3fRVrVwZgfwdZY1YkXSo-fXgdY18DaHsGTSlMdw57a3h8HWVRFyI5WVZ3Wy8Me25yfQg3UwJmYQQJJg9nWXdpcGNGY1MGYXgIUn0Oe1k5vcuTkEQKow%3D%3D&spu=biz%3D0%26ci%3D3805795%26si%3D2be48423-e436-4bc6-a430-c1471489871a%26ts%3D1787817768%26zid%3D1629)

[

Qwen3.8-Max 首发尝鲜、上新 deepseek-v4-flash，更多模态和旗舰模型共享额度，个企双版本超值优惠低至 39 元/...

](https://click.aliyun.com/m/20000000945/?cb=https%3A%2F%2Fsugar.zhihu.com%2Fplutus_adreaper_callback%3Fsi%3D1248bacc-a3a9-484a-9dd4-667d7a5f5704%26os%3D3%26zid%3D1629%26zaid%3D3785795%26zcid%3D3805795%26cid%3D3805795%26event%3D__EVENTTYPE__%26value%3D__EVENTVALUE__%26score%3D__EVENTSCORE__%26ts%3D__TIMESTAMP__%26cts%3D__TS__%26mh%3D5349c1beea4fd8c65e24c488f9b8ddcb%26adv%3D645640%26ocg%3D0%26cp%3D0%26ocs%3D0%26aic%3D0%26atp%3D0%26ct%3D0%26ed%3DGiBNJgVzfCMmUW9XFyEvRA8xBGxJICwkOhh0FlwxKw1ZY0gnWzUoISkYf1UXISFcCiIEeh4yNyw9GGJBRCUlVFZ0DHMIc2h3fRVrVwZgfwdZY1YkXSo-fXgdY18DaHsGTSlMdw57a3h8HWVRFyI5WVZ3Wy8Me25yfQg3UwJmYQQJJg9nWXdpcGNGY1MGYXgIUn0Oe1k5vcuTkEQKow%3D%3D&spu=biz%3D0%26ci%3D3805795%26si%3D2be48423-e436-4bc6-a430-c1471489871a%26ts%3D1787817768%26zid%3D1629)

赞同 352