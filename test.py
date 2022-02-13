import os.path

import requests
import yaml
from bs4 import BeautifulSoup

projectpath = os.path.abspath('.')
sep = os.sep
path = sep.join([projectpath, "highpoint.yml"])
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}


def countavg():
    """
    获取TTM(滚动市盈率)等权平均，40<countavg<45加钱就完事了
    :return:
    """
    response = requests.get("https://legulegu.com/stockdata/a-ttm-lyr", headers=headers)
    # print(response.text)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    countavg = str(soup.find_all('td')[3])[4:9]
    print("****TTM(滚动市盈率)等权平均:{0}，40<countavg<45加钱就完事了****\n".format(countavg))


def load_highpoint():
    """
    加载历史最高值
    :return:
    """
    with open(path, encoding="utf-8") as f:
        dict = yaml.safe_load(f)
        return dict


def get_gusuan(stockid):
    response = requests.get("http://fundgz.1234567.com.cn/js/{0}.js?rt=1639496117358".format(stockid), headers=headers)
    # print(response.text)
    response.encoding = 'utf-8'
    jsonpgz = response.text
    list1 = jsonpgz.split(",")[4][-7:-2]
    list2 = jsonpgz.split(",")[6][-20:-4]
    print("{0}基金估值{1}".format(list2, list1))
    return list1


def get_info(stockid):
    response = requests.get("http://fund.eastmoney.com/{0}.html?spm=aladin".format(stockid), headers=headers)
    # print(response.status_code)
    html = response.content.decode("utf-8", "ignore")
    # html = response.content.decode("gbk")
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    # print(str(soup.find_all(name='td', attrs={'class': 'alignRight bold'})[-22]))
    net_worth2 = str(soup.find_all(name='td', attrs={'class': 'alignRight bold'})[-22])[-11:-5]
    net_worth1 = str(soup.find_all(name='td', attrs={'class': 'alignRight bold'})[-20])[-11:-5]
    # print(net_worth1)
    day2 = str(soup.find_all(name='td', attrs={'class': 'alignLeft'})[-14])[-10:-5]
    day1 = str(soup.find_all(name='td', attrs={'class': 'alignLeft'})[-13])[-10:-5]
    # dict = load_highpoint()
    stockname = dict[stockid][0]
    highpoint = dict[stockid][1]
    if float(net_worth2) > float(highpoint):
        print("原最高值{0}".format(highpoint))
        highpoint = net_worth2
        dict[stockid][1] = net_worth2
        exppoint = float(highpoint) * 0.96
    else:
        stockname = dict[stockid][0]
        highpoint = dict[stockid][1]
        exppoint = float(highpoint) * 0.96
    # jiangfu = 100 - list1 / float(highpoint) * 100
    print(
        "**{0}  历史最高值：{1}\n******如果跌于最高值4%即 {4} 考虑买入******\n{2} 单位净值：{3}".format(stockname, highpoint, day2,
                                                                                 net_worth2,
                                                                                 exppoint))
    print("{2} 单位净值：{3}".format(stockname, highpoint, day1, net_worth1))
    return highpoint


if __name__ == '__main__':
    # obj = load_highpoint()
    # print(load_highpoint())
    countavg()
    dict = load_highpoint()
    for key in dict.keys():
        list1 = get_gusuan(key)
        highpoint = get_info(key)
        jiangfu = round(100 - float(list1) / float(highpoint) * 100, 5)
        print("降幅：{0}%\n".format(jiangfu))
    with open(path, "w", encoding='utf-8') as f:
        yaml.dump(dict, f, allow_unicode=True)
    # get_info("110013")
