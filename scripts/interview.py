#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""面试题库操作与记账（纯标准库，Python >= 3.9）。

用法：
  python interview.py pick --role agentic-ai-engineer [--level 2] [--kinds concept,debug]
  python interview.py ask <id>                      # 只亮题面（不含答案/追问/错答）
  python interview.py reveal <id>                   # 答案、追问、错误答案
  python interview.py log <id> --score 0-3 [--followup 0|1] [--note ...]
  python interview.py status                        # 总览与各卡均分
  python interview.py weak                          # 弱项清单（0/1 分未毕业，按卡聚合）
  python interview.py scenario <id>                 # 只给 Situation + 证据文件名（不给问题与解析）
  python interview.py evidence <id> <序号>           # 放一条证据
  python interview.py scenario-reveal <id>          # Questions + Walkthrough + Resolution

数据文件：./interview-progress.json
排期阶梯：3 分 +30 天毕业；2 分 +3 天；1 分 +1 天；0 分 +1 天（连续 2 次 0 → 提示降级补学）
"""
import argparse
import json
import pathlib
import random
import re
import sys
from datetime import date, datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_FILE = pathlib.Path("interview-progress.json")
LADDER = {3: 30, 2: 3, 1: 1, 0: 1}


def today():
    return date.today().isoformat()


# ---------- 进度 ----------

def load():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            sys.exit("进度文件损坏：%s（修复或删除 %s 后重试）" % (e, DATA_FILE))
        data.setdefault("items", {})
        data.setdefault("records", [])
        return data
    return {"items": {}, "records": []}


def save(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")


# ---------- 定位与解析 ----------

def find_repo():
    """向上找 <dir>/interviews/questions。"""
    p = pathlib.Path.cwd().resolve()
    for _ in range(5):
        cand = p / "interviews"
        if (cand / "questions").is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    return None


def parse_frontmatter(path):
    """解析题目的 YAML frontmatter（仅本仓库用到的简单键与行内列表）。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            items = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
            fm[key] = items
        elif val == "":
            fm[key] = ""      # 嵌套块（如 system:），原文另取
        else:
            fm[key] = val.strip("'\"")
    fm["_raw"] = m.group(1)
    return fm, text[m.end():]


def raw_block(fm, name):
    """从 frontmatter 原文取嵌套块（如 system: 下的缩进行）。"""
    m = re.search(r"^%s:\n((?:[ \t]+.*\n?)+)" % re.escape(name),
                  fm.get("_raw", ""), re.M)
    if not m:
        return ""
    return "\n".join(line.strip() for line in m.group(1).splitlines()
                     if line.strip())


