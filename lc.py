#!/usr/bin/env python3
"""
╔══════════════════════════════════════╗
║      LeetCode CLI  —  lc.py          ║
║  pip install colorama requests       ║
║  python lc.py                        ║
╚══════════════════════════════════════╝
"""

import os
import re
import sys
import json
import time
import glob
import subprocess
import requests
from pathlib import Path
from datetime import datetime

# ── colorama ────────────────────────────────────────────────────────────────
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Run: pip install colorama requests")
    sys.exit(1)

# ── paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "lc_config.json"
SOLVES_DIR  = BASE_DIR / "LeetCode-Solves"

# ── colors ───────────────────────────────────────────────────────────────────
C  = Fore.CYAN
Y  = Fore.YELLOW
G  = Fore.GREEN
R  = Fore.RED
M  = Fore.MAGENTA
W  = Fore.WHITE
DW = Style.DIM + Fore.WHITE
B  = Style.BRIGHT
RS = Style.RESET_ALL

DIFF_COLOR = {
    "Easy":   Fore.GREEN,
    "Medium": Fore.YELLOW,
    "Hard":   Fore.RED,
}

WIDTH = 70

# ╔══════════════════════════════════════════════════════════════════════╗
#   BOXES
# ╚══════════════════════════════════════════════════════════════════════╝

def box_top(title="", color=C):
    if title:
        pad  = WIDTH - len(title) - 4
        left = pad // 2
        right= pad - left
        return color + "╔" + "═" * left + "  " + B + title + RS + color + "  " + "═" * right + "╗" + RS
    return color + "╔" + "═" * WIDTH + "╗" + RS

def box_mid(color=C):
    return color + "╠" + "═" * WIDTH + "╣" + RS

def box_bot(color=C):
    return color + "╚" + "═" * WIDTH + "╝" + RS

def box_line(text="", color=C, text_color=W, align="left", pad=1):
    inner = WIDTH - 2 * pad
    text_plain = re.sub(r'\x1b\[[0-9;]*m', '', text)
    extra = len(text) - len(text_plain)

    if align == "center":
        total = inner + extra
        line  = text.center(total)
    elif align == "right":
        total = inner + extra
        line  = text.rjust(total)
    else:
        total = inner + extra
        line  = text.ljust(total)

    return color + "║" + " " * pad + line + " " * pad + "║" + RS

def box_empty(color=C):
    return box_line("", color=color)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause(msg="  Press Enter to continue..."):
    input(DW + msg + RS)

def center_print(text):
    plain = re.sub(r'\x1b\[[0-9;]*m', '', text)
    pad   = max(0, (WIDTH + 2 - len(plain)) // 2)
    print(" " * pad + text)

# ╔══════════════════════════════════════════════════════════════════════╗
#   CONFIG
# ╚══════════════════════════════════════════════════════════════════════╝

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            pass
    return {}

def save_config(cfg: dict):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))

# ╔══════════════════════════════════════════════════════════════════════╗
#   FIRST TIME SETUP
# ╚══════════════════════════════════════════════════════════════════════╝

def setup_screen():
    clear()
    print(box_top("🧠  LeetCode CLI  —  First Time Setup", color=M))
    print(box_empty(M))
    print(box_line("Welcome! Let's configure your credentials.", color=M, text_color=W, align="center"))
    print(box_line("Cookies are saved locally in lc_config.json", color=M, text_color=DW, align="center"))
    print(box_empty(M))
    print(box_mid(M))
    print(box_line("  Where to find cookies:", color=M))
    print(box_line("  1. Open leetcode.com  (make sure you're logged in)", color=M, text_color=DW))
    print(box_line("  2. Press F12  →  Application  →  Cookies", color=M, text_color=DW))
    print(box_line("  3. Click on https://leetcode.com", color=M, text_color=DW))
    print(box_line("  4. Copy LEETCODE_SESSION and csrftoken values", color=M, text_color=DW))
    print(box_empty(M))
    print(box_bot(M))
    print()

    username = input(Y + "  👤 LeetCode username       : " + W).strip()
    session  = input(Y + "  🍪 LEETCODE_SESSION cookie : " + W).strip()
    csrf     = input(Y + "  🔑 csrftoken cookie        : " + W).strip()
    solves   = input(Y + f" 📁 Solves folder [{SOLVES_DIR.name}]  : " + W).strip()

    if not solves:
        solves = str(SOLVES_DIR)

    cfg = {
        "username": username,
        "session_cookie": session,
        "csrf_token": csrf,
        "solves_dir": solves,
    }
    save_config(cfg)

    print()
    print(box_top(color=G))
    print(box_line(G + "✅  Config saved to lc_config.json", color=G, align="center"))
    print(box_bot(color=G))
    print()
    pause()
    return cfg

def update_cookies_screen(cfg: dict) -> dict:
    clear()
    print(box_top("⚙️   Update Cookies", color=Y))
    print(box_empty(Y))
    print(box_line("  Paste your new cookies below.", color=Y))
    print(box_line("  F12 → Application → Cookies → leetcode.com", color=Y, text_color=DW))
    print(box_empty(Y))
    print(box_bot(Y))
    print()

    session = input(Y + "  🍪 New LEETCODE_SESSION : " + W).strip()
    csrf    = input(Y + "  🔑 New csrftoken        : " + W).strip()

    if session:
        cfg["session_cookie"] = session
    if csrf:
        cfg["csrf_token"] = csrf
    save_config(cfg)

    print()
    print(G + "  ✅ Cookies updated!" + RS)
    print()
    pause()
    return cfg

