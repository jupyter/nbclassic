const { spawn } = require('child_process');
const fs = require('fs').promises;

const tasks = {
    webpack: {
        output: 'dist/main.js',
        command: ['webpack', '--mode', 'production'],
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
        command: ['lessc', '--source-map', '--include-path=nbclassic/static/style',
                 'nbclassic/static/style/ipython.less', 'nbclassic/static/style/ipython.min.css']
    },
    styleCss: {
        output: 'nbclassic/static/style/style.min.css',
        command: ['lessc', '--source-map', '--include-path=nbclassic/static/style',
                 'nbclassic/static/style/style.less', 'nbclassic/static/style/style.min.css']
    },
    translations: {
        outputs: ['fr_FR', 'ja_JP', 'nl', 'ru_RU', 'zh_CN'].map(lang => {
            const langPath = lang.includes('_') ? lang : lang;
            return `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.json`;
        }),
        buildFn: async () => {
            const languages = ['fr_FR', 'ja_JP', 'nl', 'ru_RU', 'zh_CN'];
            for (const lang of languages) {
                const langPath = lang.includes('_') ? lang : lang;
                const input = `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.po`;
                const output = `nbclassic/i18n/${langPath}/LC_MESSAGES/nbjs.json`;
                console.log(`Building translation for ${lang}...`);
                const proc = spawn('po2json', [
                    '-p', '-F', '-f', 'jed1.x', '-d', 'nbjs',
                    input, output
                ], { stdio: 'inherit' });
                await new Promise((resolve, reject) => {
                    proc.on('close', code => {
                        if (code === 0) resolve();
                        else reject(new Error(`Translation failed for ${lang} with code ${code}`));
                    });
                });
            }
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
                if (code === 0) resolve();
                else reject(new Error(`Command failed with code ${code}`));
            });
        });
    }
    console.log(`Finished ${taskName}`);
}

async function clean() {
    console.log('Cleaning build outputs...');
    for (const task of Object.values(tasks)) {
        const outputs = task.outputs || [task.output];
        for (const output of outputs) {
            try {
                await fs.unlink(output);
                console.log(`Removed ${output}`);
            } catch (err) {
                if (err.code !== 'ENOENT') {
                    console.error(`Error removing ${output}:`, err);
                }
            }
        }
    }
}

// Define the build order explicitly
const buildOrder = [
    'webpack',
    'notebook',
    'tree',
    'edit',
    'terminal',
    'auth',
    'translations',
    'ipythonCss',
    'styleCss'
];

async function runAll() {
    for (const taskName of buildOrder) {
        try {
            await runTask(taskName);
        } catch (err) {
            console.error(`Error in task ${taskName}:`, err);
            process.exit(1);
        }
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
