# 🧠 Leetcode-Solves

![Problems Solved](https://leetcode-badge-sage.vercel.app/badge/negmurodov?style=flat-square&label=Solved)
![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20SQL%20%7C%20Bash-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red?style=flat-square)
![Author](https://img.shields.io/badge/Author-isa1902-purple?style=flat-square)
![Contributors Welcome](https://img.shields.io/badge/Contributors-Welcome-orange?style=flat-square)

An open collection of LeetCode solutions — automatically parsed and saved via **lc.py**, a custom CLI tool.  
Anyone can contribute their own solution in any language. The more the merrier! 🎉

---

## 📁 Repository Structure

```
Leetcode-Solves/
├── README.md
├── CONTRIBUTING.md          ← full contribution guide
├── lc.py                    ← CLI tool (auto-downloads your solutions)
├── LICENSE
│
└── Leetcode-Solves/         ← all solutions live here
    ├── 0001_Two_Sum/
    │   ├── negmurodov_python3.txt
    │   ├── john_doe_cpp.txt
    │   └── maria_java.txt
    ├── 0004_Median_of_Two_Sorted_Arrays/
    │   └── negmurodov_python3.txt
    └── ...
```

Each `.txt` file is named `{your_github_username}_{language}.txt` and contains:
- Full problem statement
- Your accepted solution
- Submission stats (runtime, memory, date)

---

## ⚡ lc.py — CLI Tool (for repo owner)

`lc.py` automatically fetches your accepted LeetCode solutions and saves them in the correct format and folder structure.

**Setup:**
```bash
pip install colorama requests
python lc.py
```

**On first run you will be asked for:**
- LeetCode username
- `LEETCODE_SESSION` cookie
- `csrftoken` cookie

**How to get cookies:**
1. Open [leetcode.com](https://leetcode.com) (logged in)
2. Press `F12` → **Application** → **Cookies**
3. Click `https://leetcode.com`
4. Copy `LEETCODE_SESSION` and `csrftoken` values

**Main menu features:**

| Option | Description |
|--------|-------------|
| 🔍 Search | Browse and view local solutions |
| ⚡ Parse | Download new accepted solutions from LeetCode |
| 📊 Stats | See your solve count by difficulty and category |
| ⚙️ Settings | Update cookies, GitHub account, paths |
| 🐙 Git | Push solutions to GitHub directly from CLI |

---

## 🤝 How to Contribute (for everyone)

Want to add your own solution? Here's how:

### Option A — Pull Request (recommended)

1. **Fork** this repo (click Fork button top-right on GitHub)
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Leetcode-Solves.git
   cd Leetcode-Solves
   ```
3. **Find or create** the problem folder inside `Leetcode-Solves/`:
   ```
   Leetcode-Solves/0001_Two_Sum/
   ```
4. **Add your file** named `{your_github_username}_{language}.txt`:
   ```
   Leetcode-Solves/0001_Two_Sum/john_doe_python3.txt
   ```
5. **Use this file format:**
   ```
   ======================================================================
     LEETCODE #1 — Two Sum
   ======================================================================
     Difficulty  : Easy
     Category    : Array
     Tags        : Array, Hash Table
     Acceptance  : 57.6%
   ======================================================================

   PROBLEM STATEMENT
   ----------------------------------------------------------------------
   Given an array of integers nums and an integer target, return indices
   of the two numbers such that they add up to target.

   ======================================================================
     MY SOLUTION  (Python3)
   ======================================================================

   class Solution:
       def twoSum(self, nums, target):
           seen = {}
           for i, num in enumerate(nums):
               if target - num in seen:
                   return [seen[target - num], i]
               seen[num] = i

   ======================================================================
     SUBMISSION STATS
   ----------------------------------------------------------------------
     Runtime  : 45 ms        beats 92.3%
     Memory   : 16.4 MB      beats 78.1%
     Status   : Accepted ✓
     Date     : 2026-06-14
     Language : Python3
   ======================================================================
   ```
6. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add: #1 Two Sum - john_doe - Python3"
   git push origin main
   ```
7. **Open a Pull Request** — it will be reviewed and merged!

---

### Option B — Direct push (trusted contributors)

```bash
git clone https://github.com/isa1902/Leetcode-Solves.git
cd Leetcode-Solves
# add your file...
git add .
git commit -m "Add: #42 Trapping Rain Water - your_name - C++"
git push
```

---

## 📝 File Naming Convention

| What | Format | Example |
|------|--------|---------|
| Folder | `{4-digit-number}_{Problem_Title}/` | `0001_Two_Sum/` |
| File | `{github_username}_{language}.txt` | `john_doe_python3.txt` |

**Supported languages:**  
`python3` · `cpp` · `java` · `javascript` · `typescript` · `go` · `rust` · `c` · `csharp` · `kotlin` · `swift` · `mysql` · `pythondata` · `bash` · `oraclesql` · and more

---

## 📄 License

MIT © 2026 [isa1902](https://github.com/isa1902) — free to use, share, and contribute.
