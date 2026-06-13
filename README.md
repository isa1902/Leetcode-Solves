# 🧠 Leetcode-Solves

![Problems Solved](https://img.shields.io/badge/Solved-234%2B-brightgreen?style=flat-square)
![Languages](https://img.shields.io/badge/Languages-Python%20%7C%20SQL%20%7C%20Bash-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red?style=flat-square)
![Author](https://img.shields.io/badge/Author-negmurodov-purple?style=flat-square)

An open collection of LeetCode solutions — automatically parsed and saved via **lc.py**, a custom CLI tool.  
Anyone can contribute their own solution in any language.

---

## 📁 Structure

```
Leetcode-Solves/
├── README.md
├── CONTRIBUTING.md
├── lc.py                    ← CLI tool (auto-downloads solutions)
├── LICENSE
│
├── 0001_Two_Sum/
│   └── negmurodov_python3.txt
├── 0195_Tenth_Line/
│   └── negmurodov_bash.txt
└── ...
```

Each file follows the format `{username}_{language}.txt` and contains the problem statement, solution, and submission stats.

---

## ⚡ lc.py — CLI Tool

Automatically downloads your accepted LeetCode solutions and saves them in the correct format.

```bash
pip install colorama requests
python lc.py
```

On first run you'll be asked for your LeetCode username and session cookies (F12 → Application → Cookies on leetcode.com).

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full instructions.

1. Fork the repo
2. Create folder `0001_Two_Sum/` (if it doesn't exist)
3. Add your file: `yourname_python3.txt`
4. Commit: `Add: #1 Two Sum - yourname - Python`
5. Open a Pull Request

All languages welcome: Python · C++ · Java · JavaScript · Go · Rust · SQL · Bash · and more.

---

## 📄 License

MIT © 2026 [negmurodov](https://github.com/isa1902)
