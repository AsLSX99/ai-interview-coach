# ai-interview-coach

> 开源 AI 工程**面试教练**（SKILL）——驱动 [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) 的 `interviews/` 题库：**23 张题卡 482 道题 + 60 个真实事故场景 + 7 个岗位视图 + 现成整轮面试脚本**，按岗位定时模拟、逐题评分校准级别、事故场景逐条放证据、弱项自动回链到课。

面试准备的死穴是**自我感觉良好**。这个 Skill 是带着标准答案、追问题库、错误答案清单和掐表的面试官：你先答，他后对分，分数钉死级别。

## 三件套定位

| Skill | 管什么 | 单位 |
|---|---|---|
| 学习型（上课） | 输入：理解 | 一节课 |
| 特训型（练题） | 输出：写代码 | 一道题 |
| **本 Skill（面试）** | **检验：被考 + 校准** | **一道题 / 一轮面试** |

三者独立安装互不依赖，但通过题目的 `lessons`（回链补课）和 `practice`（coding 轮转给判分器）字段天然串联。

## 仓库结构

```
ai-interview-coach/
├── SKILL.md                        # 主文档：建档 + 备考模式 + 6 条铁律
├── README.md
├── LICENSE
├── references/
│   ├── cards-map.md                # 23 卡 × 6 组地图 + 7 岗位矩阵 + 倒排节奏
│   ├── scoring-rubric.md           # 0-3 分标尺 + 级别校准表 + 追问/错答规则
│   └── round-playbook.md           # 摸底/单题/整轮/事故/behavioral 各轮执行手册
├── templates/
│   ├── interview-plan.md           # 备考计划（目标/基线/日程/补学清单）
│   ├── mock-report.md              # 整轮模拟报告（校准 + 弱项 Top3 + 待办）
│   └── behavioral-story.md         # STAR 故事库 + 题型映射 + 追问链
└── scripts/
    └── interview.py                # pick/ask/reveal/log/status/weak/scenario（零依赖）
```

## 题库长什么样

**482 道题**分布在 23 张题卡（6 组：地基 / 模型 / 应用 / 智能体 / 生产 / 整轮），每题一个 markdown：

```yaml
id: why-scale-by-sqrt-dk
kind: concept          # concept|debug|trade-off|estimate|code reading|design|take-home|incident
level: 1               # 1 Screen → 2 Working → 3 Senior → 4 Staff
roles: [inference-engineer, applied-ai-engineer, ...]
minutes: 6             # 掐表用
lessons: [phases/07-transformers-deep-dive/02-self-attention-from-scratch, ...]  # 弱项回链
practice: [scaled-dot-product-attention]   # coding 轮转给特训 Skill
```

正文自带五段：**Short answer**（标准要点）→ **Full answer**（完整解析）→ **Follow-ups**（按 1-4 级递进的追问）→ **Wrong answers**（常见错误答案 + 驳斥）→ **Taught in**（出自哪节课）。

**60 个事故场景**是另一形态：Situation + 系统环境 → **证据文件逐条放**（启动日志、崩溃现场、手册原文……）→ 5 个排查问题 → Walkthrough（带数字的标准排查链）→ Resolution（flag、值、验证方式）。

## 核心机制

### 防剧透（最重要）
`ask` 只输出题面和限时，**答案、追问、错误清单全部封印**；用户限时作答完毕才 `reveal`。事故场景更严：`scenario` 只给 Situation 和证据文件名，**问题与解析封印**，证据要用户像排查事故一样点名索取，点错方向本身记分。

### 0-3 分固定标尺
| 分 | 标准 | 排期 |
|---|---|---|
| 3 | 要点齐 + 追问全过 + 有验证手段 | +30 天毕业 |
| 2 | 主干对但浅（缺边界/验证） | +3 天 |
| 1 | 沾边：方向对机制错 | +1 天 |
| 0 | 没答出 / 命中 Wrong answers | 明天重考，2 次 0 分强制回链补课 |

**追问分与主干分分开记**——级别校准只信追问分，防"背过题面"。

### 级别校准（整轮后）
得分率 ≥90% 稳 / 70-89 边缘 / 50-69 低半级 / <50 低一级。同卡两题 ≤1 分 → 该卡标红进补学清单。

### 弱项闭环
0/1 分的题自动从 frontmatter 拉出 `lessons` → `weak` 命令输出"题 · 分 · 补学课"三列清单 → 课交给学习型 Skill，coding 轮的题交给特训 Skill。

