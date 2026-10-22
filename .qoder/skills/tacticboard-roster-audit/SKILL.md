---
name: tacticboard-roster-audit
description: Audit and fill Tacticboard team rosters from players.js/data.js, including position gaps, preferred foot, positions, tags, weaknesses and source URLs; validate duplicates and schema; generate a mobile review page; write only user-confirmed rows. Use when adding or auditing a team, checking a squad, 补队, 审核球队/球员表, 惯用脚, 阵容缺口, or preparing opponent data for this project.
when_to_use: User asks to add/audit a Tacticboard team, review player data, fill missing positions, check preferred foot, or prepare a Chelsea/other club candidate table.
argument-hint: <team-name>
---

# Tacticboard 球队审核

## 概览

按「先审现有 → 查候选 → 校验 → 手机审查 → 只写确认行」处理一支球队。只改数据层，不碰比赛态、存储、备份和分析规则。

## 硬规则

- **不编数据**。每条候选必须有可打开的来源 URL；查不到就写「待确认」，不要猜。
- **弱点由 AI 查**。每个候选必须给 `weak` + `weakNote`（依据/来源）；查不到就写明“无可靠来源”并给替代观察点，不能把空白/待确认丢给用户。用户只做同意/否决。
- **对手不录数值**。只录位置、惯用脚、类型标签、弱点；`a`（pace/pass/def/air/fin/sta）只属于曼联。
- **不直接写入**。先出候选表和审查页，用户勾选后才改 `src/players.js`。
- **不擅自加字段**。当前 `players.js` 没有 `weak` 字段；弱点先放候选表/描述 `d`，除非用户明确同意加字段。
- **一次一队**。不要一次生成 19 队表格；每队单独校验、审查、写入。
- **来源冲突标「冲突」**，不要静默选一个。已知冲突见 `references/schema.md`。
- 不把 API key、token、登录信息写进项目或技能文件。

## 工作流

### 1. 先审现有

```bash
node .qoder/skills/tacticboard-roster-audit/scripts/validate_roster.cjs --team 切尔西
```

输出：现有球员数、阵型、每个槽位的需求/现有可打人数、缺口提醒。先确认球队阵型和缺口，再查人。

### 2. 查候选

来源优先级：

1. 俱乐部官网 / Premier League 官方（队籍、位置）
2. Transfermarkt（位置、惯用脚、队籍）
3. FotMob / EA FC（惯用脚交叉核对）
4. 其他可靠媒体；只作补充

按 `references/schema.md` 的候选 JSON 格式写到 `/tmp/<team>-candidates.json`。每行必须有：

`n / en / club / pos / foot / tags / weak / weakNote / src / conf / note`

标签从现有 `players.js` 的词表里选，不要造新词。位置和脚按项目枚举。`weak` 必须有候选值，`weakNote` 写明依据或“无可靠来源+替代观察点”；不要把弱点留给用户填。

### 3. 校验

```bash
node .qoder/skills/tacticboard-roster-audit/scripts/validate_roster.cjs \
  --team 切尔西 \
  --candidates /tmp/chelsea-candidates.json
```

有「阻断问题」就修候选 JSON，不要绕过。`weak` 为空或「待确认」且没有 `weakNote` 会被拦；标签不确定可以保留候选，但要说清依据。

### 4. 生成手机审查页

```bash
node .qoder/skills/tacticboard-roster-audit/scripts/make_review.cjs \
  /tmp/chelsea-candidates.json \
  /tmp/chelsea-review.html
open -a "Google Chrome" /tmp/chelsea-review.html
```

页面是一屏一队、逐行勾选、可写修改备注；底部可下载只包含已确认行的 JSON。用户确认后再进入写入。

### 5. 只写确认行

用户确认后：

1. 只把勾选行写入 `src/players.js`；保留现有字段风格（`n,en,pos,foot,club,nat,tags,pair,d`）。
2. 不写 `a`（对手）；不新增 `weak`，弱点写进 `d` 或按用户决定。
3. 需要固定首发时，在 `build.py` 的 `PREFERRED` 加该队 11 人；槽位顺序必须对齐 `FORMS`。
4. 只有用户确认才修 `src/data.js` 的旧 key/bullets 冲突。
5. 跑 `python3 build.py`；检查该队能选、能排 11 人、无 console 报错、390px 无横滚。
6. 更新 `交接文档.md` §10.5 与 `项目文档.md` §3；不提交 git，除非用户明确要求。

## 验收清单

- [ ] 现有队人数、阵型、缺口先跑过校验器
- [ ] 每行候选有来源 URL；脚/位置/标签符合枚举
- [ ] 没有和现有库重名；没有把别的队球员算进来
- [ ] 审查页可勾选、可下载确认 JSON
- [ ] 只写入勾选行；未确认行没有进库
- [ ] `python3 build.py` 通过；该队能排 11 人
- [ ] 390px 无横滚；console 无报错
- [ ] 文档已记录；真机未测要明确说

## 资源

- `references/schema.md`：字段、枚举、阵型槽位、来源规则、已知冲突、候选 JSON 示例
- `scripts/validate_roster.cjs`：只读校验现有库 + 候选 JSON
- `scripts/make_review.cjs`：生成手机审查页（无外部依赖）
