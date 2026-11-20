# Password Checker

import re
import tkinter as tk
from tkinter import ttk


COMMON_PASSWORDS = {
    "password",
    "password1",
    "123456",
    "12345678",
    "123456789",
    "qwerty",
    "abc123",
    "admin",
    "letmein",
    "welcome",
    "iloveyou",
    "012468",
    "013579",
}


def has_sequence(password):
    lowered = password.lower()
    sequences = (
        "abcdefghijklmnopqrstuvwxyz",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "0123456789",
    )

    for sequence in sequences:
        for index in range(len(sequence) - 2):
            chunk = sequence[index : index + 3]
            if chunk in lowered or chunk[::-1] in lowered:
                return True
    return False


def check_password_strength(password):
    score = 0
    issues = []
    positives = []
    is_common_password = password.lower() in COMMON_PASSWORDS

    if len(password) >= 12:
        score += 30
        positives.append("Good length")
    elif len(password) >= 8:
        score += 15
        issues.append("Use at least 12 characters")
    else:
        issues.append("Use at least 8 characters")

    checks = [
        (r"[a-z]", "lowercase letters"),
        (r"[A-Z]", "uppercase letters"),
        (r"\d", "numbers"),
        (r"[^A-Za-z0-9]", "symbols"),
    ]

    variety_count = 0
    for pattern, label in checks:
        if re.search(pattern, password):
            variety_count += 1
            positives.append(f"Includes {label}")
        else:
            issues.append(f"Add {label}")

    score += variety_count * 15

    if is_common_password:
        score -= 45
        issues.append("Avoid common passwords")

    if re.search(r"(.)\1\1", password):
        score -= 15
        issues.append("Avoid repeating the same character")

    if has_sequence(password):
        score -= 15
        issues.append("Avoid keyboard or alphabetic sequences")

    if re.search(r"(password|admin|login)", password, re.IGNORECASE):
        score -= 15
        issues.append("Avoid obvious words like password or admin")

    score = max(0, min(100, score))

    suitable = score >= 75 and len(password) >= 12 and variety_count >= 3 and not is_common_password

    if score >= 85:
        label = "Very strong"
    elif score >= 70:
        label = "Strong"
    elif score >= 45:
        label = "Medium"
    else:
        label = "Weak"

    return score, label, suitable, positives, issues


class PasswordCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Strength Checker")
        self.geometry("520x520")
        self.minsize(460, 480)

        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar(value=False)

        self.configure(bg="#f5f7fb")
        self.build_ui()
        self.password_var.trace_add("write", lambda *_: self.update_result())
        self.update_result()

    def build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f5f7fb", foreground="#18202f", font=("Helvetica", 12))
        style.configure("Title.TLabel", font=("Helvetica", 22, "bold"))
        style.configure("Muted.TLabel", foreground="#5f6b7a")
        style.configure("Result.TLabel", font=("Helvetica", 18, "bold"))
        style.configure("Suitable.TLabel", font=("Helvetica", 13, "bold"))
        style.configure("TCheckbutton", background="#ffffff", foreground="#18202f", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11))

        outer = ttk.Frame(self, padding=24)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Password Strength Checker", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Enter a password to check whether it is suitable for use.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 20))

        card = ttk.Frame(outer, style="Card.TFrame", padding=18)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Password", background="#ffffff").pack(anchor="w")

        entry_row = ttk.Frame(card, style="Card.TFrame")
        entry_row.pack(fill="x", pady=(6, 10))

        self.password_entry = ttk.Entry(entry_row, textvariable=self.password_var, show="*", font=("Helvetica", 14))
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.password_entry.focus()

        ttk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        ).pack(anchor="w", pady=(0, 16))

        self.score_bar = ttk.Progressbar(card, maximum=100, value=0)
        self.score_bar.pack(fill="x", pady=(0, 12))

        self.result_label = ttk.Label(card, text="", style="Result.TLabel", background="#ffffff")
        self.result_label.pack(anchor="w")

        self.suitable_label = ttk.Label(card, text="", style="Suitable.TLabel", background="#ffffff")
        self.suitable_label.pack(anchor="w", pady=(4, 18))

        self.details = tk.Text(
            card,
            height=10,
            wrap="word",
            borderwidth=0,
            bg="#f8fafc",
            fg="#18202f",
            font=("Helvetica", 11),
            padx=12,
            pady=12,
        )
        self.details.pack(fill="both", expand=True)
        self.details.configure(state="disabled")

        ttk.Button(card, text="Clear", command=self.clear_password).pack(anchor="e", pady=(14, 0))

    def toggle_password_visibility(self):
        self.password_entry.configure(show="" if self.show_password_var.get() else "*")

    def clear_password(self):
        self.password_var.set("")
        self.password_entry.focus()

    def update_result(self):
        password = self.password_var.get()

        if not password:
            score, label, suitable, positives, issues = 0, "No password entered", False, [], [
                "Type a password to begin the check."
            ]
        else:
            score, label, suitable, positives, issues = check_password_strength(password)

        self.score_bar.configure(value=score)
        self.result_label.configure(text=f"{label} ({score}/100)")

        if suitable:
            self.suitable_label.configure(text="Suitable for use", foreground="#167348")
        else:
            self.suitable_label.configure(text="Not suitable yet", foreground="#b42318")

        lines = []
        if positives:
            lines.append("Good:")
            lines.extend(f"  - {item}" for item in positives)

        if issues:
            if lines:
                lines.append("")
            lines.append("Improve:")
            lines.extend(f"  - {item}" for item in dict.fromkeys(issues))

        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert("1.0", "\n".join(lines))
        self.details.configure(state="disabled")


if __name__ == "__main__":
    app = PasswordCheckerApp()
    app.mainloop()
