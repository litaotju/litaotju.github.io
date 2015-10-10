git add --all
pause
set /p massage=["plz enter commit message\n>>"]
git commit -m "%massage%"
pause
git push
pause