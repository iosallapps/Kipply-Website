// Lighthouse-style basics by hand: requests (hosts, sizes, failures), console errors,
// cumulative layout shift, and axe-core accessibility violations, per page and theme.
//   AXE=/path/to/axe.min.js node _tools/audit.mjs > .redesign-preview/checks/audit.txt
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(path.join(process.env.HOME, 'Developer/ASO/Pdfino/3-pipeline/'));
const puppeteer = require('puppeteer-core');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const AXE = fs.readFileSync(process.env.AXE, 'utf8');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.xml': 'application/xml' };

const server = http.createServer((req, res) => {
    let file = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!fs.existsSync(file)) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream', 'content-length': fs.statSync(file).size });
    fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });

for (const name of ['index', 'terms', 'privacy', 'support']) {
    for (const [width, theme] of [[390, 'light'], [1440, 'light'], [390, 'dark'], [1440, 'dark']]) {
        const page = await browser.newPage();
        const requests = [];
        const errors = [];
        page.on('response', (r) => requests.push({ url: r.url(), status: r.status(), size: Number(r.headers()['content-length'] || 0) }));
        page.on('requestfailed', (r) => errors.push(`request failed: ${r.url()}`));
        page.on('console', (m) => { if (m.type() === 'error') errors.push(`console: ${m.text()}`); });
        page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
        await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: theme }]);
        await page.setViewport({ width, height: width === 390 ? 844 : 900, deviceScaleFactor: width === 390 ? 2 : 1 });
        await page.evaluateOnNewDocument(() => {
            window.__cls = 0;
            new PerformanceObserver((list) => { for (const e of list.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
        });
        await page.goto(`${base}/${name}.html`, { waitUntil: 'networkidle0' });
        // scroll through so lazy images load and any shift they cause is counted
        await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } window.scrollTo(0, 0); });
        await new Promise((r) => setTimeout(r, 400));
        const cls = await page.evaluate(() => window.__cls);
        await page.addScriptTag({ content: AXE });
        const axe = await page.evaluate(async () => { const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] } }); return r.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.map((n) => n.target.join(' ')).slice(0, 5) })); });
        const external = requests.filter((r) => !r.url.startsWith(base));
        const bytes = requests.reduce((s, r) => s + r.size, 0);
        const failed = requests.filter((r) => r.status >= 400);
        console.log(`\n== ${name}.html ${width}px ${theme}`);
        console.log(`requests: ${requests.length} (${(bytes / 1024).toFixed(0)} KB transferred), external: ${external.length}, failed: ${failed.length}, console/page errors: ${errors.length}, CLS: ${cls.toFixed(4)}`);
        for (const e of errors) console.log(`  ${e}`);
        for (const f of failed) console.log(`  ${f.status} ${f.url}`);
        for (const x of external) console.log(`  external: ${x.url}`);
        if (axe.length === 0) console.log('axe: 0 violations');
        for (const v of axe) console.log(`axe ${v.impact}: ${v.id} (${v.help}) -> ${v.nodes.join(' | ')}`);
        if (name === 'index' && width === 1440 && theme === 'light') {
            for (const r of requests) console.log(`  ${String(r.size).padStart(7)}  ${r.url.replace(base + '/', '')}`);
        }
        await page.close();
    }
}
await browser.close();
server.close();
