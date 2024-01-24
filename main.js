const electron = require('electron');
const { app, BrowserWindow, ipcMain } = electron;
const path = require('path');
const url = require('url');

/*require('electron-reload')('C:/Users/kskos/Netspider_electron/Netspider', {
  electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
});*/

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  // Point to Flask server if you're developing. 
  // For production, you might point to a file or a different server.
  const startUrl = process.env.ELECTRON_START_URL || url.format({
        pathname: path.join(__dirname, 'index_jr.html'),
        protocol: 'file:',
        slashes: true
  });

  win.loadURL(startUrl);

  win.webContents.openDevTools();

  // Load the content from Flask server
  //mainWindow.loadURL('http://localhost:5000');

  win.on('closed', () => {
    win = null;
  });
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