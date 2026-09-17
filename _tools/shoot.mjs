// Proof renders for the redesign, with the puppeteer-core install and Chrome
// the ASO pipeline already uses (read-only there).
//
//   node _tools/shoot.mjs previews   -> .redesign-preview/<page>-<width>-<theme>.png
//   node _tools/shoot.mjs og         -> og-image.png (1200x630)
//
// Serves the repo over a local HTTP server so relative links, srcset and the
// stylesheet behave as they do on GitHub Pages.
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(path.join(process.env.HOME, 'Developer/ASO/Pdfino/3-pipeline/'));
const puppeteer = require('puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(SITE, '.redesign-preview');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.xml': 'application/xml', '.txt': 'text/plain' };

function serve() {
    const server = http.createServer((req, res) => {
        let file = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file)) { res.writeHead(404); res.end('not found'); return; }
        res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
        fs.createReadStream(file).pipe(res);
    });
    return new Promise((resolve) => server.listen(0, '127.0.0.1', () => resolve(server)));
}

const mode = process.argv[2] || 'previews';
const server = await serve();
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--font-render-hinting=none', '--hide-scrollbars'] });

try {
    if (mode === 'og') {
        const page = await browser.newPage();
        await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
        await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
        await page.goto(`${base}/_tools/og.html`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: path.join(SITE, 'og-image.png'), clip: { x: 0, y: 0, width: 1200, height: 630 } });
        console.log('og-image.png');
    } else {
        fs.mkdirSync(OUT, { recursive: true });
        const pages = ['index', 'terms', 'privacy', 'support'];
        const widths = [390, 1440];
        const themes = ['light', 'dark'];
        for (const name of pages) {
            for (const width of widths) {
                for (const theme of themes) {
                    const page = await browser.newPage();
                    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: theme }, { name: 'prefers-reduced-motion', value: 'reduce' }]);
                    await page.setViewport({ width, height: width === 390 ? 844 : 900, deviceScaleFactor: width === 390 ? 2 : 1 });
                    await page.goto(`${base}/${name}.html`, { waitUntil: 'networkidle0' });
                    // open the FAQ so the answers are in the proof, and load every lazy image
                    await page.$$eval('details', (els) => els.forEach((el) => { el.open = true; }));
                    await page.$$eval('img', (imgs) => Promise.all(imgs.map((img) => { img.loading = 'eager'; return img.decode().catch(() => {}); })));
                    await new Promise((r) => setTimeout(r, 200));
                    // Chrome caps one capture at 16384 device px, so tall pages are shot in
                    // chunks (the sticky header is made static for the capture) and stitched
                    // by _tools/stitch.py into <page>-<width>-<theme>.png.
                    await page.addStyleTag({ content: '.site-header{position:static}' });
                    const height = await page.evaluate(() => document.documentElement.scrollHeight);
                    const dpr = width === 390 ? 2 : 1;
                    const chunk = Math.floor(16000 / dpr);
                    let part = 0;
                    for (let y = 0; y < height; y += chunk, part += 1) {
                        const h = Math.min(chunk, height - y);
                        const file = path.join(OUT, `${name}-${width}-${theme}.part${part}.png`);
                        await page.screenshot({ path: file, clip: { x: 0, y, width, height: h }, captureBeyondViewport: true });
                    }
                    console.log(`${name}-${width}-${theme}: ${height}px in ${part} part(s)`);
                    await page.close();
                }
            }
        }
        // the mobile menu, open
        const page = await browser.newPage();
        await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
        await page.goto(`${base}/index.html`, { waitUntil: 'networkidle0' });
        await page.click('.nav-toggle');
        await new Promise((r) => setTimeout(r, 200));
        await page.screenshot({ path: path.join(OUT, 'index-390-menu-open.png') });
        console.log('.redesign-preview/index-390-menu-open.png');
    }
} finally {
    await browser.close();
    server.close();
}