## 如何使用

**① 作为 Agent 技能安装**：本目录克隆/复制到你的 AI Agent 识别技能的目录，目录名保持 `ai-interview-coach`，`SKILL.md` 直接位于其内；课程仓库克隆到任意位置即可（脚本自动向上找 `interviews/`）。

**② 直接当开场指令**：`SKILL.md` 全文发给 Agent，再说"帮我准备 AI 工程面试"。

**③ 只用脚本**：
```bash
python scripts/interview.py pick --role agentic-ai-engineer --level 2
python scripts/interview.py ask <id>          # 只亮题
python scripts/interview.py reveal <id>       # 作答后对答案
python scripts/interview.py log <id> --score 2 --followup 1
python scripts/interview.py status            # 各卡均分
python scripts/interview.py weak              # 弱项补学清单
```

## 环境准备

| 依赖 | 用途 | 获取方式 |
|---|---|---|
| **AI Agent**（Claude Code / Codex / 其他支持 SKILL.md 的宿主） | 执行面试协议 | 你现有的工具链 |
| **课程仓库** | 题库、场景、岗位与轮次定义 | `git clone --depth 1 https://github.com/rohitg00/ai-engineering-from-scratch.git` |
| **Python ≥ 3.9** | 跑脚本 | 无第三方依赖 |

## 快速开始

1. 克隆课程仓库（任意位置）
2. 安装本 Skill（或把 `SKILL.md` 发给你的 Agent）
3. 说 **"帮我准备 AI 工程面试"** → 建档四问（岗位/级别/日期/轮次）+ 摸底轮 → 拿到 `interview-plan.md`
4. 日常：单题练 3-5 题/次；模拟期每两天一场整轮 → `mock-report.md`
5. 面试前一晚：只看 mock-report 弱项 Top3 + STAR 故事库

## 七个岗位速查

| 岗位 | 核心卡前四 |
|---|---|
| applied-ai-engineer | prompting → rag → evaluation → tokenization |
| agentic-ai-engineer | agents → protocols → multi-agent → sandboxes |
| ai-evaluation-reliability-engineer | evaluation → math → rag → agents |
| ai-data-engineer | math → tokenization → rag → evaluation |
| forward-deployed-ai-engineer | rag → prompting → agents → protocols |
| ai-developer-relations-engineer | prompting → agents → protocols → rag |
| inference-engineer | inference-serving → gpu-memory-quantization → transformers → tokenization |

完整矩阵与倒排备考节奏见 `references/cards-map.md`。

## 设计原则

1. **先答后对**——标准答案提前露脸，模拟就退化成朗读
2. **掐表执行**——真实面试没有延时，超时按未完成记
3. **追问才算校准**——题面会背，追问不会
4. **分数不信感觉**——0-3 标尺固定，Wrong answers 反向检验防蒙对
5. **弱项必须回链**——只记"多复习"是假努力，回链到课才算闭环
6. **状态永远落盘**——换会话换机器都能接

## 常见问题

**Q：和课程仓库自带的 skills 什么关系？**
互补。原仓库 `loops/` 里写着"由 interview-prep skill 跑这些轮次"——本 Skill 是独立实现的面试协议与记账工具，不依赖其内部状态格式，可单独用、可裁剪。

**Q：题库会更新吗？**
会——本仓库不复制任何题目，题库以课程仓库 `interviews/` 为准，上游 `git pull` 即同步；`cards-map.md` 是速查索引，权威以 `topics.yaml` / `roles.yaml` 为准。

**Q：没有目标公司信息怎么办？**
用仓库自带 `loops/`（如 inference-engineer 六轮 240 分钟）或按岗位卡自组六轮（screen 30 / 深度 45 / 调试 45 / 设计 60 / coding 45 / behavioral 15）。拿到真实面试结构后改建档即可。

**Q：behavioral 没话说？**
先用 `templates/behavioral-story.md` 建 STAR 故事库（每题型至少一个故事），再进轮——没故事的 behavioral 轮只能干聊。

**Q：进度文件要提交 git 吗？**
建议提交（复盘资产）；想私有加进 `.gitignore`。

## 致谢

- 题库、场景、答案与全部课件：[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)（MIT）
- 本仓库只提供面试协议与记账工具，题目与答案版权归原作者所有

## License

[MIT](./LICENSE)
