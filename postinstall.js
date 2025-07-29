const fs = require("fs");
const path = require("path");

function ensureSymlink(sourcePath, targetPath) {
  try {
    fs.symlinkSync(
      path.resolve(sourcePath),
      path.resolve(targetPath),
      "junction"
    );
    console.log(`Symlink created: ${sourcePath} -> ${targetPath}`);
  } catch (e) {
    if (e.code !== "EEXIST") {
      console.error(`Error creating symlink: ${e.message}`);
    }
  }
}

// Symlink static assets
ensureSymlink(
  "node_modules",
  "nbclassic/static/components"
);

ensureSymlink(
    "node_modules/@bower_components/react",
    "nbclassic/static/components/react"
);
