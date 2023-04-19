import requests, json

searchUrl = 'https://dongmanhuayuan.myheartsite.com/api/acg/search'
detailUrl = 'https://dongmanhuayuan.myheartsite.com/api/acg/detail'

proxies = {
    'http': 'http://localhost:10809',
    'https': 'http://localhost:10809'
}
# Aria config Start #
REMOTEA_DDR="192.168.1.50"
DONLOAD_FOLDER = "/downloads/新番"
TOKEN = "downl0ad"
# Aria config End #

# Database config Start #
subcribeList = "subscription_list.py"
databaseFolder = "./database/"
# Database config End #

# *********************************** Aria donwnload code *********************************** #
def ariaDonload(fileURL,filePath=DONLOAD_FOLDER,token=TOKEN,aria2RemoteURL=REMOTEA_DDR,port="6800"):
	if filePath != "":
		filePath = {"dir":filePath}
	else:
		filePath = {}
	token = "token:" + token
	requestHeaders = {
				"Accept":"application/json, text/plain, */*",
				"Content-Type":"application/json;charset=UTF-8"
			}
	requestPayload = {
				"jsonrpc":"2.0",
				"method":"aria2.addUri",
				"id":"QXJpYU5nXzE1NjYzNjc2NTZfMC4xMDk3NDc1ODUzNzE4MzEyNw==",
				"params":
					[token,[fileURL],filePath]
			}
	response = requests.post(url="http://"+aria2RemoteURL+":"+port+"/jsonrpc", headers=requestHeaders, data=json.dumps(requestPayload), timeout=5)
	print(response.json())
	if "[200]" in str(response):
		print("[投送成功] 行动编号: " + response.json()['result'])
		return 200
	elif "error" in response.json():
		message = response.json()['error']['message']
		if message == "Unauthorized":
			warning = "[投送失败] 行动暗号错误"
		elif message == "No URI to download.":
			warning = "[投送失败] 运载目的地错误"
		print(warning)

# *********************************** Website anaylse code *********************************** #
def getDownloadLink(link):
    data = {
        'link': link
    }
    print("Start searching for Download link")
    response = requests.post(detailUrl, data=data, proxies=proxies)
    result = response.json()
    formatted_result = json.dumps(result, indent=4, ensure_ascii=False)

    # 输出link
    magnetLink1 = result['data']['magnetLink1']
    magnetLink2 = result['data']['magnetLink2']
    print("Get link1: " + magnetLink1)
    print("Get link2: " + magnetLink2)

    return magnetLink2    

def anaylseSearchResult(result):
    # 获取 totalNum 值
    keyword = result['data']['keyword']
    totalNum = result['data']['totalNum']
    print("\033[32m" + keyword + " found total " + str(totalNum) + " results" + "\033[0m")
    
    # 获取搜索结果列表
    searchList = result['data']['searchData']
    for i in range(0,len(searchList)):
        # print(searchList[i]['link'])
        link = getDownloadLink(searchList[i]['link'])
        # 开始下载
        print("Start downloading......")
        # ariaDonload(link)

    # 分割线
    print("\033[94m<<<============================ Search \"" + keyword + "\" end ============================>>>\033[0m")


def getSearchResult(keyword):
    data = {
        'keyword': keyword,
        'page': 1,
        'searchType': '',
        'serverType': 'server2'
    }

    # 输出格式化结果
    print("Start searching for \"" + keyword + "\"")
    response = requests.post(searchUrl, data=data, proxies=proxies)
    result = response.json()
    formatted_result = json.dumps(result, indent=4, ensure_ascii=False)

    # 输出格式化结果
    # print(formatted_result)
    return result

# *********************************** Database code *********************************** #
import os
def readJSON(path, key="", value=""):
	with open(path, 'r', encoding='utf-8') as jsonFile:
		jsonDict = json.load(jsonFile)
		return jsonDict

def writeJSON(path, newJSON):
	with open(path, "w", encoding='utf-8') as jsonFile:
		json.dump(newJSON, jsonFile, indent=4, ensure_ascii=False)
		return 200

def checkDatabase(title):
	if os.path.exists(databaseFolder):
		for fileName in os.listdir(databaseFolder):
			if(fileName.find(title) != -1):
				return True
	else:
		os.mkdir(databaseFolder)
		print("mkdir", databaseFolder)
	return False

def creatNewDatabase(Bangumi):
	rssDict = {
		'keyWord': Bangumi['keyword'],
		'items':[]
	}
	writeJSON(databaseFolder+Bangumi['title']+".json", rssDict)


# *********************************** main code *********************************** #
if __name__ == '__main__':
    # searchResult = getSearchResult('ani 我家的英雄 baha')
    # anaylseSearchResult(searchResult)

	if os.path.isfile(subcribeList):
		from subscription_list import subscription_List
		for Bangumi in subscription_List:
			print("--------------------------------" + Bangumi['title'] + "--------------------------------")
			if(checkDatabase(Bangumi['title'])):
				print("Found", Bangumi['title'])
				print("Start checking for updates.")
			else:
				print("Database not found", Bangumi['title'])
				print("Create it.")
				creatNewDatabase(Bangumi)
			localInfo = readJSON(databaseFolder+Bangumi['title']+".json")
			localInfoItem = localInfo['items']
			
			searchResult=getSearchResult(localInfo['keyWord'])
			anaylseSearchResult(searchResult)
            # 换行
			print(' ')

    # # 读取 JSON 文件
    # with open('test_1_link.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)

    # # 调用函数
    # anaylseSearchResult(data)
    


