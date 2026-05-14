import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "patients.json"


def load_patients():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_patients(patients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=2)


class VetClinicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vet Clinic")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg="#F5F5F7")

        self.patients = load_patients()
        self.filtered_ids = []
        self.selected_id = None

        self._setup_style()
        self._build_ui()
        self.refresh_list()

    # ---------- UI ----------
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("App.TFrame", background="#F5F5F7")
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("Title.TLabel", background="#F5F5F7", foreground="#1D1D1F", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background="#F5F5F7", foreground="#6E6E73", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#FFFFFF", foreground="#1D1D1F", font=("Segoe UI", 12, "bold"))
        style.configure("TLabel", background="#FFFFFF", foreground="#1D1D1F", font=("Segoe UI", 10))
        style.configure("TEntry", padding=6, fieldbackground="#FFFFFF")
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        style.map("Primary.TButton", background=[("active", "#0077ED"), ("!active", "#0A84FF")], foreground=[("!disabled", "white")])

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame", padding=16)
        root.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="ВетКартотека", style="Title.TLabel").pack(side="left")
        self.total_label = ttk.Label(header, text="", style="Subtitle.TLabel")
        self.total_label.pack(side="right")

        # Main area
        main = ttk.Frame(root, style="App.TFrame")
        main.pack(fill="both", expand=True)

        # Left card
        left_card = ttk.Frame(main, style="Card.TFrame", padding=14)
        left_card.pack(side="left", fill="y", padx=(0, 12))
        left_card.configure(width=340)

        ttk.Label(left_card, text="Пациенты", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_list())
        search_entry = ttk.Entry(left_card, textvariable=self.search_var)
        search_entry.pack(fill="x", pady=(0, 10))
        search_entry.insert(0, "")

        self.listbox = tk.Listbox(
            left_card,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#1D1D1F",
            selectbackground="#DCEBFF",
            selectforeground="#1D1D1F",
            relief="flat",
            borderwidth=0,
            activestyle="none",
            highlightthickness=1,
            highlightbackground="#E5E5EA",
            highlightcolor="#0A84FF",
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        btn_new = ttk.Button(left_card, text="Новый пациент", style="Primary.TButton", command=self.new_patient)
        btn_new.pack(fill="x", pady=(10, 0))

        # Right card (form)
        right_card = ttk.Frame(main, style="Card.TFrame", padding=18)
        right_card.pack(side="left", fill="both", expand=True)

        self.form_title = ttk.Label(right_card, text="Карточка пациента", style="CardTitle.TLabel")
        self.form_title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        self.fields = {}
        field_config = [
            ("Кличка", "name"),
            ("Вид", "species"),
            ("Порода", "breed"),
            ("Дата рождения", "birth"),
            ("Пол", "sex"),
            ("Окрас", "color"),
            ("Чип/Клеймо", "chip"),
            ("Владелец", "owner"),
            ("Телефон", "phone"),
            ("E-mail", "email"),
            ("Адрес", "address"),
            ("Вакцинация", "vaccine"),
            ("Дегельминтизация", "deworm"),
            ("Аллергии", "allergies"),
            ("Хрон. болезни", "chronic"),
        ]

        row = 1
        for i, (label, key) in enumerate(field_config):
            col = 0 if i % 2 == 0 else 2
            if i % 2 == 0 and i != 0:
                row += 1

            ttk.Label(right_card, text=label).grid(row=row, column=col, sticky="w", padx=(0, 8), pady=6)
            var = tk.StringVar()
            entry = ttk.Entry(right_card, textvariable=var, width=28)
            entry.grid(row=row, column=col + 1, sticky="ew", pady=6)
            self.fields[key] = var

        row += 1
        ttk.Label(right_card, text="Примечания").grid(row=row, column=0, sticky="nw", padx=(0, 8), pady=6)
        self.notes = tk.Text(
            right_card,
            height=5,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#1D1D1F",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E5E5EA",
            highlightcolor="#0A84FF",
            wrap="word",
        )
        self.notes.grid(row=row, column=1, columnspan=3, sticky="nsew", pady=6)

        row += 1
        self.created_label = ttk.Label(right_card, text="", background="#FFFFFF", foreground="#6E6E73")
        self.created_label.grid(row=row, column=0, columnspan=4, sticky="e", pady=(2, 10))

        row += 1
        btn_bar = ttk.Frame(right_card, style="Card.TFrame")
        btn_bar.grid(row=row, column=0, columnspan=4, sticky="w")

        ttk.Button(btn_bar, text="Сохранить", style="Primary.TButton", command=self.save_patient).pack(side="left", padx=(0, 8))
        ttk.Button(btn_bar, text="Очистить", command=self.clear_form).pack(side="left", padx=(0, 8))
        ttk.Button(btn_bar, text="Удалить", command=self.delete_patient).pack(side="left")

        # Grid behavior
        right_card.grid_columnconfigure(1, weight=1)
        right_card.grid_columnconfigure(3, weight=1)
        right_card.grid_rowconfigure(row - 2, weight=1)

    # ---------- Logic ----------
    def refresh_list(self):
        query = self.search_var.get().strip().lower()
        self.listbox.delete(0, tk.END)
        self.filtered_ids = []

        for p in self.patients:
            name = p.get("name", "")
            owner = p.get("owner", "")
            species = p.get("species", "")

            text = f"{name} — {owner}" if owner else name
            hay = f"{name} {owner} {species}".lower()

            if query and query not in hay:
                continue

            self.listbox.insert(tk.END, text)
            self.filtered_ids.append(p["id"])

        self.total_label.config(text=f"Пациентов: {len(self.patients)}")

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        patient_id = self.filtered_ids[sel[0]]
        patient = next((p for p in self.patients if p["id"] == patient_id), None)
        if not patient:
            return

        self.selected_id = patient_id
        self.fill_form(patient)
        self.form_title.config(text=f"Пациент: {patient.get('name', '')}")

    def fill_form(self, patient):
        for key, var in self.fields.items():
            var.set(patient.get(key, ""))
        self.notes.delete("1.0", tk.END)
        self.notes.insert("1.0", patient.get("notes", ""))
        created = patient.get("created", "")
        self.created_label.config(text=f"Создано: {created}" if created else "")

    def collect_form(self):
        data = {k: v.get().strip() for k, v in self.fields.items()}
        data["notes"] = self.notes.get("1.0", "end-1c").strip()
        return data

    def clear_form(self):
        for var in self.fields.values():
            var.set("")
        self.notes.delete("1.0", tk.END)
        self.created_label.config(text="")
        self.form_title.config(text="Карточка пациента")

    def new_patient(self):
        self.selected_id = None
        self.listbox.selection_clear(0, tk.END)
        self.clear_form()

    def save_patient(self):
        data = self.collect_form()

        if not data["name"]:
            messagebox.showwarning("Ошибка", "Введите кличку животного.")
            return
        if not data["owner"]:
            messagebox.showwarning("Ошибка", "Введите владельца.")
            return

        if self.selected_id is None:
            data["id"] = datetime.now().strftime("%Y%m%d%H%M%S%f")
            data["created"] = datetime.now().strftime("%d.%m.%Y %H:%M")
            self.patients.append(data)
            self.selected_id = data["id"]
        else:
            for i, p in enumerate(self.patients):
                if p["id"] == self.selected_id:
                    data["id"] = p["id"]
                    data["created"] = p.get("created", "")
                    self.patients[i] = data
                    break

        save_patients(self.patients)
        self.refresh_list()
        self.form_title.config(text=f"Пациент: {data['name']}")
        messagebox.showinfo("Готово", "Карточка сохранена.")

    def delete_patient(self):
        if self.selected_id is None:
            messagebox.showinfo("Внимание", "Сначала выберите пациента.")
            return

        patient = next((p for p in self.patients if p["id"] == self.selected_id), None)
        if not patient:
            return

        if not messagebox.askyesno("Подтверждение", f"Удалить «{patient.get('name', 'Пациент')}»?"):
            return

        self.patients = [p for p in self.patients if p["id"] != self.selected_id]
        save_patients(self.patients)
        self.selected_id = None
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Готово", "Карточка удалена.")


if __name__ == "__main__":
    app = VetClinicApp()
    app.mainloop()