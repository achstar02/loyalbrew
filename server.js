const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;
const ROOT = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625';

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(ROOT, req.url === '/' ? '/index.html' : req.url);
  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'text/plain';
  
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('Not Found');
      } else {
        res.writeHead(500);
        res.end('Server Error');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
});

server.listen(PORT, () => console.log('Server running on port ' + PORT));
