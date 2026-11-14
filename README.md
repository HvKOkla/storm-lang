
# Storm Language

**Storm** is a modern, developer-friendly transpiler that compiles to **Verse** for Fortnite and UEFN.

## 📖 Why Storm?
Verse is a powerful language, but its strict syntax (effects, explicit mutability, formatting) can be hard to read and write. Storm was created to make Verse development faster, cleaner, and more accessible for creators.

## ✨ Features (Work in Progress)
- [x] Lexer & Parser (Python Prototype)
- [x] Basic Code Generation to Verse
- [ ] Classes and Interfaces
- [ ] C++ Core (for high performance)
- [ ] Unreal Engine 5 Plugin
- [ ] VS Code Extension

## 🚀 Getting Started (Python Prototype)

### Prerequisites
- Python 3.10 or higher

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/storm-lang.git
cd storm-lang/1_python_prototype
```

### 2. Write a `.storm` file
Create a file named `my_file.storm`:
```storm
// A simple pure function
pure fn add(a: int, b: int) -> int {
    let x = 10
    var y: int = 20
    y += 1
    if x == 10 {
        return a + b
    }
    return 0
}
```

### 3. Compile to Verse
Run the compiler:
```bash
python stormc.py my_file.storm
```

### 4. Use in Fortnite
Open the generated `my_file.verse` file, copy its contents, and paste it into UEFN (Unreal Editor for Fortnite).

## 🛠️ Project Structure
- `1_python_prototype/`: The fast, flexible Python prototype.
- `2_cpp_core/`: The future high-performance C++ core engine.
- `3_ue5_plugin/`: The future Unreal Engine 5 integration.

## ⚠️ Disclaimer
Storm is an independent community project and is **not affiliated with, endorsed by, or sponsored by Epic Games**. Fortnite, UEFN, and Verse are trademarks of Epic Games.
```