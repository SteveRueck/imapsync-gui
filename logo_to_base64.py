"""
logo_to_base64.py
─────────────────
Konvertiert dein Logo-Bild in einen Base64-String und trägt ihn
automatisch in about.json ein.

Verwendung:
    python logo_to_base64.py mein_logo.png

Unterstützte Formate: PNG, JPG, GIF, BMP, ICO
Das Skript legt about.json an (oder aktualisiert es), wenn es
im selben Verzeichnis liegt.

Empfehlung für das Logo:
  - Format:    PNG mit transparentem Hintergrund
  - Größe:     ca. 400 × 160 px (wird in der GUI auf max. 200 × 80 px skaliert)
"""

import base64, json, os, sys

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python logo_to_base64.py <Bilddatei>")
        print("Beispiel:   python logo_to_base64.py logo.png")
        sys.exit(1)

    img_path = sys.argv[1]
    if not os.path.isfile(img_path):
        print(f"[FEHLER] Datei nicht gefunden: {img_path}")
        sys.exit(1)

    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    about_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "about.json")

    # Vorhandene about.json laden oder neue anlegen
    if os.path.isfile(about_path):
        with open(about_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "name":    "Dein Name",
            "email":   "deine@email.de",
            "blog":    "https://deinblog.de",
            "version": "0.3.0"
        }

    data["logo_b64"] = b64

    with open(about_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Logo eingetragen in: {about_path}")
    print(f"     Bildgröße: {os.path.getsize(img_path) / 1024:.1f} KB")
    print(f"     Base64-Länge: {len(b64)} Zeichen")
    print()
    print("Nächste Schritte:")
    print("  1. about.json mit deinen Daten (Name, E-Mail, Blog) befüllen")
    print("  2. build_exe_v0_3_0.bat ausführen – die EXE liest about.json beim Start")

if __name__ == "__main__":
    main()
