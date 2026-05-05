# NWACS FINAL - PowerShell修复脚本
# 运行方式：在PowerShell中运行
# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
# .\apply_fix.ps1

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  NWACS FINAL - 三次质量检验PowerShell修复脚本" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

$BasePath = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $BasePath) {
    $BasePath = Get-Location
}
$MainFile = Join-Path $BasePath "NWACS_FINAL.py"

Write-Host "[1/3] 检查系统完整性..." -ForegroundColor Yellow

$RequiredFiles = @(
    @{Name="NWACS_FINAL.py"; Desc="主程序"},
    @{Name="ai_detector_and_rewriter.py"; Desc="AI去痕模块"},
    @{Name="quality_check_and_save_v2.py"; Desc="质量检测模块"},
    @{Name="three_time_quality_check.py"; Desc="三次检验模块"}
)

$AllExist = $true
foreach ($file in $RequiredFiles) {
    $filepath = Join-Path $BasePath $file.Name
    if (Test-Path $filepath) {
        $size = (Get-Item $filepath).Length
        Write-Host "  [OK] $($file.Name) ($size bytes) - $($file.Desc)" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $($file.Name) - $($file.Desc)" -ForegroundColor Red
        $AllExist = $false
    }
}

if (-not $AllExist) {
    Write-Host "`n[ERROR] 系统检查失败，缺少部分核心文件" -ForegroundColor Red
    exit 1
}

Write-Host "`n[OK] 所有核心文件都存在" -ForegroundColor Green

Write-Host "`n[2/3] 应用修复..." -ForegroundColor Yellow

# 读取主文件
$content = Get-Content $MainFile -Raw -Encoding UTF8

# 检查是否已经修复
if ($content -match "from three_time_quality_check") {
    Write-Host "  [SKIP] 已检测到三次检验集成，跳过修复" -ForegroundColor Cyan
} else {
    # 旧代码
    $oldCode = @'
        # 3. 集成质量检测功能
        try:
            from quality_check_and_save_v2 import QualityChecker
            checker = QualityChecker(processed_opening, 1)
            passed, report = checker.run_all_checks()

            if not passed:
                print("⚠️ 质量检测提示：建议后续人工完善内容")
        except Exception as e:
            print(f"⚠️ 质量检测模块加载跳过: {e}")
'@

    # 新代码（三次检验）
    $newCode = @'
        # 3. 集成质量检测功能（使用三次检验流程）
        print("\n" + "="*60)
        print("🔍 开始三次质量检验流程...")
        print("   最多检验3次，不合格将重新处理")
        print("="*60)

        try:
            # 导入三次检验模块
            from three_time_quality_check import call_three_time_quality_check

            # 使用完整的三次检验流程
            processed_opening, quality_passed, quality_report = call_three_time_quality_check(
                processed_opening,
                chapter_num=1,
                novel_title=novel_name
            )

            if quality_passed:
                print("✅ 三次检验全部通过！")
            else:
                print("⚠️ 三次检验未完全通过，已生成并保存，建议人工审核")

        except Exception as e:
            print(f"⚠️ 三次检验流程执行: {e}")
            print("   回退到基础质量检测...")
            try:
                from quality_check_and_save_v2 import QualityChecker
                checker = QualityChecker(processed_opening, 1)
                passed, report = checker.run_all_checks()

                if not passed:
                    print("⚠️ 质量检测提示：建议后续人工完善内容")
            except Exception as e2:
                print(f"⚠️ 质量检测模块加载跳过: {e2}")
'@

    # 执行替换
    if ($content -match [regex]::Escape($oldCode)) {
        $content = $content -replace [regex]::Escape($oldCode), $newCode

        # 保存文件
        $content | Set-Content $MainFile -Encoding UTF8 -NoNewline

        Write-Host "  [OK] 修复成功！三次质量检验已集成" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] 找不到需要替换的代码段" -ForegroundColor Red
        Write-Host "  可能代码已经被修改或格式不同" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n[3/3] 验证修复..." -ForegroundColor Yellow

# 验证
$verify = Get-Content $MainFile -Raw -Encoding UTF8
if ($verify -match "from three_time_quality_check import call_three_time_quality_check") {
    Write-Host "  [OK] 验证通过！三次检验已集成" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] 验证失败" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  修复完成！现在可以运行: python NWACS_FINAL.py" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

exit 0
