const fs = require('fs');
const path = require('path');

const sourceFile = path.join('nbclassic', 'static', 'components', 'marked', 'lib', 'marked.umd.js');
const destFile = path.join('nbclassic', 'static', 'components', 'marked', 'lib', 'marked.js');

// Check file existence
const sourceExists = fs.existsSync(sourceFile);
const destExists = fs.existsSync(destFile);

if (!sourceExists && !destExists) {
    // Both files missing - critical error
    console.error(`Error: ${destFile} is required but cannot be created (${sourceFile} not found)`);
    process.exit(1);
} else if (!sourceExists) {
    // Source missing but dest exists - skip copy
    console.log(`Copy skipped: ${sourceFile} not found (using existing ${destFile})`);
    process.exit(0);
}

// Source exists, attempt copy
try {
    fs.copyFileSync(sourceFile, destFile);
    console.log(`Successfully copied ${sourceFile} to ${destFile}`);
} catch (err) {
    console.error(`Error copying file: ${err.message}`);
    process.exit(1);
}
