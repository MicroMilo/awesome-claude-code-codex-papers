# v0.3 中文发布包

> 状态：以下均为可发布草稿，本仓库没有自动代发任何内容。真正发帖前请再次核对目标社区的最新规则。

[English version](launch-kit.md)

## 可直接使用的事实

- 项目：**Awesome Claude Code & Codex Papers / Agent Papers**
- 仓库：https://github.com/MicroMilo/awesome-claude-code-codex-papers
- 网站：https://micromilo.github.io/awesome-claude-code-codex-papers/
- 方法证据矩阵：https://micromilo.github.io/awesome-claude-code-codex-papers/methods/
- 证据洞察：https://micromilo.github.io/awesome-claude-code-codex-papers/insights/
- 可复用会议采集 Skill：https://micromilo.github.io/awesome-claude-code-codex-papers/skill/
- 当前审计范围：13 个会议系列的 **18,269 条官方清单记录**；其中 **13 篇论文**目前通过严格的产品级收录门槛。
- 收录门槛：必须是正式接收的 2026 论文，并且真正运行 Claude Code 或 Codex CLI 产品。仅使用 Claude/GPT 模型不算。
- 审计规则：官方清单中每条记录都有 `included`、`excluded`、`pending` 或 `duplicate` 结果；全文受阻时保留 pending。
- 许可证：MIT。

不要把 18,269 说成“18,269 篇相关论文”。准确说法是“审计/索引了 18,269 条官方会议清单记录，目前 13 篇通过产品级收录门槛”。

## 发布原则

1. 先讲清楚这个项目解决了什么研究问题，不要用“求 Star”开场。
2. 面向开发者发洞察页，面向研究者发方法矩阵，面向爬虫/数据工程读者发 Skill 页。
3. 每篇帖子只问一个具体问题，让它形成真正讨论。
4. 明确说明自己是维护者。
5. 不要同一天复制粘贴到所有社区，也不要组织点赞。
6. 回答质疑时发具体论文证据页，不做跨论文排行榜。

## 推荐顺序

| 天数 | 渠道 | 投稿方式 | 目标 |
|---|---|---|---|
| 第 1 天 | openai/codex Show and tell | 使用英文发布包中的草稿 | 找到真实 Codex 用户与缺失论文 |
| 第 2 天 | V2EX 分享创造 | 分享采集方法、踩坑和洞察，不写成纯广告 | 获得中文开发者反馈 |
| 第 3 天 | GitHubDaily Issue | 开源项目自荐 | 获得中文 GitHub 用户曝光 |
| 第 4 天 | HelloGitHub Issue | 按官方模板提交“人工智能”类别 | 获得月刊审核 |
| 第 5 天 | 阮一峰周刊 Issue | 提交简洁、可核验的开源项目介绍 | 获得泛技术读者曝光 |
| 第 6 天起 | 逐篇联系论文作者 | 只发对应的证据页 | 获得事实修正与作者分享 |

每个大渠道至少间隔一天。先根据评论里真正出现的问题调整下一篇开头，不要机械群发。

## 1. V2EX

建议节点：**分享创造**。V2EX FAQ 欢迎发布自己的新作品，但反对只注册账号搬运自己网站链接；正文必须有真实方法与经验：https://www.v2ex.com/faq

### 标题

```text
我筛了 18,269 条会议论文记录，只收真正运行 Claude Code / Codex CLI 的论文
```

### 正文

```markdown
我在维护一个开源论文目录，想解决一个很具体的问题：搜索 “Codex paper” 时，经常把历史 Codex 模型、GPT API 使用，以及真正的 Codex CLI 产品混在一起；Claude 也有类似问题。

所以我用了一个更严格的门槛：论文必须在 2026 年正式会议被接收，并且真的运行 Claude Code 或 Codex CLI 产品，作为 baseline、被测系统、宿主、wrapper 或产品级比较对象。只使用 Claude/GPT 模型不收。

目前做了几件事：

1. 索引 13 个会议系列的 18,269 条官方清单记录；
2. 每条记录都保留 included / excluded / pending / duplicate，不静默丢弃；
3. 先用官方标题和摘要做高召回初筛，只有候选才下载 PDF；
4. 对收录论文保留准确模型字符串、方法、结果、控制条件、证据位置和限制；
5. 现在有 13 篇通过产品级门槛，并为每篇生成了可分享证据页。

目录：https://micromilo.github.io/awesome-claude-code-codex-papers/

方法证据矩阵：https://micromilo.github.io/awesome-claude-code-codex-papers/methods/

采集 Skill：https://micromilo.github.io/awesome-claude-code-codex-papers/skill/

看完这些论文后，我目前的判断是：产品并不是不会写局部代码，更常见的短板是长任务状态、阶段组合、领域证据和独立验证。这只是当前 13 篇论文支持的工作假设，不是厂商排名。

我最想听的反馈是：你认为“必须真正运行产品”这个收录门槛是否太严格？有没有已经正式接收、但我漏掉的 2026 论文？
```

不要在正文中要求点赞或 Star。不要添加群二维码、无关项目和营销口号。

## 2. GitHubDaily

