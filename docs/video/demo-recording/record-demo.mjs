// Records one browser session of the MILO chat with the live model: a question, the tool steps, the source viewer,
// a fact recorded by a tool call, a blocked action waiting for approval, and the summary and proposed spec.
import puppeteer from "puppeteer-core";
const timeline = [];
let tStart = 0;

const [, , base, password, out, ffmpegPath] = process.argv;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// The virtual display only: the real desktop is never captured.
const display = process.env.RECORD_DISPLAY ?? ":99";
const browser = await puppeteer.launch({
  headless: false,
  env: { ...process.env, DISPLAY: display },
  executablePath: "/usr/bin/google-chrome",
  args: ["--no-sandbox", "--kiosk", "--test-type", "--disable-infobars", "--window-position=0,0", "--window-size=1440,900", "--force-device-scale-factor=1"],
  defaultViewport: null,
});
const [page] = await browser.pages();
// The screen grab starts first and runs in real time, so every scene keeps its real length.
const { spawn } = await import("node:child_process");
const fs = await import("node:fs");
tStart = Date.now();
const grab = spawn(ffmpegPath, ["-y", "-loglevel", "error", "-f", "x11grab", "-framerate", "25", "-video_size", "1440x900", "-i", display + ".0+0,0", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out]);
await sleep(1500);
const captionsOn = process.env.RECORD_CAPTIONS !== "0"; // subtitles are added after recording, from the narration
const caption = (text) => (timeline.push({ text, at: (Date.now() - tStart) / 1000 }), captionsOn ? page.evaluate((t) => {
  let el = document.getElementById("demo-caption");
  if (!el) {
    el = document.createElement("div");
    el.id = "demo-caption";
    el.style.cssText = "position:fixed;left:50%;bottom:36px;transform:translateX(-50%);z-index:99;max-width:70%;text-align:center;color:#fff;font:600 22px/1.35 system-ui,sans-serif;text-shadow:0 1px 3px rgba(0,0,0,.95),0 0 12px rgba(0,0,0,.6);pointer-events:none";
    document.body.appendChild(el);
  }
  el.textContent = t;
}, text) : null);


await page.goto(base + "/", { waitUntil: "networkidle0" });
// Frames are taken on a clock and kept with their real times, so the video plays at real speed even when the page is still.
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

grab.kill("SIGINT");
await new Promise((r) => grab.on("exit", r));
await browser.close();
fs.writeFileSync(out.replace(/\.mp4$/, ".timeline.json"), JSON.stringify(timeline, null, 2));
console.log("recorded", out);
