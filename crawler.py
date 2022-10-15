import urllib.request as req
import re
import bs4

def crawlerFunc():
    t_arr=[]

    # 抓取 PTT Stock版的網頁原始碼 (HTML)
    pages=2
    url="/bbs/Stock/index.html"
    getTitles(pages, url, t_arr)

    # 關鍵字詞分析
    tags=getKeyWords(t_arr)

    # 產生html Code
    html_text="<h2>=== 抓取 <a href='https://www.ptt.cc"+url+"' target='_blank'>PTT Stock版</a> 最新關鍵分詞 ===</h2>\n"
    html_text+="選取頁數： "+str(pages)+" 頁</br>\n"
    html_text+="選取標題數： "+str(len(t_arr))+" 筆</br>\n"
    html_text+="前10關鍵字詞："+"、".join(tags)

    return html_text

# 關鍵字詞分析
def getKeyWords(t_arr):
    import jieba
    import jieba.analyse

    data=" ".join(t_arr)
    tags=jieba.analyse.extract_tags(data, 10)
    return tags

# 抓取 PTT Stock版各網頁標題
def getTitles(pages, url, t_arr):
    if pages>0:
        pttURL="https://www.ptt.cc"
        url=pttURL+url

        # 建立一個 Request 物件，附加 Request Headers 的資訊
        request=req.Request(url, headers={
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data=response.read().decode("utf-8")

        # 解析原始碼，取得每篇文章的標題
        html_text=bs4.BeautifulSoup(data, "html.parser") # 讓 BeautifulSoup 協助我們解析 HTML 格式文件
        titles=html_text.find_all("div", {"class":"title"}) # 尋找 class="title" 的 div 標籤
        for i in range(len(titles)):
            if titles[i].a != None: # 如果標題包含 a 標籤 (沒有被刪除) 印出來
                t = titles[i].a.string
                regex=re.compile(r'^Re: ')
                t=regex.sub('', t)
                regex=re.compile(r'\[\w+\]\s')
                t=regex.sub('', t)
                t_arr.append(t)

        # 抓取上一頁的連結
        pages-=1
        url=html_text.find("a", string="‹ 上頁")["href"] # 找到內文是 < 上頁 的 a 標籤
        return getTitles(pages, url, t_arr)