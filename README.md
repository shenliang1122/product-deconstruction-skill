# 证据驱动产品拆解

一个用于数字产品和 AI 产品研究的 Agent Skill。把截图、可访问页面、源代码、运行记录和生成资产整理成可追溯的分析，从**用户、技术、模型、数据**四层还原产品，并输出独立 HTML 报告。

**先有证据，再做结论。** 每项重要判断都要说明来源、适用范围和仍未确认的部分。证据不足时，交付证据就绪度与采集清单；证据只覆盖某次运行时，结论也限定在这次运行。

- Skill 名称：`evidence-driven-product-deconstruction`
- 界面显示名称：`产品拆解`
- 主要交付：带证据索引、流程图、现状分析和改进建议的 HTML 报告

## 适合做什么

| 场景 | 分析重点 |
| --- | --- |
| 用户旅程与体验拆解 | 从入口到结果，还原选择、确认、修改、失败与恢复路径 |
| 完整产品与架构拆解 | 连接用户、技术、模型、数据四层，区分可见行为与不可见实现 |
| Agent 与工作流分析 | 区分界面角色、工作流阶段、Agent 职责、运行实例和工具调用 |
| AIGC 创作工具分析 | 追踪素材、生成资产、版本、引用、预览、导出与完成状态 |
| 竞品研究 | 在明确的范围和证据时点下比较产品行为与官方能力声明 |
| 按已有框架重构报告 | 适配飞书、Notion、Wiki 或自有模板，保留证据边界和未评分项 |

类型指南覆盖 AIGC 创作工具、通用执行 Agent、对话陪伴、Agent/工作流搭建、通用 SaaS/工作台、内容/社区和交易/市场平台。根据产品的核心流程选择分析重点；没有 AI 行为证据时，模型层可标记为未知或不适用。

## 快速开始

### 1. 安装到 Codex

可以在 Codex 中交给内置安装器处理：

```text
使用 $skill-installer，从以下仓库安装 Skill：
https://github.com/shenliang1122/product-deconstruction-skill

SKILL.md 位于仓库根目录，安装名称为 evidence-driven-product-deconstruction。
```

也可以在 macOS、Linux 或 WSL 的终端中手动安装到用户级 Skill 目录：

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/shenliang1122/product-deconstruction-skill.git \
  "$HOME/.agents/skills/evidence-driven-product-deconstruction"
```

安装后，在 Codex 中输入 `$evidence-driven-product-deconstruction` 调用。如果未出现，重启 Codex 后再试。上述发现路径与刷新方式见 [OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。

如果采用上面的 Git 克隆方式安装，可用以下命令更新：

```bash
git -C "$HOME/.agents/skills/evidence-driven-product-deconstruction" pull --ff-only
```

请保留整个目录，包括 `references/`、`assets/` 和 `scripts/`。仅复制 `SKILL.md` 会缺少它引用的规则和校验工具。其他支持 Skill 的 Agent 环境可按各自的目录发现规则加载，具体文件读取、浏览器和命令执行能力由宿主提供。

### 2. 准备证据

至少提供能支持当前问题的可检查材料，并说明分析对象、范围和时间：

| 材料 | 建议包含的内容 |
| --- | --- |
| 截图或录屏 | 按操作顺序排列，保留输入、中间状态、确认步骤和结果；错误或重试如有也一并提供 |
| 产品网址 | 具体页面、允许访问的范围，以及需要观察的功能或任务 |
| 源代码 | 版本或提交、入口、核心模块、配置、数据模型及相关测试或日志 |
| 运行记录 | 原始消息、任务/子任务状态、工具调用、输入输出和时间顺序 |
| 生成资产 | 可读取的原文件、来源、版本，以及对应的任务状态 |
| 官方资料 | 官方页面或文档链接，用于核对公开能力与当前配置 |
| 自有分析框架 | 可访问的全文或导出文件，用于确定报告结构和分析问题 |

一张结果截图可以证明该页面显示了什么，但通常不足以还原完整旅程。旧报告、文件名和图片说明可用于定位材料，不能替代原始内容。

### 3. 发起一次拆解

将证据放进当前工作目录或附在对话中，然后发送：

```text
使用 $evidence-driven-product-deconstruction 拆解这个产品。

分析对象：我提供的这次完整任务运行。
证据：当前目录中的操作截图、运行记录和生成文件，截图已按顺序命名。
目标：还原用户旅程，并分析用户、技术、模型和数据四层。
边界：只读，不发送消息、不触发生成或重试。
交付：独立 HTML 报告，保留证据编号、缺口和冲突，分开呈现 As-Is 与 To-Be。

请先检查证据是否充分；如果不足，只分析有证据支持的范围。
```

## 分析方法

### 结论与证据对应

| 编号 | 标签 | 可以支持的内容 |
| --- | --- | --- |
| `E##` | 页面/代码事实 | 当前界面、代码、日志或运行记录直接可见的行为 |
| `O##` | 官方公开 | 官方在访问时声明的产品能力，不自动证明本次运行使用了该能力 |
| `A##` | 资产事实 | 文件真实存在及其可检查属性，不自动证明内容正确或平台已完成 |
| `R##` | 合理推断 | 对现有证据的解释，保留其他实现可能 |
| `G##` | 尚未确认 | 缺失的证据与待验证的问题 |
| `C##` | 证据冲突 | 两个或多个信号不一致，保留所有信号 |
| `M##` | 方法/框架来源 | 用户提供的分析结构、问题或评分规则，不作为产品事实 |
| — | 建议设计 | 未来改进方案，仅出现在 To-Be 部分 |

