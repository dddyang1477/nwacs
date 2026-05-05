$content = Get-Content "NWACS_FINAL.py" -Raw -Encoding UTF8

if ($content -match "call_three_time_quality_check") {
    Write-Host "Already fixed!"
    exit
}

$old = '        # 3. Integrate quality check function
        try:
            from quality_check_and_save_v2 import QualityChecker
            checker = QualityChecker(processed_opening, 1)
            passed, report = checker.run_all_checks()

            if not passed:
                print("Warning: Quality check suggests manual review")
        except Exception as e:
            print(f"Quality check module skipped: {e}")'

$new = '        # 3. Integrate three-time quality check process
        print("\n" + "="*60)
        print("Starting three-time quality check process...")
        print("   Up to 3 checks, will reprocess if failed")
        print("="*60)

        try:
            from three_time_quality_check import call_three_time_quality_check
            processed_opening, quality_passed, quality_report = call_three_time_quality_check(
                processed_opening,
                chapter_num=1,
                novel_title=novel_name
            )

            if quality_passed:
                print("All three checks passed!")
            else:
                print("Warning: Not all checks passed, suggest manual review")

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

$content = $content -replace [regex]::Escape($old), $new
$content | Set-Content "NWACS_FINAL.py" -Encoding UTF8 -NoNewline
Write-Host "Fix applied!"