def github_account_screen(cfg: dict) -> dict:
    """Add or update GitHub username + Personal Access Token."""
    clear()
    print(box_top("🐙  GitHub Account", color=C))
    print(box_empty(C))
    print(box_line("  A Personal Access Token (PAT) lets you push via HTTPS", color=C))
    print(box_line("  without entering a password every time.", color=C, text_color=DW))
    print(box_empty(C))
    print(box_mid(C))
    print(box_line("  How to create a PAT:", color=C))
    print(box_line("  1. github.com → Settings → Developer settings", color=C, text_color=DW))
    print(box_line("  2. Personal access tokens → Tokens (classic)", color=C, text_color=DW))
    print(box_line("  3. Generate new token → tick [repo] scope → copy", color=C, text_color=DW))
    print(box_empty(C))
    print(box_bot(C))
    print()

    gh_user  = input(Y + "  GitHub username (e.g. negmurodov) : " + W).strip()
    gh_token = input(Y + "  GitHub PAT token                  : " + W).strip()

    if gh_user:
        cfg["github_username"] = gh_user
    if gh_token:
        cfg["github_token"] = gh_token
    save_config(cfg)

    if gh_user and gh_token:
        print()
        print(G + "  ✅ GitHub credentials saved!" + RS)
        print()
        print(DW + "  Tip: When you set a remote URL in Git, use the format:" + RS)
        print(DW + f"  https://{gh_user}:<TOKEN>@github.com/{gh_user}/REPO.git" + RS)
        print()
        use_in_remote = input(Y + "  Auto-embed token into current remote URL? [y/N]: " + W).strip().lower()
        if use_in_remote == "y":
            repo_root = str(Path(cfg.get("solves_dir", str(SOLVES_DIR))).parent)
            _, remote_url, _ = _run_git(["remote", "get-url", "origin"], repo_root)
            if remote_url:
                clean = re.sub(r"https://[^@]+@", "https://", remote_url)
                new_url = clean.replace("https://", f"https://{gh_user}:{gh_token}@")
                code, _, err = _run_git(["remote", "set-url", "origin", new_url], repo_root)
                if code == 0:
                    print(G + "  ✅ Remote URL updated with credentials." + RS)
                else:
                    print(R + f"  ❌ Could not update remote: {err}" + RS)
            else:
                print(Y + "  No remote origin set yet. Use Git → [2] Set remote URL first." + RS)
            print()

    pause()
    return cfg


def settings_screen(cfg: dict) -> dict:
    while True:
        clear()
        gh_user = cfg.get("github_username", "—")
        gh_token_status = G + "✔ set" + RS if cfg.get("github_token") else R + "✘ not set" + RS
        print(box_top("⚙️   Settings", color=Y))
        print(box_empty(Y))
        repo_root_display = cfg.get("repo_root") or DW + "(auto: parent of solves dir)" + RS
        print(box_line(f"  Username    : {Y}{cfg.get('username','?')}", color=Y))
        print(box_line(f"  Solves dir  : {DW}{cfg.get('solves_dir','?')}", color=Y))
        print(box_line(f"  Repo root   : {DW}{repo_root_display}", color=Y))
        print(box_line(f"  GitHub      : {C}{gh_user}{RS}  token: {gh_token_status}", color=Y))
        print(box_empty(Y))
        print(box_mid(Y))
        print(box_line("  [1] Update cookies (LEETCODE_SESSION + csrftoken)", color=Y))
        print(box_line("  [2] Change username", color=Y))
        print(box_line("  [3] Change solves folder path", color=Y))
        print(box_line("  [4] 🐙  Add / update GitHub account  (for git push)", color=Y))
        print(box_line("  [5] Change repo root (git folder)", color=Y))
        print(box_line("  [6] Back", color=Y))
        print(box_empty(Y))
        print(box_bot(Y))
        print()

        ch = input(Y + "  → " + W).strip()

        if ch == "1":
            cfg = update_cookies_screen(cfg)
        elif ch == "2":
            new = input(Y + "  New username: " + W).strip()
            if new:
                cfg["username"] = new
                save_config(cfg)
                print(G + "  ✅ Saved!" + RS)
                time.sleep(1)
        elif ch == "3":
            new = input(Y + "  New path: " + W).strip()
            if new:
                cfg["solves_dir"] = new
                save_config(cfg)
                print(G + "  ✅ Saved!" + RS)
                time.sleep(1)
        elif ch == "4":
            cfg = github_account_screen(cfg)
        elif ch == "5":
            clear()
            print(box_top("📁  Repo Root", color=C))
            print(box_empty(C))
            print(box_line("  This is the folder where .git lives (your git repo root).", color=C))
            print(box_line(f"  Current: {DW}{cfg.get('repo_root') or '(auto)'}{RS}", color=C))
            print(box_empty(C))
            print(box_line(f"  {DW}Example: C:\\Users\\isa20\\Documents\\Leetcode-Solves{RS}", color=C))
            print(box_bot(C))
            print()
            new = input(Y + "  New repo root path (leave blank to auto): " + W).strip()
            if new:
                cfg["repo_root"] = new
            else:
                cfg.pop("repo_root", None)
            save_config(cfg)
            print(G + "  ✅ Saved!" + RS)
            time.sleep(1)
        elif ch == "6":
            break

    return cfg

# ╔══════════════════════════════════════════════════════════════════════╗
#   LOCAL FILE DATABASE
# ╚══════════════════════════════════════════════════════════════════════╝

