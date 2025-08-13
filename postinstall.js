const fs = require("fs");
const path = require("path");

function ensureSymlink(sourcePath, targetPath) {
  const source = path.resolve(sourcePath);
  const target = path.resolve(targetPath);

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
    fs.symlinkSync(
      path.resolve(source),
      path.resolve(target),
      "junction"
    );
    console.log(`Symlink created: ${sourcePath} -> ${targetPath}`);
  } catch (e) {
    if (e.code !== "EEXIST") {
      console.error(`Error creating symlink: ${e.message}`);
    }
  }
}

// Symlink other static assets no longer in bower_components
ensureSymlink(
  "node_modules",
  "nbclassic/static/components"
);
ensureSymlink(
  "node_modules/mathjax",
  "nbclassic/static/components/MathJax"
);
