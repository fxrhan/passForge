# PassForge 🔥

<p align="center">
  <b>Intelligence-Driven Password List Generator</b><br>
  <i>Forge targeted password lists from personal intelligence</i>
  <br><br>
  <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/license-GPLv3-green.svg" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
</p>

---

## 🎯 What is PassForge?

**PassForge** is a state-of-the-art password list generator that creates highly targeted wordlists based on personal information. Unlike generic password generators, PassForge uses **intelligence-driven algorithms** including:

- 🧠 **ML-Based Pattern Analysis** - Patterns from real password breach databases
- 🔤 **Phonetic Variations** - Sound-alike spellings people actually use
- 🧬 **Word Mutations** - Plurals, truncations, and text-speak variations
- 📅 **Advanced Date Formats** - 11 different date pattern variations
- 🌍 **Temporal Intelligence** - Seasons, months, and contextual combinations
- ⚡ **36+ Pattern Types** - Generates 200K-600K+ passwords per target

**Perfect for:** Penetration Testing, Security Research, Password Recovery, Red Team Operations

---

## ✨ Key Features

### **Advanced Pattern Generation**
- ✅ **Reverse Words** - `alice` → `ecila`
- ✅ **Phonetic Spelling** - `phone` → `fone`, `cool` → `kool`
- ✅ **Word Mutations** - Plurals, repetitions, truncations
- ✅ **ML Patterns** - Based on RockYou, LinkedIn, Adobe breach analysis
- ✅ **Date Variations** - 11 formats (DDMMYYYY, MMDDYY, ISO, etc.)
- ✅ **Temporal Passwords** - Months, seasons with years
- ✅ **Advanced Substitutions** - Multi-character leet speak
- ✅ **Keyboard Patterns** - Common keyboard walks
- ✅ **Special Multipliers** - `!!!`, `!@#`, `@#$`

### **Technical Excellence**
- ✅ **Cross-Platform** - Windows, Linux, macOS
- ✅ **Fast & Efficient** - Optimized string operations
- ✅ **Clean Code** - Professional standards, minimal duplication
- ✅ **Progress Indicators** - Real-time generation feedback
- ✅ **Comprehensive Testing** - Automated compatibility tests

---

## 🚀 Quick Start

### Installation

**Linux/macOS:**
```bash
git clone https://github.com/fxrhan/passforge.git
cd passforge
pip3 install -r requirements.txt
python3 passforge.py -h
```

**Windows:**
```powershell
git clone https://github.com/fxrhan/passforge.git
cd passforge
pip install -r requirements.txt
python passforge.py -h
```

### Basic Usage

```bash
# Generate password list for a person
python passforge.py -p

# With all advanced features
python passforge.py -p -l -n -y

# For a company
python passforge.py -c

# Set minimum password length
python passforge.py -p -m 8
```

---

## 💻 Usage Examples

### Example 1: Person Target

```bash
python passforge.py -p
```

**Input:**
```
[>] Name: Alice
[>] Surname: Johnson
[>] Nickname: Ali
[>] Birth day: 15
[>] Birth month: 03
[>] Birth year: 1990
[>] First pet: Luna
[>] Keywords: travel, photography
```

**Output:** `output/Alice-Johnson.txt` with 200K+ passwords including:
```
alice, Alice, ALICE, ecila
alice123, Alice!, alice@2024
alice15031990, 15031990alice
alicejan, alicesummer
@lice, alic3, @lic3
fone, kool, nikolas (phonetic)
alices, alicealice, lc (mutations)
Alice1!, Alice@123, !alice! (ML patterns)
...and 200,000+ more
```

### Example 2: Company Target

```bash
python passforge.py -c -l -n
```

**Input:**
```
[>] Name: TechCorp
[>] Web domain: techcorp.com
[>] Birth year: 2010
[>] Keywords: innovation, cloud, AI
```

**Output:** `output/TechCorp.txt` with targeted corporate passwords

---

## 📊 Command-Line Options

```
usage: passforge.py [-h] [-p | -c | -v] [-l | -L] [-y] [-n] [-m MINLENGTH]

PassForge - Intelligence-Driven Password List Generator

options:
  -h, --help            Show this help message and exit
  -p, --person          Target is a person
  -c, --company         Target is a company
  -v, --version         Show version information
  
Advanced Options:
  -l, --leet            Add complete leet speak passwords
  -L, --leetall         Add ALL possible leet combinations
  -y, --years           Add year variations (1985-1999)
  -n, --numbers         Add number variations (1-20)
  -m MINLENGTH          Set minimum password length
```

---

## 🎨 Pattern Examples

### **Basic Patterns**
```
alice, Alice, ALICE
alice., alice-, alice_
alice123, alice1990
```

### **Advanced Patterns**
```
ecila (reverse)
myalice, lovealice (prefixes)
alice!!!, alice@#$ (multipliers)
```

### **Date Variations**
```
15031990, 150390, 031590
15-03-1990, 15/03/1990
19900315 (ISO format)
```

### **Phonetic Variations**
```
phone → fone, Fone
nicholas → nikolas, Nikolas
cool → kool, Kool, cul
```