def scan_files(solves_dir: str) -> list[dict]:
    """Scan all .txt files and build index.
    New structure: root / {num}_{Title} / {username}_{lang}.txt
    Skips README.txt files.
    """
    root  = Path(solves_dir)
    index = []
    seen  = set()  # deduplicate by problem number

    for f in root.rglob("*.txt"):
        # skip readme files
        if f.name.lower().startswith("readme"):
            continue

        folder = f.parent
        folder_name = folder.name  # e.g. "0195_Tenth_Line"

        # parse folder: {num}_{Title}
        m = re.match(r'^(\d+)_(.+)$', folder_name)
        if m:
            num   = int(m.group(1))
            title = m.group(2).replace("_", " ")
        else:
            # fallback: try to parse from filename itself (old format)
            m2 = re.match(r'^(\d+)_(.+)$', f.stem)
            if m2:
                num   = int(m2.group(1))
                title = m2.group(2).replace("_", " ")
            else:
                num, title = 0, f.stem

        # read difficulty and category from file content
        difficulty = "Unknown"
        category   = "Other"
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            dm = re.search(r'Difficulty\s*:\s*(\w+)', text)
            if dm:
                difficulty = dm.group(1)
            cm = re.search(r'Category\s*:\s*(\S+)', text)
            if cm:
                category = cm.group(1)
        except Exception:
            pass

        # only add one entry per problem number (first file found)
        if num not in seen:
            seen.add(num)
            index.append({
                "num":        num,
                "title":      title,
                "category":   category,
                "difficulty": difficulty,
                "path":       f,
            })

    index.sort(key=lambda x: x["num"])
    return index

def find_problem(index: list[dict], query: str) -> list[dict]:
    """Search by number or keyword."""
    q = query.strip().lower()

    # exact number
    if q.isdigit():
        num = int(q)
        return [p for p in index if p["num"] == num]

    # keyword in title or category
    return [p for p in index if q in p["title"].lower() or q in p["category"].lower()]

def read_file_sections(path: Path) -> dict:
    """Parse .txt file into sections."""
    text = path.read_text(encoding="utf-8")
    sections = {
        "header":    "",
        "problem":   "",
        "hints":     "",
        "solution":  "",
        "stats":     "",
        "lang":      "",
    }

    # split on separator lines
    sep = "=" * 70
    sep2= "-" * 70

    parts = text.split(sep)
    # parts[0] = empty, parts[1] = header block, parts[2] = problem, ...

    raw = text

    # extract header (between first and second ===)
    m = re.search(r'={70}\n(.*?)\n={70}', raw, re.DOTALL)
    if m:
        sections["header"] = m.group(1).strip()

    # problem statement
    m = re.search(r'PROBLEM STATEMENT\n-{70}\n(.*?)(?=\n={70}|\nHINTS|\Z)', raw, re.DOTALL)
    if m:
        sections["problem"] = m.group(1).strip()

    # hints
    m = re.search(r'HINTS\n-{70}\n(.*?)(?=\n={70}|\Z)', raw, re.DOTALL)
    if m:
        sections["hints"] = m.group(1).strip()

    # solution
    m = re.search(r'MY SOLUTION\s+\(([^)]+)\)\n={70}\n\n(.*?)\n\n={70}', raw, re.DOTALL)
    if m:
        sections["lang"]     = m.group(1)
        sections["solution"] = m.group(2).strip()

    # stats
    m = re.search(r'SUBMISSION STATS\n-{70}\n(.*?)(?=\n={70}|\Z)', raw, re.DOTALL)
    if m:
        sections["stats"] = m.group(1).strip()

    return sections

# ╔══════════════════════════════════════════════════════════════════════╗
#   VIEW PROBLEM
# ╚══════════════════════════════════════════════════════════════════════╝

def wrap_text(text: str, width: int) -> list[str]:
    lines = []
    for paragraph in text.splitlines():
        if paragraph.strip() == "":
            lines.append("")
            continue
        while len(paragraph) > width:
            cut = paragraph[:width].rfind(" ")
            if cut == -1:
                cut = width
            lines.append(paragraph[:cut])
            paragraph = paragraph[cut:].lstrip()
        lines.append(paragraph)
    return lines

def print_problem(prob: dict):
    clear()
    sec = read_file_sections(prob["path"])

    dc    = DIFF_COLOR.get(prob["difficulty"], W)
    inner = WIDTH - 2

    # ── header ──────────────────────────────────────────────────────────
    num_str   = Y + B + f"#{prob['num']}" + RS
    title_str = W + B + prob["title"] + RS
    diff_str  = dc + B + f"[{prob['difficulty']}]" + RS
    cat_str   = DW + prob["category"] + RS

    header_left  = f"  {num_str}  ·  {title_str}"
    header_right = f"{diff_str}  {cat_str}  "

    print(box_top(color=C))
    print(box_line(header_left + "  " + header_right, color=C))
    print(box_mid(C))

    # ── problem ──────────────────────────────────────────────────────────
    print(box_line(C + B + "  PROBLEM STATEMENT" + RS, color=C))
    print(box_line(DW + "  " + "─" * (inner - 2) + RS, color=C))
    wrapped = wrap_text(sec["problem"], inner - 4)
    for line in wrapped[:40]:   # max 40 lines to not overflow terminal
        print(box_line("  " + line, color=C, text_color=W))

    if sec["hints"]:
        print(box_empty(C))
        print(box_line(M + "  HINTS" + RS, color=C))
        for h in sec["hints"].splitlines():
            print(box_line("  " + h, color=C, text_color=DW))

    # ── solution ─────────────────────────────────────────────────────────
    print(box_mid(C))
    lang_label = G + B + f"  MY SOLUTION  ({sec['lang'] or 'Unknown'})" + RS
    print(box_line(lang_label, color=C))
    print(box_line(DW + "  " + "─" * (inner - 2) + RS, color=C))

    code_lines = sec["solution"].splitlines()
    for line in code_lines[:60]:
        print(box_line("  " + line, color=C, text_color=Fore.LIGHTWHITE_EX))

    # ── stats ─────────────────────────────────────────────────────────────
    print(box_mid(C))
    print(box_line(Y + "  SUBMISSION STATS" + RS, color=C))
    print(box_line(DW + "  " + "─" * (inner - 2) + RS, color=C))

    for stat_line in sec["stats"].splitlines():
        # color beats % green if > 50
        m = re.search(r'beats (\d+\.?\d*)%', stat_line)
        if m:
            pct = float(m.group(1))
            color = Fore.GREEN if pct >= 50 else Fore.YELLOW
            stat_line = re.sub(
                r'(beats \d+\.?\d*%)',
                color + r'\1' + RS,
                stat_line
            )
        print(box_line("  " + stat_line, color=C))

    print(box_bot(C))
    print()
    pause()

