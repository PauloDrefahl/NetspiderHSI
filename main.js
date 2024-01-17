// main.js
const electron = require('electron');
const { app, BrowserWindow, ipcMain } = electron;
const path = require('path');
const url = require('url');

let win;

function createWindow() {
    win = new BrowserWindow({ width: 800, height: 1200 });
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file',
        slashes: true
    }));
    // Open the DevTools.
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (win === null) {
        createWindow();
    }
});
