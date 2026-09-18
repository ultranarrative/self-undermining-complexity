/* Encrypts the page content with the site password and writes index.html.
   Only the content is encrypted; the stylesheet and the solver ship in clear,
   because neither reveals anything the note is protecting. */
const fs = require("fs");
const crypto = require("crypto");

const PASSWORD = process.env.SITE_PASSWORD || "selfdestructive";
const ITER = 250000;

const logo = fs.readFileSync("logo.b64", "utf8").trim();
const content = fs.readFileSync("content.html", "utf8").replaceAll("__LOGO__", logo);

const salt = crypto.randomBytes(16);
const iv = crypto.randomBytes(12);
const key = crypto.pbkdf2Sync(PASSWORD, salt, ITER, 32, "sha256");
const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
const ct = Buffer.concat([cipher.update(content, "utf8"), cipher.final(), cipher.getAuthTag()]);

const payload = {
  salt: salt.toString("base64"),
  iv: iv.toString("base64"),
  ct: ct.toString("base64"),
  iter: ITER
};

const out = fs.readFileSync("shell.html", "utf8")
  .replaceAll("__LOGO__", logo)
  .replace("__PAYLOAD__", JSON.stringify(payload));

fs.writeFileSync("index.html", out);
console.log("index.html:", (out.length/1024).toFixed(1), "KB");
console.log("content encrypted:", content.length, "chars ->", ct.length, "bytes");

/* Round-trip through the exact WebCrypto calls the page makes. */
(async () => {
  const subtle = globalThis.crypto.subtle;
  const b64 = s => Uint8Array.from(Buffer.from(s, "base64"));
  const km = await subtle.importKey("raw", new TextEncoder().encode(PASSWORD),
    "PBKDF2", false, ["deriveKey"]);
  const k = await subtle.deriveKey(
    {name:"PBKDF2", salt:b64(payload.salt), iterations:payload.iter, hash:"SHA-256"},
    km, {name:"AES-GCM", length:256}, false, ["decrypt"]);
  const plain = await subtle.decrypt({name:"AES-GCM", iv:b64(payload.iv)}, k, b64(payload.ct));
  const got = new TextDecoder().decode(plain);
  console.log(got === content ? "round trip OK" : "ROUND TRIP FAILED");

  let rejected = false;
  try{
    const kbad = await subtle.deriveKey(
      {name:"PBKDF2", salt:b64(payload.salt), iterations:payload.iter, hash:"SHA-256"},
      await subtle.importKey("raw", new TextEncoder().encode("wrongpassword"),
        "PBKDF2", false, ["deriveKey"]),
      {name:"AES-GCM", length:256}, false, ["decrypt"]);
    await subtle.decrypt({name:"AES-GCM", iv:b64(payload.iv)}, kbad, b64(payload.ct));
  }catch(e){ rejected = true; }
  console.log(rejected ? "wrong password rejected OK" : "WRONG PASSWORD ACCEPTED");

  const src = fs.readFileSync("index.html", "utf8");
  const leaks = ["Compartments do not move", "91 percent", "0.972", "Stouffer"]
    .filter(s => src.includes(s));
  console.log(leaks.length === 0
    ? "no findings in plaintext OK"
    : "LEAKED IN PLAINTEXT: " + leaks.join(", "));
})();
