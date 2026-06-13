@echo off
echo ============================================
echo  IMAPSync GUI - EXE Build Script
echo ============================================
echo.

:: ── Python-Befehl ermitteln ──────────────────
set PYTHON_CMD=

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :found
)

python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :found
)

echo [FEHLER] Python wurde nicht im PATH gefunden!
echo.
echo Loesungsmoeglichkeiten:
echo  1. Python neu installieren und dabei "Add Python to PATH" anhaeken
echo  2. Python manuell zum PATH hinzufuegen:
echo     Systemsteuerung ^> Umgebungsvariablen ^> PATH ^> Python-Ordner eintragen
echo     z.B. C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\
echo  3. Alternativ: imapsync_gui.py direkt per Doppelklick starten
echo     (falls .py-Dateien mit Python verknuepft sind)
echo.
pause
exit /b 1

:found
echo [OK] Python gefunden: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: ── PyInstaller prüfen / installieren ────────
echo [1/3] Pruefe PyInstaller...
%PYTHON_CMD% -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nicht gefunden - wird installiert...
    %PYTHON_CMD% -m pip install pyinstaller
    if errorlevel 1 (
        echo [FEHLER] PyInstaller konnte nicht installiert werden.
        echo Bitte manuell ausfuehren: %PYTHON_CMD% -m pip install pyinstaller
        pause
        exit /b 1
    )
) else (
    echo [OK] PyInstaller ist bereits installiert.
)

echo.
echo [2/3] Vorbereitung: laufende Instanz beenden (falls aktiv)...
taskkill /F /IM IMAPSync_GUI.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Alte EXE manuell loeschen, damit PyInstaller keinen PermissionError bekommt
if exist "dist\IMAPSync_GUI.exe" (
    del /F /Q "dist\IMAPSync_GUI.exe" >nul 2>&1
    if exist "dist\IMAPSync_GUI.exe" (
        echo.
        echo [FEHLER] dist\IMAPSync_GUI.exe ist gesperrt und kann nicht geloescht werden.
        echo Bitte schliessen Sie die Anwendung und alle Virenscanner-Quarantaenen,
        echo dann starten Sie dieses Script erneut.
        pause
        exit /b 1
    )
)

echo [2/3] Erstelle EXE (kann 1-2 Minuten dauern)...
%PYTHON_CMD% -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "IMAPSync_GUI" ^
    imapsync_gui.py

if errorlevel 1 (
    echo.
    echo [FEHLER] EXE-Erstellung fehlgeschlagen.
    echo Haeufige Ursachen:
    echo  - EXE wird noch verwendet oder ist durch Virenscanner gesperrt
    echo  - Antivirus: Ausnahme fuer diesen Ordner hinzufuegen
    echo  - Alternativ direkt ausfuehren: %PYTHON_CMD% imapsync_gui.py
    pause
    exit /b 1
)

echo.
echo [3/3] Fertig!
echo ============================================
echo  EXE erstellt: dist\IMAPSync_GUI.exe
echo ============================================
echo.
pause
