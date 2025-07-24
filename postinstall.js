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

//  Symlink bower_components
ensureSymlink("node_modules/@bower_components", "nbclassic/static/components");

// Symlink other static assets no longer in bower_components
ensureSymlink(
  "node_modules/font-awesome",
  "nbclassic/static/components/font-awesome"
);
