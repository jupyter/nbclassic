const fs = require("fs");
const path = require("path");

const isWin = process.platform === "win32";
const LINK_TYPE = isWin ? "junction" : "dir";

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function ensureSymlink(sourcePath, targetPath) {
  const source = path.resolve(sourcePath);
  const target = path.resolve(targetPath);

  ensureDir(path.dirname(target));

  if (!fs.existsSync(source)) {
    console.warn(`Skipping symlink; source missing: ${source}`);
    return false;
  }

  try {
    const stat = fs.lstatSync(target);
    if (!stat.isSymbolicLink()) {
      console.log(`Removing non-symlink at: ${target}`);
      fs.rmSync(target, { recursive: true, force: true });
    } else {
      const exists = fs.readlinkSync(target);
      if (path.resolve(exists) === source) {
        console.log(`Symlink exists at: ${target}`);
        return;
      }
      console.log(`Replacing symlink at: ${target}`);
      fs.unlinkSync(target);
    }
  } catch (e) {
    if (e.code !== "ENOENT") {
      console.error(`Error checking symlink: ${e.message}`);
    }
  }

  try {
    fs.symlinkSync(source, target, LINK_TYPE);
    console.log(`Symlink created: ${sourcePath} -> ${targetPath}`);
  } catch (e) {
    if (e.code !== "EEXIST") {
      console.error(`Error creating symlink: ${e.message}`);
    }
  }
}

ensureDir("nbclassic/static/components");

[
  "marked",
  "font-awesome",
  "backbone",
  "bootstrap",
  "bootstrap-tour",
  "jed",
  "moment",
  "text-encoding",
  "underscore",
  "jquery",
  "jquery-ui",
  "jquery-typeahead",
  "codemirror",
  "react",
  "react-dom",
  "es6-promise",
  "requirejs",
  "requirejs-plugins",
  "requirejs-text",
  "google-caja-sanitizer",
  "mathjax",
].forEach((pkg) => {
  const dst = pkg === "mathjax" ? "MathJax" : pkg;
  ensureSymlink(`node_modules/${pkg}`, `nbclassic/static/components/${dst}`);
});
