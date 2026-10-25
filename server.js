'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const root = path.resolve(__dirname);
const port = Number(process.env.PORT || 4186);
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.wav': 'audio/wav', '.ogg': 'audio/ogg', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.md': 'text/plain; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  let name;
  try { name = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); } catch (_) { res.writeHead(400); return res.end('Bad request'); }
  const file = path.resolve(root, '.' + (name === '/' ? '/index.html' : name));
  const relative = path.relative(root, file);
  if (relative.startsWith('..') || path.isAbsolute(relative) || relative.split(path.sep).some(p => p.startsWith('.'))) { res.writeHead(403); return res.end('Forbidden'); }
  if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405); return res.end('Method not allowed'); }
  fs.stat(file, (error, stat) => {
    if (error || !stat.isFile()) { res.writeHead(404); return res.end('Not found'); }
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
    if (req.method === 'HEAD') return res.end();
    const stream = fs.createReadStream(file); stream.on('error', () => res.destroy()); stream.pipe(res);
  });
});
server.on('error', error => { console.error(error.code === 'EADDRINUSE' ? `端口 ${port} 已被使用。可在 PowerShell 设置 $env:PORT=4174 后重试。` : error.message); process.exitCode = 1; });
server.listen(port, '0.0.0.0', () => {
  if (process.env.EMBER_OPEN_GAME === '1' && process.platform === 'win32') {
    require('node:child_process').execFile('rundll32.exe', ['url.dll,FileProtocolHandler', `http://localhost:${port}`], { windowsHide: true }, () => {});
  }
  console.log('\n余烬防线 · 本地试玩服务\n');
  console.log(`电脑打开  http://localhost:${port}`);
  for (const entries of Object.values(os.networkInterfaces())) for (const item of entries || []) if (item.family === 'IPv4' && !item.internal) console.log(`手机候选地址  http://${item.address}:${port}`);
  console.log('\n手机与电脑连接同一 Wi-Fi。如系统询问，请仅允许专用网络访问。\n此服务仅用于可信局域网开发，请勿做公网端口映射。\n按 Ctrl+C 停止。\n');
});


