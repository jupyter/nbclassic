const fs = require('fs');
const path = require('path');
const https = require('https');

// Define source and destination paths for each file
const files = [
  {
    url: 'https://cdn.jsdelivr.net/npm/create-react-class@15.6.3/create-react-class.min.js',
    dest: path.join('nbclassic', 'static', 'components', 'create-react-class', 'index.js')
  },
  {
    url: 'https://unpkg.com/xterm@3.1.0/dist/xterm.js',
    dest: path.join('nbclassic', 'static', 'components', 'xterm.js', 'index.js')
  },
  {
    url: 'https://unpkg.com/xterm@3.1.0/dist/addons/fit/fit.js',
    dest: path.join('nbclassic', 'static', 'components', 'xterm.js-fit', 'index.js')
  },
  {
    url: 'https://unpkg.com/xterm@3.1.0/dist/xterm.css',
    dest: path.join('nbclassic', 'static', 'components', 'xterm.js-css', 'index.css')
  }
];

// Create directories if they don't exist
files.forEach(file => {
  const dir = path.dirname(file.dest);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created directory: ${dir}`);
  }
});

// Download function
function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    // Check if destination already exists
    if (fs.existsSync(dest)) {
      console.log(`File already exists: ${dest}`);
      return resolve();
    }

    console.log(`Downloading ${url} to ${dest}`);
    const file = fs.createWriteStream(dest);

    https.get(url, response => {
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download ${url}: ${response.statusCode}`));
        return;
      }

      response.pipe(file);

      file.on('finish', () => {
        file.close(() => resolve());
      });
    }).on('error', err => {
      fs.unlink(dest, () => {}); // Delete the file if there was an error
      reject(err);
    });
  });
}

// Download all files
async function downloadAllFiles() {
  for (const file of files) {
    try {
      await downloadFile(file.url, file.dest);
    } catch (err) {
      console.error(`Error downloading ${file.url}: ${err.message}`);
      process.exit(1);
    }
  }
  console.log('Successfully downloaded all xterm files');
}

downloadAllFiles();
