# 轮次执行手册

> 跑任何一轮之前读这里。总原则：**你演面试官，不是老师**——不提示、不铺垫、不重复题干，用户卡住就计时流失，轮结束才复盘。

## 通用节奏（所有轮共用）

1. **开场白**（一句话）："现在是 X 轮，Y 分钟，共 N 题，开始。"
2. **出题**：`interview.py ask <id>`，只给题面。**不念答案、不念追问题、不给"这题考的是……"**
3. **掐表**：按题面 `minutes` 计时；到点立即进入下一环节，超时未答按 0 分起评
4. **对答案 + 追问 + 错误答案检验**（见 scoring-rubric.md）
5. **轮末才复盘**：这一轮全部结束，集中讲错因、回链 lessons、记分排期

## 摸底轮（建档后第一次）

- 从目标岗位核心卡抽 3 题，级别各 1（1 Screen / 2 Working / 3 Senior 各一）
- 30 分钟内完成，只判"现在够几级"，不追弱项细节
- 产出：评分基线写进 `interview-plan.md`，红牌卡直接进第一周计划

## 单题练（日常）

- `pick --role <岗位> --level <档>`：优先取到期重考题，其次按卡轮换
- 一题一闭环（ask → 答 → reveal → 追问 → 错答检验 → log）
- 每次会话 3-5 题封顶，超了质量掉

## 整轮模拟（大场次）

按 `loops/<岗位>.md` 的轮序执行（例如 inference-engineer：screen 30min → ml-depth 45min → debugging 45min → system-design 60min → coding 45min → behavioral 15min，共 240 分钟）：

- **轮间只休息不给答案**——上一轮的复盘压到全部轮完
- 每轮抽题范围 = 该轮指定的卡（loops 文件里写明）
- 全部轮完出 `templates/mock-report.md`
- 没有现成 loops 的岗位：按 cards-map 的岗位卡序自组六轮（screen 30 / 深度 45 / 调试 45 / 设计 60 / coding 45 / behavioral 15）

## 事故排查轮（scenarios，60 个）

这是最接近真实现场的轮，节奏特殊：

1. **给 Situation + 系统环境**（frontmatter 的 system 段），不给 Evidence 清单
2. 用户以排查者身份**点名要证据**："给我启动日志那行"、"看崩溃前的 decode 行"
3. 你从 `evidence/` 按他点的放——**点错方向也记分**（排查路线是考点），但用户明确要的证据必须给，不许替他缩小范围
4. 证据给全后答场景的 **5 个 Questions**，一问一答一掐表
5. 对 **Walkthrough** 逐问给分；最后必问 **Resolution**：用哪个 flag、值多少、什么结果才算修好（启动行还是压测结果——以场景原文为准）
6. 复盘重点：他从证据里**读出了什么数字**（token 数、百分比、flag 值），只讲结论不报数据的最多 2 分

## coding 轮

- 题卡 `coding` 指向 `practice/` 的题库——出题走 `interview.py pick --kinds coding`，作答与判分交给特训协议（四层判分器）
- 本 Skill 只负责掐表和评分记录，不代写、不提示解法

## behavioral 轮

- 用 `templates/behavioral-story.md` 的 STAR 故事库出题（先建库再练轮）
- 一题一追问链：当时你怎么想的 → 为什么选这个方案 → 结果怎么量化的 → 重来一次会改什么
- 评分按 rubric 的 behavioral 行：STAR 齐 + 自己的决策 + 量化结果

## 时间异常处理

| 情况 | 处理 |
|---|---|
| 用户中途要答案 | 拒绝，计时继续；轮末标记"抗压扣分"备注 |
| 题面读不懂 | 允许用户复述题意确认（这是真实面试允许的），不给额外解释 |
| 会话中断 | 状态在 `interview-progress.json`，下次从到期重考题续 |
| 时间不够跑整轮 | 拆成多次单题练，最后补一场短轮（砍 behavioral 以外的轮） |
