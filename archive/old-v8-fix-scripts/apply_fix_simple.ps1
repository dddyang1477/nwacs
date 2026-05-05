# NWACS FINAL - Simple PowerShell Fix Script
# Usage: .\apply_fix_simple.ps1

Write-Host "============================================================"
Write-Host "NWACS FINAL - Three-Time Quality Check Fix Script"
Write-Host "============================================================"
Write-Host ""

$BasePath = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $BasePath) {
    $BasePath = Get-Location
}
$MainFile = Join-Path $BasePath "NWACS_FINAL.py"

Write-Host "[1/3] Checking system integrity..."
Write-Host ""

$RequiredFiles = @(
    "NWACS_FINAL.py",
    "ai_detector_and_rewriter.py",
    "quality_check_and_save_v2.py",
    "three_time_quality_check.py"
)

$AllExist = $true
foreach ($file in $RequiredFiles) {
    $filepath = Join-Path $BasePath $file
    if (Test-Path $filepath) {
        $size = (Get-Item $filepath).Length
        Write-Host "  [OK] $file ($size bytes)"
    } else {
        Write-Host "  [MISSING] $file"
        $AllExist = $false
    }
}

if (-not $AllExist) {
    Write-Host ""
    Write-Host "[ERROR] System check failed. Some files are missing." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] All core files exist."
Write-Host ""

Write-Host "[2/3] Applying fix..."

# Read main file
$content = Get-Content $MainFile -Raw -Encoding UTF8

# Check if already fixed
if ($content -match "from three_time_quality_check") {
    Write-Host "  [SKIP] Already has three-time check, skipping."
} else {
    # Old code
    $oldCode = '        # 3. Integrate quality check function
        try:
            from quality_check_and_save_v2 import QualityChecker
            checker = QualityChecker(processed_opening, 1)
            passed, report = checker.run_all_checks()

            if not passed:
                print("Warning: Quality check suggests manual review")
        except Exception as e:
            print(f"Quality check module skipped: {e}")'

    # New code (three-time check)
    $newCode = '        # 3. Integrate three-time quality check process
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
                print(f"Quality check module skipped: {e2}")'

    # Execute replace
    if ($content -match [regex]::Escape($oldCode)) {
        $content = $content -replace [regex]::Escape($oldCode), $newCode

        # Save file
        $content | Set-Content $MainFile -Encoding UTF8 -NoNewline

        Write-Host "  [OK] Fix applied successfully!" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] Cannot find code to replace" -ForegroundColor Red
        Write-Host "  Code may have been modified already or format is different"
        exit 1
    }
}

Write-Host ""
Write-Host "[3/3] Verifying fix..."

# Verify
$verify = Get-Content $MainFile -Raw -Encoding UTF8
if ($verify -match "from three_time_quality_check import call_three_time_quality_check") {
    Write-Host "  [OK] Verification passed!" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Verification failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================"
Write-Host "Fix completed! Now you can run: python NWACS_FINAL.py" -ForegroundColor Green
Write-Host "============================================================"
Write-Host ""

exit 0
