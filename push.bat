echo off
git status

set /p x="是否继续进行git add? (y/n):"
if %x%==y goto :git
if %x%==n goto :nothing

:git 
git add --all
set /p massage="plz enter commit message>>"
git commit -m "%massage%"
git push origin master
pause

:nothing
echo "nothing changed"
pause