### **Word Mutations**
```
alice → alices, alicealice, lc
password → passwords, psswrd
```

### **ML-Based Patterns**
```
Alice1!, Alice2024, Alice@123
ALICE!, ALICE!!
!alice!, @alice@
AlIcE, AlIcE1 (alternating)
```

---

## 📈 Performance

| Input Size | Passwords Generated | Time |
|------------|---------------------|------|
| Small (5-7 attrs) | 80K-120K | ~5-10 sec |
| Medium (10-12 attrs) | 200K-300K | ~15-30 sec |
| Large (15+ attrs) | 400K-600K+ | ~30-60 sec |

---

## 🔬 Technical Details

### **Pattern Types (36+)**
1. Basic words & case variations
2. Symbol combinations
3. Number patterns (1-20)
4. Year patterns (1985-1999)
5. Word combinations
6. Reverse words
7. Common suffixes (11 types)
8. Common prefixes (6 types)
9. Special multipliers (9 types)
10. Keyboard patterns (11 types)
11. Advanced capitalization (5 types)
12. Date variations (11 formats)
13. Temporal passwords (months/seasons)
14. Advanced substitutions
15. Phonetic variations (10 patterns)
16. Word mutations (8 types)
17. ML-based patterns (40+ patterns)

### **ML Pattern Sources**
- RockYou Database (32M passwords)
- LinkedIn Leak (117M passwords)
- Adobe Breach (150M passwords)
- General password research

---

## 🛡️ Use Cases

### **Penetration Testing**
Generate targeted wordlists for authorized security assessments

### **Red Team Operations**
Create realistic password lists for social engineering scenarios

### **Password Recovery**
Assist in legitimate password recovery efforts

### **Security Research**
Analyze password patterns and human behavior

### **Security Awareness**
Demonstrate how personal information becomes passwords

---

## 🌍 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | ✅ Fully Supported | Windows 10, 11, Server |
| **Linux** | ✅ Fully Supported | All major distributions |
| **macOS** | ✅ Fully Supported | Intel & Apple Silicon |

---

## 📊 Comparison with Other Tools

| Feature | PassForge | CUPP | CeWL | Crunch | John the Ripper | Hashcat |
|---------|-----------|------|------|--------|-----------------|---------|
| **Target-Specific** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **ML-Based Patterns** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Phonetic Variations** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Word Mutations** | ✅ Yes | ❌ Limited | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| **Date Formats** | ✅ 11 types | ✅ Basic | ❌ No | ❌ No | ❌ No | ❌ No |
| **Temporal Intelligence** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Keyboard Patterns** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Pattern Types** | **36+** | ~15 | ~5 | ~3 | Rule-based | Rule-based |
| **Output Size** | 200K-600K+ | 50K-100K | 10K-50K | Unlimited | N/A | N/A |
| **Cross-Platform** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| **Colorful Output** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Real Breach Analysis** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Active Development** | ✅ Yes | ⚠️ Limited | ⚠️ Limited | ✅ Yes | ✅ Yes | ✅ Yes |
| **Learning Curve** | 🟢 Easy | 🟢 Easy | 🟢 Easy | 🟡 Medium | 🔴 Hard | 🔴 Hard |
| **Best For** | OSINT/Targeted | Personal Info | Web Scraping | Brute Force | Cracking | Cracking |

### **Why PassForge Stands Out:**

1. **🧠 Intelligence-Driven** - Uses ML patterns from real password breaches
2. **🔤 Linguistic Intelligence** - Phonetic variations and word mutations
3. **📊 Comprehensive Coverage** - 36+ pattern types vs competitors' 3-15
4. **🎯 Targeted Approach** - Designed specifically for OSINT and social engineering
5. **🎨 Modern UX** - Colorful, intuitive interface with progress indicators
6. **⚡ High Output** - Generates 10-40x more passwords than basic generators

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For bugs or feature requests, open an [issue](https://github.com/fxrhan/passforge/issues).

---

## ⚖️ Legal Disclaimer

**PassForge is intended for:**
- ✅ Authorized penetration testing
- ✅ Security research
- ✅ Educational purposes
- ✅ Legitimate password recovery

**NOT for:**
- ❌ Unauthorized access
- ❌ Illegal activities
- ❌ Malicious purposes

**Users are responsible for ensuring their use complies with applicable laws and regulations.**

---

## 📝 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

```
PassForge - Intelligence-Driven Password List Generator
Copyright (C) 2025 fxrhan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

---

## 👤 Author

**fxrhan**
- GitHub: [@fxrhan](https://github.com/fxrhan)
- Project: [PassForge](https://github.com/fxrhan/passforge)

---

## 🌟 Acknowledgments

- **Inspired by:** [longtongue](https://github.com/edoardottt/longtongue) by [@edoardottt](https://github.com/edoardottt)
- Real-world password breach analysis (RockYou, LinkedIn, Adobe)
- Security research community
- Password generation research and best practices

---

<p align="center">
  <b>⭐ Star this repo if you find it useful!</b><br>
  <sub>Made with 🔥 by fxrhan</sub>
</p>
