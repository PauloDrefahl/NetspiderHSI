// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const fs = require('node:fs');
const { contextBridge, shell } = require('electron/renderer');
const io = require('socket.io-client');

// Connect to the server using a fixed port number of 5173.
const socket = io.connect(`http://127.0.0.1:5173`);

contextBridge.exposeInMainWorld('socket', {
    on: (channel, callback) => {
        socket.on(channel, (event, ...args) => callback(event, ...args));
    },
    emit: (channel, ...args) => {
        socket.emit(channel, ...args);
    },
});

// Editing KeywordsFile & KeysetsFile
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

// Scheduling Scrapers
contextBridge.exposeInMainWorld('scraperFile', {

    getSchedules: () => {
        try {
            const filePath = 'scheduled_scrapers.json';

            if (fs.existsSync(filePath)) {
                const scheduledScrapers = fs.readFileSync(filePath, 'utf-8');
                return JSON.parse(scheduledScrapers); // Return parsed JSON from file
            } else {
                return {};
            }
        } catch (error) {
            console.error('Error reading scheduled_scrapers file:', error);
            return {};
        }
    },

    saveScraperData: (fileName, data) => {
        const filePath = 'scheduled_scrapers.json';
    
        try {
            let existingSchedules = {};
    
            // Check if the file exists and read scheduled_scrapers.json
            if (fs.existsSync(filePath)) {
                try {
                    const fileContent = fs.readFileSync(filePath, 'utf-8');
                    
                    // Check if the file is empty
                    if (fileContent.trim()) {
                        existingSchedules = JSON.parse(fileContent);
                    }
                } catch (parseError) {
                    console.error(`Error parsing the existing file ${fileName}:`, parseError);
                    // If parsing fails, send an empty object
                    existingSchedules = {};
                }
            }
    
            // Merge the new schedule with the existing
            const mergedData = { ...existingSchedules, ...data };
    
            // Attempt to write the merged data back to the file
            try {
                fs.writeFileSync(filePath, JSON.stringify(mergedData, null, 2));
                console.log(`Schedule successfully written to ${fileName}`);
            } catch (writeError) {
                console.error(`Error writing to file ${fileName}:`, writeError);
                throw writeError;
            }
        } catch (err) {
            console.error(`Error in saveScraperData for file ${fileName}:`, err);
            throw err;
        }
    },

    deleteScraperData: (fileName, data) => {
        const filePath = 'scheduled_scrapers.json'; // Use the provided fileName

        try {
            if (fs.existsSync(filePath)) {
                // Read the existing data from the file
                const fileContent = fs.readFileSync(filePath, 'utf-8');
                let existingSchedules = {};

                // Parse the file content to JSON
                try {
                    existingSchedules = JSON.parse(fileContent);
                } catch (parseError) {
                    console.error('Error parsing the scheduled_scraper file:', parseError);
                    return;
                }

                // Check if the scraperName exists in the data object
                const scraperName = data.scraperName;  // Extract scraperName from the data object

                if (existingSchedules.hasOwnProperty(scraperName)) {
                    // Delete the scraper by its name
                    delete existingSchedules[scraperName];

                    // Write the updated content back to the file
                    try {
                        fs.writeFileSync(filePath, JSON.stringify(existingSchedules, null, 2));
                        console.log(`Scraper with name "${scraperName}" deleted successfully.`);
                    } catch (writeError) {
                        console.error('Error writing to the scheduled_scrapers file:', writeError);
                    }
                } else {
                    console.log(`Scraper with name "${scraperName}" not found.`);
                }
            } else {
                console.error(`${fileName} file not found.`);
            }
        } catch (err) {
            console.error('Error in deleteScraperData:', err);
        }
    }

});