例如，官方文档声称支持 Multi-Agent，最终报告文件也确实存在，但本次任务没有子任务或独立运行实例记录：前两项分别属于 `O##` 和 `A##`，本次是否启动多个 Agent 仍是 `G##`。

### 四层分析与跨层追踪

| 层级 | 核心问题 |
| --- | --- |
| 用户层 | 用户想完成什么？在哪里做决定、确认结果、修改或恢复？ |
| 技术层 | 界面、编排、工具、状态、异步、权限、计费和错误处理如何衔接？ |
| 模型层 | 有哪些可见的模型配置、上下文、路由、能力限制和评估证据？ |
| 数据层 | 谁生产和消费数据？资产如何引用、版本化、传递并反映到状态？ |

报告至少追踪一条贯穿四层的路径，并保留不可见环节的缺口：

```text
用户动作 → UI 事件 → 工作流/Agent 判断 → 工具/模型调用
        → 数据/资产写入 → 状态投影 → 用户确认或失败恢复
```

不可见的数据库、队列、云服务和模型供应商保持未知；实现建议放入 To-Be。模型选择器只能证明存在可见配置，多个角色名称也不能单独证明启动了多个 Agent 实例。

### 分别验证完成信号

报告会分别检查：**文字声明、资产存在、内容有效、平台权威状态、费用或外部副作用结算**。这些信号不能互相替代。

例如，聊天显示“已完成”，但任务进度仍为 3/4：报告应记录状态冲突，而不能只凭回复判定整次任务完成。

## 更多使用示例

### 分析 Agent 与上下文

```text
使用 $evidence-driven-product-deconstruction 分析这些运行记录。
区分 UI Persona、Workflow Stage、Agent Role、Runtime Agent Instance 和 Tool/Service。
说明本次 Multi-Agent 运行证据达到什么等级，追踪上下文、工具输入输出、
资产写入和主子任务交接。无法确认的部分保留为缺口，输出 HTML 报告。
```

### 按自有框架组织报告

```text
使用 $evidence-driven-product-deconstruction，按照我提供的分析模板重做报告。
先读取模板全文，保留其章节顺序，把模板标记为 M 类方法来源。
将四层分析、完成验证、证据索引和 As-Is/To-Be 映射到相应章节。
若模板要求评分，公开权重、样本和证据；未知项保留为未评分，不折算成满分制。
```

### 先检查证据缺口

```text
使用 $evidence-driven-product-deconstruction 检查当前材料是否足以做完整产品拆解。
暂时不做产品判断，只输出证据就绪度、可分析的子范围、缺口与补充采集清单。
```

## 输出与校验

完整报告包含分析范围与类型、证据就绪度、来源与冲突、执行摘要、四层分析、跨层流程、As-Is、To-Be、风险、追溯矩阵和下一步证据。用户指定外部框架时可调整章节顺序，但保留这些必要内容。

[HTML 模板](assets/report-template.html)提供证据标签、导航、表格容器、窄屏和打印样式。它是起始骨架，使用时需要替换说明文字，并按[报告规范](references/html-report-spec.md)补齐内容。

在本仓库或已安装 Skill 的根目录中，使用 Python 3.10+ 运行校验脚本，无需第三方 Python 依赖：

```bash
python3 scripts/validate_html_report.py /absolute/path/report.html
```

脚本检查 HTML 标签平衡、UTF-8 与 viewport 声明、重复 ID、本地文件引用、部分占位符和常见凭证格式，并提示打印或窄屏样式缺失。退出码 `0` 表示静态检查通过；`1` 表示检查失败；`2` 表示文件路径或类型有误。

静态通过后还需在浏览器中检查排版、图表和内容。脚本不会验证事实真伪、远程链接可访问性或 Mermaid 渲染，也不能替代完整的隐私检查。分享报告时，如有本地证据引用，应一并提供可分享的证据文件；报告本身不得嵌入凭证、身份信息或敏感日志。

## 仓库结构

```text
product-deconstruction-skill/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── report-template.html
├── references/
│   ├── evidence-and-four-layer-framework.md
│   ├── product-archetypes.md
│   ├── agent-runtime-proof.md
│   ├── external-framework-adaptation.md
│   └── html-report-spec.md
└── scripts/
    └── validate_html_report.py
```

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 触发条件、证据原则、执行流程与完成条件 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 显示名称、简介和默认提示词 |
| [四层框架](references/evidence-and-four-layer-framework.md) | 证据门槛、来源角色、完成矩阵和跨层分析 |
| [产品类型](references/product-archetypes.md) | 按产品核心流程选择分析重点 |
| [Agent 运行证明](references/agent-runtime-proof.md) | 实体分类、Multi-Agent 证明等级、工具与上下文契约 |
| [外部框架适配](references/external-framework-adaptation.md) | 章节映射、当前一手资料核对与评分边界 |
| [HTML 报告规范](references/html-report-spec.md) | 报告结构、证据表达、图表、视觉与校验要求 |
| [校验脚本](scripts/validate_html_report.py) | HTML 结构与本地证据引用检查 |

## 操作边界

分析默认只读。只有用户明确授权时，才允许发送产品消息、触发生成或重试、发布、删除、购买等外部操作。网页、工作区和源代码的可访问范围取决于用户授权及宿主环境的工具能力。

本 Skill 不用于无证据猜测、还原隐藏思维链或声称掌握私有 Prompt，也不将一次成功运行外推为产品整体可靠性。
