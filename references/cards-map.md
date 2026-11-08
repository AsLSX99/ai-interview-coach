# 题卡地图与岗位矩阵

> 建档选岗位、抽题定范围用。权威数据是课程仓库的 `interviews/topics.yaml`（23 卡 6 组）和 `interviews/roles.yaml`（7 岗位），本文件是速查版；有出入以仓库为准。

## 23 张题卡 × 6 组

### Foundations（地基，人人必考）
| 卡 | 题量 | 考什么 |
|---|---|---|
| math-classical-ml | 22 | 线性代数、概率、优化、传统模型 |
| deep-learning | 22 | 反向传播、损失、优化器、训练不收敛怎么查 |
| transformers | 24 | 注意力、位置编码、KV cache、长上下文代价 |
| tokenization-decoding | 22 | 分词、采样、beam search、解码策略 |

### Models（训练后的事）
| 卡 | 题量 | 考什么 |
|---|---|---|
| post-training | 24 | SFT/RLHF/DPO、对齐流程 |
| inference-serving | 32 | batching、KV cache、prefix cache、调度器、压测 |
| gpu-memory-quantization | 10 | 显存估算、量化、硬件选型 |

### Applications（应用层）
| 卡 | 题量 | 考什么 |
|---|---|---|
| rag | 26 | 检索、重排、分块、评测 |
| prompting-structured-output | 22 | 提示工程、结构化输出、工具调用格式 |
| evaluation | 26 | 指标设计、基准陷阱、LLM-as-judge |
| multimodal | 22 | 图文音视频模型与融合 |

### Agents（智能体）
| 卡 | 题量 | 考什么 |
|---|---|---|
| agents | 26 | agent 循环、规划、记忆、工具 |
| protocols | 22 | MCP / A2A / Skills 协议 |
| multi-agent | 20 | 多智能体协作与拓扑 |
| sandboxes | 18 | 沙箱隔离与执行安全 |
| evidence-reverse-engineering | 14 | 二进制证据、逆向 |

### Production（生产运维）
| 卡 | 题量 | 考什么 |
|---|---|---|
| production-mlops | 26 | 发布、监控、回滚、流水线 |
| cost-capacity | 22 | 成本核算、容量规划 |
| safety | 22 | 越狱防御、红队、治理 |

### Rounds（整轮）
| 卡 | 题量 | 考什么 |
|---|---|---|
| system-design | 22 | 系统设计题 |
| scenarios | 60 | **事故排查场景**（逐条放证据） |
| coding | 22 | 编码题（指向 practice/ 题库） |
| behavioral | 16 | 行为面 |

**题量合计 542 项**（482 道题 + 60 个场景）。

## 题型（kind）与级别（level）

| kind | 形式 | 打分侧重 |
|---|---|---|
| concept | 概念解释 | 因果链完整、不背定义 |
| debug | 给症状找根因 | 定位路径 + 验证手段 |
| trade-off | 选型/取舍 | 边界条件 + 决策依据 |
| estimate | 估算 | 假设明确 + 量级正确 |
| code reading | 读代码找问题 | 指出脆弱行 + 解释为什么 |
| design | 设计题 | 需求→约束→方案→验证 |
| take-home | 作业题 | 架构 + 可运行 + 权衡说明 |
| incident | 事故场景 | 证据驱动的排查链 |

| level | 档位 | 追问深度 |
|---|---|---|
| 1 | Screen | 一道概念/估算，过了就过 |
| 2 | Working | 能落地：边界、验证、常见坑 |
| 3 | Senior | 能取舍：为什么不用另一种方案 |
| 4 | Staff | 能统盘：跨系统影响、成本、演进路线 |

## 7 个岗位 × 卡片矩阵（roles.yaml）

| 岗位 id | 中文 | 核心卡（前 8） |
|---|---|---|
| `applied-ai-engineer` | 应用 AI 工程师 | prompting-structured-output → rag → evaluation → tokenization-decoding → cost-capacity → safety → post-training → multimodal |
| `agentic-ai-engineer` | 智能体工程师 | agents → protocols → multi-agent → sandboxes → prompting → evaluation → safety → multimodal |
| `ai-evaluation-reliability-engineer` | AI 评测与可靠性 | evaluation → math → rag → agents → production-mlops → safety → … |
| `ai-data-engineer` | AI 数据工程师 | math → tokenization → rag → evaluation → production-mlops → cost-capacity → … |
| `forward-deployed-ai-engineer` | 前置交付工程师 | rag → prompting → agents → protocols → evaluation → cost-capacity → safety → … |
| `ai-developer-relations-engineer` | 开发者关系 | prompting → agents → protocols → rag → evaluation → transformers → … |
| `inference-engineer` | 推理工程 | inference-serving → gpu-memory-quantization → transformers → tokenization → cost-capacity → … |

每个岗位完整卡片序（含 rounds 收尾卡）见 `roles.yaml`；带 `path` 的岗位在 `learning-paths/` 有完整职业路径 JSON。

## 按面试日期倒排的推荐节奏

| 距面试 | 每天 | 重点 |
|---|---|---|
| >3 周 | 2-3 题 + 1 个场景 | 弱项卡从 0 分题的 lessons 补起 |
| 1-3 周 | 4-5 题 + 每两天 1 场景 | 进入整轮模拟，掐表 |
| <1 周 | 每天 1 整轮 + behavioral | 只刷 2-3 分边缘题，0 分题不再碰新卡 |
| 前一晚 | 不新题 | 过一遍 mock-report 的弱项 Top3 和 STAR 故事 |