入口：https://github.com/GitHubDaily/GitHubDaily/issues/new

GitHubDaily README 明确欢迎通过 Issue 推荐或自荐开源项目。

### 标题

```text
【开源自荐】Agent Papers：只收真正评测 Claude Code / Codex CLI 的会议论文
```

### 正文

```markdown
## 项目地址

https://github.com/MicroMilo/awesome-claude-code-codex-papers

## 项目简介

Agent Papers 是一个面向 Claude Code 与 Codex CLI 产品级研究的开源论文数据库。项目不把“使用 Claude/GPT 模型”的论文误当成产品论文，而是从会议官方清单出发，审核论文是否真正运行产品。

当前已索引 13 个会议系列的 18,269 条官方记录，13 篇论文通过严格收录门槛。每篇展示准确模型、方法、结果、同模型/同预算控制、证据位置和限制；所有 excluded 与 pending 记录也可审计。

## 亮点

- 中英文可交互网站，可按会议、领域、产品、模型、证据强度和方法筛选；
- 每篇论文与每条研究洞察都有可分享的永久证据页；
- 提供方法矩阵，避免结果脱离模型和对比限制传播；
- 自带可复用的会议论文采集 Skill，采用 metadata-first 策略，减少无意义 PDF 下载；
- MIT 开源，YAML/JSON 数据、审计记录和验证脚本完整保留。

网站：https://micromilo.github.io/awesome-claude-code-codex-papers/
```

## 3. HelloGitHub

官方中文模板：https://github.com/521xueweihan/HelloGitHub/issues/new?template=submit-cn.yaml

模板要求：仅收 GitHub 开源项目；标题约 20 字且不超过 50 字；描述 32–256 字；需要单独填写亮点；类别可选“人工智能”。先在 HelloGitHub 搜索项目 URL，避免重复提交。

### 表单内容

项目地址：

```text
https://github.com/MicroMilo/awesome-claude-code-codex-papers
```

类别：

```text
人工智能
```

项目标题：

```text
审计 Claude Code 与 Codex 论文证据
```

项目描述：

```text
一个从会议官方清单出发的 coding agent 论文数据库，只收真正运行 Claude Code 或 Codex CLI 产品的正式论文。网站可按会议、领域、模型和方法筛选，并展示结果、证据位置与对比限制。
```

亮点：

```text
它不会把普通 Claude/GPT API 论文误当作产品研究；18,269 条官方记录均保留 included、excluded、pending 或 duplicate 状态。每篇收录论文和每条洞察都有永久证据页，同时提供可复用的 metadata-first 会议采集 Skill。
```

截图：上传 `assets/social-preview.png`，并补充方法页截图。

## 4. 阮一峰科技爱好者周刊

入口：https://github.com/ruanyf/weekly/issues/new

周刊长期通过 GitHub Issue 接受自荐。保持介绍短、信息密度高，避免把标题写成广告。

### 标题

```text
【开源自荐】Agent Papers：工业 coding agent 会议论文证据库
```

### 正文

```markdown
项目地址：https://github.com/MicroMilo/awesome-claude-code-codex-papers

这是一个专门收录 Claude Code 与 Codex CLI 产品级研究的开源论文数据库。它从 2026 会议官方清单出发，已索引 13 个会议系列的 18,269 条记录，只有真正运行产品的论文才进入主目录；仅使用 Claude/GPT 模型不会被误收。

每篇论文都展示准确模型、方法、论文结果、控制条件、证据位置和限制，并为 included / excluded / pending / duplicate 保留可审计记录。项目同时提供中英文网站、方法证据矩阵，以及可复用的 metadata-first 会议采集 Skill。

在线目录：https://micromilo.github.io/awesome-claude-code-codex-papers/
```

## 5. 论文作者核验

这通常比广撒网更有效。只联系已经收录论文的作者；每封邮件写对应模型、结果和证据位置，不群发同一封模板。

### 邮件主题

```text
贵论文在 Claude Code / Codex 开源证据目录中的记录核验
```

### 邮件正文

```text
[老师/作者姓名] 您好，

我在维护一个开源目录，专门收录正式会议中真正评测 Claude Code 或 Codex CLI 产品的论文。我们为贵论文《[论文标题]》整理了单独的证据页：

[论文证据页 URL]

当前记录包括 [产品/模型]、[论文报告结果] 和 [证据位置]，同时明确写出了对比限制，没有把它做成跨论文排行榜。

想请您帮忙核对是否存在事实错误，或是否遗漏了产品版本、预算、工具权限等实验配置。如果记录准确且对读者有帮助，也欢迎转发给关注这篇工作的研究者。

谢谢！
MicroMilo
```

## 数据记录

每次发布前、发布后 24 小时和 7 天各记录一次：

| 日期 | 渠道 | 发帖链接 | GitHub 独立访客 | 独立 Clone | Star | 可见 Referrer | 有价值纠错 | 备注 |
|---|---|---|---:|---:|---:|---|---:|---|
| | | | | | | | | |

不要只看 Star。论文纠错、作者回复、有效贡献者、缺失论文线索和 RSS 订阅（如果可见）同样重要。
