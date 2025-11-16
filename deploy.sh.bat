#!/bin/bash
# Linux/Mac: chmod +x deploy.sh && ./deploy.sh
# Windows: Save as deploy.bat and run

git init
git add .
git commit -m "Initial Nexus v4.1 Release - Full External Cheat"
git branch -M main
git remote add origin https://github.com/luckyluxx1/nexusprib.git
git push -u origin main

echo "✅ Repo deployed! Visit: https://github.com/luckyluxx1/nexusprib"