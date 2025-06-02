const { exec, execFile } = require('node:child_process');
const path = require('node:path');
const { app, BrowserWindow, Menu } = require('electron/main');

const inProduction = app.isPackaged;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) app.quit();

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

const createWindow = async () => {
    // Create a custom menu
    const menuTemplate = [
        { role: 'fileMenu' },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'forceReload' },
                ...(inProduction ? [] : [{ role: 'toggleDevTools' }]),
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' },
            ],
        },
    ];

    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);

    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 800,
        webPreferences: {
            // Allow the preload script to import arbitrary Node.js modules.
            nodeIntegration: true,
            preload: path.join(__dirname, 'static/scripts/preload.js'),
            devTools: !inProduction,
        },
        icon: path.join(__dirname, 'download-removebg-preview.ico'),
    });

    // and load the index.html of the app.
    await mainWindow.loadFile(path.join(__dirname, 'index.html'));
};


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.whenReady().then(createWindow);

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
