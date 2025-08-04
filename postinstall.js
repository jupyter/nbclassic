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

//  Symlink bower_components
ensureSymlink("node_modules/@bower_components", "nbclassic/static/components");

// Symlink other static assets no longer in bower_components
ensureSymlink(
  "node_modules/marked",
  "nbclassic/static/components/marked"
);
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
ensureSymlink(
  "node_modules/jquery",
  "nbclassic/static/components/jquery"
);
ensureSymlink(
  "node_modules/jquery-ui",
  "nbclassic/static/components/jquery-ui"
);
ensureSymlink(
  "node_modules/jquery-typeahead",
  "nbclassic/static/components/jquery-typeahead"
);
ensureSymlink(
  "node_modules/mathjax",
  "nbclassic/static/components/MathJax"
);
ensureSymlink(
  "node_modules/es6-promise",
  "nbclassic/static/components/es6-promise"
);
