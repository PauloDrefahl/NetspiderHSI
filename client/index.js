const { app, BrowserWindow, Menu} = require('electron');
const path = require('path');
const { execFile, exec } = require('child_process');



// Specify the path to your Flask executable
const flaskExecutablePath = 'resources/NetSpiderServer.exe';

let flaskProcess = execFile(flaskExecutablePath);

flaskProcess.stdout.on('data', (data) => {
  console.log(`[Flask stdout]: ${data.toString().trim()}`);
});

flaskProcess.stderr.on('data', (data) => {
  console.error(`[Flask stderr]: ${data.toString().trim()}`);
});

flaskProcess.on('exit', (code, signal) => {
  console.log(`Flask process exited with code ${code} and signal ${signal}`);
});

const flaskPID = flaskProcess.pid

// You can also listen for events like 'exit' or 'close' to handle the process lifecycle
flaskProcess.on('exit', (code, signal) => {
  console.log(`Flask process exited with code ${code} and signal ${signal}`);
  console.log(`Flask pid: ${flaskPID}`)
});

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
    app.quit();
}

const createWindow = () => {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 1200,
        webPreferences: {
            nodeIntegration: true,
            preload: path.join(__dirname, 'dashboard/scripts/preload.js'),
            devTools: true // Disable developer tools
        },
        icon: 'download-removebg-preview.ico'
    });

    mainWindow.setIcon(path.join(__dirname, 'download-removebg-preview.ico'));

    // and load the index.html of the app.
    mainWindow.loadFile(path.join(__dirname, 'index.html')).then(r => r);

    // Prevent opening of developer tools
    mainWindow.webContents.on('context-menu', (e, props) => {
        if (props.editFlags.canInspect) {
            e.preventDefault();
        }
    });
    // Create a custom menu
    const menuTemplate = [
        {
            label: 'File',
            submenu: [
                { role: 'quit' }
            ]
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'forcereload' },
                { role: 'separator'},
                { role: 'resetZoom'},
                { role: 'zoomIn'},
                { role: 'zoomOut'},
                { type: 'separator' },
                {
                    label: 'Toggle Developer Tools',
                    accelerator: process.platform === 'darwin' ? 'Command+Alt+I' : 'Ctrl+Shift+I',
                    click: () => {
                        const focusedWindow = BrowserWindow.getFocusedWindow();
                        if (focusedWindow) {
                            focusedWindow.webContents.toggleDevTools();
                        }
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);
};


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.on('ready', () => {
    // Add a delay before creating the window
    setTimeout(() => {
        createWindow();
    }, 1500); // 15000 milliseconds = 15 seconds
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

//kill all NetSpiderServer processes
app.on('before-quit', async () => {
  process.kill(flaskPID, 'SIGKILL');
  exec('taskkill /IM NetSpiderServer.exe /F');
  exec('taskkill /IM NetSpiderServer.exe /F');
  exec('taskkill /IM uc_driver.exe /F');
});
