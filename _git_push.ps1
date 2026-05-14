$ErrorActionPreference = "Stop"
$repoPath = "d:\Trae CN\github\nwacs\nwacs"
$remoteUrl = "https://github.com/dddyang1477/NWACS.git"

try {
    Write-Host "=== Step 1: Initialize Git repository ==="
    Set-Location $repoPath
    git init 2>&1 | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
    
    Write-Host "=== Step 2: Add all files ==="
    git add -A 2>&1 | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
    
    Write-Host "=== Step 3: Create initial commit ==="
    git commit -m "NWACS v8 - Full project upload" 2>&1 | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
    
    Write-Host "=== Step 4: Add remote origin ==="
    git remote add origin $remoteUrl 2>&1 | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
    
    Write-Host "=== Step 5: Force push to overwrite remote ==="
    git push -u origin master --force 2>&1 | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
    
    Write-Host "=== DONE ==="
} catch {
    Write-Host "ERROR: $_"
    $_ | Out-File -FilePath "$repoPath\_git_log.txt" -Encoding utf8 -Append
}