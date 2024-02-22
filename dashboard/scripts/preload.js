// preload.js
// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { ipcRenderer, contextBridge } = require('electron');
const io = require('socket.io-client');
const fs = require('fs');

// Read the port from a text file;
const portFilePath = 'open_ports.txt';
const port = parseInt(fs.readFileSync(portFilePath, 'utf-8').trim());

// Create a new socket connection with the dynamic port
const socket = io.connect(`http://127.0.0.1:${port}`);

contextBridge.exposeInMainWorld('ipcRenderer', ipcRenderer);

contextBridge.exposeInMainWorld('socket', {
    on: (channel, callback) => {
        socket.on(channel, (event, ...args) => callback(event, ...args));
    },
    emit: (channel, ...args) => {
        socket.emit(channel, ...args);
    },
});