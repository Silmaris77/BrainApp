$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "Uruchamianie aplikacji Neuroliderzy z nowym systemem UI..."
Write-Host "-----------------------------------------------------"

# Uruchom aplikację z nową wersją głównego pliku
streamlit run main_ui.py
