"use strict";

const Insta = require("./Insta");

const { app, BrowserWindow, Menu, webContents } = require("electron");
const path = require("path");
const axios = require('axios');


const username = "username";
const password = "password";


let subpy = null;
const ig = new Insta(username, password);

const FLASK_DIST_FOLDER = "dist-flask"; // python distributable folder
const FLASK_SRC_FOLDER = "web_app"; // path to the python source
const FLASK_MODULE = "run"; // the name of the main module

const isRunningInBundle = () => {
  return require("fs").existsSync(path.join(__dirname, FLASK_DIST_FOLDER));
};

const getPythonScriptPath = () => {
  if (!isRunningInBundle()) {
    //console.log(path.join(__dirname, FLASK_SRC_FOLDER, FLASK_MODULE+".py"));
    return path.join(__dirname, FLASK_SRC_FOLDER, FLASK_MODULE+".py");
  }
  if (process.platfom === "win32") {
    return path.join(
      __dirname,
      FLASK_DIST_FOLDER,
      FLASK_MODULE.slice(0, -3) + ".exe"
    );
  }
  return path.join(__dirname, FLASK_DIST_FOLDER, FLASK_MODULE);
};

const startPythonSubprocess = () => {
  let script = getPythonScriptPath();
  if (isRunningInBundle()) {
    subpy = require("child_process").execFile(script, []);
  } else {
    subpy = require("child_process").spawn("python", [script]);
  }
  //console.log(subpy);
};

function createWindow(){
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  })




const isMac = process.platform === 'darwin'

const template = [
  // { role: 'appMenu' }
  ...(isMac ? [{
    label: app.name,
    submenu: [
      { role: 'about' },
      { type: 'separator' },
      { type: 'separator' },
      { role: 'quit' }
    ]
  }] : []),
  // { role: 'fileMenu' }
  {
    label: 'File',
    submenu: [
      isMac ? { role: 'close' } : { role: 'quit' }
    ]
  },
  {
    role: 'help',
    submenu: [
      {
        label: 'Instagram',
        click: async () =>{
          const { shell } = require('electron')
          await shell.openExternal('https://instagram.com')
        }
      },
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },


    ]
  }
]


app.setAboutPanelOptions({ 
        applicationName: 'followers.', 
        applicationVersion: '1.0.0', 
        credits: '64CIByte', 
        //copyright: "Copyright",
        authors: ['Erick Meyer', 'Frank Cao', 'Jiacong Li'], 
        website: 'cs.drexel.edu/~eam463/ci102', 
        iconPath: path.join(__dirname, '../assets/image.png'), 
    }); 


const menu = Menu.buildFromTemplate(template)
Menu.setApplicationMenu(menu)

//unshift
//if(process.platform == 'darwin'){
//template.unshift({label:'',});
//}



  //use puppeteer to get content
  win.webContents.on('did-navigate', (e, redirectUrl) =>{
    let partial_url="http://127.0.0.1:5000/pupsearch/";
    if(redirectUrl.includes(partial_url) ){
      const USER_URL = redirectUrl.replace("http://127.0.0.1:5000/pupsearch/","");
      setTimeout(async () => {
        win.loadFile('splash.html');
        await ig.postData(await ig.getData(USER_URL)).then(win.loadURL('http://127.0.0.1:5000/'));
      }, 1);
    }
  })





  //Catch pressing quit button
  //did-naviage-in-page for page navigation with #
  win.webContents.on('did-navigate', (e, redirectUrl) =>{
    if(win.webContents.getURL() == "http://127.0.0.1:5000/quit"){
      setTimeout(() => {app.quit()}, 1);
    }
  })



win.webContents.on('new-window', function(e, url) {
  if(url == "https://canvasjs.com/"){
    e.preventDefault();
  }

  });


//init pup
//startup

  (async () => {
    await ig.init();
    await ig.login();
  })();

  win.loadFile('splash.html');

  let preLoad = async()=>{
    const res = axios.get('http://127.0.0.1:5000/settings').catch(error => {preLoad()});
    if(typeof await res != "undefined"){
       win.loadURL('http://127.0.0.1:5000/');
    }
  };
  preLoad();
}

app.whenReady().then(()=>{
  startPythonSubprocess();
  createWindow();
})

app.on('window-all-closed', ()=>{
  if (process.platform !== 'darwin'){
    app.quit()
  }
})

app.on('activate', ()=>{
  if (BrowserWindow.getAllWindows().length === 0){
    createWindow()
  }
  if (subpy == null) {
    console.log('start sub on active')
    startPythonSubprocess();
  }
})

app.on('quit', async ()=>{
//win.loadURL('http://127.0.0.1:5000/update');
  await ig.close();

  subpy.kill();
});
