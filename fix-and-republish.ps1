# 修复包名并重新发布脚本

Write-Host "=== 修复包名并重新发布 ===" -ForegroundColor Green
Write-Host ""

# 1. 删除旧的构建文件
Write-Host "步骤 1: 清理旧的构建文件..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist
    Write-Host "  ✓ 已删除 dist/" -ForegroundColor Green
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force build
    Write-Host "  ✓ 已删除 build/" -ForegroundColor Green
}
if (Test-Path "*.egg-info") {
    Remove-Item -Recurse -Force *.egg-info
    Write-Host "  ✓ 已删除 egg-info/" -ForegroundColor Green
}

Write-Host ""

# 2. 删除旧的 Git Tag
Write-Host "步骤 2: 删除旧的 Tag (v1.0.0)..." -ForegroundColor Yellow
try {
    git tag -d v1.0.0 2>$null
    Write-Host "  ✓ 已删除本地 Tag" -ForegroundColor Green
} catch {
    Write-Host "  - 本地 Tag 不存在" -ForegroundColor Gray
}

try {
    git push origin :refs/tags/v1.0.0 2>$null
    Write-Host "  ✓ 已删除远程 Tag" -ForegroundColor Green
} catch {
    Write-Host "  - 远程 Tag 不存在或已删除" -ForegroundColor Gray
}

Write-Host ""

# 3. 提交修改
Write-Host "步骤 3: 提交包名修改..." -ForegroundColor Yellow
git add setup.py pyproject.toml
git commit -m "fix: change package name to mcp-data-analysis-server"
Write-Host "  ✓ 已提交修改" -ForegroundColor Green

Write-Host ""

# 4. 推送到 GitHub
Write-Host "步骤 4: 推送到 GitHub..." -ForegroundColor Yellow
git push origin main
Write-Host "  ✓ 已推送代码" -ForegroundColor Green

Write-Host ""

# 5. 创建新的 Tag
Write-Host "步骤 5: 创建新的 Tag (v1.0.0)..." -ForegroundColor Yellow
git tag -a v1.0.0 -m "Release v1.0.0 with fixed package name"
git push origin v1.0.0
Write-Host "  ✓ 已创建并推送 Tag" -ForegroundColor Green

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "✓ 完成！" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "新的包名: mcp-data-analysis-server" -ForegroundColor Cyan
Write-Host "GitHub Actions 将自动重新构建和发布" -ForegroundColor Cyan
Write-Host ""
Write-Host "查看进度:" -ForegroundColor Yellow
Write-Host "  https://github.com/BACH-AI-Tools/data-analysis-mcp/actions" -ForegroundColor Blue
Write-Host ""
Write-Host "发布后安装:" -ForegroundColor Yellow
Write-Host "  pip install mcp-data-analysis-server" -ForegroundColor Blue
Write-Host ""

