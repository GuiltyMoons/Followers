from pyppeteer import launch
class Insta():
    def __init__(self, username="", password=""):
        self.__username = username
        self.__password = password
        self.__base_url = "https://instagram.com"
        self.__login_url = self.__base_url
        self.__api_url = self.__login_url+"/{}/?__a=1"

    #Getters
    def getUsername(self):
        return self.__username

    #Setters
    def getPassword(self):
        return self.__password


    async def startup(self):
       self.__browser = await launch({'headless': False,
           'autoClose':False,
           'handleSIGINT':False,
           'handleSIGTERM':False,
           'handleSIGHUP':False})

    async def close(self):
        await self.__browser.close()

    async def login(self):
        username = self.__username
        password = self.__password
        try:
            self.__page = await self.__browser.newPage()
            await self.__page.goto('http://instagram.com')
            await self.__page.waitForSelector('input[name="username"]');
            await self.__page.type('input[name="username"]', username);
            await self.__page.type('input[name="password"]', password);
            await self.__page.click('button[type="submit"]');
            await self.__page.waitForSelector("._6q-tv")
            return True
        except:
            return False

    async def getData(self, username):
        await self.__page.goto(self.__api_url.format(username))
        data = await self.__page.evaluate(('document.body.innerText'))

        followers_start_index = data.find('followed_by\":{\"count\":')
        count = followers_start_index+22
        num_followers=""

        while not data[count]=="}":
            num_followers+=str(data[count])
            count+=1



        following_start_index = data.find('\"edge_follow\"')
        count = following_start_index+23
        num_following = ""

        while not data[count] == "}":
            num_following+=str(data[count])
            count+=1



        profile_pic_start_index = data.find("\"profile_pic_url_hd\"")
        count = profile_pic_start_index+22
        url = ""

        while not data[count] == "\"":
            url += data[count]
            count+=1

        return (num_followers, num_following, url)
