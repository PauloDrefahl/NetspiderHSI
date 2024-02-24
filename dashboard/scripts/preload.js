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

contextBridge.exposeInMainWorld('editFile', {
    addKeywordToFile: (keywordsFile, keyword) => {
        fs.appendFile(keywordsFile, '\n' + keyword, (err) => {
            if (err) {
                console.error('Error appending keyword to file:', err);
            } else {
                console.log('Keyword appended to file successfully');
            }
        })
    },
    removeKeywordsFromFile: (keywordsFile, keywordsToRemove) => {
        fs.readFile(keywordsFile, 'utf-8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return;
            }

            // Split the file content into lines
            let lines = data.split('\n');

            // Remove each keyword from the lines
            keywordsToRemove.forEach(keyword => {
                lines = lines.filter(line => line.trim() !== keyword);
            });

            // Join the lines back into a single string
            const updatedContent = lines.join('\n');

            // Write the updated content back to the file
            fs.writeFile(keywordsFile, updatedContent, 'utf-8', (err) => {
                if (err) {
                    console.error('Error writing file:', err);
                } else {
                    console.log('Keywords removed from file successfully');
                }
            });
        });
    }
});