def all_questions(repo):
    out = []
    for card_dir in sorted((repo / "interviews" / "questions").iterdir()):
        if not card_dir.is_dir():
            continue
        for md in sorted(card_dir.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            fm, _ = parse_frontmatter(md)
            if fm:
                fm["_path"] = md
                out.append(fm)
    return out


def find_question(repo, qid):
    for fm in all_questions(repo):
        if fm.get("id") == qid:
            return fm
    return None


def role_cards(repo, role_id):
    """极简解析 roles.yaml：取该岗位的 cards 行内列表。"""
    path = repo / "interviews" / "roles.yaml"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    block = re.search(r"- id:\s*%s\b(.*?)(?=\n- id:|\Z)" % re.escape(role_id),
                      text, re.S)
    if not block:
        return None
    m = re.search(r"cards:\s*\[([^\]]*)\]", block.group(1))
    if not m:
        return None
    return [c.strip() for c in m.group(1).split(",") if c.strip()]


# ---------- 命令 ----------

def cmd_pick(args):
    repo = find_repo()
    if not repo:
        sys.exit("未找到课程仓库的 interviews/ 目录（先 git clone 课程仓库）")
    data = load()
    items = all_questions(repo)
    if args.role:
        cards = role_cards(repo, args.role)
        if cards is None:
            sys.exit("roles.yaml 里找不到岗位 %r（可用 id 见 references/cards-map.md）" % args.role)
        items = [q for q in items if q.get("card") in cards]
    if args.level:
        items = [q for q in items if str(q.get("level")) == str(args.level)]
    if args.kinds:
        kinds = {k.strip() for k in args.kinds.split(",") if k.strip()}
        items = [q for q in items if q.get("kind") in kinds]
    if args.card:
        items = [q for q in items if q.get("card") == args.card]
    if not items:
        sys.exit("没有符合过滤条件的题（放宽 --level/--kinds/--card）")

    def is_due(q):
        e = data["items"].get(q.get("id", ""), {})
        return e.get("due", "0000-00-00") <= today()

    due = [q for q in items if is_due(q)]
    fresh = [q for q in items
             if not data["items"].get(q.get("id", ""), {}).get("graduated")]
    pool = due or fresh or items
    q = random.choice(pool)
    qid = q.get("id", "?")
    entry = data["items"].get(qid, {})
    tag = "到期重考" if is_due(q) else ("已练" if qid in data["items"] else "新题")
    print("%s | %s" % (tag, qid))
    print("题面：%s" % q.get("title", ""))
    print("卡：%s · 题型：%s · 级别：%s · 限时 %s 分钟" % (
        q.get("card", "?"), q.get("kind", "?"), q.get("level", "?"),
        q.get("minutes", "?")))
    if entry.get("history"):
        last = entry["history"][-1]
        print("上次：%s 分（%s）" % (last.get("score"), last.get("ts", "")[:10]))
    print("下一步：python interview.py ask %s" % qid)


def cmd_ask(args):
    repo = find_repo()
    fm = find_question(repo, args.id) if repo else None
    if not fm:
        sys.exit("找不到题目 %r" % args.id)
    body = fm["_path"].read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n.*?\n---\n(.*)$", body, re.S)
    stem = m.group(1) if m else body
    # 只保留到第一个答案小节之前
    cut = re.split(r"\n## Short answer", stem)[0]
    print("=" * 60)
    print(fm.get("title", args.id))
    print("限时 %s 分钟 · 题型 %s · 级别 %s" % (
        fm.get("minutes", "?"), fm.get("kind", "?"), fm.get("level", "?")))
    print("-" * 60)
    print(cut.strip())
    print("=" * 60)
    print("（计时开始。答案/追问/错误清单已封印：interview.py reveal）")


def cmd_reveal(args):
    repo = find_repo()
    fm = find_question(repo, args.id) if repo else None
    if not fm:
        sys.exit("找不到题目 %r" % args.id)
    body = fm["_path"].read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n.*?\n---\n(.*)$", body, re.S)
    stem = m.group(1) if m else body
    parts = re.split(r"\n## Short answer", stem, maxsplit=1)
    if len(parts) < 2:
        sys.exit("该题没有 Short answer 节（结构异常）")
    rest = ("## Short answer" + parts[1]).replace("## Short answer\n", "", 1)
    print("=" * 60)
    print("【Short answer】")
    for section in re.split(r"\n(?=## )", rest):
        print(section.rstrip())
    print("=" * 60)
    print("对答案顺序：主干分 → 追问（Follow-ups 按目标级别）→ 错答检验（Wrong answers）")


def cmd_log(args):
    if args.score not in (0, 1, 2, 3):
        sys.exit("--score 取值 0-3")
    data = load()
    qid = args.id
    entry = data["items"].setdefault(qid, {"history": [], "level": 0})
    # 补齐题目的卡片归属（status/weak 按卡聚合靠它）
    if "card" not in entry:
        repo = find_repo()
        fm = find_question(repo, qid) if repo else None
        if repo and not fm:
            data["items"].pop(qid, None)
            save(data)
            sys.exit("题库中找不到 %r（id 拼写核对：pick 输出的第一列）" % qid)
        if fm:
            entry["card"] = fm.get("card", "?")
            entry["kind"] = fm.get("kind", "?")
            entry["level"] = fm.get("level", "?")
            entry["title"] = fm.get("title", "")
            entry["lessons"] = fm.get("lessons", []) or []
    rec = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "id": qid,
        "score": args.score,
        "followup": args.followup,
        "note": args.note or "",
    }
    entry["history"].append(rec)
    entry["last_score"] = args.score

    if args.score == 3:
        entry["graduated"] = True
        entry["due"] = "9999-12-31"
        print("%s 毕业（3 分），不再入队" % qid)
    else:
        days = LADDER[args.score]
        entry["due"] = (date.today() + timedelta(days=days)).isoformat()
        print("%s 记 %s 分 → %s 到期（+%d 天）" % (
            qid, args.score, entry["due"], days))
        zeros = [h for h in entry["history"] if h["score"] == 0]
        if len(zeros) >= 2:
            print("注意：已 2 次 0 分 → 按协议进补学清单（回 frontmatter lessons），"
                  "先补课再重考")
    data["records"].append(rec)
    save(data)


def card_stats(items):
    stats = {}
    for qid, e in items.items():
        card = e.get("card", "?")
        scores = [h["score"] for h in e.get("history", [])]
        if not scores:
            continue
        s = stats.setdefault(card, {"n": 0, "sum": 0, "weak": 0, "grad": 0})
        s["n"] += 1
        s["sum"] += scores[-1]
        if scores[-1] <= 1 and not e.get("graduated"):
            s["weak"] += 1
        if e.get("graduated"):
            s["grad"] += 1
    return stats


def cmd_status(_args):
    data = load()
    items, records = data["items"], data["records"]
    if not items:
        print("还没有记录。先：python interview.py pick --role <岗位>")
        return
    grad = [k for k, e in items.items() if e.get("graduated")]
    due = [k for k, e in items.items()
           if not e.get("graduated") and e.get("due", "0000") <= today()]
    scores = [r["score"] for r in records]
    print("记录 %d 条 · 平均 %.2f · 毕业 %d · 今日到期重考 %d" % (
        len(records), sum(scores) / len(scores), len(grad), len(due)))
    print("-" * 56)
    stats = card_stats(items)
    for card in sorted(stats):
        s = stats[card]
        print("%-28s 均分 %.1f · 题数 %d · 弱 %d · 毕业 %d" % (
            card, s["sum"] / s["n"], s["n"], s["weak"], s["grad"]))
    if due:
        print("-" * 56)
        print("到期：%s" % "、".join(sorted(due)[:8]))


