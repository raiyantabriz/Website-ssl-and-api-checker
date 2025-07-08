@echo off
taskkill /f /im ngrok.exe > nul 2>&1
start flask run --host=0.0.0.0 --port=5000
timeout /t 5
ngrok start --all --config=ngrok.yml
pause