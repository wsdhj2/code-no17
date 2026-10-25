$ErrorActionPreference = 'Stop'
$gameUrl = 'http://localhost:4186'
try {
    $runningGame = Invoke-WebRequest -Uri $gameUrl -UseBasicParsing -TimeoutSec 2
    if ($runningGame.Content -match 'engine.js' -and $runningGame.Content -match 'frontline.js') {
        Start-Process $gameUrl
        Write-Host '游戏服务已在运行。已打开浏览器。'
        exit 0
    }
} catch {}
$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) { $gameNodePath = $node.Source } else { $gameNodePath = 'C:\Users\31681\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' }
if (-not (Test-Path -LiteralPath $gameNodePath)) { throw '没有找到 Node.js。可以直接双击 index.html 离线游玩。' }
$env:EMBER_OPEN_GAME = '1'
& $gameNodePath "$PSScriptRoot\server.js"
