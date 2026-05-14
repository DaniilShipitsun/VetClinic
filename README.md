# 🐾 ВетКартотека — Vet Clinic Patient Manager (Python GUI)

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-FF6F00)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-Educational%20Use-10B981)](LICENSE)

ВетКартотека is a desktop application for managing patient records in a veterinary clinic with a modern dark-themed interface.
It is built with **Python** and **Tkinter** using fully custom widgets — no third-party UI libraries required.

---

## 📋 Table of Contents

- [✨ Highlights](#-highlights)
- [🚀 Features](#-features)
- [🔮 How It Works](#-how-it-works)
- [🗂 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚡ Quick Start](#-quick-start)
- [📄 License](#-license)

---

## ✨ Highlights

- Modern dark-themed desktop interface with purple accent colors
- Real-time search by pet name or owner name
- Filter patients by species with one click
- Full patient card with medical information
- Data stored locally in a human-readable JSON file

---

## 🚀 Features

### 🐾 Patient Card
- Add, edit and delete patient records
- Fields: name, species, breed, birth date, sex, color, microchip number
- Auto-generated unique ID and creation timestamp

### 👤 Owner Information
- Fields: full name, phone, e-mail, address
- Name and pet name are required — validated before saving

### 💉 Medical Information
- Vaccination and deworming dates
- Allergy and chronic disease notes
- Free-form notes field (multiline)

### 🔍 Search & Filter
- Instant search by pet name or owner name via `StringVar.trace`
- Species filter buttons: All / Dog / Cat / Bird / Rodent / Other
- Both filters work simultaneously

### 🎨 Custom Widgets
- `RoundedFrame` — card container with smooth corners drawn on Canvas
- `ModernEntry` — input field with placeholder text and focus animation
- `PurpleButton` — interactive button with hover effect and three styles: `primary`, `danger`, `ghost`

### 💾 Data Storage
- Saves to `patients.json` with full Cyrillic support (`ensure_ascii=False`)
- Loads automatically on startup; creates fresh list if file doesn't exist
- Human-readable formatting with `indent=2`

---

## 🔮 How It Works

1. On launch, `load_patients()` reads `patients.json` from the working directory
2. The left panel shows the patient list with species icons (🐶 🐱 🐦 🐭)
3. Selecting a patient fills the right-panel form via `_fill_form()`
4. On save, `_collect_form()` gathers all field values, validates required fields, then calls `save_patients()`
5. Search input is tracked via `StringVar.trace("w", ...)` — list refreshes on every keystroke
6. Toast notifications appear for 2 seconds after save or delete via `after(2000, toast.destroy)`

---

## 🗂 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| tkinter | GUI framework (standard library) |
| json | Data serialization (standard library) |
| os | File existence check (standard library) |
| datetime | Auto-generated record ID and creation date |
| re | Input validation (phone, e-mail) |

---

## 📁 Project Structure

```
vet_clinic/
├── vet_clinic.py      # Main application (single-file)
├── patients.json      # Auto-created data file
└── README.md
```

---

## ⚡ Quick Start

**Requirements:** Python 3.x (tkinter is included in the standard library)

```bash
# Clone the repository
git clone https://github.com/your-username/vet-kartoteka.git
cd vet-kartoteka

# Run the application
python vet_clinic.py
```

No additional packages to install — everything used is part of Python's standard library.

---

## 📄 License

This project was created for educational purposes as part of a coursework assignment.
Free to use and modify for learning.
