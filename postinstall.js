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
ensureSymlink(
  "node_modules/backbone",
  "nbclassic/static/components/backbone"
);
ensureSymlink(
  "node_modules/bootstrap",
  "nbclassic/static/components/bootstrap"
);
ensureSymlink(
  "node_modules/bootstrap-tour",
  "nbclassic/static/components/bootstrap-tour"
);
ensureSymlink(
  "node_modules/jed",
  "nbclassic/static/components/jed"
);
ensureSymlink(
  "node_modules/moment",
  "nbclassic/static/components/moment"
);
ensureSymlink(
  "node_modules/text-encoding",
  "nbclassic/static/components/text-encoding"
);
ensureSymlink(
  "node_modules/underscore",
  "nbclassic/static/components/underscore"
);
