$body = @{
    msg_type = "text"
    content = @{
        text = "🧪 NWACS飞书测试消息 - " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    }
} | ConvertTo-Json -Compress

$params = @{
    Uri = "https://open.feishu.cn/open-apis/bot/v2/hook/d22b9add-1188-4593-8bbb-15bc87647a56"
    Method = "Post"
    ContentType = "application/json"
    Body = $body
}

Write-Host "正在发送飞书测试消息..."
Write-Host "URL: $($params.Uri)"
Write-Host "Body: $body"
Write-Host ""

try {
    $response = Invoke-RestMethod @params
    Write-Host "响应: $($response | ConvertTo-Json)"
    if ($response.code -eq 0) {
        Write-Host "✅ 发送成功！" -ForegroundColor Green
    } else {
        Write-Host "❌ 发送失败: $($response.msg)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 发生错误: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
