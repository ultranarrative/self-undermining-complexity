/* Builds the public page into ../docs, which is what GitHub Pages serves. */
const fs = require("fs");
const path = require("path");

const logo = "data:image/svg+xml;base64," +
  fs.readFileSync(path.join(__dirname, "logo.svg")).toString("base64");
const content = fs.readFileSync("content.html", "utf8").replaceAll("__LOGO__", logo);
const page = fs.readFileSync("shell.html", "utf8")
  .replaceAll("__LOGO__", logo)
  .replace("__CONTENT__", content);

const out = path.join(__dirname, "..", "docs");
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "index.html"), page);
fs.writeFileSync(path.join(out, ".nojekyll"), "");
console.log("docs/index.html:", (page.length / 1024).toFixed(1), "KB");

for (const marker of ["PAYLOAD", "crypto.subtle", "gate-form", "type=\"password\""]) {
  if (page.includes(marker)) console.log("  ! gate remnant:", marker);
}
console.log(page.includes("__CONTENT__") ? "  ! content not inlined" : "  content inlined");
