# Password Strength Checker

A small desktop app, written in Python with Tkinter, that scores a password as you type and tells you whether it is suitable for use. It also lists what is good about the password and what to improve.

Everything runs locally. The password is never sent anywhere or saved.

## Features

- Live feedback: the score, label and suggestions update with every keystroke
- Score from 0 to 100 shown on a progress bar
- Strength label: Weak, Medium, Strong or Very strong
- A clear "Suitable for use" / "Not suitable yet" verdict
- "Good" and "Improve" lists explaining the result
- Show/hide password toggle and a Clear button

## Requirements

- Python 3.8 or newer
- Tkinter (included with most Python installs; on some Linux systems install it with `sudo apt install python3-tk`)

No third-party packages are needed.

## Usage

```bash
git clone https://github.com/Firestorm101456/password-checker.git
cd password-checker
python password_checker.py
```

Replace `password_checker.py` with the name of the main script in the repo if it differs.

## How scoring works

| Check | Effect on score |
| --- | --- |
| Length of 12 or more characters | +30 |
| Length of 8 to 11 characters | +15 |
| Each character type present (lowercase, uppercase, numbers, symbols) | +15 each (up to +60) |
| Password is on the common-passwords list | -45 |
| Same character repeated 3 or more times in a row | -15 |
| Keyboard or alphabetic/numeric sequence (e.g. `abc`, `qwe`, `789`, also reversed) | -15 |
| Contains an obvious word (`password`, `admin`, `login`, `user`, `name`) | -15 |

The final score is limited to the range 0 to 100.

### Strength labels

| Score | Label |
| --- | --- |
| 85 and above | Very strong |
| 70 to 84 | Strong |
| 45 to 69 | Medium |
| Below 45 | Weak |

### "Suitable for use"

A password is marked suitable only if all of these are true:

- Score is 75 or higher
- Length is at least 12 characters
- At least 3 of the 4 character types are used
- It is not on the common-passwords list

## Project structure

```
password-checker/
├── password_checker.py   # scoring logic and Tkinter interface
└── README.md
```

The code has two main parts:

- `check_password_strength(password)` returns the score, label, suitability, positives and issues
- `PasswordCheckerApp` is the Tkinter window that displays the results

## Limitations

- The common-passwords list is short and built in; it is not a full breach database
- The checker uses rules of thumb and cannot guarantee a password is safe. Use a password manager and unique passwords for every account.

## License

Add a license of your choice (for example MIT) here.
