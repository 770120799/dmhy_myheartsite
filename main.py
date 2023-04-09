import requests
import json

url = 'https://dongmanhuayuan.myheartsite.com/api/acg/search'

def anaylseSearchResult(result):
    # 获取 totalNum 值
    keyword = result['data']['keyword']
    totalNum = result['data']['totalNum']
    print(keyword + " found total " + str(totalNum) + " results")

def getSearchResult(keyword):
    data = {
        'keyword': keyword,
        'page': 1,
        'searchType': '',
        'serverType': 'server1'
    }
    proxies = {
        'http': 'http://localhost:10809',
        'https': 'http://localhost:10809'
    }

    # 输出格式化结果
    print("Start searching for \"" + keyword + "\"")
    response = requests.post(url, data=data, proxies=proxies)
    result = response.json()
    formatted_result = json.dumps(result, indent=4, ensure_ascii=False)

    # 输出格式化结果
    print(formatted_result)
    return result

if __name__ == '__main__':
    # searchResult = getSearchResult('ani 我家的英雄 baha')
    # anaylseSearchResult(searchResult)


    # 读取 JSON 文件
    with open('test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 调用函数
    anaylseSearchResult(data)