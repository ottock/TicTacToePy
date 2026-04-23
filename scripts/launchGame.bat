@echo off
echo +++ LAUNCHING GAME +++
cd /d ..
call .venv\Scripts\activate
python src\main.py
echo +++ ENDING GAME +++