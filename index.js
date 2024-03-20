const fs = require('fs').promises;
const chokidar = require('chokidar');
const util = require('util');
const { app, BrowserWindow} = require('electron');
const path = require('path');
const { execFile, exec } = require('child_process');



// Specify the path to your Flask executable
const flaskExecutablePath = 'C:\\Users\\Zach\\PycharmProjects\\NetSpiderHSI\\NetSpiderServer.exe';


// Use exec to run the Flask executable
// let flaskProcess = execFile(flaskExecutablePath, (error, stdout, stderr) => {
//   if (error) {
//     console.error(`Error: ${error.message}`);
//     return;
//   }
//   if (stderr) {
//     console.error(`stderr: ${stderr}`);
//     return;
//   }
//   console.log(`stdout: ${stdout}`);
// });\
//
// const flaskPID = flaskProcess.pid
//
// // You can also listen for events like 'exit' or 'close' to handle the process lifecycle
// flaskProcess.on('exit', (code, signal) => {
//   console.log(`Flask process exited with code ${code} and signal ${signal}`);
//   console.log(`Flask pid: ${flaskPID}`)
// });

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
            preload: path.join(__dirname, 'dashboard/scripts/preload.js')
        },
        icon: 'dashboard/icons/download-removebg-preview.ico'
    });

    // and load the index.html of the app.
    mainWindow.loadFile(path.join(__dirname, 'index.html'));
};



// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.on('ready', () => {
    // Add a delay before creating the window
    setTimeout(() => {
        createWindow();
    }, 1000); // 3000 milliseconds = 3 seconds
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

const directoryPath = 'C:\\Users\\kskos\\PycharmProjects\\HSI_Back_Test3\\result';
// Read directory and filter out files, keeping only directories
/*fs.readdir(directoryPath, { withFileTypes: true }, (err, files) => {
    if (err) {
        console.error('Error reading the directory', err);
        return;
    }

    const folders = files.filter(file => file.isDirectory()).map(folder => folder.name);

    // Convert array of folders to JSON format
    const jsonFolders = JSON.stringify(folders, null, 2);

    // Output the JSON string
    console.log(jsonFolders);

    // Optionally, write the JSON to a file
    fs.writeFile('folders.json', jsonFolders, (err) => {
        if (err) {
            console.error('Error writing to file', err);
            return;
        }
        console.log('Folders list saved to folders.json');
    });
});*/

// Function to read directory and write folders.json
async function updateFoldersJson() {
    try {
        const files = await fs.readdir(directoryPath, { withFileTypes: true });
        const folders = files.filter(file => file.isDirectory()).map(folder => folder.name);

        // sort the folders into alphanumerical order
        folders.sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));

        const jsonFolders = JSON.stringify(folders, null, 2);
        console.log(jsonFolders);
        await fs.writeFile('folders.json', jsonFolders);
        console.log('Folders list updated in folders.json');
    } catch (err) {
        console.error('Error accessing the directory or writing to file', err);
    }
}

// Initial update
updateFoldersJson();

// Watch the directory for changes using chokidar
const watcher = chokidar.watch(directoryPath, {
    ignored: /^\./, // ignore dotfiles
    persistent: true,
    ignoreInitial: false, // Do not fire add events when starting
});

// Add event listeners for add, change, and unlink
watcher
    .on('addDir', path => {
        console.log(`Directory ${path} has been added`);
        updateFoldersJson();
        // Trigger a reload of the current page

    })
    .on('unlinkDir', path => {
        console.log(`Directory ${path} has been removed`);
        updateFoldersJson();
        // Trigger a reload of the current page

    })
    .on('error', error => console.error(`Watcher error: ${error}`))
    .on('ready', () => console.log('Initial scan complete. Ready for changes'));


//kill all NetSpiderServer processes
// app.on('before-quit', async () => {
//   process.kill(flaskPID, 'SIGKILL')
//   exec('taskkill /IM NetSpiderServer.exe /F');
//   exec('taskkill /IM NetSpiderServer.exe /F');
//   exec('taskkill /IM undetected_chromedriver.exe /F')
// });
