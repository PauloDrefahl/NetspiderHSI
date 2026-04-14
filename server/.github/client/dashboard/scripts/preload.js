// preload.js
// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { ipcRenderer, contextBridge, shell } = require('electron');
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

contextBridge.exposeInMainWorld('electronPath', {
    join: (...args) => path.join(...args)
});

contextBridge.exposeInMainWorld('nodePaths', {
    __dirname: __dirname,
    // You can also expose other Node.js path functionalities as needed
});

contextBridge.exposeInMainWorld('electronAPI', {
    readJson: (filePath) => new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
                return;
            }
            try {
                const jsonData = JSON.parse(data);
                resolve(jsonData);
            } catch (parseErr) {
                reject(parseErr);
            }
        });
    })
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
    },
    addKeyset: (keywordSetsFile, keywordsToAdd, setName) => {
        fs.readFile(keywordSetsFile, 'utf-8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return;
            }

            let keywordSets;
            try {
                // Parse the JSON data from the file
                keywordSets = JSON.parse(data);
                console.log(keywordSets)
            } catch (error) {
                console.error('Error parsing JSON:', error);
                return;
            }

            // Add the new keyset
            keywordSets[setName] = keywordsToAdd;

            // Convert the updated object back to JSON
            const updatedContent = JSON.stringify(keywordSets);

            // Write the updated content back to the file
            fs.writeFile(keywordSetsFile, updatedContent, 'utf-8', (err) => {
                if (err) {
                    console.error('Error writing file:', err);
                } else {
                    console.log('Keyset added to file successfully');
                }
            });
        });
    },
    removeKeyset: (keywordSetsFile, keysetName) => {
        fs.readFile(keywordSetsFile, 'utf-8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return;
            }

            let keywordSets;
            try {
                // Parse the JSON data from the file
                keywordSets = JSON.parse(data);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                return;
            }

            // Check if the keyset exists
            if (keywordSets.hasOwnProperty(keysetName)) {
                // Delete the keyset
                delete keywordSets[keysetName];

                // Convert the updated object back to JSON
                const updatedContent = JSON.stringify(keywordSets);

                // Write the updated content back to the file
                fs.writeFile(keywordSetsFile, updatedContent, 'utf-8', (err) => {
                    if (err) {
                        console.error('Error writing file:', err);
                    } else {
                        console.log('Keyset removed from file successfully');
                    }
                });
            } else {
                console.log('Keyset not found:', keysetName);
            }
        });
    },
    reloadKeysetsFromFile: (filePath, callback) => {
        fs.readFile(filePath, 'utf-8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                if (callback) {
                    callback(err);
                }
                return;
            }

            try {
                // Parse the JSON data from the file
                jsonData = JSON.parse(data);
                console.log("reloaded json data", jsonData)
                console.log('Keysets reloaded from file successfully');
                if (callback) {
                    callback(null, jsonData);
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
                if (callback) {
                    callback(error);
                }
            }
        });
    },
    openResults: (folderPath) => {
        // Check if folderPath is provided
        if (!folderPath) {
            console.error('Folder path is required.');
            return;
        }

        // Open the folder using the shell module
        shell.openExternal('file://' + folderPath)
            .then(() => {
                console.log('Folder opened successfully.');
            })
            .catch((error) => {
                console.error('Error opening folder:', error);
            });
    }
});

