# m5rcode – The Unofficial Programming Language (Python)

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-experimental-orange.svg)

**m5rcode** is an experimental, unofficial programming language written entirely in **Python**.  
It ships with a custom **REPL shell** (`m5rshell`) and a `.m5r` **file interpreter**, so you can explore ideas interactively or run full scripts.

---

## ✨ Features

- **m5rshell – The REPL Shell**  
  Interact with m5rcode in real time using our powerful and intuitive Read–Eval–Print–Loop.
  - Built-in commands:
    - `new` – create a new `.m5r` script
    - `nano` – open a script in the built-in editor
    - `run` – execute a script
    - `fastfetch` – display system/runtime info
    - `credits` – show contributors & version details
    - `exit` – leave the shell
    - `cd` – change directories
  - Seamless, developer-friendly CLI experience.

- **.m5r File Runner (Interpreter)**  
  Our robust interpreter brings your `.m5r` files to life.  
  Designed for **efficiency and clarity**, it executes scripts quickly with readable output—great for both small utilities and larger apps.

---

## 🔧 Requirements

- Python **3.8+**
- macOS, Linux, or Windows

---

## 📦 Installation

Clone this repository:

```bash
git clone https://github.com/m5rcel/m5rcode.git
cd m5rcode
```

(If your project uses dependencies, add them to `requirements.txt`, then:)
```bash
# optional
pip install -r requirements.txt
```

---

## ⚡ Quick Start

### Run the REPL shell
```bash
python3 m5rshell.py
```

Example REPL session:
```
m5rshell> new hello.m5r
m5rshell> nano hello.m5r
# (edit and save)
m5rshell> run hello.m5r
```

### Run a `.m5r` script directly
```bash
python3 m5r.py examples/hello.m5r
```

---

## 📝 Example

Create `hello.m5r`:

```m5r
# hello.m5r
print("Hello, World from m5rcode!")
```

Run it:

```bash
python3 m5r.py hello.m5r
```

Output:
```
Hello, World from m5rcode!
```

---

## 📂 Project Structure

```
m5rcode/
├─ m5rshell.py         # The REPL shell (Python)
├─ m5r.py              # The .m5r file interpreter (Python)
├─ examples/           # Sample m5rcode scripts
├─ docs/               # Additional documentation
└─ README.md
```

---

## 🧭 Roadmap (suggested)

- Language spec and grammar docs
- Standard library primitives
- Better error messages & diagnostics
- Packaging to PyPI (`pip install m5rcode`)
- Editor/IDE extensions (syntax highlighting)

---

## 🤝 Contributing

Contributions are welcome!  
If you plan a larger change, open an issue first to discuss scope/design.

1. Fork the repo and create a feature branch.
2. Make your changes with clear commits.
3. Add/update examples or docs if needed.
4. Open a Pull Request describing your changes.

---

## 🐛 Troubleshooting

- **`python3: command not found`** – Install Python from https://python.org or use your OS package manager.
- **Permission issues on macOS/Linux** – Use `python3 file.py` instead of making scripts executable, or `chmod +x` as needed.
- **Windows path issues** – Use `py` launcher: `py m5rshell.py`.

---

## 👥 Credits

- **Creator:** [m5rcel](https://github.com/m5rcel)  
- **Contributors:** Community members supporting the project

---

## 📜 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