# ╔══════════════════════════════════════════════════════════════════════╗
#   SEARCH SCREEN
# ╚══════════════════════════════════════════════════════════════════════╝

def search_screen(index: list[dict]):
    while True:
        clear()
        print(box_top("🔍  Search Problems", color=C))
        print(box_empty(C))
        print(box_line("  Enter problem number (620) or keyword (array, dp, tree...)", color=C, text_color=DW))
        print(box_line("  Type 'back' to return to main menu.", color=C, text_color=DW))
        print(box_empty(C))
        print(box_bot(C))
        print()

        q = input(C + "  🔍 Search: " + W).strip()
        if q.lower() in ("back", "b", ""):
            break

        results = find_problem(index, q)

        if not results:
            print()
            print(R + f"  ❌ No results for '{q}'" + RS)
            print()
            pause()
            continue

        if len(results) == 1:
            print_problem(results[0])
            continue

        # multiple results → pick one
        while True:
            clear()
            print(box_top(f"🔍  Results for '{q}'  ({len(results)} found)", color=C))
            print(box_empty(C))

            for i, p in enumerate(results[:20], 1):
                dc   = DIFF_COLOR.get(p["difficulty"], W)
                line = (f"  [{Y}{i:2d}{RS}]  "
                        f"{Y}#{p['num']:<6}{RS}"
                        f"{W}{p['title']:<40}{RS}"
                        f"{dc}{p['difficulty']:<8}{RS}"
                        f"{DW}{p['category']}{RS}")
                print(box_line(line, color=C))

            if len(results) > 20:
                print(box_line(DW + f"  ... and {len(results)-20} more. Refine your search.", color=C))

            print(box_empty(C))
            print(box_bot(C))
            print()

            ch = input(C + "  Pick number (or 'back'): " + W).strip()
            if ch.lower() in ("back", "b", ""):
                break
            if ch.isdigit() and 1 <= int(ch) <= min(len(results), 20):
                print_problem(results[int(ch) - 1])
            else:
                print(R + "  Invalid choice." + RS)

# ╔══════════════════════════════════════════════════════════════════════╗
#   STATS SCREEN
# ╚══════════════════════════════════════════════════════════════════════╝

def stats_screen(index: list[dict], username: str):
    clear()

    total  = len(index)
    easy   = sum(1 for p in index if p["difficulty"] == "Easy")
    medium = sum(1 for p in index if p["difficulty"] == "Medium")
    hard   = sum(1 for p in index if p["difficulty"] == "Hard")

    cats = {}
    for p in index:
        cats[p["category"]] = cats.get(p["category"], 0) + 1
    top_cats = sorted(cats.items(), key=lambda x: -x[1])[:8]

    print(box_top(f"📊  Stats  —  {username}", color=G))
    print(box_empty(G))
    print(box_line(G + B + f"  Total Solved : {total}" + RS, color=G))
    print(box_empty(G))
    print(box_line(f"  {Fore.GREEN}Easy   : {easy}{RS}", color=G))
    print(box_line(f"  {Fore.YELLOW}Medium : {medium}{RS}", color=G))
    print(box_line(f"  {Fore.RED}Hard   : {hard}{RS}", color=G))
    print(box_empty(G))
    print(box_mid(G))
    print(box_line(G + "  Top Categories:" + RS, color=G))
    print(box_empty(G))

    max_count = top_cats[0][1] if top_cats else 1
    bar_width = 30

    for cat, count in top_cats:
        filled = int(bar_width * count / max_count)
        bar    = Fore.GREEN + "█" * filled + DW + "░" * (bar_width - filled) + RS
        line   = f"  {W}{cat:<20}{RS} {bar}  {Y}{count}{RS}"
        print(box_line(line, color=G))

    print(box_empty(G))
    print(box_bot(G))
    print()
    pause()

# ╔══════════════════════════════════════════════════════════════════════╗
#   PARSER
# ╚══════════════════════════════════════════════════════════════════════╝

GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY_ALL_AC_LIST = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug limit: $limit skip: $skip filters: $filters
  ) {
    total: totalNum
    questions: data {
      frontendQuestionId: questionFrontendId
      title titleSlug difficulty
      topicTags { name slug }
      status
    }
  }
}
"""

QUERY_PROBLEM_DETAIL = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId questionFrontendId title titleSlug
    content difficulty topicTags { name slug } stats hints
  }
}
"""

QUERY_SUBMISSIONS = """
query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String) {
  submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug) {
    submissions { id statusDisplay lang runtime timestamp memory }
  }
}
"""

