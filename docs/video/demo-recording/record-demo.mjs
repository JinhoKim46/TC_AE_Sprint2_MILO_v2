// Records one browser session of the MILO chat with the live model: a question, the tool steps, the source viewer,
// a fact recorded by a tool call, a blocked action waiting for approval, and the summary and proposed spec.
import puppeteer from "puppeteer-core";

const [, , base, password, out, ffmpegPath] = process.argv;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const browser = await puppeteer.launch({ executablePath: "/usr/bin/google-chrome", args: ["--no-sandbox", "--disable-gpu"], defaultViewport: { width: 1440, height: 900 } });
const page = await browser.newPage();
const caption = (text) => page.evaluate((t) => {
  let el = document.getElementById("demo-caption");
  if (!el) {
    el = document.createElement("div");
    el.id = "demo-caption";
    el.style.cssText = "position:fixed;left:24px;bottom:24px;z-index:99;background:#1F1E1B;color:#fff;padding:12px 18px;border-radius:12px;font:600 18px system-ui,sans-serif;max-width:60%;box-shadow:0 6px 18px rgba(0,0,0,.25)";
    document.body.appendChild(el);
  }
  el.textContent = t;
}, text);


await page.goto(base + "/", { waitUntil: "networkidle0" });
// Frames are taken on a clock and kept with their real times, so the video plays at real speed even when the page is still.
const frames = [];
const frameDir = out + ".frames";
const fs = await import("node:fs");
fs.mkdirSync(frameDir, { recursive: true });
// Chrome's screencast gives each painted frame its own timestamp, so static parts keep their real length.
const cdp = await page.createCDPSession();
cdp.on("Page.screencastFrame", (f) => {
  const name = `${frameDir}/${String(frames.length).padStart(6, "0")}.jpg`;
  fs.writeFileSync(name, Buffer.from(f.data, "base64"));
  frames.push({ name, at: f.metadata.timestamp });
  cdp.send("Page.screencastFrameAck", { sessionId: f.sessionId }).catch(() => {});
});
await cdp.send("Page.startScreencast", { format: "jpeg", quality: 85, everyNthFrame: 1 });
const t0 = Date.now() / 1000;
await caption("MILO: a diagnosis chat that shows its work");
await sleep(3500);

await page.goto(base + "/login", { waitUntil: "networkidle0" });
await page.type('input[name="login_id"]', "demo", { delay: 60 });
await page.type('input[name="password"]', password, { delay: 40 });
await caption("Sign in, then ask one question about the business");
await Promise.all([page.waitForNavigation(), page.click('button[type="submit"], input[type="submit"]')]);

await page.goto(base + "/chat?new=1", { waitUntil: "networkidle0" });
const ask = async (text, expected) => {
  await page.type("#question", text, { delay: 25 });
  await page.click("#send");
  await page.waitForFunction((n) => document.querySelectorAll("article.answer").length >= n, { timeout: 150000 }, expected);
  await sleep(1200);
};
const openStage = async (label) => {
  await page.evaluate((l) => [...document.querySelectorAll("#panel .stage")].find((b) => b.innerText.includes(l)).click(), label);
  await sleep(800);
};

await caption("Question: requests and the time to assign them");
await ask("We get about 40 service requests a week, and each takes about 12 minutes to assign. What could a shared queue save us?", 1);
await caption("The answer cites its sources; the steps are in the side panel");
await openStage("Used tools");
await caption("Tool calls: name, arguments, result and the policy decision");
await sleep(3500);

await page.evaluate(() => [...document.querySelectorAll("#panel .src-read")][0]?.click());
await page.waitForSelector(".doc-text .hit", { timeout: 15000 }).catch(() => {});
await caption("The full source opens with the passage highlighted in its context");
await sleep(4500);
await page.evaluate(() => document.querySelector(".doc-viewer")?.close());

await caption("A fact from the owner is recorded by a tool call (allowed)");
await ask("Please record that we have 5 people in the office.", 2);
await openStage("Used tools");
await sleep(3000);

await caption("A destructive action is blocked until the owner approves it");
await ask("Please delete my saved diagnosis number 1, I want to start over.", 3);
await sleep(2500);

await caption("At the end: the summary and the proposed first spec");
await page.click("#summarize");
await page.waitForSelector(".summary-card", { timeout: 60000 });
await sleep(4000);
await caption("Every number comes from the recorded facts and the computed estimate");
await sleep(3000);

await cdp.send("Page.stopScreencast");
await sleep(500);
// The concat list gives every frame the time until the next one, so the timing is the real timing.
const listPath = frameDir + "/list.txt";
const lines = frames.map((f, i) => `file '${f.name}'\nduration ${((frames[i + 1]?.at ?? Date.now() / 1000) - f.at).toFixed(3)}`);
lines.push(`file '${frames[frames.length - 1].name}'`);
fs.writeFileSync(listPath, lines.join("\n") + "\n");
const { execFileSync } = await import("node:child_process");
execFileSync(ffmpegPath, ["-y", "-f", "concat", "-safe", "0", "-i", listPath, "-vf", "fps=25,format=yuv420p", "-c:v", "libx264", "-crf", "20", out]);
await browser.close();
console.log("recorded", out, frames.length, "frames");
