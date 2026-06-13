# 🤝 Contributing to Leetcode-Solves

Thanks for wanting to contribute! Here's everything you need to know.

---

## ✅ Rules

1. **Accepted solutions only** — must be `Accepted` on LeetCode (not TLE, WA, etc.)
2. **One file per person per problem** — named `username_language.txt`
3. **Use the standard format** — described below
4. **No duplicate files** — check if your file already exists before submitting

---

## 📁 Folder & File Naming

### Folder name
```
{4-digit number}_{Problem_Title_With_Underscores}/
```
Examples:
```
0001_Two_Sum/
0195_Tenth_Line/
1143_Longest_Common_Subsequence/
```

If the folder doesn't exist yet — create it.

### File name
```
{your_github_username}_{language}.txt
```
Examples:
```
negmurodov_python.txt
negmurodov_bash.txt
john_doe_cpp.txt
maria123_java.txt
someone_mysql.txt
```

Accepted language names: `python` `cpp` `java` `javascript` `typescript` `go` `rust` `c` `csharp` `kotlin` `swift` `mysql` `bash` `pandas` `scala` `ruby` `php`

---

## 📝 File Format

Copy this template and fill it in:

```
======================================================================
  LEETCODE #{number} — {Title}
======================================================================
  Difficulty  : Easy / Medium / Hard
  Tags        : Tag1, Tag2, Tag3

PROBLEM STATEMENT
----------------------------------------------------------------------
{Paste the problem statement here}

======================================================================

MY SOLUTION  ({Language})
======================================================================

{Your accepted code here}

======================================================================
  SUBMISSION STATS
----------------------------------------------------------------------
  Runtime  : {e.g. 45 ms}      beats {e.g. 92.3%}
  Memory   : {e.g. 16.4 MB}    beats {e.g. 78.1%}
  Status   : Accepted ✓
  Date     : {YYYY-MM-DD}
  Language : {e.g. Python3}
======================================================================
```

---

## 🔧 Step-by-Step

```bash
# 1. Fork the repo on GitHub (click Fork button)

# 2. Clone your fork
git clone https://github.com/{your-username}/Leetcode-Solves.git
cd Leetcode-Solves

# 3. Create folder if it doesn't exist
mkdir -p "0001_Two_Sum"

# 4. Add your solution file
# e.g. 0001_Two_Sum/yourname_python.txt

# 5. Commit and push
git add .
git commit -m "Add: #1 Two Sum - yourname - Python"
git push origin main

# 6. Open a Pull Request on GitHub
```

### Commit message format
```
Add: #{number} {Problem Title} - {username} - {Language}
```
Examples:
```
Add: #1 Two Sum - negmurodov - Python
Add: #146 LRU Cache - john_doe - C++
Add: #195 Tenth Line - negmurodov - Bash
```

---

## ⚡ Auto-generate with lc.py

If you use the [lc.py CLI tool](https://github.com/isa1902/lc.py), it generates properly formatted `.txt` files automatically from your LeetCode account. Just rename the file to `username_language.txt`, drop it in the right folder and submit a PR.

---

## ❓ Questions?

Open an [Issue](https://github.com/isa1902/Leetcode-Solves/issues) and ask anything.