def cmd_weak(_args):
    repo = find_repo()
    data = load()
    by_card = {}
    for qid, e in data["items"].items():
        scores = [h["score"] for h in e.get("history", [])]
        if e.get("graduated") or not scores or scores[-1] > 1:
            continue
        lessons = []
        if repo:
            fm = find_question(repo, qid)
            if fm:
                lessons = fm.get("lessons", []) or []
        by_card.setdefault(e.get("card", "?"), []).append(
            (qid, scores[-1], lessons))
    if not by_card:
        print("没有弱项（没有 0/1 分未毕业的题）。")
        return
    for card in sorted(by_card):
        print("【%s】" % card)
        for qid, sc, lessons in sorted(by_card[card], key=lambda x: x[1]):
            print("  %-40s %d分  补学: %s" % (
                qid, sc, "、".join(lessons) if lessons else "（无回链，按卡补）"))


def cmd_scenario(args):
    repo = find_repo()
    if not repo:
        sys.exit("未找到课程仓库")
    path = repo / "interviews" / "scenarios" / args.id / "README.md"
    if not path.exists():
        sys.exit("找不到场景 %r" % args.id)
    fm, body = parse_frontmatter(path)
    sit = re.split(r"\n## Evidence", body)[0]
    print("=" * 60)
    print(fm.get("title", args.id))
    print("限时 %s 分钟 · 级别 %s" % (fm.get("minutes", "?"), fm.get("level", "?")))
    system = raw_block(fm, "system")
    if system:
        print("系统环境：")
        for line in system.splitlines():
            print("  %s" % line)
    print("-" * 60)
    print(sit.strip())
    ev_dir = path.parent / "evidence"
    if ev_dir.is_dir():
        files = sorted(p.name for p in ev_dir.iterdir() if p.is_file())
        print("-" * 60)
        print("可用证据（用户点名才放，序号对应）：")
        for i, name in enumerate(files, 1):
            print("  %2d. %s" % (i, name))
    print("=" * 60)
    print("（Questions / Walkthrough / Resolution 已封印：scenario-reveal）")


def cmd_evidence(args):
    repo = find_repo()
    ev_dir = repo / "interviews" / "scenarios" / args.id / "evidence"
    if not repo or not ev_dir.is_dir():
        sys.exit("找不到场景 %r 的证据目录" % args.id)
    files = sorted(p for p in ev_dir.iterdir() if p.is_file())
    try:
        idx = int(args.n)
        target = files[idx - 1]
    except (ValueError, IndexError):
        sys.exit("序号须在 1..%d" % len(files))
    print("--- 证据 %d：%s ---" % (idx, target.name))
    print(target.read_text(encoding="utf-8", errors="replace"))


def cmd_scenario_reveal(args):
    repo = find_repo()
    path = (repo / "interviews" / "scenarios" / args.id / "README.md") if repo else None
    if not path or not path.exists():
        sys.exit("找不到场景 %r" % args.id)
    _, body = parse_frontmatter(path)
    for section in ("## Questions", "## Walkthrough", "## Resolution"):
        m = re.search(re.escape(section) + r"\n(.*?)(?=\n## |\Z)", body, re.S)
        if m:
            print("\n## %s" % section[3:])
            print(m.group(1).strip())
    print("\n（逐问给分；报得出数字才算，见 scoring-rubric.md）")


def main():
    ap = argparse.ArgumentParser(description="面试题库操作与记账")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pick", help="抽题")
    p.add_argument("--role", default=None)
    p.add_argument("--level", default=None)
    p.add_argument("--kinds", default=None, help="逗号分隔，如 concept,debug")
    p.add_argument("--card", default=None)
    p.set_defaults(func=cmd_pick)

    for name, fn, extra in (("ask", cmd_ask, ("id",)),
                            ("reveal", cmd_reveal, ("id",)),
                            ("scenario", cmd_scenario, ("id",)),
                            ("scenario-reveal", cmd_scenario_reveal, ("id",))):
        p = sub.add_parser(name)
        p.add_argument(extra[0])
        p.set_defaults(func=fn)

    p = sub.add_parser("evidence")
    p.add_argument("id")
    p.add_argument("n")
    p.set_defaults(func=cmd_evidence)

    p = sub.add_parser("log", help="记分并排期")
    p.add_argument("id")
    p.add_argument("--score", type=int, required=True)
    p.add_argument("--followup", type=int, default=None, choices=[0, 1])
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("status", help="总览")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("weak", help="弱项清单")
    p.set_defaults(func=cmd_weak)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
