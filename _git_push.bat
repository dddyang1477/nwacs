@echo off
cd /d "d:\Trae CN\github\nwacs\nwacs"
echo === Step 1: git init === > _git_result.txt
git init >> _git_result.txt 2>&1
echo === Step 2: git add === >> _git_result.txt
git add -A >> _git_result.txt 2>&1
echo === Step 3: git commit === >> _git_result.txt
git commit -m "NWACS v8 - Full project upload" >> _git_result.txt 2>&1
echo === Step 4: git remote === >> _git_result.txt
git remote add origin https://github.com/dddyang1477/NWACS.git >> _git_result.txt 2>&1
echo === Step 5: git push === >> _git_result.txt
git push -u origin master --force >> _git_result.txt 2>&1
echo === DONE === >> _git_result.txt
type _git_result.txt