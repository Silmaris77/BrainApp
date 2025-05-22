@echo off
echo Uruchamianie aplikacji Neuroliderzy z nowym systemem UI...
echo -----------------------------------------------------

:: Ustaw katalog roboczy na katalog ze skryptem
cd /d %~dp0

:: Uruchom aplikację z nową wersją głównego pliku
streamlit run main_ui.py
