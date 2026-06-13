# IMAPSync GUI

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

🇩🇪 [Deutsch](#deutsch) · 🇬🇧 [English](#english)

---

<a name="deutsch"></a>
## 🇩🇪 Deutsch

**Eine grafische Windows-Oberfläche für [imapsync](https://imapsync.lamiral.info)**

### Hintergrund

Dieses Tool entstand im Rahmen eines Umzugs von **Microsoft Office 365** zu **Mailbox.org**.
imapsync ist das ideale Werkzeug für solche Migrationen – hat aber keine grafische Oberfläche.
IMAPSync GUI schließt diese Lücke.

Entstehungsgeschichte und Anleitung im Blog:
**[lex-blog.de](https://lex-blog.de)**

### Features

- Grafische Eingabemaske für alle relevanten imapsync-Parameter
- Ordnerbaum direkt vom Quellserver laden (IMAP)
- Ordner gezielt ein- oder ausschließen
- Häufig benötigte Flags als Checkboxen
- Konfigurationen als Profile speichern und laden
- Automatische `.bat`-Erstellung und Direktstart aus der GUI
- Echtzeit-Log mit farbiger Ausgabe
- Mehrsprachig: 🇩🇪 Deutsch, 🇬🇧 English, 🇪🇸 Español, 🇫🇷 Français, 🇮🇹 Italiano
- Eigenständige `.exe` – kein Python erforderlich

### Voraussetzungen

| Für | Anforderung |
|---|---|
| `.py` direkt starten | Python 3.9+, tkinter (in Windows-Python enthalten) |
| Fertige `.exe` | Keine – vollständig eigenständig |
| imapsync selbst | Separat von [imapsync.lamiral.info](https://imapsync.lamiral.info) @gilleslamiral @imapsync beziehen |

### Schnellstart

**Als Python-Skript:**
```bash
python imapsync_gui.py
```

**Als EXE bauen:**
```
build_exe_v0_3_0.bat
```
Das Skript installiert PyInstaller bei Bedarf automatisch und erstellt `dist\IMAPSync_GUI.exe`.

### Projektstruktur

```
imapsync-gui/
├── imapsync_gui.py          # Hauptanwendung
├── IMAPSync_GUI.spec         # PyInstaller-Konfiguration
├── build_exe_v0_3_0.bat      # Build-Skript
├── about.json                # Optional: Kontaktdaten überschreiben
├── logo_to_base64.py         # Hilfsskript: Logo in Quellcode einbetten
├── LICENSE                   # GNU GPL v3
└── README.md                 # Diese Datei
```

### Unterstützung

Wenn IMAPSync GUI dir Zeit gespart hat – über einen Kaffee freue ich mich 😊

[![Kaffee spendieren](https://img.shields.io/badge/☕_Kaffee_spendieren-Stripe-635BFF?style=for-the-badge)](https://buy.stripe.com/14A9ATdSsbQ6aNE8ludMI0l)

---

### Lizenz

Copyright © 2026 **Steve Rückwardt** – [lex-blog.de](https://lex-blog.de) | [info@lex-blog.de](mailto:info@lex-blog.de)

Dieses Projekt steht unter der **GNU General Public License v3.0**.
Du darfst den Code verwenden, verändern und weitergeben – aber nur unter denselben
Lizenzbedingungen und mit Nennung des Urhebers. Abgeleitete Werke müssen ebenfalls
als Open Source veröffentlicht werden.

Vollständiger Lizenztext: [LICENSE](LICENSE) · [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0)

### Hinweis zu imapsync

IMAPSync GUI ist ein unabhängiges Drittanbieter-Projekt und steht in keiner
offiziellen Verbindung zum imapsync-Projekt von Gilles Lamiral.
imapsync selbst unterliegt eigenen Lizenzbedingungen.

---

<a name="english"></a>
## 🇬🇧 English

**A graphical Windows interface for [imapsync](https://imapsync.lamiral.info)**

### Background

This tool was created during a migration from **Microsoft Office 365** to **Mailbox.org**.
imapsync is the go-to tool for such migrations – but it has no graphical interface.
IMAPSync GUI fills that gap.

Full story and instructions on the blog:
**[lex-blog.de](https://lex-blog.de)**

### Features

- Graphical input form for all relevant imapsync parameters
- Load folder tree directly from the source server (IMAP)
- Include or exclude specific folders
- Frequently used flags available as checkboxes
- Save and reload configurations as profiles
- Automatic `.bat` file generation and direct launch from the GUI
- Real-time log output with colour highlighting
- Multilingual: 🇩🇪 Deutsch, 🇬🇧 English, 🇪🇸 Español, 🇫🇷 Français, 🇮🇹 Italiano
- Standalone `.exe` – no Python installation required

### Requirements

| For | Requirement |
|---|---|
| Run `.py` directly | Python 3.9+, tkinter (included in Windows Python) |
| Ready-to-use `.exe` | None – fully self-contained |
| imapsync itself | Obtain separately from [imapsync.lamiral.info](https://imapsync.lamiral.info) @gilleslamiral @imapsync |

### Quick Start

**Run as Python script:**
```bash
python imapsync_gui.py
```

**Build the EXE:**
```
build_exe_v0_3_0.bat
```
The script installs PyInstaller automatically if needed and produces `dist\IMAPSync_GUI.exe`.

### Project Structure

```
imapsync-gui/
├── imapsync_gui.py          # Main application
├── IMAPSync_GUI.spec         # PyInstaller configuration
├── build_exe_v0_3_0.bat      # Build script
├── about.json                # Optional: override contact details without rebuild
├── logo_to_base64.py         # Helper: embed a new logo into the source code
├── LICENSE                   # GNU GPL v3
└── README.md                 # This file
```

### Support this project

If IMAPSync GUI saved you some time, a coffee is always appreciated 🙂

[![Buy me a coffee](https://img.shields.io/badge/☕_Buy_me_a_coffee-Stripe-635BFF?style=for-the-badge)](https://buy.stripe.com/14A9ATdSsbQ6aNE8ludMI0l)

---

### License

Copyright © 2026 **Steve Rückwardt** – [lex-blog.de](https://lex-blog.de) | [info@lex-blog.de](mailto:info@lex-blog.de)

This project is licensed under the **GNU General Public License v3.0**.
You are free to use, modify, and redistribute this code – but only under the same
license terms and with attribution to the original author. Derivative works must
also be released as open source.

Full license text: [LICENSE](LICENSE) · [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0)

### Note on imapsync

IMAPSync GUI is an independent third-party project and is not officially affiliated
with the imapsync project by Gilles Lamiral.
imapsync itself is subject to its own license terms.
