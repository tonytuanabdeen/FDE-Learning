'use strict';

/**
 * Minimal zero-dependency static file server for Heroku.
 *
 * Serves the FDE onboarding field guide plus the images/ and assets/ folders.
 * - Listens on the port Heroku assigns via process.env.PORT (defaults to 3000 locally).
 * - "/" returns the field guide HTML so it is the landing page.
 * - Blocks path traversal so only files inside this project can be served.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const ROOT = __dirname;
const PORT = process.env.PORT || 3000;
const DEFAULT_FILE = 'salesforce-fde-onboarding-field-guide.html';

// Only files with these extensions are served; keeps the surface small and safe.
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.webm': 'video/webm',
  '.mp4': 'video/mp4',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain; charset=utf-8',
};

function send(res, status, body, headers) {
  res.writeHead(status, Object.assign({ 'Content-Type': 'text/plain; charset=utf-8' }, headers || {}));
  res.end(body);
}

const server = http.createServer((req, res) => {
  // Decode and normalize the requested path.
  let pathname;
  try {
    pathname = decodeURIComponent(url.parse(req.url).pathname);
  } catch (err) {
    return send(res, 400, 'Bad Request');
  }

  if (pathname === '/') {
    pathname = '/' + DEFAULT_FILE;
  }

  // Resolve against ROOT and reject anything that escapes it (path traversal).
  const filePath = path.join(ROOT, pathname);
  if (filePath !== ROOT && !filePath.startsWith(ROOT + path.sep)) {
    return send(res, 403, 'Forbidden');
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      return send(res, 404, 'Not Found');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext];
    if (!contentType) {
      return send(res, 415, 'Unsupported Media Type');
    }

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'public, max-age=3600',
    });
    fs.createReadStream(filePath)
      .on('error', () => send(res, 500, 'Internal Server Error'))
      .pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`FDE field guide server listening on port ${PORT}`);
});
