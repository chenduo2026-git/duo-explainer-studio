#!/usr/bin/env node
import { copyFile, mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (!key?.startsWith('--') || value === undefined) throw new Error(`Invalid argument near ${key}`);
    args[key.slice(2)] = value;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
for (const required of ['html', 'timing', 'output']) {
  if (!args[required]) throw new Error(`Missing --${required}`);
}

const playwrightModule = args.playwright || 'playwright';
const { chromium } = await import(playwrightModule);
const timing = JSON.parse(await readFile(resolve(args.timing), 'utf8'));
const waitMs = Math.ceil(Number(timing.record_duration || timing.target_duration + 0.8) * 1000);
const outputPath = resolve(args.output);
await mkdir(dirname(outputPath), { recursive: true });
const recordDir = await mkdtemp(join(tmpdir(), 'duo-slide-record-'));

const launchOptions = { headless: true };
if (args.executable) launchOptions.executablePath = resolve(args.executable);

let browser;
try {
  browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: recordDir, size: { width: 1920, height: 1080 } },
  });
  const page = await context.newPage();
  const video = page.video();
  await page.goto(`${pathToFileURL(resolve(args.html)).href}?render=1`, { waitUntil: 'load' });
  await page.waitForTimeout(waitMs);
  await context.close();
  const recordedPath = await video.path();
  await copyFile(recordedPath, outputPath);
  console.log(JSON.stringify({ output: outputPath, duration_seconds: waitMs / 1000 }));
} finally {
  if (browser) await browser.close();
  await rm(recordDir, { recursive: true, force: true });
}
