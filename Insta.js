const puppeteer = require('puppeteer');
const axios = require('axios');

class Insta{
  constructor(username, password){
    this.username = username;
    this.password = password;
    this.baseUrl="https://instagram.com";
  }

  async init(){
    this.browser = await puppeteer.launch({ headless: false }); // default is true
    //this.browser = await puppeteer.launch();
  }

  async login(){
    this.page = await this.browser.newPage();
    await this.page.goto(`${this.baseUrl}/accounts/login/`);
    await this.page.waitForSelector('input[name="username"]');
    await this.page.type('input[name="username"]', this.username);
    await this.page.type('input[name="password"]', this.password);
    await this.page.click('button[type="submit"]');
    await this.page.waitForSelector('._6q-tv');
  }

  async getData(username){
    await this.page.goto(`${this.baseUrl}/${username}/?__a=1`);
    let data = JSON.parse(await this.page.evaluate('document.body.innerText'));



    const numFollowers = data.graphql.user.edge_followed_by.count;
    const numFollowing = data.graphql.user.edge_follow.count;
    const uname = data.graphql.user.username;
    const profilePicURL = data.graphql.user.profile_pic_url;

    const userData = {
      username: uname,
      followers: numFollowers,
      following: numFollowing,
      profilePicURL: profilePicURL
    };


    return userData;
  }

  async close(){
    await this.browser.close();
  }

  async postData(data){
    try{
      const res = await axios.post('http://127.0.0.1:5000/getData',data);
    } catch(err){
      console.log(err);
    }
  }


}


module.exports = Insta;


//Just testing
//ig = new Insta('username', 'password');
//
//(async () => {
//  await ig.init();
//  await ig.login();
//
//
//  await ig.postData(await ig.getData('erickmeyer'));
//  await ig.postData(await ig.getData('amandaaloura'));
//
//
//  await ig.close();
//})(); 
