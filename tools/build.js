const { spawn } = require('child_process');
const fs = require('fs').promises;

// Find binary paths for Windows compatibility
const webpackPath = require.resolve('webpack/bin/webpack.js');
const lesscPath = require.resolve('less/bin/lessc');
const po2jsonPath = require.resolve('po2json/bin/po2json');

const LANGUAGES = ['fr_FR', 'ja_JP', 'nl', 'ru_RU', 'zh_CN'];

const tasks = {
    webpack: {
        output: 'dist/main.js',
        command: ['node', webpackPath, '--mode', 'production'],
    },
    notebook: {
        output: 'nbclassic/static/notebook/js/main.min.js',
        command: ['node', 'tools/build-main.js', 'notebook'],
    },
    tree: {
        output: 'nbclassic/static/tree/js/main.min.js',
        command: ['node', 'tools/build-main.js', 'tree'],
    },
    edit: {
        output: 'nbclassic/static/edit/js/main.min.js',
        command: ['node', 'tools/build-main.js', 'edit'],
    },
    terminal: {
        output: 'nbclassic/static/terminal/js/main.min.js',
        command: ['node', 'tools/build-main.js', 'terminal'],
    },
    auth: {
        output: 'nbclassic/static/auth/js/main.min.js',
        command: ['node', 'tools/build-main.js', 'auth'],
    },
    ipythonCss: {
        output: 'nbclassic/static/style/ipython.min.css',
        command: ['node', lesscPath, '--source-map', '--include-path=nbclassic/static/style',
                 'nbclassic/static/style/ipython.less', 'nbclassic/static/style/ipython.min.css']
    },
    styleCss: {
        output: 'nbclassic/static/style/style.min.css',
        command: ['node', lesscPath, '--source-map', '--include-path=nbclassic/static/style',
                 'nbclassic/static/style/style.less', 'nbclassic/static/style/style.min.css']
    },
    translations: {
        outputs: LANGUAGES.map(lang => {
            const langPath = lang.includes('_') ? lang : lang;
            return `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.json`;
        }),
        buildFn: async () => {
            await Promise.all(LANGUAGES.map(async lang => {
                const langPath = lang.includes('_') ? lang : lang;
                const input = `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.po`;
                const output = `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.json`;
                console.log(`Building translation for ${lang}...`);
                const proc = spawn('node', [
                    po2jsonPath, '-p', '-F', '-f', 'jed1.x', '-d', 'nbjs',
                    input, output
                ], { stdio: 'inherit' });
                await new Promise((resolve, reject) => {
                    proc.on('close', code => {
                        if (code === 0) {
                            console.log(`Finished translation for ${lang}`);
                            resolve();
                        } else {
                            reject(new Error(`Translation failed for ${lang} with code ${code}`));
                        }
                    });
                });
            }));
        }
    }
};

async function runTask(taskName) {
    const task = tasks[taskName];
    if (!task) {
        throw new Error(`Unknown task: ${taskName}`);
    }
    console.log(`Building ${taskName}...`);
    if (task.buildFn) {
        await task.buildFn();
    } else {
        const proc = spawn(task.command[0], task.command.slice(1), { stdio: 'inherit' });
        await new Promise((resolve, reject) => {
            proc.on('close', code => {
                if (code === 0) {
                    console.log(`Finished ${taskName}`);
                    resolve();
                } else {
                    reject(new Error(`Command failed with code ${code}`));
                }
            });
            proc.on('error', reject);
        });
    }
}

async function clean() {
    console.log('Cleaning build outputs...');
    const cleanTasks = Object.values(tasks).map(async task => {
        const outputs = task.outputs || [task.output];
        await Promise.all(outputs.map(async output => {
            try {
                await fs.unlink(output);
                console.log(`Removed ${output}`);
            } catch (err) {
                if (err.code !== 'ENOENT') {
                    console.error(`Error removing ${output}:`, err);
                }
            }
        }));
    });
    await Promise.all(cleanTasks);
}

async function runAll() {
    try {
        // Run webpack first
        await runTask('webpack');

        // Run everything else in parallel
        const remainingTasks = Object.keys(tasks).filter(task => task !== 'webpack');
        await Promise.all(remainingTasks.map(taskName => runTask(taskName)));
    } catch (err) {
        console.error('Build failed:', err);
        process.exit(1);
    }
}

const command = process.argv[2];
if (command === 'clean') {
    clean().catch(err => {
        console.error(err);
        process.exit(1);
    });
} else if (command) {
    runTask(command).catch(err => {
        console.error(err);
        process.exit(1);
    });
} else {
    runAll().catch(err => {
        console.error(err);
        process.exit(1);
    });
}
