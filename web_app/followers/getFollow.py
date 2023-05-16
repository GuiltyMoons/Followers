import requests
import json
import urllib.parse

userId = "NA"
instagramName = "NA"

def encodeUrl(url):
    return urllib.parse.quote(url, safe='~()*!.\'')

def pythonToJson(pythonObj): # obj = dictionary
    obj = pythonObj
    json_obj = json.dumps(obj, separators=(',', ':'))    
    return json_obj

def website(instaUser): #returns url needed to find user id, instaUser = instagram username
    url = "https://www.instagram.com/{}/?__a=1".format(instaUser)
    return url

def getFollowCont(optId):
    headers = { 'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
    'cache-control':'no-cache',
    'dnt':'1',
    'pragma':'no-cache',
    'referer':'https',
    'sec-fetch-mode':'no-cors',
    'sec-fetch-site':'cross-site',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    r = {
        "id": optId,
        "include_reel": True,
        "fetch_mutual": True,
        "first": 50
        }
    web = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=" + encodeUrl(pythonToJson(r))
    result = requests.get(url=web, headers=headers)
    src = result.content
    return src

def getIdContent(name):
    headers = { 'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7,la;q=0.6',
    'cache-control':'no-cache',
    'dnt':'1',
    'pragma':'no-cache',
    'referer':'https',
    'sec-fetch-mode':'no-cors',
    'sec-fetch-site':'cross-site',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }

    global instagramName
    instagramName = name
    web = website(instagramName)
    idResult = requests.get(url=web, headers=headers)
    idHtml = idResult.content

    return idHtml

def getId(userName):
    id = []
    pageCont = str(getIdContent(userName))
    ind = [x.isdigit() for x in pageCont].index(True)

    for num in pageCont[ind:]:
        if num.isdigit() == True:
            id.append(num)
        elif num.isdigit() == False:
            break
    idStr = "".join(id)
    return idStr

def getNumFollower(id):
    numFollow = []
    followCont = str(getFollowCont(id))
    ind =[x.isdigit() for x in followCont].index(True)

    for num in followCont[ind:]:
        if num.isdigit() == True:
            numFollow.append(num)
        elif num.isdigit() == False:
            break
    numFolStr = "".join(numFollow)
    return numFolStr

def main(userName):
    userId = getId(userName)
    numFollow = getNumFollower(userId)
    return numFollow
