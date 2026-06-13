======================================================================
  Leetcode-Solves  —  Open Source Solutions Collection
======================================================================

  An open collection of LeetCode solutions where anyone can
  contribute their own solution in any language.

  GitHub : https://github.com/isa1902/Leetcode-Solves
  Author : negmurodov (isa1902)

======================================================================
  FOLDER STRUCTURE
======================================================================

  Leetcode-Solves/
  ├── README.txt                  ← you are here
  ├── CONTRIBUTING.md             ← how to add your solution
  ├── lc.py                       ← CLI tool (auto-generates files)
  │
  ├── 0001_Two_Sum/
  │   ├── negmurodov_python.txt
  │   ├── someone_java.txt
  │   └── another_cpp.txt
  │
  ├── 0195_Tenth_Line/
  │   └── negmurodov_bash.txt
  └── ...

======================================================================
  FILE NAMING CONVENTION
======================================================================

  Folder : {4-digit number}_{Problem_Title}/
  File   : {your_github_username}_{language}.txt

  Examples:
    negmurodov_python.txt
    john_doe_cpp.txt
    maria_java.txt
    someone_mysql.txt

======================================================================
  FILE FORMAT  (inside each .txt)
======================================================================

  ======================================================================
    LEETCODE #{number} — {Title}
  ======================================================================
    Difficulty  : Easy / Medium / Hard
    Category    : Array / DP / Graph / ...
    Tags        : Tag1, Tag2
    Acceptance  : 49.5%

  PROBLEM STATEMENT
  ----------------------------------------------------------------------
  {Problem description here}

  ======================================================================

  MY SOLUTION  ({Language})
  ======================================================================

  {Your accepted code here}

  ======================================================================
    SUBMISSION STATS
  ----------------------------------------------------------------------
    Runtime  : 45 ms        beats 92.3%
    Memory   : 16.4 MB      beats 78.1%
    Status   : Accepted ✓
    Date     : 2026-06-05
    Language : Python3
  ======================================================================

======================================================================
  lc.py  —  CLI TOOL
======================================================================

  Automatically parses and downloads your LeetCode solutions.
  Files are saved in the correct format and folder structure.

  Requirements:
    pip install colorama requests

  Run:
    python lc.py

  On first run you will be asked for:
    - LeetCode username
    - LEETCODE_SESSION cookie
    - csrftoken cookie

  How to get cookies:
    1. Open leetcode.com (logged in)
    2. Press F12 → Application → Cookies
    3. Click https://leetcode.com
    4. Copy LEETCODE_SESSION and csrftoken values

======================================================================
  HOW TO CONTRIBUTE
======================================================================

  See CONTRIBUTING.md for full instructions.

  Quick version:
    1. Fork the repo on GitHub
    2. Create folder: 0001_Two_Sum/  (if it doesn't exist)
    3. Add your file: yourname_python.txt
    4. Commit: "Add: #1 Two Sum - yourname - Python"
    5. Open a Pull Request

  All languages accepted:
    Python · C++ · Java · JavaScript · Go · Rust · C · C#
    Kotlin · Swift · MySQL · Bash · Pandas · TypeScript · and more

======================================================================
  LICENSE  —  MIT
======================================================================

  Free to use, share, and contribute.
  Copyright (c) 2026 negmurodov

======================================================================
