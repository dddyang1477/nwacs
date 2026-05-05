# NWACS FINAL - PowerShell Fix Script v2
# Usage: .\apply_fix_v2.ps1

Write-Host "============================================================"
Write-Host "NWACS FINAL - Three-Time Quality Check Fix Script v2"
Write-Host "============================================================"
Write-Host ""

$BasePath = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $BasePath) {
    $BasePath = Get-Location
}
$MainFile = Join-Path $BasePath "NWACS_FINAL.py"

Write-Host "[1/3] Checking if fix is needed..."

# Read main file
$content = Get-Content $MainFile -Raw -Encoding UTF8

# Check if already fixed
if ($content -match "call_three_time_quality_check") {
    Write-Host "  [ALREADY] Three-time check is already integrated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "============================================================"
    Write-Host "Fix already applied. No action needed." -ForegroundColor Green
    Write-Host "============================================================"
    exit 0
}

Write-Host "  [NEED FIX] Three-time check not found, will apply fix now."
Write-Host ""

Write-Host "[2/3] Applying fix by line number..."

# Get file as array of lines
$lines = Get-Content $MainFile -Encoding UTF8
$totalLines = $lines.Count

Write-Host "  Total lines: $totalLines"

# Find the exact line with "集成质量检测功能"
$startLine = -1
for ($i = 0; $i -lt $totalLines; $i++) {
    if ($lines[$i] -match "集成质量检测功能") {
        $startLine = $i + 1  # PowerShell is 1-indexed
        Write-Host "  Found target at line: $startLine"
        break
    }
}

if ($startLine -eq -1) {
    Write-Host "  [ERROR] Cannot find target code" -ForegroundColor Red
    exit 1
}

# Find the end of the try block (next "except" at same indentation)
$endLine = $startLine
$indentLevel = 0
$foundTry = $false
for ($i = $startLine; $i -lt $totalLines; $i++) {
    $line = $lines[$i]

    if ($line -match "^\s*try:") {
        $foundTry = $true
        $indentLevel = ($line -replace "try:", "").Length - ($line.Length - $line.TrimStart().Length)
    }

    if ($foundTry -and $line -match "^\s*except\s+Exception") {
        $endLine = $i + 1  # Include the except line
        break
    }
}

Write-Host "  Block to replace: lines $startLine to $endLine"

# Create new replacement code
$newCode = @'
        # 3. Integrate three-time quality check process
        print("\n" + "="*60)
        print("Starting three-time quality check process...")
        print("   Up to 3 checks, will reprocess if failed")
        print("="*60)

        try:
            # Import three-time check module
            from three_time_quality_check import call_three_time_quality_check

            # Use complete three-time check process
            processed_opening, quality_passed, quality_report = call_three_time_quality_check(
                processed_opening,
                chapter_num=1,
                novel_title=novel_name
            )

            if quality_passed:
                print("All three checks passed!")
            else:
                print("Warning: Not all checks passed, saved anyway, suggest manual review")

        except Exception as e:
            print(f"Three-time check error: {e}")
            print("   Falling back to basic quality check...")
            try:
                from quality_check_and_save_v2 import QualityChecker
                checker = QualityChecker(processed_opening, 1)
                passed, report = checker.run_all_checks()

                if not passed:
                    print("Warning: Quality check suggests manual review")
            except Exception as e2:
                print(f"Quality check module skipped: {e2}")
'@

# Replace lines
$newLines = @()
for ($i = 0; $i -lt $totalLines; $i++) {
    $lineNum = $i + 1

    if ($lineNum -ge $startLine -and $lineNum -le $endLine) {
        # Insert new code at startLine
        if ($lineNum -eq $startLine) {
            $newLines += $newCode -split "`n"
        }
    } else {
        $newLines += $lines[$i]
    }
}

# Write back
$newLines | Set-Content $MainFile -Encoding UTF8

Write-Host "  [OK] File updated!" -ForegroundColor Green
Write-Host ""

Write-Host "[3/3] Verifying fix..."

# Verify
$verify = Get-Content $MainFile -Raw -Encoding UTF8
if ($verify -match "call_three_time_quality_check") {
    Write-Host "  [OK] Verification passed!" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Verification failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================"
Write-Host "Fix completed successfully!" -ForegroundColor Green
Write-Host "Now you can run: python NWACS_FINAL.py"
Write-Host "============================================================"
Write-Host ""

exit 0