QUERY_SUB_DETAIL = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtime runtimeDisplay runtimePercentile
    memory memoryDisplay memoryPercentile
    code timestamp
    lang { name verboseName }
  }
}
"""

def make_api_session(cfg: dict) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "User-Agent":   "Mozilla/5.0",
        "Referer":      "https://leetcode.com",
        "x-csrftoken":  cfg["csrf_token"],
    })
    s.cookies.set("LEETCODE_SESSION", cfg["session_cookie"], domain="leetcode.com")
    s.cookies.set("csrftoken",        cfg["csrf_token"],     domain="leetcode.com")
    return s

def gql(sess, query, variables):
    r = sess.post(GRAPHQL_URL, json={"query": query, "variables": variables}, timeout=15)
    if r.status_code in (400, 401, 403):
        raise PermissionError(f"HTTP {r.status_code} — token may be expired")
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(str(data["errors"]))
    return data.get("data", {})

def clean_html(html):
    if not html:
        return ""
    html = html.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&")
    html = html.replace("&nbsp;"," ").replace("&quot;",'"').replace("&#39;","'")
    html = re.sub(r"<br\s*/?>","\n", html)
    html = re.sub(r"</p>|</div>","\n", html)
    html = re.sub(r"<li>","\n  • ", html)
    html = re.sub(r"<sup>","^", html)
    html = re.sub(r"</sup>|<sub>|</sub>","", html)
    html = re.sub(r"<[^>]+>","", html)
    lines = [l.rstrip() for l in html.splitlines()]
    out, blanks = [], 0
    for l in lines:
        if l == "":
            blanks += 1
            if blanks <= 1: out.append(l)
        else:
            blanks = 0; out.append(l)
    return "\n".join(out).strip()

def format_txt(problem, submission, detail):
    SEP  = "=" * 70
    SEP2 = "-" * 70
    num        = problem.get("questionFrontendId") or problem.get("questionId","?")
    title      = problem.get("title","Unknown")
    difficulty = problem.get("difficulty","Unknown")
    tags       = [t["name"] for t in problem.get("topicTags",[])]
    all_tags   = ", ".join(tags) if tags else "N/A"
    category   = tags[0] if tags else "Other"
    content    = clean_html(problem.get("content",""))
    hints      = problem.get("hints",[])
    try:
        stats      = json.loads(problem.get("stats") or "{}")
        acceptance = stats.get("acRate","N/A")
    except Exception:
        acceptance = "N/A"
    lang_info  = detail.get("lang") or {}
    lang_name  = lang_info.get("verboseName") or submission.get("lang","Unknown")
    code       = detail.get("code") or "# Code not available"
    rt_display = detail.get("runtimeDisplay") or submission.get("runtime","N/A")
    rt_pct     = detail.get("runtimePercentile")
    mem_display= detail.get("memoryDisplay") or submission.get("memory","N/A")
    mem_pct    = detail.get("memoryPercentile")
    rt_str     = f"beats {rt_pct:.1f}%"  if rt_pct  else ""
    mem_str    = f"beats {mem_pct:.1f}%" if mem_pct else ""
    ts = submission.get("timestamp")
    try:    date_str = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d") if ts else "N/A"
    except: date_str = "N/A"

    lines = [
        SEP, f"  LEETCODE #{num} — {title}", SEP,
        f"  Difficulty  : {difficulty}",
        f"  Category    : {category}",
        f"  Tags        : {all_tags}",
        f"  Acceptance  : {acceptance}", SEP, "",
        "PROBLEM STATEMENT", SEP2, content,
    ]
    if hints:
        lines += ["", "HINTS", SEP2]
        for i,h in enumerate(hints,1):
            lines.append(f"  Hint {i}: {clean_html(h)}")
    lines += [
        "", SEP, f"  MY SOLUTION  ({lang_name})", SEP, "", code, "",
        SEP, "  SUBMISSION STATS", SEP2,
        f"  Runtime  : {rt_display:<12} {rt_str}",
        f"  Memory   : {mem_display:<12} {mem_str}",
        f"  Status   : Accepted ✓",
        f"  Date     : {date_str}",
        f"  Language : {lang_name}", SEP,
    ]
    return "\n".join(lines)

def save_txt(content, problem, solves_dir, username="user", lang_name="unknown"):
    num        = problem.get("questionFrontendId") or problem.get("questionId", 0)
    title      = problem.get("title", "Unknown")
    # folder: 0001_Two_Sum/
    safe_title = re.sub(r"[^\w\s-]", "", title).strip()
    safe_title = re.sub(r"\s+", "_", safe_title)
    folder_name = f"{int(num):04d}_{safe_title}"
    folder      = Path(solves_dir) / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    # file: negmurodov_python.txt
    safe_lang = re.sub(r"[^\w]", "", lang_name).lower()
    safe_user = re.sub(r"[^\w]", "_", username).lower()
    fname = f"{safe_user}_{safe_lang}.txt"
    path  = folder / fname
    path.write_text(content, encoding="utf-8")
    return path

def existing_nums(solves_dir: str) -> set[int]:
    root = Path(solves_dir)
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
        return set()
    nums = set()
    for folder in root.iterdir():
        if folder.is_dir():
            m = re.match(r'^(\d+)_', folder.name)
            if m:
                nums.add(int(m.group(1)))
    return nums

def parse_screen(cfg: dict, index_ref: list):
    clear()
    print(box_top("⚡  Parse New Solutions", color=M))
    print(box_empty(M))
    print(box_line("  Fetching your solved problems from LeetCode...", color=M))
    print(box_line("  Already downloaded files will be skipped.", color=M, text_color=DW))
    print(box_empty(M))
    print(box_bot(M))
    print()

    try:
        sess = make_api_session(cfg)
    except Exception as e:
        print(R + f"  ❌ Could not create session: {e}" + RS)
        pause()
        return

    # fetch list
    print(M + "  📋 Fetching solved list..." + RS)
    solved, skip_api, limit = [], 0, 100
    total_api = None
    try:
        while True:
            data = gql(sess, QUERY_ALL_AC_LIST, {
                "categorySlug": "", "skip": skip_api,
                "limit": limit, "filters": {"status": "AC"}
            })
            ql = data.get("problemsetQuestionList", {})
            qs = ql.get("questions", [])
            if total_api is None:
                total_api = ql.get("total", 0)
            if not qs:
                break
            solved.extend(qs)
            skip_api += limit
            print(f"  → {min(skip_api, total_api)}/{total_api}", end="\r")
            if skip_api >= total_api:
                break
            time.sleep(1)
    except PermissionError:
        print()
        print(R + "\n  ⚠️  Token expired! Go to Settings → Update Cookies.\n" + RS)
        pause()
        return
    except Exception as e:
        print(R + f"\n  ❌ Error: {e}" + RS)
        pause()
        return

    existing = existing_nums(cfg["solves_dir"])
    new_ones  = [p for p in solved if int(p.get("frontendQuestionId", 0)) not in existing]

    print(f"\n  ✅ {len(solved)} solved  |  {len(existing)} already saved  |  {G}{len(new_ones)} new{RS}\n")

    if not new_ones:
        print(G + "  🎉 Everything is up to date!" + RS)
        print()
        pause()
        return

    print(M + f"  Downloading {len(new_ones)} new solutions...\n" + RS)
    success, failed = 0, []

    for i, prob in enumerate(new_ones, 1):
        slug  = prob["titleSlug"]
        title = prob.get("title", slug)
        num   = prob.get("frontendQuestionId", "?")

        print(f"  [{i:3d}/{len(new_ones)}] #{num}  {title}")

        try:
            time.sleep(1.5)
            detail_prob = gql(sess, QUERY_PROBLEM_DETAIL, {"titleSlug": slug}).get("question", {})
            if not detail_prob:
                raise ValueError("empty")
            if not detail_prob.get("topicTags") and prob.get("topicTags"):
                detail_prob["topicTags"] = prob["topicTags"]
            if not detail_prob.get("difficulty"):
                detail_prob["difficulty"] = prob.get("difficulty", "Easy")

            time.sleep(1.5)
            subs_data = gql(sess, QUERY_SUBMISSIONS, {
                "offset": 0, "limit": 20, "lastKey": None, "questionSlug": slug
            })
            subs = subs_data.get("submissionList", {}).get("submissions", [])
            ac   = [s for s in subs if s.get("statusDisplay") == "Accepted"]
            if not ac:
                print(f"         ⚠  no AC submission")
                failed.append((num, title, "no AC"))
                continue
            sub = ac[0]

            time.sleep(1.5)
            sub_detail = gql(sess, QUERY_SUB_DETAIL, {"submissionId": int(sub["id"])}).get("submissionDetails", {})

            content  = format_txt(detail_prob, sub, sub_detail)
            linfo    = sub_detail.get("lang") or {}
            lname    = linfo.get("name") or sub.get("lang", "unknown")
            path     = save_txt(content, detail_prob, cfg["solves_dir"],
                                username=cfg.get("username", "user"),
                                lang_name=lname)
            print(G + f"         ✅ → {path}" + RS)
            success += 1

        except PermissionError:
            print(R + "\n  ⚠️  Token expired! Go to Settings → Update Cookies.\n" + RS)
            break
        except Exception as e:
            print(R + f"         ❌ {e}" + RS)
            failed.append((num, title, str(e)))
            time.sleep(2)

    # rebuild index
    index_ref.clear()
    index_ref.extend(scan_files(cfg["solves_dir"]))

    print()
    print(box_top(color=G))
    print(box_line(G + f"  ✅ {success} new solutions saved!", color=G, align="center"))
    if failed:
        print(box_line(R + f"  ❌ {len(failed)} failed", color=G, align="center"))
    print(box_bot(color=G))
    print()
    pause()

# ╔══════════════════════════════════════════════════════════════════════╗
#   MAIN MENU
# ╚══════════════════════════════════════════════════════════════════════╝

# ╔══════════════════════════════════════════════════════════════════════╗
#   GIT
# ╚══════════════════════════════════════════════════════════════════════╝

def _run_git(args: list[str], cwd: str) -> tuple[int, str, str]:
    """Run a git command in cwd. Returns (returncode, stdout, stderr)."""
    # Make sure the directory actually exists before passing it to subprocess
    cwd_path = Path(cwd)
    if not cwd_path.exists():
        try:
            cwd_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return -1, "", f"Cannot create directory '{cwd}': {e}"
    try:
        r = subprocess.run(
            ["git"] + args,
            cwd=str(cwd_path),
            capture_output=True,
            text=True,
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return -1, "", "git not found. Install Git and add it to PATH."
    except NotADirectoryError:
        return -1, "", f"Path is not a directory: {cwd}"

def _git_is_repo(path: str) -> bool:
    code, _, _ = _run_git(["rev-parse", "--is-inside-work-tree"], path)
    return code == 0

def _print_git_result(ok: bool, msg: str):
    color = G if ok else R
    icon  = "✅" if ok else "❌"
    print(f"\n{color}  {icon}  {msg}{RS}\n")

def git_screen(cfg: dict):
    solves_dir = cfg.get("solves_dir", str(SOLVES_DIR))
    # Use explicit repo_root from config if set, otherwise parent of solves_dir
    repo_root  = cfg.get("repo_root") or str(Path(solves_dir).parent)

    while True:
        clear()
        is_repo   = _git_is_repo(repo_root)
        repo_icon = G + "✔ git repo" + RS if is_repo else R + "✘ not a repo" + RS

        # read remote url if exists
        _, remote_url, _ = _run_git(["remote", "get-url", "origin"], repo_root)
        remote_str = DW + (remote_url if remote_url else "no remote set") + RS

        # current branch
        _, branch, _ = _run_git(["branch", "--show-current"], repo_root)
        branch_str = (C + branch + RS) if branch else DW + "—" + RS

        print(box_top("🐙  Git", color=C))
        print(box_empty(C))
        print(box_line(f"  Repo root : {DW}{repo_root}{RS}", color=C))
        print(box_line(f"  Status    : {repo_icon}", color=C))
        print(box_line(f"  Remote    : {remote_str}", color=C))
        print(box_line(f"  Branch    : {branch_str}", color=C))
        print(box_empty(C))
        print(box_mid(C))
        print(box_line(f"  {Y}[1]{RS}  🌱  git init  (initialize repo)", color=C))
        print(box_line(f"  {Y}[2]{RS}  🔗  Set remote origin URL", color=C))
        print(box_line(f"  {Y}[3]{RS}  ➕  git add + commit", color=C))
        print(box_line(f"  {Y}[4]{RS}  🚀  git push", color=C))
        print(box_line(f"  {Y}[5]{RS}  🔄  git add + commit + push  (all-in-one)", color=C))
        print(box_line(f"  {Y}[6]{RS}  📋  git status", color=C))
        print(box_line(f"  {Y}[7]{RS}  📜  git log  (last 10)", color=C))
        print(box_line(f"  {Y}[8]{RS}  🔙  Back", color=C))
        print(box_empty(C))
        print(box_bot(C))
        print()

        ch = input(C + "  → " + W).strip()

        if ch == "1":
            _git_cmd_init(repo_root, cfg)
        elif ch == "2":
            _git_cmd_set_remote(repo_root)
        elif ch == "3":
            _git_cmd_add_commit(repo_root)
        elif ch == "4":
            _git_cmd_push(repo_root)
        elif ch == "5":
            _git_cmd_add_commit(repo_root, auto_push=True)
        elif ch == "6":
            _git_cmd_status(repo_root)
        elif ch == "7":
            _git_cmd_log(repo_root)
        elif ch in ("8", "q", "back"):
            break


def _git_cmd_init(repo_root: str, cfg: dict):
    clear()
    print(box_top("🌱  git init", color=G))
    print(box_empty(G))

    already_repo = _git_is_repo(repo_root)

    if already_repo:
        print(box_line(f"  {Y}Already a git repo — skipping init.{RS}", color=G))
    else:
        # force main as default branch name
        _run_git(["config", "--global", "init.defaultBranch", "main"], repo_root)
        code, out, err = _run_git(["init", "-b", "main"], repo_root)
        ok = code == 0
        _print_git_result(ok, out if ok else err)

    # create .gitignore if missing
    gi_path = Path(repo_root) / ".gitignore"
    if not gi_path.exists():
        gi_path.write_text(
            "# LeetCode CLI\nlc_config.json\n__pycache__/\n*.pyc\n.DS_Store\n",
            encoding="utf-8",
        )
        print(f"  {G}📄  .gitignore created{RS}\n")

    # set user identity if not configured
    _, uname, _ = _run_git(["config", "user.name"], repo_root)
    if not uname:
        username = cfg.get("username", "")
        if username:
            _run_git(["config", "user.name", username], repo_root)
            _run_git(["config", "user.email", f"{username}@users.noreply.github.com"], repo_root)
            print(f"  {G}👤  Git user set to '{username}'{RS}\n")

    # make initial commit so branch main physically exists
    if not already_repo:
        _run_git(["add", "-A"], repo_root)
        code2, out2, err2 = _run_git(
            ["commit", "-m", "Initial commit — LeetCode solutions"], repo_root
        )
        if code2 == 0:
            print(f"  {G}📦  Initial commit created on branch main{RS}\n")
        else:
            print(f"  {Y}Could not make initial commit: {err2}{RS}\n")

    print(box_bot(G))
    pause()


def _git_cmd_set_remote(repo_root: str):
    clear()
    print(box_top("🔗  Set Remote Origin", color=C))
    print(box_empty(C))
    print(box_line(f"  {DW}Example: https://github.com/username/LeetCode-Solves.git{RS}", color=C))
    print(box_bot(C))
    print()

    url = input(Y + "  Remote URL: " + W).strip()
    if not url:
        print(R + "  Cancelled." + RS)
        pause()
        return

    # check if origin already exists
    _, existing, _ = _run_git(["remote", "get-url", "origin"], repo_root)
    if existing:
        code, out, err = _run_git(["remote", "set-url", "origin", url], repo_root)
    else:
        code, out, err = _run_git(["remote", "add", "origin", url], repo_root)

    _print_git_result(code == 0, f"Remote set to: {url}" if code == 0 else err)
    pause()


def _git_cmd_add_commit(repo_root: str, auto_push: bool = False):
    clear()
    print(box_top("➕  Add & Commit", color=Y))
    print(box_empty(Y))

    # show short status
    _, status_out, _ = _run_git(["status", "--short"], repo_root)
    if status_out:
        for line in status_out.splitlines()[:15]:
            print(box_line(f"  {DW}{line}{RS}", color=Y))
    else:
        print(box_line(f"  {G}Nothing to commit — working tree clean.{RS}", color=Y))
        print(box_bot(Y))
        pause()
        return

    print(box_empty(Y))
    print(box_bot(Y))
    print()

    msg = input(Y + "  Commit message [leave blank = auto]: " + W).strip()
    if not msg:
        count_added = len([l for l in status_out.splitlines() if l.startswith(("A", "?", "M"))])
        msg = f"Add {count_added} solution(s) — {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # stage all
    code, _, err = _run_git(["add", "-A"], repo_root)
    if code != 0:
        _print_git_result(False, err)
        pause()
        return

    # commit
    code, out, err = _run_git(["commit", "-m", msg], repo_root)
    _print_git_result(code == 0, out if code == 0 else err)

    if auto_push and code == 0:
        _git_cmd_push(repo_root, silent_header=True)
    else:
        pause()


def _git_cmd_push(repo_root: str, silent_header: bool = False):
    if not silent_header:
        clear()
        print(box_top("🚀  git push", color=M))
        print(box_empty(M))
        print(box_bot(M))
        print()

    # detect branch
    _, branch, _ = _run_git(["branch", "--show-current"], repo_root)
    if not branch:
        # no commits yet — branch does not physically exist
        print(f"  {R}❌  No commits found. Run [3] Add + Commit first, then push.{RS}\n")
        pause()
        return

    # check remote is set
    _, remote_url, _ = _run_git(["remote", "get-url", "origin"], repo_root)
    if not remote_url:
        print(f"  {R}❌  No remote origin set. Use [2] Set remote origin URL first.{RS}\n")
        pause()
        return

    print(f"  {DW}Pushing to origin/{branch} ...{RS}\n")
    code, out, err = _run_git(["push", "-u", "origin", branch], repo_root)
    _print_git_result(code == 0, out if (code == 0 and out) else (err or "Push complete."))
    pause()


def _git_cmd_status(repo_root: str):
    clear()
    print(box_top("📋  git status", color=C))
    _, out, err = _run_git(["status"], repo_root)
    for line in (out or err).splitlines():
        print(box_line(f"  {DW}{line}{RS}", color=C))
    print(box_bot(C))
    pause()


def _git_cmd_log(repo_root: str):
    clear()
    print(box_top("📜  git log", color=C))
    _, out, err = _run_git(
        ["log", "--oneline", "--graph", "--decorate", "-20"], repo_root
    )
    for line in (out or err).splitlines():
        print(box_line(f"  {DW}{line}{RS}", color=C))
    print(box_bot(C))
    pause()


def main_menu(cfg: dict):
    solves_dir = cfg.get("solves_dir", str(SOLVES_DIR))
    username   = cfg.get("username", "unknown")

    index = scan_files(solves_dir)

    while True:
        clear()
        total  = len(index)
        easy   = sum(1 for p in index if p["difficulty"] == "Easy")
        medium = sum(1 for p in index if p["difficulty"] == "Medium")
        hard   = sum(1 for p in index if p["difficulty"] == "Hard")

        solved_str = (f"{G}{easy}E{RS}  {Y}{medium}M{RS}  {R}{hard}H{RS}  "
                      f"│  {W}{B}{total} total{RS}")

        print(box_top(color=C))
        print(box_line(
            C + B + "  🧠 LeetCode CLI" + RS + "  " + DW + f"—  {username}" + RS,
            color=C
        ))
        print(box_line("  " + solved_str, color=C))
        print(box_mid(C))
        print(box_empty(C))
        print(box_line(f"  {Y}[1]{RS}  🔍  Search / View problem", color=C))
        print(box_line(f"  {Y}[2]{RS}  ⚡  Parse new solutions", color=C))
        print(box_line(f"  {Y}[3]{RS}  📊  Stats", color=C))
        print(box_line(f"  {Y}[4]{RS}  ⚙️   Settings", color=C))
        print(box_line(f"  {Y}[5]{RS}  🐙  Git", color=C))
        print(box_line(f"  {Y}[6]{RS}  🚪  Exit", color=C))
        print(box_empty(C))
        print(box_line(DW + "  Tip: type a problem number directly (e.g. 620)", color=C))
        print(box_empty(C))
        print(box_bot(C))
        print()

        ch = input(C + "  → " + W).strip()

        if ch == "1":
            search_screen(index)
        elif ch == "2":
            parse_screen(cfg, index)
        elif ch == "3":
            stats_screen(index, username)
        elif ch == "4":
            cfg = settings_screen(cfg)
            # reload index if dir changed
            index = scan_files(cfg.get("solves_dir", solves_dir))
            solves_dir = cfg.get("solves_dir", solves_dir)
            username   = cfg.get("username", username)
        elif ch == "5":
            git_screen(cfg)
        elif ch in ("6", "q", "exit"):
            clear()
            print()
            center_print(C + B + "👋  Goodbye!" + RS)
            print()
            sys.exit(0)
        elif ch.isdigit():
            results = find_problem(index, ch)
            if results:
                print_problem(results[0])
            else:
                print(R + f"\n  ❌ Problem #{ch} not found in local files.\n" + RS)
                pause()

# ╔══════════════════════════════════════════════════════════════════════╗
#   ENTRY
# ╚══════════════════════════════════════════════════════════════════════╝

def main():
    cfg = load_config()

    if not cfg or not cfg.get("username"):
        cfg = setup_screen()

    main_menu(cfg)

if __name__ == "__main__":
    main()
