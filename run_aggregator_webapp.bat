@echo off
chcp 65001 > nul
title Chay WebApp - Du An Suc Khoe Mr Phi
echo =======================================================
echo   KHOI DONG HE THONG TONG HOP TAI LIEU - MR PHI
echo =======================================================
echo Dang mo WebApp tai: http://localhost:8502 ...
cd /d "%~dp0"
python -m streamlit run webapp_aggregator.py --server.port 8502 --browser.gatherUsageStats false
pause
