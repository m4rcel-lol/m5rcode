# m5rcode – The Unofficial Polyglot Programming Language

![Polyglot](https://img.shields.io/badge/language-Python%2FJS%2FPHP%2FC%23%2FC++-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-experimental-orange.svg)

**m5rcode** is an experimental **polyglot programming language** written with a blend of **Python, JavaScript, PHP, C#, and C++**.  
It uses obfuscation and cross-language embedding to allow developers to write multi-language scripts in a single file (`.m5r`).  
The project includes a custom **REPL shell** (`m5rshell`) and an **interpreter** for `.m5r` files.  

---

## ✨ Features

- **Polyglot Language Core**
  - Mix **Python, JavaScript, PHP, CSS, C#, and C++** in a single `.m5r` file.
  - Interpreter extracts, executes, and blends code blocks.
  - Supports obfuscation for added challenge and uniqueness.

- **m5rshell – The REPL Shell**
  - Interactive REPL for testing code snippets.
  - Commands:  
    - `new`, `nano`, `run`, `fastfetch`, `credits`, `exit`, `cd`
  - Developer-friendly CLI for creating & running `.m5r` scripts.

- **.m5r File Runner (Interpreter)**
  - Executes `.m5r` polyglot files directly.
  - Efficient, multi-language-aware execution engine.
  - Provides fast output even for obfuscated code.

---

## 🔧 Requirements

- Python **3.8+**

---

## 📦 Installation

Clone this repository:

```bash
git clone https://github.com/m4rcel-lol/m5rcode.git
cd m5rcode
```

---

## ⚡ Quick Start

### Run the REPL shell
```bash
python3 m5rshell.py
```
---

## 📝 Example

Here’s a `hello.m5r` script that prints **Hello world** in all supported languages:

```m5r
<?py
_ = ''.join([chr(c) for c in [72,101,108,108,111,32,119,111,114,108,100]])
print(_)
?>

<?js
(function(){
    var x=[72,101,108,108,111,32,119,111,114,108,100];
    var s='';
    for(var i of x){ s+=String.fromCharCode(i); }
    console.log(s);
})();
?>

<?php
${a}=array(72,101,108,108,111,32,119,111,114,108,100);
echo implode(array_map('chr',${a})) . "\n";
?>

<?css
body { color: #00ff00; background: black; }
?>

<?cs
Console.WriteLine(string.Join("", new int[] {72,101,108,108,111,32,119,111,114,108,100}.Select(c => (char)c)));
?>

<?cpp
int arr[] = {72,101,108,108,111,32,119,111,114,108,100};
for(int i = 0; i < 11; i++) std::cout << (char)arr[i];
std::cout << std::endl;
?>
```

---

## 📂 Project Structure

```
m5rcode/
├─ m5rshell.py         # The REPL shell
├─ m5r_interpreter.py              # The .m5r polyglot interpreter
├─ files/           # Sample m5rcode scripts
├─ utils/               # Handling everything
├─ commands # Commands handling
└─ README.md
```

---

## 🤝 Contributing

Contributions are welcome!  
If you want to add support for more languages, open an issue or PR.

---

## 👥 Credits

- **Creator:** [m5rcel](https://github.com/m4rcel-lol)  
- **Contributors:** The m5rcode community  

---

## 📜 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
