import os
import lxml
import requests
import re
from bs4 import BeautifulSoup
def get_pdf():
    data_path = "./BaiduPDF"
    bool = os.path.exists(data_path)
    if (bool == False):
        os.mkdir(data_path)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Referer": "https://xueshu.baidu.com/"
    }
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Referer": "https://xueshu.baidu.com/usercenter/paper/"
                   "show?paperid=0341a45e1b3de453248d33f802022ff0&site=xueshu_se"
    }
    # 要搜索的名字
    search_key = input("请输入你要搜索的文献关键字:")
    # search_key ="python"
    # 百度学术返回的地址
    search_url = "https://xueshu.baidu.com/s?wd=" + search_key + "&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D"
    down_url = "https://sci.bban.top//pdf//10.1016//s1093-3263%252899%252900019-4.pdf"
    # 请求关键字得到的网页
    search_res = requests.get(url=search_url, headers=headers)
    pdf_list = re.findall(r"(//xueshu.baidu.com/usercenter/paper/show\?paperid=.*site=xueshu_se.*?)", search_res.text)
    for item in range(len(pdf_list)):
        # print(pdf_list[item])
        pdf_url = "https:"+pdf_list[item]
        # print(pdf_url)
        pdf_res = requests.get(url=pdf_url,headers=headers2)
        pdf_soup = BeautifulSoup(pdf_res.text,"lxml")
        # 获取pdf_name
        # ISBN数据抛弃
        pdf_name_get = pdf_soup.find_all("a",attrs={"data-click":"{'act_block':'main','button_tp':'title'}"})
        pdf_ret_isbn = re.findall(r"<p class=\"label_s\">ISBN：</p>", pdf_res.text)
        if len(pdf_name_get)&(len(pdf_ret_isbn)==0):
            # 去除头尾空格或者换行符
            pdf_name = str.strip(str(pdf_name_get[0].string))
            print("《%s》"%pdf_name,end="")
            pdf_doi_get = pdf_soup.find_all("p",attrs={"data-click":"{'button_tp':'doi'}"})
            if len(pdf_doi_get):
                pdf_doi =str.strip(str(pdf_doi_get[0].string))
                print("DOI编码为: %s"%pdf_doi)
                down_url = "https://sci.bban.top//pdf//" + pdf_doi + ".pdf"
                down_pdf = requests.get(url=down_url,headers=headers)
                # time.sleep(5)
                down_res = re.findall(r"<title>404 Not Found</title>",down_pdf.text)
                if len(down_res):
                    print("抱歉，不允许下载！")
                else:
                    sets = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
                    for char in pdf_name:
                        if char in sets:
                            pdf_name = pdf_name.replace(char, '')
                    with open(r"%s/%s.pdf"%(data_path,pdf_name), "wb")as file:
                        file.write(down_pdf.content)
            else:
                print("没有DOI编码")
        elif len(pdf_name_get)&(len(pdf_ret_isbn)!=0):
            pdf_name = str.strip(str(pdf_name_get[0].string))
            print("《%s》是isbn编码，无法免费下载"%pdf_name)
        else:
            pass




if __name__ == '__main__':
    get_pdf()