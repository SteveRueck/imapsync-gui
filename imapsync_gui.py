"""
IMAPSync GUI – Grafische Windows-Oberfläche für imapsync
Version 0.3.0

Copyright (C) 2026  Steve Rückwardt <info@lex-blog.de>
https://lex-blog.de

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json, os, subprocess, threading, imaplib, re, base64, sys
from urllib.request import urlopen
from urllib.error import URLError

# ═══════════════════════════════════════════════════════════════
#  FARBEN
# ═══════════════════════════════════════════════════════════════
BG_MAIN   = "#1e1e2e"
BG_CARD   = "#2a2a3e"
BG_INPUT  = "#313145"
FG_TEXT   = "#cdd6f4"
FG_LABEL  = "#a6adc8"
ACCENT    = "#89b4fa"
ACCENT_DK = "#6c9bd9"
SUCCESS   = "#a6e3a1"
WARNING   = "#f9e2af"
DANGER    = "#f38ba8"
BORDER    = "#45475a"
RADIUS    = 12
TAB_R     = 9

# ═══════════════════════════════════════════════════════════════
#  ÜBERSETZUNGEN
# ═══════════════════════════════════════════════════════════════
LANGS = {"Deutsch": "de", "English": "en", "Español": "es",
         "Français": "fr", "Italiano": "it"}

T = {
"de": {
    "app_title":"IMAPSync GUI","subtitle":"Windows-Oberfläche für imapsync",
    "tab_config":"⚙️  Konfiguration","tab_folders":"📁  Ordner",
    "tab_options":"🔧  Optionen","tab_profiles":"💾  Profile",
    "tab_run":"▶  Ausführung","tab_settings":"🌐  Einstellungen",
    "exe_section":"IMAPSync Executable","browse":"Durchsuchen…",
    "src":"📤  Quellserver","dst":"📥  Zielserver",
    "hostname":"Hostname / IP:","port":"Port:","username":"Benutzername:",
    "password":"Passwort:","ssl":"SSL","tls":"STARTTLS",
    "dry_run":"🧪  Testlauf (--dry) – nichts wird tatsächlich kopiert",
    "folder_title":"Ordner-Filter (Include / Exclude)",
    "fetch_btn":"📋  Ordner vom Quellserver abrufen",
    "mode_inc":"Nur diese Ordner synchronisieren (--include)",
    "mode_exc":"Diese Ordner ausschließen (--exclude)",
    "sel_all":"Alle auswählen","desel_all":"Alle abwählen",
    "fetching":"Verbinde mit Quellserver…","fetch_ok":"Ordner geladen.",
    "fetch_err":"Fehler beim Abrufen","no_src_host":"Bitte zuerst Quellserver konfigurieren.",
    "folder_hint":"Keine Ordner ausgewählt = alle Ordner werden synchronisiert.",
    "sync_behavior":"Sync-Verhalten","more_opts":"Weitere Optionen",
    "extra_args":"Zusätzliche Argumente (Freitext)",
    "extra_hint":"z.B.  --maxage 30  --regexflag 's/\\\\Seen//'",
    "profiles_title":"Gespeicherte Profile","save_p":"💾  Speichern",
    "load_p":"📂  Laden","del_p":"🗑  Löschen",
    "p_name":"Profilname:","p_save_btn":"Speichern",
    "col_src":"Quellserver","col_dst":"Zielserver","col_usr":"Benutzer",
    "no_profile":"Bitte ein Profil auswählen.",
    "confirm_del":"Profil wirklich löschen?",
    "gen_bat":"🔍  Befehl generieren & .bat erstellen",
    "run_bat":"▶  .bat ausführen","copy_clip":"📋  Kopieren",
    "clear_log":"🗑  Log leeren","stop":"⏹  Stopp",
    "cmd_prev":"Generierter Befehl","log_title":"Log-Ausgabe",
    "st_ready":"Bereit.","st_run":"Läuft…","st_done":"Abgeschlossen ✓",
    "st_stop":"Gestoppt","st_err":"Fehler",
    "st_saved":"BAT gespeichert","st_copied":"In Zwischenablage kopiert ✓",
    "err_fields":"Bitte Quell- und Zielserver angeben.",
    "err_bat_nf":"Bitte zuerst den Befehl generieren.",
    "err_bat_save":".bat konnte nicht gespeichert werden",
    "msg_bat_saved":"✅  .bat gespeichert: ","msg_run_start":"▶  Starte: ",
    "msg_done":"✅  IMAPSync abgeschlossen (Exit 0)",
    "msg_exit":"⚠️  Exit-Code: ","msg_stopped":"⏹  Prozess gestoppt.",
    "msg_err":"❌  Fehler: ",
    "settings_title":"Einstellungen","lang_label":"Sprache:",
    "bat_path_label":"Pfad der .bat-Datei:","choose_bat":"Pfad wählen…",
    "restart_hint":"Sprache wird sofort angewendet.",
    "o_delete2":"E-Mails auf Ziel löschen die auf Quelle fehlen",
    "o_delete2dup":"Duplikate auf Ziel löschen",
    "o_subscribeall":"Alle Ordner abonnieren",
    "o_automap":"Ordner automatisch mappen",
    "o_nofldrsz":"Ordnergrößen nicht berechnen (schneller)",
    "o_justfolders":"Nur Ordner anlegen, keine E-Mails",
    "o_useuid":"UIDs für Abgleich verwenden",
    "o_noskipdup":"Duplikate nicht überspringen",
    "o_nomodver":"Modulversionen nicht ausgeben",
    "o_norelck":"Keine Update-Prüfung",
    "o_noauthmd5":"MD5-Auth deaktivieren",
    "o_notls":"TLS vollständig deaktivieren",
    "o_nosyncacls":"ACLs nicht synchronisieren",
    "o_expunge1":"Gelöschte auf Quelle bereinigen",
    "o_expunge2":"Gelöschte auf Ziel bereinigen",
    "tab_about":"(i)  Über",
    "about_title":"Über dieses Tool",
    "about_author":"Entwickler",
    "about_contact":"Kontakt",
    "about_blog":"Blog",
    "about_version":"Version",
    "about_desc":"IMAPSync GUI ist eine grafische Windows-Oberfläche für das Kommandozeilen-Tool imapsync. Entwickelt um E-Mail-Migrationen zwischen IMAP-Servern einfacher zu machen.",
    "about_open_mail":"E-Mail schreiben",
    "about_open_blog":"Blog öffnen",
    "about_imapsync":"IMAPSync-Projekt",
    "about_based_on":"Basiert auf:",
    "about_contact_title":"Kontakt",
},
"en": {
    "app_title":"IMAPSync GUI","subtitle":"Windows interface for imapsync",
    "tab_config":"⚙️  Configuration","tab_folders":"📁  Folders",
    "tab_options":"🔧  Options","tab_profiles":"💾  Profiles",
    "tab_run":"▶  Execution","tab_settings":"🌐  Settings",
    "exe_section":"IMAPSync Executable","browse":"Browse…",
    "src":"📤  Source Server","dst":"📥  Destination Server",
    "hostname":"Hostname / IP:","port":"Port:","username":"Username:",
    "password":"Password:","ssl":"SSL","tls":"STARTTLS",
    "dry_run":"🧪  Dry Run (--dry) – nothing is actually copied",
    "folder_title":"Folder Filter (Include / Exclude)",
    "fetch_btn":"📋  Fetch folders from source server",
    "mode_inc":"Sync only these folders (--include)",
    "mode_exc":"Exclude these folders (--exclude)",
    "sel_all":"Select all","desel_all":"Deselect all",
    "fetching":"Connecting to source server…","fetch_ok":"Folders loaded.",
    "fetch_err":"Error fetching folders","no_src_host":"Please configure source server first.",
    "folder_hint":"No folders selected = all folders will be synchronized.",
    "sync_behavior":"Sync Behavior","more_opts":"More Options",
    "extra_args":"Additional Arguments (free text)",
    "extra_hint":"e.g.  --maxage 30  --regexflag 's/\\\\Seen//'",
    "profiles_title":"Saved Profiles","save_p":"💾  Save",
    "load_p":"📂  Load","del_p":"🗑  Delete",
    "p_name":"Profile name:","p_save_btn":"Save",
    "col_src":"Source Server","col_dst":"Destination Server","col_usr":"User",
    "no_profile":"Please select a profile.",
    "confirm_del":"Really delete this profile?",
    "gen_bat":"🔍  Generate command & create .bat",
    "run_bat":"▶  Run .bat","copy_clip":"📋  Copy",
    "clear_log":"🗑  Clear Log","stop":"⏹  Stop",
    "cmd_prev":"Generated Command","log_title":"Log Output",
    "st_ready":"Ready.","st_run":"Running…","st_done":"Completed ✓",
    "st_stop":"Stopped","st_err":"Error",
    "st_saved":"BAT saved","st_copied":"Copied to clipboard ✓",
    "err_fields":"Please enter source and destination server.",
    "err_bat_nf":"Please generate the command first.",
    "err_bat_save":"Could not save .bat file",
    "msg_bat_saved":"✅  .bat saved: ","msg_run_start":"▶  Starting: ",
    "msg_done":"✅  IMAPSync completed (Exit 0)",
    "msg_exit":"⚠️  Exit code: ","msg_stopped":"⏹  Process stopped.",
    "msg_err":"❌  Error: ",
    "settings_title":"Settings","lang_label":"Language:",
    "bat_path_label":".bat file path:","choose_bat":"Choose path…",
    "restart_hint":"Language is applied immediately.",
    "o_delete2":"Delete on dest messages not on source",
    "o_delete2dup":"Delete duplicates on destination",
    "o_subscribeall":"Subscribe all folders",
    "o_automap":"Auto-map folders",
    "o_nofldrsz":"Skip folder size calculation (faster)",
    "o_justfolders":"Create folders only, no messages",
    "o_useuid":"Use UIDs for matching",
    "o_noskipdup":"Don't skip duplicates",
    "o_nomodver":"Don't print module versions",
    "o_norelck":"Skip release check",
    "o_noauthmd5":"Disable MD5 auth",
    "o_notls":"Fully disable TLS",
    "o_nosyncacls":"Don't sync ACLs",
    "o_expunge1":"Expunge deleted on source",
    "o_expunge2":"Expunge deleted on destination",
    "tab_about":"(i)  About",
    "about_title":"About this Tool",
    "about_author":"Developer",
    "about_contact":"Contact",
    "about_blog":"Blog",
    "about_version":"Version",
    "about_desc":"IMAPSync GUI is a graphical Windows interface for the command-line tool imapsync. Built to make e-mail migrations between IMAP servers easier.",
    "about_open_mail":"Send e-mail",
    "about_open_blog":"Open blog",
    "about_imapsync":"IMAPSync project",
    "about_based_on":"Based on:",
    "about_contact_title":"Contact",
},
"es": {
    "app_title":"IMAPSync GUI","subtitle":"Interfaz Windows para imapsync",
    "tab_config":"⚙️  Configuración","tab_folders":"📁  Carpetas",
    "tab_options":"🔧  Opciones","tab_profiles":"💾  Perfiles",
    "tab_run":"▶  Ejecución","tab_settings":"🌐  Ajustes",
    "exe_section":"Ejecutable IMAPSync","browse":"Examinar…",
    "src":"📤  Servidor origen","dst":"📥  Servidor destino",
    "hostname":"Nombre de host / IP:","port":"Puerto:","username":"Usuario:",
    "password":"Contraseña:","ssl":"SSL","tls":"STARTTLS",
    "dry_run":"🧪  Simulación (--dry) – no se copia nada realmente",
    "folder_title":"Filtro de carpetas (Incluir / Excluir)",
    "fetch_btn":"📋  Obtener carpetas del servidor origen",
    "mode_inc":"Sincronizar solo estas carpetas (--include)",
    "mode_exc":"Excluir estas carpetas (--exclude)",
    "sel_all":"Seleccionar todo","desel_all":"Deseleccionar todo",
    "fetching":"Conectando al servidor origen…","fetch_ok":"Carpetas cargadas.",
    "fetch_err":"Error al obtener carpetas","no_src_host":"Configure primero el servidor origen.",
    "folder_hint":"Sin carpetas seleccionadas = se sincronizan todas.",
    "sync_behavior":"Comportamiento de sincronización","more_opts":"Más opciones",
    "extra_args":"Argumentos adicionales (texto libre)","extra_hint":"p.ej.  --maxage 30",
    "profiles_title":"Perfiles guardados","save_p":"💾  Guardar",
    "load_p":"📂  Cargar","del_p":"🗑  Eliminar",
    "p_name":"Nombre del perfil:","p_save_btn":"Guardar",
    "col_src":"Servidor origen","col_dst":"Servidor destino","col_usr":"Usuario",
    "no_profile":"Seleccione un perfil.","confirm_del":"¿Eliminar este perfil?",
    "gen_bat":"🔍  Generar comando & crear .bat","run_bat":"▶  Ejecutar .bat",
    "copy_clip":"📋  Copiar","clear_log":"🗑  Limpiar log","stop":"⏹  Detener",
    "cmd_prev":"Comando generado","log_title":"Salida del log",
    "st_ready":"Listo.","st_run":"Ejecutando…","st_done":"Completado ✓",
    "st_stop":"Detenido","st_err":"Error","st_saved":"BAT guardado",
    "st_copied":"Copiado al portapapeles ✓",
    "err_fields":"Ingrese los servidores origen y destino.",
    "err_bat_nf":"Genere primero el comando.",
    "err_bat_save":"No se pudo guardar el archivo .bat",
    "msg_bat_saved":"✅  .bat guardado: ","msg_run_start":"▶  Iniciando: ",
    "msg_done":"✅  IMAPSync completado (Exit 0)",
    "msg_exit":"⚠️  Código de salida: ","msg_stopped":"⏹  Proceso detenido.",
    "msg_err":"❌  Error: ","settings_title":"Ajustes","lang_label":"Idioma:",
    "bat_path_label":"Ruta del archivo .bat:","choose_bat":"Elegir ruta…",
    "restart_hint":"El idioma se aplica de inmediato.",
    "o_delete2":"Eliminar en destino lo que no está en origen",
    "o_delete2dup":"Eliminar duplicados en destino",
    "o_subscribeall":"Suscribir todas las carpetas",
    "o_automap":"Mapear carpetas automáticamente",
    "o_nofldrsz":"No calcular tamaños de carpetas (más rápido)",
    "o_justfolders":"Solo crear carpetas, sin mensajes",
    "o_useuid":"Usar UIDs para comparación",
    "o_noskipdup":"No omitir duplicados","o_nomodver":"No mostrar versiones de módulos",
    "o_norelck":"Sin comprobación de actualizaciones","o_noauthmd5":"Desactivar auth MD5",
    "o_notls":"Deshabilitar TLS completamente","o_nosyncacls":"No sincronizar ACLs",
    "o_expunge1":"Limpiar eliminados en origen","o_expunge2":"Limpiar eliminados en destino",
    "tab_about":"(i)  Acerca de",
    "about_title":"Acerca de esta herramienta",
    "about_author":"Desarrollador",
    "about_contact":"Contacto",
    "about_blog":"Blog",
    "about_version":"Versión",
    "about_desc":"IMAPSync GUI es una interfaz gráfica de Windows para la herramienta de línea de comandos imapsync. Creada para facilitar las migraciones de correo entre servidores IMAP.",
    "about_open_mail":"Enviar correo",
    "about_open_blog":"Abrir blog",
    "about_imapsync":"Proyecto IMAPSync",
    "about_based_on":"Basado en:",
    "about_contact_title":"Contacto",
},
"fr": {
    "app_title":"IMAPSync GUI","subtitle":"Interface Windows pour imapsync",
    "tab_config":"⚙️  Configuration","tab_folders":"📁  Dossiers",
    "tab_options":"🔧  Options","tab_profiles":"💾  Profils",
    "tab_run":"▶  Exécution","tab_settings":"🌐  Paramètres",
    "exe_section":"Exécutable IMAPSync","browse":"Parcourir…",
    "src":"📤  Serveur source","dst":"📥  Serveur destination",
    "hostname":"Nom d'hôte / IP :","port":"Port :","username":"Nom d'utilisateur :",
    "password":"Mot de passe :","ssl":"SSL","tls":"STARTTLS",
    "dry_run":"🧪  Simulation (--dry) – rien n'est réellement copié",
    "folder_title":"Filtre de dossiers (Inclure / Exclure)",
    "fetch_btn":"📋  Récupérer les dossiers du serveur source",
    "mode_inc":"Synchroniser uniquement ces dossiers (--include)",
    "mode_exc":"Exclure ces dossiers (--exclude)",
    "sel_all":"Tout sélectionner","desel_all":"Tout désélectionner",
    "fetching":"Connexion au serveur source…","fetch_ok":"Dossiers chargés.",
    "fetch_err":"Erreur lors de la récupération","no_src_host":"Configurez d'abord le serveur source.",
    "folder_hint":"Aucun dossier sélectionné = tous les dossiers seront synchronisés.",
    "sync_behavior":"Comportement de synchronisation","more_opts":"Plus d'options",
    "extra_args":"Arguments supplémentaires (texte libre)","extra_hint":"ex.  --maxage 30",
    "profiles_title":"Profils enregistrés","save_p":"💾  Enregistrer",
    "load_p":"📂  Charger","del_p":"🗑  Supprimer",
    "p_name":"Nom du profil :","p_save_btn":"Enregistrer",
    "col_src":"Serveur source","col_dst":"Serveur destination","col_usr":"Utilisateur",
    "no_profile":"Veuillez sélectionner un profil.",
    "confirm_del":"Vraiment supprimer ce profil ?",
    "gen_bat":"🔍  Générer la commande & créer .bat","run_bat":"▶  Exécuter .bat",
    "copy_clip":"📋  Copier","clear_log":"🗑  Vider le log","stop":"⏹  Arrêter",
    "cmd_prev":"Commande générée","log_title":"Sortie du journal",
    "st_ready":"Prêt.","st_run":"En cours…","st_done":"Terminé ✓",
    "st_stop":"Arrêté","st_err":"Erreur","st_saved":"BAT enregistré",
    "st_copied":"Copié dans le presse-papiers ✓",
    "err_fields":"Veuillez entrer les serveurs source et destination.",
    "err_bat_nf":"Veuillez d'abord générer la commande.",
    "err_bat_save":"Impossible d'enregistrer le fichier .bat",
    "msg_bat_saved":"✅  .bat enregistré : ","msg_run_start":"▶  Démarrage : ",
    "msg_done":"✅  IMAPSync terminé (Exit 0)",
    "msg_exit":"⚠️  Code de sortie : ","msg_stopped":"⏹  Processus arrêté.",
    "msg_err":"❌  Erreur : ","settings_title":"Paramètres","lang_label":"Langue :",
    "bat_path_label":"Chemin du fichier .bat :","choose_bat":"Choisir le chemin…",
    "restart_hint":"La langue est appliquée immédiatement.",
    "o_delete2":"Supprimer sur dest ce qui manque sur source",
    "o_delete2dup":"Supprimer les doublons sur destination",
    "o_subscribeall":"S'abonner à tous les dossiers",
    "o_automap":"Mapper automatiquement les dossiers",
    "o_nofldrsz":"Ne pas calculer la taille des dossiers (plus rapide)",
    "o_justfolders":"Créer les dossiers uniquement, pas les messages",
    "o_useuid":"Utiliser les UIDs pour la comparaison",
    "o_noskipdup":"Ne pas ignorer les doublons","o_nomodver":"Ne pas afficher les versions des modules",
    "o_norelck":"Pas de vérification des mises à jour","o_noauthmd5":"Désactiver l'auth MD5",
    "o_notls":"Désactiver TLS complètement","o_nosyncacls":"Ne pas synchroniser les ACL",
    "o_expunge1":"Purger les supprimés sur source","o_expunge2":"Purger les supprimés sur destination",
    "tab_about":"(i)  À propos",
    "about_title":"À propos de cet outil",
    "about_author":"Développeur",
    "about_contact":"Contact",
    "about_blog":"Blog",
    "about_version":"Version",
    "about_desc":"IMAPSync GUI est une interface graphique Windows pour l'outil en ligne de commande imapsync. Conçue pour faciliter les migrations d'e-mails entre serveurs IMAP.",
    "about_open_mail":"Envoyer un e-mail",
    "about_open_blog":"Ouvrir le blog",
    "about_imapsync":"Projet IMAPSync",
    "about_based_on":"Basé sur :",
    "about_contact_title":"Contact",
},
"it": {
    "app_title":"IMAPSync GUI","subtitle":"Interfaccia Windows per imapsync",
    "tab_config":"⚙️  Configurazione","tab_folders":"📁  Cartelle",
    "tab_options":"🔧  Opzioni","tab_profiles":"💾  Profili",
    "tab_run":"▶  Esecuzione","tab_settings":"🌐  Impostazioni",
    "exe_section":"Eseguibile IMAPSync","browse":"Sfoglia…",
    "src":"📤  Server sorgente","dst":"📥  Server destinazione",
    "hostname":"Nome host / IP:","port":"Porta:","username":"Nome utente:",
    "password":"Password:","ssl":"SSL","tls":"STARTTLS",
    "dry_run":"🧪  Simulazione (--dry) – niente viene copiato davvero",
    "folder_title":"Filtro cartelle (Includi / Escludi)",
    "fetch_btn":"📋  Recupera cartelle dal server sorgente",
    "mode_inc":"Sincronizza solo queste cartelle (--include)",
    "mode_exc":"Escludi queste cartelle (--exclude)",
    "sel_all":"Seleziona tutto","desel_all":"Deseleziona tutto",
    "fetching":"Connessione al server sorgente…","fetch_ok":"Cartelle caricate.",
    "fetch_err":"Errore nel recupero","no_src_host":"Configurare prima il server sorgente.",
    "folder_hint":"Nessuna cartella selezionata = tutte le cartelle verranno sincronizzate.",
    "sync_behavior":"Comportamento di sincronizzazione","more_opts":"Altre opzioni",
    "extra_args":"Argomenti aggiuntivi (testo libero)","extra_hint":"es.  --maxage 30",
    "profiles_title":"Profili salvati","save_p":"💾  Salva",
    "load_p":"📂  Carica","del_p":"🗑  Elimina",
    "p_name":"Nome profilo:","p_save_btn":"Salva",
    "col_src":"Server sorgente","col_dst":"Server destinazione","col_usr":"Utente",
    "no_profile":"Selezionare un profilo.","confirm_del":"Eliminare davvero questo profilo?",
    "gen_bat":"🔍  Genera comando & crea .bat","run_bat":"▶  Esegui .bat",
    "copy_clip":"📋  Copia","clear_log":"🗑  Pulisci log","stop":"⏹  Stop",
    "cmd_prev":"Comando generato","log_title":"Output del log",
    "st_ready":"Pronto.","st_run":"In esecuzione…","st_done":"Completato ✓",
    "st_stop":"Fermato","st_err":"Errore","st_saved":"BAT salvato",
    "st_copied":"Copiato negli appunti ✓",
    "err_fields":"Inserire i server sorgente e destinazione.",
    "err_bat_nf":"Generare prima il comando.",
    "err_bat_save":"Impossibile salvare il file .bat",
    "msg_bat_saved":"✅  .bat salvato: ","msg_run_start":"▶  Avvio: ",
    "msg_done":"✅  IMAPSync completato (Exit 0)",
    "msg_exit":"⚠️  Codice di uscita: ","msg_stopped":"⏹  Processo fermato.",
    "msg_err":"❌  Errore: ","settings_title":"Impostazioni","lang_label":"Lingua:",
    "bat_path_label":"Percorso file .bat:","choose_bat":"Scegli percorso…",
    "restart_hint":"La lingua viene applicata immediatamente.",
    "o_delete2":"Elimina su dest ciò che manca su sorgente",
    "o_delete2dup":"Elimina duplicati su destinazione",
    "o_subscribeall":"Iscriviti a tutte le cartelle",
    "o_automap":"Mappa automaticamente le cartelle",
    "o_nofldrsz":"Non calcolare le dimensioni delle cartelle (più veloce)",
    "o_justfolders":"Crea solo cartelle, nessun messaggio",
    "o_useuid":"Usa gli UID per il confronto",
    "o_noskipdup":"Non saltare i duplicati","o_nomodver":"Non mostrare le versioni dei moduli",
    "o_norelck":"Nessun controllo aggiornamenti","o_noauthmd5":"Disabilita auth MD5",
    "o_notls":"Disabilita TLS completamente","o_nosyncacls":"Non sincronizzare gli ACL",
    "o_expunge1":"Pulisci eliminati su sorgente","o_expunge2":"Pulisci eliminati su destinazione",
    "tab_about":"(i)  Informazioni",
    "about_title":"Informazioni su questo strumento",
    "about_author":"Sviluppatore",
    "about_contact":"Contatto",
    "about_blog":"Blog",
    "about_version":"Versione",
    "about_desc":"IMAPSync GUI è un'interfaccia grafica Windows per lo strumento a riga di comando imapsync. Creata per semplificare le migrazioni e-mail tra server IMAP.",
    "about_open_mail":"Invia e-mail",
    "about_open_blog":"Apri blog",
    "about_imapsync":"Progetto IMAPSync",
    "about_based_on":"Basato su:",
    "about_contact_title":"Contatto",
},
}


# ═══════════════════════════════════════════════════════════════
#  GERUNDETER CARD-RAHMEN (Canvas-basiert)
# ═══════════════════════════════════════════════════════════════
class Card(tk.Canvas):
    """Gerundeter Rahmen. Widgets in card.inner platzieren."""
    def __init__(self, master, radius=RADIUS, bg=BG_CARD, outline=BORDER, **kw):
        kw.setdefault("highlightthickness", 0)
        kw.setdefault("bd", 0)
        parent_bg = BG_MAIN
        try:
            parent_bg = master.cget("bg")
        except Exception:
            pass
        super().__init__(master, bg=parent_bg, **kw)
        self._r       = radius
        self._fill    = bg
        self._outline = outline
        self.inner = tk.Frame(self, bg=bg)
        self._win  = self.create_window(0, 0, anchor="nw", window=self.inner)
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 4 or h < 4:
            return
        self.delete("shape")
        r = min(self._r, w // 2, h // 2)
        pts = [
            r, 0,   w-r, 0,
            w, 0,   w,   r,
            w, h-r, w,   h,
            w-r, h, r,   h,
            0, h,   0,   h-r,
            0, r,   0,   0,
            r, 0,
        ]
        self.create_polygon(pts, smooth=True,
                            fill=self._fill, outline=self._outline,
                            width=1, tags="shape")
        self.tag_lower("shape")
        self.itemconfig(self._win, width=w, height=h)


# ═══════════════════════════════════════════════════════════════
#  CUSTOM NOTEBOOK MIT GERUNDETEN TABS (Canvas-basiert)
# ═══════════════════════════════════════════════════════════════
class RoundedNotebook(tk.Frame):
    """
    Moderne Tab-Leiste: Pill-förmige Chips, kein smooth-Artefakt,
    aktiver Tab mit Accent-Unterstrich und hellem Hintergrund.
    """
    TAB_H   = 36          # Chip-Höhe
    TAB_PAD = 6           # Abstand zwischen Chips
    V_PAD   = 8           # vertikaler Abstand oben/unten in der Bar
    BAR_H   = TAB_H + V_PAD * 2

    def __init__(self, master, **kw):
        super().__init__(master, bg=BG_MAIN, **kw)
        self._bar = tk.Canvas(self, bg=BG_MAIN,
                              height=self.BAR_H,
                              highlightthickness=0, bd=0)
        self._bar.pack(fill="x", padx=12, pady=(10, 0))
        self._sep = tk.Frame(self, bg=BORDER, height=1)
        self._sep.pack(fill="x", padx=12)
        self._area = tk.Frame(self, bg=BG_MAIN)
        self._area.pack(fill="both", expand=True, padx=12, pady=10)
        self._tabs: list[dict] = []
        self._active = -1
        self._bar.bind("<Configure>", lambda e: self._redraw_bar())
        self._bar.bind("<Button-1>", self._on_click)
        self._bar.bind("<Motion>",   self._on_hover)
        self._hover = -1

    # ── Öffentliche API ──────────────────────────────────────
    def add(self, frame: tk.Frame, text: str = ""):
        idx = len(self._tabs)
        self._tabs.append({"text": text, "frame": frame, "x1": 0, "x2": 0})
        if idx == 0:
            self.select(0)
        else:
            frame.pack_forget()
        self._redraw_bar()

    def select(self, idx: int):
        if 0 <= self._active < len(self._tabs):
            self._tabs[self._active]["frame"].pack_forget()
        self._active = idx
        self._tabs[idx]["frame"].pack(in_=self._area,
                                      fill="both", expand=True)
        self._redraw_bar()

    def update_labels(self, texts: list):
        for i, t in enumerate(texts):
            if i < len(self._tabs):
                self._tabs[i]["text"] = t
        self._redraw_bar()

    def force_redraw(self):
        """Erzwingt Layout-Update und zeichnet danach neu – für den ersten Render."""
        self.update_idletasks()
        self._bar.update_idletasks()
        self._redraw_bar()

    # ── Koordinaten live berechnen ───────────────────────────
    def _get_tab_coords(self, W):
        """Gibt Liste von (x1, x2) für jeden Tab zurück – immer frisch berechnet."""
        n   = len(self._tabs)
        pad = self.TAB_PAD
        tab_w = (W - pad * (n + 1)) // n
        coords = []
        for i in range(n):
            x1 = pad + i * (tab_w + pad)
            x2 = (W - pad) if i == n - 1 else (x1 + tab_w)
            coords.append((x1, x2))
        return coords

    # ── Zeichnen ─────────────────────────────────────────────
    def _redraw_bar(self):
        self._bar.delete("all")
        W = self._bar.winfo_width()
        if W < 10 or not self._tabs:
            return

        n   = len(self._tabs)
        H   = self.TAB_H
        vp  = self.V_PAD
        r   = 8
        ul  = 3
        coords = self._get_tab_coords(W)

        for i, tab in enumerate(self._tabs):
            x1, x2 = coords[i]
            # Für Klick-Detection cachen
            tab["x1"], tab["x2"] = x1, x2
            y1, y2 = vp, vp + H

            active  = (i == self._active)
            hovered = (i == self._hover) and not active

            bg = "#2e2e48" if active else ("#252538" if hovered else BG_CARD)

            self._draw_pill(x1, y1, x2, y2, r, bg,
                            BORDER if not active else "#3d3d5c",
                            tag=f"t{i}")

            if active:
                self._bar.create_rectangle(
                    x1 + r, y2 - ul, x2 - r, y2,
                    fill=ACCENT, outline="", tags=f"t{i}")

            fg     = ACCENT if active else (FG_TEXT if hovered else FG_LABEL)
            weight = "bold" if active else "normal"
            self._bar.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=tab["text"], fill=fg,
                font=("Segoe UI", 9, weight),
                tags=f"t{i}")

    def _draw_pill(self, x1, y1, x2, y2, r, fill, outline, tag):
        """Pill-Form: gefüllte Fläche + optionaler 1px-Rahmen."""
        c = self._bar
        # ── Füllfläche aus Rechtecken + Kreisbögen ──────────
        c.create_rectangle(x1+r, y1,   x2-r, y2,   fill=fill, outline="", tags=tag)
        c.create_rectangle(x1,   y1+r, x2,   y2-r, fill=fill, outline="", tags=tag)
        c.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,
                     fill=fill, outline="", style="pieslice", tags=tag)
        c.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,
                     fill=fill, outline="", style="pieslice", tags=tag)
        c.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,
                     fill=fill, outline="", style="pieslice", tags=tag)
        c.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,
                     fill=fill, outline="", style="pieslice", tags=tag)

        if not outline:
            return

        # ── Rahmen: 4 Kanten + 4 Ecken als separate Bögen ──
        # Oben
        c.create_line(x1+r, y1, x2-r, y1, fill=outline, width=1, tags=tag)
        # Unten
        c.create_line(x1+r, y2, x2-r, y2, fill=outline, width=1, tags=tag)
        # Links
        c.create_line(x1, y1+r, x1, y2-r, fill=outline, width=1, tags=tag)
        # Rechts
        c.create_line(x2, y1+r, x2, y2-r, fill=outline, width=1, tags=tag)
        # Ecken als Bögen (nur Kontur, kein fill)
        c.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,
                     outline=outline, style="arc", width=1, tags=tag)
        c.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,
                     outline=outline, style="arc", width=1, tags=tag)
        c.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,
                     outline=outline, style="arc", width=1, tags=tag)
        c.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,
                     outline=outline, style="arc", width=1, tags=tag)

    # ── Interaktion ──────────────────────────────────────────
    def _on_click(self, e):
        W = self._bar.winfo_width()
        if W < 10: return
        for i, (x1, x2) in enumerate(self._get_tab_coords(W)):
            if x1 <= e.x <= x2:
                self.select(i)
                return

    def _on_hover(self, e):
        W = self._bar.winfo_width()
        hit = -1
        if W >= 10:
            for i, (x1, x2) in enumerate(self._get_tab_coords(W)):
                if x1 <= e.x <= x2:
                    hit = i
                    break
        if hit != self._hover:
            self._hover = hit
            self._bar.config(cursor="hand2" if hit >= 0 else "")
            self._redraw_bar()


# ═══════════════════════════════════════════════════════════════
#  HAUPT-ANWENDUNG
# ═══════════════════════════════════════════════════════════════
class IMAPSyncApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("IMAPSync GUI")
        self.geometry("1080x800")
        self.minsize(900, 680)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        self._lang        = tk.StringVar(value="de")
        self.bat_path     = tk.StringVar(value=os.path.join(os.getcwd(), "imapsync_run.bat"))
        self.imap_exe     = tk.StringVar(value="imapsync")
        self.profiles_dir = os.path.join(os.getcwd(), "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)
        self._process     = None
        self._run_count   = 0

        self._folder_mode = tk.StringVar(value="include")
        self._folder_vars: dict = {}

        self._about_data  = self._load_about()

        self._build_styles()
        self._build_ui()
        self._load_profile_list()
        # Layout abwarten, dann Tab-Leiste mit korrekter Fensterbreite zeichnen
        self.after(10, self.nb.force_redraw)

    # ── Übersetzungs-Helfer ──────────────────────────────────
    def t(self, key: str) -> str:
        lang = self._lang.get()
        return T.get(lang, T["de"]).get(key, T["de"].get(key, key))

    # ═══════════════════════════════════════════════════════════
    #  STYLES
    # ═══════════════════════════════════════════════════════════
    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=BG_MAIN, foreground=FG_TEXT,
                    font=("Segoe UI", 10), fieldbackground=BG_INPUT,
                    bordercolor=BORDER, troughcolor=BG_CARD,
                    selectbackground=ACCENT, selectforeground=BG_MAIN)
        s.configure("TFrame",  background=BG_MAIN)
        s.configure("TLabel",  background=BG_MAIN, foreground=FG_TEXT)
        s.configure("TEntry",  fieldbackground=BG_INPUT, foreground=FG_TEXT,
                    insertcolor=FG_TEXT, relief="flat", padding=6)
        s.configure("TCheckbutton", background=BG_CARD, foreground=FG_TEXT)
        s.map("TCheckbutton", background=[("active", BG_CARD)])
        s.configure("TRadiobutton", background=BG_CARD, foreground=FG_TEXT)
        s.map("TRadiobutton", background=[("active", BG_CARD)])
        s.configure("TCombobox", fieldbackground=BG_INPUT, foreground=FG_TEXT)
        s.configure("TScrollbar", background=BORDER, troughcolor=BG_INPUT,
                    arrowcolor=FG_LABEL, bordercolor=BG_CARD)
        s.configure("Treeview", background=BG_INPUT, fieldbackground=BG_INPUT,
                    foreground=FG_TEXT, rowheight=26, borderwidth=0)
        s.map("Treeview", background=[("selected", ACCENT)],
              foreground=[("selected", BG_MAIN)])
        s.configure("Treeview.Heading", background=BG_CARD,
                    foreground=ACCENT, font=("Segoe UI", 9, "bold"), relief="flat")
        for name, bg, hov in [
            ("Acc.TButton",  ACCENT,   ACCENT_DK),
            ("Suc.TButton",  SUCCESS,  "#7ec87a"),
            ("Dan.TButton",  DANGER,   "#d96070"),
            ("Neu.TButton",  BG_INPUT, BORDER),
        ]:
            s.configure(name, background=bg, foreground=BG_MAIN,
                        font=("Segoe UI", 10, "bold"), relief="flat",
                        padding=(12, 6), borderwidth=0)
            s.map(name, background=[("active", hov), ("pressed", hov)])

    # ═══════════════════════════════════════════════════════════
    #  HAUPT-UI
    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        # Titelleiste
        hdr = tk.Frame(self, bg=BG_CARD, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  📧  IMAPSync GUI", bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=10)
        self._subtitle_lbl = tk.Label(hdr, text=self.t("subtitle"),
                                       bg=BG_CARD, fg=FG_LABEL,
                                       font=("Segoe UI", 9))
        self._subtitle_lbl.pack(side="left")

        self.nb = RoundedNotebook(self)
        self.nb.pack(fill="both", expand=True, padx=4, pady=(0, 8))

        self._f_config   = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_folders  = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_options  = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_profiles = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_run      = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_settings = tk.Frame(self.nb, bg=BG_MAIN)
        self._f_about    = tk.Frame(self.nb, bg=BG_MAIN)

        self._tab_keys = ["tab_config","tab_folders","tab_options",
                          "tab_profiles","tab_run","tab_settings","tab_about"]
        for frame, key in zip([self._f_config, self._f_folders, self._f_options,
                                self._f_profiles, self._f_run, self._f_settings,
                                self._f_about],
                               self._tab_keys):
            self.nb.add(frame, text=self.t(key))

        self._build_config()
        self._build_folders()
        self._build_options()
        self._build_profiles()
        self._build_run()
        self._build_settings()
        self._build_about()

    # ── Label-Refresh nach Sprachwechsel ─────────────────────
    def _refresh_all_labels(self):
        self._subtitle_lbl.config(text=self.t("subtitle"))
        self.nb.update_labels([self.t(k) for k in self._tab_keys])
        # Config
        self._exe_lbl_w.config(text=f"{self.t('exe_section')}:")
        self._browse_btn.config(text=self.t("browse"))
        self._src_head.config(text=self.t("src"))
        self._dst_head.config(text=self.t("dst"))
        self._dry_cb.config(text=self.t("dry_run"))
        for lbls, sv in [(self._src_lbls, self._src), (self._dst_lbls, self._dst)]:
            for lbl, key in zip(lbls, ["hostname","port","username","password"]):
                lbl.config(text=self.t(key))
        # Ordner
        self._folder_head.config(text=self.t("folder_title"))
        self._fetch_btn_w.config(text=self.t("fetch_btn"))
        self._mode_inc_rb.config(text=self.t("mode_inc"))
        self._mode_exc_rb.config(text=self.t("mode_exc"))
        self._selall_btn.config(text=self.t("sel_all"))
        self._deselall_btn.config(text=self.t("desel_all"))
        self._folder_hint_lbl.config(text=self.t("folder_hint"))
        # Optionen
        self._opt_head1.config(text=f" {self.t('sync_behavior')} ")
        self._opt_head2.config(text=f" {self.t('more_opts')} ")
        self._extra_head.config(text=f" {self.t('extra_args')} ")
        self._extra_hint_lbl.config(text=self.t("extra_hint"))
        for key, (var, flag, lbl_w, desc_w) in self._opt_widgets.items():
            desc_w.config(text=self.t(f"o_{key}"))
        # Profile
        self._prof_head.config(text=self.t("profiles_title"))
        self._save_p_btn.config(text=self.t("save_p"))
        self._load_p_btn.config(text=self.t("load_p"))
        self._del_p_btn.config(text=self.t("del_p"))
        self.profile_tree.heading("src",  text=self.t("col_src"))
        self.profile_tree.heading("dst",  text=self.t("col_dst"))
        self.profile_tree.heading("user", text=self.t("col_usr"))
        # Run
        self._cmd_head.config(text=f" {self.t('cmd_prev')} ")
        self._gen_btn.config(text=self.t("gen_bat"))
        self._run_btn.config(text=self.t("run_bat"))
        self._copy_btn.config(text=self.t("copy_clip"))
        self._clrlog_btn.config(text=self.t("clear_log"))
        self._stop_btn.config(text=self.t("stop"))
        self._log_head.config(text=f" {self.t('log_title')} ")
        # Settings
        self._sett_head.config(text=self.t("settings_title"))
        self._lang_lbl.config(text=self.t("lang_label"))
        self._bat_lbl.config(text=self.t("bat_path_label"))
        self._bat_choose_btn.config(text=self.t("choose_bat"))
        self._restart_hint.config(text=self.t("restart_hint"))
        self.status_var.set(self.t("st_ready"))
        self._refresh_about_labels()

    # ═══════════════════════════════════════════════════════════
    #  TAB 1 – KONFIGURATION
    # ═══════════════════════════════════════════════════════════
    def _build_config(self):
        p = self._f_config

        # EXE + Dry-Run – flache Zeilen ohne Card-Canvas-Overhead
        exe_row = tk.Frame(p, bg=BG_CARD)
        exe_row.pack(fill="x", padx=6, pady=(6, 2))
        self._exe_lbl_w = tk.Label(exe_row, text=f"{self.t('exe_section')}:",
                                    bg=BG_CARD, fg=ACCENT,
                                    font=("Segoe UI", 9, "bold"), width=22, anchor="w")
        self._exe_lbl_w.pack(side="left", padx=(8, 4), pady=5)
        ttk.Entry(exe_row, textvariable=self.imap_exe).pack(
            side="left", fill="x", expand=True, pady=5)
        self._browse_btn = ttk.Button(exe_row, text=self.t("browse"),
                                       style="Neu.TButton",
                                       command=self._browse_exe)
        self._browse_btn.pack(side="left", padx=(6, 8), pady=5)

        dry_row = tk.Frame(p, bg=BG_CARD)
        dry_row.pack(fill="x", padx=6, pady=(0, 6))
        self.dry = tk.BooleanVar()
        self._dry_cb = ttk.Checkbutton(dry_row,
                                        text=self.t("dry_run"),
                                        variable=self.dry,
                                        style="TCheckbutton")
        self._dry_cb.pack(anchor="w", padx=8, pady=5)

        # Server-Spalten
        cols = tk.Frame(p, bg=BG_MAIN)
        cols.pack(fill="both", expand=True, padx=6)
        cols.columnconfigure(0, weight=1)
        cols.columnconfigure(1, weight=1)

        src_card = Card(cols)
        src_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self._src_head = tk.Label(src_card.inner, text=self.t("src"),
                                   bg=BG_CARD, fg=ACCENT,
                                   font=("Segoe UI", 11, "bold"))
        self._src_head.pack(anchor="w", padx=12, pady=(10, 4))
        src_grid = tk.Frame(src_card.inner, bg=BG_CARD)
        src_grid.pack(fill="both", expand=True)
        self._src, self._src_lbls = self._server_form(src_grid)

        dst_card = Card(cols)
        dst_card.grid(row=0, column=1, sticky="nsew")
        self._dst_head = tk.Label(dst_card.inner, text=self.t("dst"),
                                   bg=BG_CARD, fg=ACCENT,
                                   font=("Segoe UI", 11, "bold"))
        self._dst_head.pack(anchor="w", padx=12, pady=(10, 4))
        dst_grid = tk.Frame(dst_card.inner, bg=BG_CARD)
        dst_grid.pack(fill="both", expand=True)
        self._dst, self._dst_lbls = self._server_form(dst_grid)

    def _server_form(self, parent):
        v = {
            "host": tk.StringVar(), "port": tk.StringVar(value="993"),
            "user": tk.StringVar(), "pass": tk.StringVar(),
            "ssl":  tk.BooleanVar(value=True),
            "tls":  tk.BooleanVar(value=False),
        }
        field_keys = ["hostname", "port", "username", "password"]
        var_keys   = ["host",     "port", "user",     "pass"]
        lbls = []
        for i, (tkey, vkey) in enumerate(zip(field_keys, var_keys)):
            lbl = tk.Label(parent, text=self.t(tkey),
                           bg=BG_CARD, fg=FG_LABEL, font=("Segoe UI", 9))
            lbl.grid(row=i, column=0, sticky="w", padx=(12, 4), pady=5)
            lbls.append(lbl)
            ttk.Entry(parent, textvariable=v[vkey],
                      show="●" if vkey == "pass" else "").grid(
                row=i, column=1, sticky="ew", padx=(0, 12), pady=5)
        parent.columnconfigure(1, weight=1)
        cf = tk.Frame(parent, bg=BG_CARD)
        cf.grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 12))
        ttk.Checkbutton(cf, text=self.t("ssl"), variable=v["ssl"],
                        style="TCheckbutton").pack(side="left", padx=8)
        ttk.Checkbutton(cf, text=self.t("tls"), variable=v["tls"],
                        style="TCheckbutton").pack(side="left", padx=8)
        return v, lbls

    # ═══════════════════════════════════════════════════════════
    #  TAB 2 – ORDNER INCLUDE / EXCLUDE
    # ═══════════════════════════════════════════════════════════
    def _build_folders(self):
        p = self._f_folders
        self._folder_sep = "."          # IMAP-Trennzeichen; wird beim Laden gesetzt
        self._tv_checked: dict = {}     # iid -> BooleanVar (nur Blätter + Eltern)

        ctrl_card = Card(p)
        ctrl_card.pack(fill="x", padx=6, pady=(6, 4))
        self._folder_head = tk.Label(ctrl_card.inner, text=self.t("folder_title"),
                                      bg=BG_CARD, fg=ACCENT,
                                      font=("Segoe UI", 11, "bold"))
        self._folder_head.pack(anchor="w", padx=12, pady=(10, 6))

        mode_row = tk.Frame(ctrl_card.inner, bg=BG_CARD)
        mode_row.pack(fill="x", padx=12, pady=(0, 4))
        self._mode_inc_rb = ttk.Radiobutton(mode_row, text=self.t("mode_inc"),
                                             variable=self._folder_mode,
                                             value="include")
        self._mode_inc_rb.pack(side="left", padx=(0, 20))
        self._mode_exc_rb = ttk.Radiobutton(mode_row, text=self.t("mode_exc"),
                                             variable=self._folder_mode,
                                             value="exclude")
        self._mode_exc_rb.pack(side="left")

        btn_row = tk.Frame(ctrl_card.inner, bg=BG_CARD)
        btn_row.pack(fill="x", padx=12, pady=(4, 4))
        self._fetch_btn_w = ttk.Button(btn_row, text=self.t("fetch_btn"),
                                        style="Acc.TButton",
                                        command=self._start_fetch_folders)
        self._fetch_btn_w.pack(side="left", padx=(0, 8))
        self._selall_btn = ttk.Button(btn_row, text=self.t("sel_all"),
                                       style="Neu.TButton",
                                       command=self._select_all_folders)
        self._selall_btn.pack(side="left", padx=(0, 8))
        self._deselall_btn = ttk.Button(btn_row, text=self.t("desel_all"),
                                         style="Neu.TButton",
                                         command=self._deselect_all_folders)
        self._deselall_btn.pack(side="left", padx=(0, 16))
        self._expand_btn = ttk.Button(btn_row, text="⊞  Alle ausklappen",
                                       style="Neu.TButton",
                                       command=self._expand_all_folders)
        self._expand_btn.pack(side="left", padx=(0, 8))
        self._collapse_btn = ttk.Button(btn_row, text="⊟  Alle einklappen",
                                         style="Neu.TButton",
                                         command=self._collapse_all_folders)
        self._collapse_btn.pack(side="left")

        self._fetch_status = tk.StringVar(value="")
        tk.Label(ctrl_card.inner, textvariable=self._fetch_status,
                 bg=BG_CARD, fg=FG_LABEL, font=("Segoe UI", 9)).pack(
            anchor="w", padx=12, pady=(2, 6))

        # Treeview mit Checkbox-Spalte
        tv_frame = tk.Frame(p, bg=BG_CARD)
        tv_frame.pack(fill="both", expand=True, padx=6, pady=(0, 4))

        style = ttk.Style()
        style.configure("Folder.Treeview",
                        background=BG_INPUT, fieldbackground=BG_INPUT,
                        foreground=FG_TEXT, rowheight=22,
                        borderwidth=0, font=("Segoe UI", 9))
        style.map("Folder.Treeview",
                  background=[("selected", BG_INPUT)],
                  foreground=[("selected", ACCENT)])
        style.configure("Folder.Treeview.Heading",
                        background=BG_CARD, foreground=ACCENT,
                        font=("Segoe UI", 9, "bold"), relief="flat")

        self._folder_tree = ttk.Treeview(tv_frame, style="Folder.Treeview",
                                          columns=("check",), show="tree headings",
                                          selectmode="none")
        self._folder_tree.heading("#0",     text="Ordner")
        self._folder_tree.heading("check",  text="✓")
        self._folder_tree.column("#0",      width=480, stretch=True)
        self._folder_tree.column("check",   width=36,  stretch=False, anchor="center")

        vsb = ttk.Scrollbar(tv_frame, orient="vertical",
                             command=self._folder_tree.yview)
        hsb = ttk.Scrollbar(tv_frame, orient="horizontal",
                             command=self._folder_tree.xview)
        self._folder_tree.configure(yscrollcommand=vsb.set,
                                     xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._folder_tree.pack(fill="both", expand=True)

        self._folder_tree.bind("<Button-1>", self._on_folder_click)
        self._folder_tree.bind("<MouseWheel>",
                                lambda e: self._folder_tree.yview_scroll(
                                    int(-1*(e.delta/120)), "units"))

        self._folder_hint_lbl = tk.Label(p, text=self.t("folder_hint"),
                                          bg=BG_MAIN, fg=FG_LABEL,
                                          font=("Segoe UI", 9, "italic"))
        self._folder_hint_lbl.pack(anchor="w", padx=12, pady=(0, 4))

    def _start_fetch_folders(self):
        if not self._src["host"].get().strip():
            messagebox.showwarning("", self.t("no_src_host"))
            return
        self._fetch_status.set(self.t("fetching"))
        self._fetch_btn_w.config(state="disabled")
        threading.Thread(target=self._fetch_folders, daemon=True).start()

    def _fetch_folders(self):
        host = self._src["host"].get().strip()
        port = int(self._src["port"].get() or 993)
        user = self._src["user"].get().strip()
        pw   = self._src["pass"].get()
        ssl  = self._src["ssl"].get()
        try:
            M = imaplib.IMAP4_SSL(host, port) if ssl else imaplib.IMAP4(host, port)
            M.login(user, pw)
            _, raw = M.list()
            M.logout()
            names = []
            detected_sep = "."
            for item in raw:
                if not item:
                    continue
                decoded = item.decode("utf-8", errors="replace")                           if isinstance(item, bytes) else str(item)
                # Trennzeichen aus erster Zeile lesen: (\Flags) "SEP" ...
                sm = re.match(r'\([^)]*\)\s+"([^"]+)"\s+', decoded)
                if sm and len(sm.group(1)) == 1:
                    detected_sep = sm.group(1)
                # quoted name
                m = re.match(r'\([^)]*\)\s+(?:"[^"]*"|NIL)\s+"(.+)"\s*$', decoded)
                if m:
                    names.append(m.group(1))
                    continue
                # unquoted name
                m = re.match(r'\([^)]*\)\s+(?:"[^"]*"|NIL)\s+(\S.+?)\s*$', decoded)
                if m:
                    name = m.group(1).strip().strip('"')
                    if name:
                        names.append(name)
                    continue
                tok = decoded.rsplit(None, 1)
                if len(tok) == 2:
                    name = tok[1].strip().strip('"')
                    if name and not name.startswith("("):
                        names.append(name)
            sep = detected_sep
            self.after(0, lambda n=sorted(set(names)), s=sep:
                       self._populate_folder_list(n, s))
        except Exception as ex:
            self.after(0, lambda e=str(ex): self._fetch_status.set(
                f"{self.t('fetch_err')}: {e}"))
        finally:
            self.after(0, lambda: self._fetch_btn_w.config(state="normal"))

    def _populate_folder_list(self, names: list, sep: str = "."):
        self._folder_sep = sep
        self._folder_vars.clear()
        self._tv_checked.clear()

        # Treeview leeren
        for iid in self._folder_tree.get_children():
            self._folder_tree.delete(iid)

        if not names:
            self._fetch_status.set("⚠  0 Ordner gefunden")
            return

        # Baum aus Ordnernamen aufbauen
        # node_map: voller Pfad -> iid im Treeview
        node_map: dict = {}

        def get_or_create_parent(parts, full_parts):
            """Stellt sicher, dass alle Elternknoten existieren."""
            if len(parts) <= 1:
                return ""
            parent_parts = parts[:-1]
            parent_path  = sep.join(full_parts[:len(parent_parts)])
            if parent_path in node_map:
                return node_map[parent_path]
            # Elternteil anlegen (existiert nicht als echter Ordner)
            grand = get_or_create_parent(parent_parts, full_parts)
            label = parent_parts[-1]
            iid   = self._folder_tree.insert(
                grand, "end", text=f"  {label}",
                values=("☐",), open=False, tags=("parent_virtual",))
            node_map[parent_path] = iid
            var = tk.BooleanVar(value=False)
            self._folder_vars[parent_path] = var
            self._tv_checked[iid] = (var, parent_path)
            return iid

        for full_name in names:
            parts = full_name.split(sep)
            parent_iid = get_or_create_parent(parts, parts)
            label = parts[-1]
            iid   = self._folder_tree.insert(
                parent_iid, "end", text=f"  {label}",
                values=("☐",), open=False)
            node_map[full_name] = iid
            var = tk.BooleanVar(value=False)
            self._folder_vars[full_name] = var
            self._tv_checked[iid] = (var, full_name)

        # Nur Top-Level aufgeklappt lassen? Nein – alle zugeklappt by default.
        # Top-Level-Einträge bleiben so wie insert sie angelegt hat (open=False).

        top = len(self._folder_tree.get_children())
        self._fetch_status.set(
            f"✅  {len(names)} Ordner geladen  ({top} Hauptordner)")

    def _on_folder_click(self, event):
        """Checkbox-Toggle beim Klick auf die check-Spalte oder den Ordnernamen."""
        region = self._folder_tree.identify_region(event.x, event.y)
        iid    = self._folder_tree.identify_row(event.y)
        if not iid:
            return
        col = self._folder_tree.identify_column(event.x)
        # Klick auf Checkbox-Spalte (#1) ODER auf den Namen (#0)
        if col in ("#0", "#1"):
            self._toggle_folder(iid, recursive=True)

    def _toggle_folder(self, iid, value=None, recursive=True):
        """Schaltet Checkbox um; wenn recursive=True, auch alle Kinder."""
        if iid not in self._tv_checked:
            return
        var, _ = self._tv_checked[iid]
        new_val = (not var.get()) if value is None else value
        var.set(new_val)
        symbol = "☑" if new_val else "☐"
        self._folder_tree.set(iid, "check", symbol)
        if recursive:
            for child in self._folder_tree.get_children(iid):
                self._toggle_folder(child, value=new_val, recursive=True)

    def _expand_all_folders(self):
        def _expand(iid):
            self._folder_tree.item(iid, open=True)
            for child in self._folder_tree.get_children(iid):
                _expand(child)
        for iid in self._folder_tree.get_children():
            _expand(iid)

    def _collapse_all_folders(self):
        def _collapse(iid):
            self._folder_tree.item(iid, open=False)
            for child in self._folder_tree.get_children(iid):
                _collapse(child)
        for iid in self._folder_tree.get_children():
            _collapse(iid)

    def _select_all_folders(self):
        for iid in self._tv_checked:
            self._toggle_folder(iid, value=True, recursive=False)

    def _deselect_all_folders(self):
        for iid in self._tv_checked:
            self._toggle_folder(iid, value=False, recursive=False)

    # ═══════════════════════════════════════════════════════════
    #  TAB 3 – OPTIONEN
    # ═══════════════════════════════════════════════════════════
    def _build_options(self):
        p = self._f_options
        p.columnconfigure(0, weight=1)
        p.columnconfigure(1, weight=1)
        self._opt_widgets: dict = {}

        left_opts = [
            ("delete2",      "--delete2"),
            ("delete2dup",   "--delete2duplicates"),
            ("subscribeall", "--subscribeall"),
            ("automap",      "--automap"),
            ("nofldrsz",     "--nofoldersizes"),
            ("justfolders",  "--justfolders"),
            ("useuid",       "--useuid"),
        ]
        right_opts = [
            ("noskipdup",  "--noskipduplicates"),
            ("nomodver",   "--no_modulesversion"),
            ("norelck",    "--noreleasecheck"),
            ("noauthmd5",  "--noauthmd5"),
            ("notls",      "--notls"),
            ("nosyncacls", "--nosyncacls"),
            ("expunge1",   "--expunge1"),
            ("expunge2",   "--expunge2"),
        ]

        lc = Card(p)
        lc.grid(row=0, column=0, sticky="nsew", padx=(6, 4), pady=6)
        self._opt_head1 = tk.Label(lc.inner, text=f" {self.t('sync_behavior')} ",
                                    bg=BG_CARD, fg=ACCENT,
                                    font=("Segoe UI", 10, "bold"))
        self._opt_head1.pack(anchor="w", padx=10, pady=(10, 4))
        self._build_option_rows(lc.inner, left_opts)

        rc = Card(p)
        rc.grid(row=0, column=1, sticky="nsew", padx=(4, 6), pady=6)
        self._opt_head2 = tk.Label(rc.inner, text=f" {self.t('more_opts')} ",
                                    bg=BG_CARD, fg=ACCENT,
                                    font=("Segoe UI", 10, "bold"))
        self._opt_head2.pack(anchor="w", padx=10, pady=(10, 4))
        self._build_option_rows(rc.inner, right_opts)

        ec = Card(p)
        ec.grid(row=1, column=0, columnspan=2, sticky="ew", padx=6, pady=(0, 6))
        self._extra_head = tk.Label(ec.inner, text=f" {self.t('extra_args')} ",
                                     bg=BG_CARD, fg=ACCENT,
                                     font=("Segoe UI", 10, "bold"))
        self._extra_head.pack(anchor="w", padx=10, pady=(10, 2))
        self.extra_args = tk.StringVar()
        ttk.Entry(ec.inner, textvariable=self.extra_args).pack(
            fill="x", padx=10, pady=(0, 4))
        self._extra_hint_lbl = tk.Label(ec.inner, text=self.t("extra_hint"),
                                         bg=BG_CARD, fg=FG_LABEL,
                                         font=("Segoe UI", 9, "italic"))
        self._extra_hint_lbl.pack(anchor="w", padx=10, pady=(0, 10))

    def _build_option_rows(self, parent, opts):
        for key, flag in opts:
            var = tk.BooleanVar()
            row = tk.Frame(parent, bg=BG_CARD)
            row.pack(fill="x", padx=8, pady=3)
            lbl_w = tk.Label(row, text=flag, bg=BG_CARD, fg=ACCENT,
                             font=("Consolas", 9, "bold"), width=24, anchor="w")
            lbl_w.pack(side="left")
            ttk.Checkbutton(row, variable=var, style="TCheckbutton").pack(side="left")
            desc_w = tk.Label(row, text=self.t(f"o_{key}"),
                              bg=BG_CARD, fg=FG_LABEL, font=("Segoe UI", 9), anchor="w")
            desc_w.pack(side="left", padx=(4, 0))
            self._opt_widgets[key] = (var, flag, lbl_w, desc_w)

    # ═══════════════════════════════════════════════════════════
    #  TAB 4 – PROFILE
    # ═══════════════════════════════════════════════════════════
    def _build_profiles(self):
        p = self._f_profiles

        lc = Card(p)
        lc.pack(fill="both", expand=True, padx=6, pady=(6, 6))
        self._prof_head = tk.Label(lc.inner, text=self.t("profiles_title"),
                                    bg=BG_CARD, fg=ACCENT,
                                    font=("Segoe UI", 11, "bold"))
        self._prof_head.pack(anchor="w", padx=12, pady=(10, 6))

        tv_f = tk.Frame(lc.inner, bg=BG_CARD)
        tv_f.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.profile_tree = ttk.Treeview(tv_f,
                                          columns=("src","dst","user"),
                                          show="headings", height=14)
        self.profile_tree.heading("src",  text=self.t("col_src"))
        self.profile_tree.heading("dst",  text=self.t("col_dst"))
        self.profile_tree.heading("user", text=self.t("col_usr"))
        for col, w in [("src",240),("dst",240),("user",180)]:
            self.profile_tree.column(col, width=w)
        sb = ttk.Scrollbar(tv_f, orient="vertical",
                           command=self.profile_tree.yview)
        self.profile_tree.configure(yscrollcommand=sb.set)
        self.profile_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        br = tk.Frame(p, bg=BG_MAIN)
        br.pack(fill="x", padx=6, pady=(0, 6))
        self._save_p_btn = ttk.Button(br, text=self.t("save_p"),
                                       style="Acc.TButton",
                                       command=self._save_profile)
        self._save_p_btn.pack(side="left", padx=(0, 8))
        self._load_p_btn = ttk.Button(br, text=self.t("load_p"),
                                       style="Suc.TButton",
                                       command=self._load_profile)
        self._load_p_btn.pack(side="left", padx=(0, 8))
        self._del_p_btn = ttk.Button(br, text=self.t("del_p"),
                                      style="Dan.TButton",
                                      command=self._delete_profile)
        self._del_p_btn.pack(side="left")

    # ═══════════════════════════════════════════════════════════
    #  TAB 5 – AUSFÜHRUNG & LOG
    # ═══════════════════════════════════════════════════════════
    def _build_run(self):
        p = self._f_run

        cc = Card(p)
        cc.pack(fill="x", padx=6, pady=(6, 6))
        self._cmd_head = tk.Label(cc.inner, text=f" {self.t('cmd_prev')} ",
                                   bg=BG_CARD, fg=ACCENT,
                                   font=("Segoe UI", 10, "bold"))
        self._cmd_head.pack(anchor="w", padx=10, pady=(8, 2))
        self.cmd_preview = tk.Text(cc.inner, height=4, bg=BG_INPUT, fg=SUCCESS,
                                    font=("Consolas", 9), relief="flat",
                                    insertbackground=FG_TEXT, wrap="word",
                                    state="disabled")
        self.cmd_preview.pack(fill="x", padx=10, pady=(0, 10))

        br = tk.Frame(p, bg=BG_MAIN)
        br.pack(fill="x", padx=6, pady=(0, 6))
        self._gen_btn  = ttk.Button(br, text=self.t("gen_bat"),
                                     style="Acc.TButton",
                                     command=self._generate_bat)
        self._gen_btn.pack(side="left", padx=(0, 8))
        self._run_btn  = ttk.Button(br, text=self.t("run_bat"),
                                     style="Suc.TButton",
                                     command=self._run_bat)
        self._run_btn.pack(side="left", padx=(0, 8))
        self._copy_btn = ttk.Button(br, text=self.t("copy_clip"),
                                     style="Neu.TButton",
                                     command=self._copy_to_clipboard)
        self._copy_btn.pack(side="left", padx=(0, 8))
        self._stop_btn = ttk.Button(br, text=self.t("stop"),
                                     style="Dan.TButton",
                                     command=self._stop_process,
                                     state="disabled")
        self._stop_btn.pack(side="left", padx=(0, 8))
        self._clrlog_btn = ttk.Button(br, text=self.t("clear_log"),
                                       style="Neu.TButton",
                                       command=self._clear_log)
        self._clrlog_btn.pack(side="right")

        sr = tk.Frame(p, bg=BG_MAIN)
        sr.pack(fill="x", padx=6, pady=(0, 4))
        self.status_var  = tk.StringVar(value=self.t("st_ready"))
        self._status_lbl = tk.Label(sr, textvariable=self.status_var,
                                     bg=BG_MAIN, fg=FG_LABEL,
                                     font=("Segoe UI", 9))
        self._status_lbl.pack(side="left")

        # LOG – persistent, wird NICHT automatisch geleert
        lc = Card(p)
        lc.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self._log_head = tk.Label(lc.inner, text=f" {self.t('log_title')} ",
                                   bg=BG_CARD, fg=ACCENT,
                                   font=("Segoe UI", 10, "bold"))
        self._log_head.pack(anchor="w", padx=10, pady=(8, 2))
        self.log = scrolledtext.ScrolledText(
            lc.inner, bg=BG_INPUT, fg=FG_TEXT,
            font=("Consolas", 9), relief="flat",
            insertbackground=FG_TEXT, state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for tag, col in [("ok", SUCCESS), ("warn", WARNING),
                          ("err", DANGER), ("info", ACCENT), ("sep", BORDER)]:
            self.log.tag_config(tag, foreground=col)

    # ═══════════════════════════════════════════════════════════
    #  TAB 6 – EINSTELLUNGEN
    # ═══════════════════════════════════════════════════════════
    def _build_settings(self):
        p = self._f_settings

        sc = Card(p)
        sc.pack(fill="x", padx=6, pady=(6, 6))
        self._sett_head = tk.Label(sc.inner, text=self.t("settings_title"),
                                    bg=BG_CARD, fg=ACCENT,
                                    font=("Segoe UI", 13, "bold"))
        self._sett_head.pack(anchor="w", padx=14, pady=(12, 8))

        lr = tk.Frame(sc.inner, bg=BG_CARD)
        lr.pack(fill="x", padx=14, pady=(0, 6))
        self._lang_lbl = tk.Label(lr, text=self.t("lang_label"),
                                   bg=BG_CARD, fg=FG_TEXT,
                                   font=("Segoe UI", 10))
        self._lang_lbl.pack(side="left", padx=(0, 10))
        lang_display = tk.StringVar(value="Deutsch")
        lc = ttk.Combobox(lr, textvariable=lang_display,
                           values=list(LANGS.keys()),
                           state="readonly", width=18)
        lc.pack(side="left")

        def on_lang(e=None):
            self._lang.set(LANGS.get(lang_display.get(), "de"))
            self._refresh_all_labels()

        lc.bind("<<ComboboxSelected>>", on_lang)

        self._restart_hint = tk.Label(sc.inner, text=self.t("restart_hint"),
                                       bg=BG_CARD, fg=FG_LABEL,
                                       font=("Segoe UI", 9, "italic"))
        self._restart_hint.pack(anchor="w", padx=14, pady=(0, 12))

        bc = Card(p)
        bc.pack(fill="x", padx=6, pady=(0, 6))
        self._bat_lbl = tk.Label(bc.inner, text=self.t("bat_path_label"),
                                  bg=BG_CARD, fg=ACCENT,
                                  font=("Segoe UI", 10, "bold"))
        self._bat_lbl.pack(anchor="w", padx=14, pady=(12, 4))
        bar = tk.Frame(bc.inner, bg=BG_CARD)
        bar.pack(fill="x", padx=14, pady=(0, 12))
        ttk.Entry(bar, textvariable=self.bat_path).pack(
            side="left", fill="x", expand=True, padx=(0, 8))
        self._bat_choose_btn = ttk.Button(bar, text=self.t("choose_bat"),
                                           style="Neu.TButton",
                                           command=self._choose_bat_path)
        self._bat_choose_btn.pack(side="left")

    # ═══════════════════════════════════════════════════════════
    #  BEFEHL BAUEN
    # ═══════════════════════════════════════════════════════════
    def _build_command(self) -> str:
        src, dst = self._src, self._dst
        exe = self.imap_exe.get().strip().strip('"') or "imapsync"
        # Leerzeichen im Pfad? -> quoten, sonst ohne Anführungszeichen
        parts = [f'"{exe}"' if " " in exe else exe]

        # WICHTIG: parts.extend() statt parts += damit kein UnboundLocalError
        def q(s):
            """Wert quoten; bestehende Quotes zuerst entfernen."""
            return '"'  + s.strip().strip('"') + '"'

        def add_srv(sv, n):
            parts.extend([f"--host{n}", q(sv["host"].get()),
                          f"--user{n}", q(sv["user"].get()),
                          f"--password{n}", q(sv["pass"].get()),
                          f"--port{n}", sv["port"].get().strip()])
            if sv["ssl"].get(): parts.append(f"--ssl{n}")
            if sv["tls"].get(): parts.append(f"--tls{n}")

        add_srv(src, 1)
        add_srv(dst, 2)

        if self.dry.get():
            parts.append("--dry")

        for key, (var, flag, *_) in self._opt_widgets.items():
            if var.get():
                parts.append(flag)

        # Ordner aus Treeview-Auswahl holen
        selected = [path for iid, (var, path) in self._tv_checked.items()
                    if var.get()]
        if selected:
            fflag = "--include" if self._folder_mode.get() == "include" else "--exclude"
            for folder in selected:
                parts.extend([fflag, f'"{folder}"'])

        extra = self.extra_args.get().strip()
        if extra:
            parts.append(extra)

        return " ".join(parts)

    # ═══════════════════════════════════════════════════════════
    #  AKTIONEN
    # ═══════════════════════════════════════════════════════════
    def _generate_bat(self):
        if not self._src["host"].get() or not self._dst["host"].get():
            messagebox.showwarning("", self.t("err_fields"))
            return
        try:
            cmd = self._build_command()
        except Exception as ex:
            messagebox.showerror("Fehler in _build_command", str(ex))
            return
        bat = f"@echo off\necho IMAPSync wird gestartet...\n{cmd}\npause\n"
        try:
            with open(self.bat_path.get(), "w", encoding="utf-8") as f:
                f.write(bat)
        except Exception as ex:
            messagebox.showerror("", f"{self.t('err_bat_save')}:\n{ex}")
            return
        self.cmd_preview.config(state="normal")
        self.cmd_preview.delete("1.0", "end")
        self.cmd_preview.insert("1.0", cmd)
        self.cmd_preview.config(state="disabled")
        self._log(f"{self.t('msg_bat_saved')}{self.bat_path.get()}\n", "ok")
        self._set_status(self.t("st_saved"), SUCCESS)

    def _run_bat(self):
        bat = self.bat_path.get()
        if not os.path.isfile(bat):
            messagebox.showwarning("", self.t("err_bat_nf"))
            return
        self._run_count += 1
        sep = "═" * 58
        self._log(f"\n{sep}\n  ▶  Run #{self._run_count}\n{sep}\n", "sep")
        self._log(f"{self.t('msg_run_start')}{bat}\n", "info")
        self._set_status(self.t("st_run"), WARNING)
        self._stop_btn.config(state="normal")
        threading.Thread(target=self._run_process, args=(bat,), daemon=True).start()

    def _run_process(self, bat_path):
        try:
            self._process = subprocess.Popen(
                ["cmd.exe", "/c", bat_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW)
            for line in self._process.stdout:
                lo = line.lower()
                tag = ("err"  if any(w in lo for w in ["error","fehler","failed"]) else
                       "warn" if "warn" in lo else
                       "ok"   if any(w in lo for w in ["ok","done","success","completed"]) else
                       None)
                self._log(line, tag)
            self._process.wait()
            rc = self._process.returncode
            if rc == 0:
                self._log(f"\n{self.t('msg_done')}\n", "ok")
                self._set_status(self.t("st_done"), SUCCESS)
            else:
                self._log(f"\n{self.t('msg_exit')}{rc}\n", "warn")
                self._set_status(f"{self.t('st_err')} (Exit {rc})", WARNING)
        except Exception as ex:
            self._log(f"\n{self.t('msg_err')}{ex}\n", "err")
            self._set_status(self.t("st_err"), DANGER)
        finally:
            self.after(0, lambda: self._stop_btn.config(state="disabled"))
            self._process = None

    def _stop_process(self):
        if self._process:
            self._process.terminate()
            self._log(f"\n{self.t('msg_stopped')}\n", "warn")
            self._set_status(self.t("st_stop"), WARNING)

    # ═══════════════════════════════════════════════════════════
    #  PROFILE
    # ═══════════════════════════════════════════════════════════
    def _profile_to_dict(self):
        return {
            "src":  {k: v.get() for k, v in self._src.items()},
            "dst":  {k: v.get() for k, v in self._dst.items()},
            "opts": {k: var.get() for k, (var, *_) in self._opt_widgets.items()},
            "dry":  self.dry.get(),
            "extra_args": self.extra_args.get(),
            "bat_path":   self.bat_path.get(),
            "imap_exe":   self.imap_exe.get(),
            "folder_mode": self._folder_mode.get(),
        }

    def _dict_to_profile(self, data):
        def apply(d, saved):
            for k, v in saved.items():
                if k in d: d[k].set(v)
        apply(self._src, data.get("src", {}))
        apply(self._dst, data.get("dst", {}))
        for k, val in data.get("opts", {}).items():
            if k in self._opt_widgets:
                self._opt_widgets[k][0].set(val)
        self.dry.set(data.get("dry", False))
        self.extra_args.set(data.get("extra_args", ""))
        self.bat_path.set(data.get("bat_path", ""))
        self.imap_exe.set(data.get("imap_exe", "imapsync"))
        self._folder_mode.set(data.get("folder_mode", "include"))

    def _save_profile(self):
        name = self._ask_profile_name()
        if not name:
            return
        path = os.path.join(self.profiles_dir, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._profile_to_dict(), f, indent=2, ensure_ascii=False)
        self._log(f"💾  Profil gespeichert: {name}\n", "ok")
        self._load_profile_list()

    def _load_profile(self):
        sel = self.profile_tree.selection()
        if not sel:
            messagebox.showinfo("", self.t("no_profile"))
            return
        tag = self.profile_tree.item(sel[0], "tags")
        fname = tag[0] if tag else None
        if not fname:
            return
        with open(os.path.join(self.profiles_dir, fname), encoding="utf-8") as f:
            self._dict_to_profile(json.load(f))
        self._log(f"📂  Profil geladen: {fname}\n", "info")

    def _delete_profile(self):
        sel = self.profile_tree.selection()
        if not sel:
            return
        tag = self.profile_tree.item(sel[0], "tags")
        fname = tag[0] if tag else None
        if not fname:
            return
        if messagebox.askyesno("", self.t("confirm_del")):
            os.remove(os.path.join(self.profiles_dir, fname))
            self._load_profile_list()
            self._log(f"🗑  Profil gelöscht: {fname}\n", "warn")

    def _load_profile_list(self):
        for row in self.profile_tree.get_children():
            self.profile_tree.delete(row)
        for fname in sorted(os.listdir(self.profiles_dir)):
            if not fname.endswith(".json"):
                continue
            try:
                with open(os.path.join(self.profiles_dir, fname), encoding="utf-8") as f:
                    d = json.load(f)
                self.profile_tree.insert("", "end",
                    values=(d.get("src",{}).get("host",""),
                            d.get("dst",{}).get("host",""),
                            d.get("src",{}).get("user","")),
                    tags=(fname,))
            except Exception:
                pass

    def _ask_profile_name(self):
        dlg = tk.Toplevel(self)
        dlg.title("")
        dlg.configure(bg=BG_CARD)
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.geometry("360x150")
        tk.Label(dlg, text=self.t("p_name"),
                 bg=BG_CARD, fg=FG_TEXT,
                 font=("Segoe UI", 10)).pack(pady=(22, 6))
        var = tk.StringVar(value=self._src["host"].get() or "profil1")
        e = ttk.Entry(dlg, textvariable=var, width=34)
        e.pack()
        e.focus_set()
        result = [None]
        def ok():
            result[0] = var.get().strip().replace(" ", "_")
            dlg.destroy()
        ttk.Button(dlg, text=self.t("p_save_btn"), style="Acc.TButton",
                   command=ok).pack(pady=14)
        dlg.wait_window()
        return result[0]

    # ═══════════════════════════════════════════════════════════
    #  HILFSMETHODEN
    # ═══════════════════════════════════════════════════════════
    def _log(self, msg, tag=None):
        def _w():
            self.log.config(state="normal")
            self.log.insert("end", msg, tag or "")
            self.log.see("end")
            self.log.config(state="disabled")
        self.after(0, _w)

    def _set_status(self, msg, color=FG_LABEL):
        self.after(0, lambda: (self.status_var.set(msg),
                               self._status_lbl.config(foreground=color)))

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
        self._run_count = 0

    def _copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self._build_command())
        self._set_status(self.t("st_copied"), SUCCESS)

    def _browse_exe(self):
        path = filedialog.askopenfilename(
            filetypes=[("Executable", "*.exe *.pl *"),
                       ("Alle Dateien", "*.*")])
        if path:
            self.imap_exe.set(path)

    def _choose_bat_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".bat",
            filetypes=[("Batch-Datei", "*.bat"), ("Alle", "*.*")])
        if path:
            self.bat_path.set(path)

    # ═══════════════════════════════════════════════════════════
    #  ABOUT – Daten laden
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def _load_about() -> dict:
        """Eingebettete Standarddaten – werden von about.json im Programmordner überschrieben."""
        # ── Eingebettete Defaults (Logo bereits drin) ──────────────
        embedded = {
            "name":     "Steve Rückwardt - TAS LEX-Partner.Net",
            "email":    "info@lex-blog.de",
            "blog":     "https://lex-blog.de",
            "version":  "0.3.0",
            "logo_b64": "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"
        }
        # ── Optionale about.json überschreibt einzelne Felder ──────
        if getattr(sys, "frozen", False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "about.json")
        try:
            with open(path, encoding="utf-8") as f:
                embedded.update(json.load(f))
        except FileNotFoundError:
            pass
        except Exception as ex:
            print(f"[about.json] Fehler: {ex}")
        return embedded

    # ═══════════════════════════════════════════════════════════
    #  TAB 7 – ÜBER / ABOUT
    # ═══════════════════════════════════════════════════════════
    def _build_about(self):
        import webbrowser, io
        p = self._f_about
        d = self._about_data
        imapsync_url = "https://imapsync.lamiral.info"

        # ── Grid-Layout: Banner oben, zwei Karten darunter ────
        p.columnconfigure(0, weight=1)
        p.columnconfigure(1, weight=1)
        p.rowconfigure(1, weight=1)

        # ══════════════════════════════════════════════════════
        # ZEILE 0 – Logo-Banner (volle Breite)
        # ══════════════════════════════════════════════════════
        banner = tk.Frame(p, bg=BG_CARD)
        banner.grid(row=0, column=0, columnspan=2,
                    sticky="ew", padx=6, pady=(6, 0))

        # Logo als vorbereitetes PNG direkt in tk.PhotoImage –
        # kein Pillow zur Laufzeit nötig
        LOGO_B64 = "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"
        try:
            self._about_logo_img = tk.PhotoImage(data=LOGO_B64)
            tk.Label(banner, image=self._about_logo_img,
                     bg=BG_CARD).pack(side="left", padx=24, pady=14)
        except Exception as ex:
            print(f"[logo] {ex}")
            tk.Label(banner, text="📧  IMAPSync GUI",
                     bg=BG_CARD, fg=ACCENT,
                     font=("Segoe UI", 22, "bold")).pack(
                side="left", padx=24, pady=14)

        self._about_ver_lbl = tk.Label(
            banner, text=f"v {d.get('version', '0.3.0')}",
            bg=BG_CARD, fg=FG_LABEL, font=("Segoe UI", 11))
        self._about_ver_lbl.pack(side="right", padx=24)

        # ══════════════════════════════════════════════════════
        # ZEILE 1 LINKS – Über das Tool
        # ══════════════════════════════════════════════════════
        left_card = Card(p)
        left_card.grid(row=1, column=0, sticky="nsew",
                       padx=(6, 3), pady=6)
        lc = left_card.inner
        lc.columnconfigure(0, weight=1)

        self._about_title_lbl = tk.Label(
            lc, text=self.t("about_title"),
            bg=BG_CARD, fg=ACCENT,
            font=("Segoe UI", 13, "bold"), anchor="w")
        self._about_title_lbl.pack(anchor="w", padx=20, pady=(20, 4))
        tk.Frame(lc, bg=ACCENT, height=2).pack(fill="x", padx=20, pady=(0, 16))

        self._about_desc_lbl = tk.Label(
            lc, text=self.t("about_desc"),
            bg=BG_CARD, fg=FG_TEXT, font=("Segoe UI", 10),
            wraplength=400, justify="left", anchor="nw")
        self._about_desc_lbl.pack(anchor="w", padx=20, pady=(0, 20))

        tk.Frame(lc, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 14))

        # IMAPSync-Link – vollständig übersetzt
        link_row = tk.Frame(lc, bg=BG_CARD)
        link_row.pack(anchor="w", padx=20, pady=(0, 20))
        self._about_based_lbl = tk.Label(
            link_row, text=f"🔗  {self.t('about_based_on')}  ",
            bg=BG_CARD, fg=FG_LABEL, font=("Segoe UI", 9))
        self._about_based_lbl.pack(side="left")
        self._about_imap_lbl = tk.Label(
            link_row, text=imapsync_url,
            bg=BG_CARD, fg=ACCENT,
            font=("Segoe UI", 9, "underline"), cursor="hand2")
        self._about_imap_lbl.pack(side="left")
        self._about_imap_lbl.bind(
            "<Button-1>", lambda e: webbrowser.open(imapsync_url))

        # ── Lizenzhinweis ────────────────────────────────────
        tk.Frame(lc, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 14))
        lic_row = tk.Frame(lc, bg=BG_CARD)
        lic_row.pack(anchor="w", padx=20, pady=(0, 20))
        tk.Label(lic_row, text="⚖  ",
                 bg=BG_CARD, fg=FG_LABEL,
                 font=("Segoe UI", 9)).pack(side="left")
        lic_url = "https://www.gnu.org/licenses/gpl-3.0"
        lic_lbl = tk.Label(
            lic_row, text="GNU General Public License v3.0",
            bg=BG_CARD, fg=ACCENT,
            font=("Segoe UI", 9, "underline"), cursor="hand2")
        lic_lbl.pack(side="left")
        lic_lbl.bind("<Button-1>", lambda e: webbrowser.open(lic_url))
        tk.Label(lic_row,
                 text="  © 2026 Steve Rückwardt – lex-blog.de",
                 bg=BG_CARD, fg=FG_LABEL,
                 font=("Segoe UI", 9)).pack(side="left")

        # ══════════════════════════════════════════════════════
        # ZEILE 1 RECHTS – Kontakt
        # ══════════════════════════════════════════════════════
        right_card = Card(p)
        right_card.grid(row=1, column=1, sticky="nsew",
                        padx=(3, 6), pady=6)
        rc = right_card.inner

        # Kontakt-Titel übersetzt
        self._about_contact_title_lbl = tk.Label(
            rc, text=f"👤  {self.t('about_contact_title')}",
            bg=BG_CARD, fg=ACCENT,
            font=("Segoe UI", 13, "bold"), anchor="w")
        self._about_contact_title_lbl.pack(anchor="w", padx=20, pady=(20, 4))
        tk.Frame(rc, bg=ACCENT, height=2).pack(fill="x", padx=20, pady=(0, 20))

        self._about_contact_lbls = []   # (label_widget, key) für Refresh

        def contact_row(icon_text, label_key, value, url=None):
            """Einheitliches Grid-Layout: Icon | Label | Wert"""
            row = tk.Frame(rc, bg=BG_CARD)
            row.pack(anchor="w", fill="x", padx=20, pady=8)
            tk.Label(row, text=icon_text,
                     bg=BG_CARD, fg=ACCENT,
                     font=("Segoe UI", 11),
                     width=3, anchor="center").grid(
                row=0, column=0, sticky="w")
            lbl = tk.Label(row, text=self.t(label_key),
                     bg=BG_CARD, fg=FG_LABEL,
                     font=("Segoe UI", 9, "bold"),
                     width=12, anchor="w")
            lbl.grid(row=0, column=1, sticky="w", padx=(4, 12))
            self._about_contact_lbls.append((lbl, label_key))
            if url:
                val_lbl = tk.Label(row, text=value,
                                   bg=BG_CARD, fg=ACCENT,
                                   font=("Segoe UI", 10, "underline"),
                                   cursor="hand2", anchor="w")
                val_lbl.grid(row=0, column=2, sticky="w")
                val_lbl.bind("<Button-1>",
                             lambda e, u=url: webbrowser.open(u))
            else:
                tk.Label(row, text=value,
                         bg=BG_CARD, fg=FG_TEXT,
                         font=("Segoe UI", 10), anchor="w").grid(
                    row=0, column=2, sticky="w")
            row.columnconfigure(2, weight=1)

        contact_row("◉",  "about_author",  d.get("name",  "–"))
        contact_row("@",  "about_contact", d.get("email", "–"),
                    url=f"mailto:{d.get('email','')}")
        contact_row("↗",  "about_blog",    d.get("blog",  "–"),
                    url=d.get("blog", ""))

    # ── About-Labels bei Sprachwechsel aktualisieren ─────────
    def _refresh_about_labels(self):
        d = self._about_data
        self._about_title_lbl.config(text=self.t("about_title"))
        self._about_ver_lbl.config(text=f"v {d.get('version','0.3.0')}")
        self._about_desc_lbl.config(text=self.t("about_desc"))
        self._about_based_lbl.config(
            text=f"🔗  {self.t('about_based_on')}  ")
        self._about_contact_title_lbl.config(
            text=f"👤  {self.t('about_contact_title')}")
        for lbl, key in self._about_contact_lbls:
            lbl.config(text=self.t(key))


# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = IMAPSyncApp()
    app.mainloop()
