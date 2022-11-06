from flask import Flask, render_template

app=Flask(__name__) # __name__ 代表目前執行的模組
app.config.from_pyfile('configs.py')

@app.route("/") # 函式的裝飾 (Decorator): 以函式為基礎，提供附加功能
def home():
    return render_template("index.html")

@app.route("/students")
def pandas():
    import students

    return students.pandasMain()
# @app.route("/students")
# def pandas():
#     import students_allin

#     return students_allin.pandasMain()

@app.route("/crawler", methods=['GET', 'POST']) # Crawler、jieba
def crawler():
    import crawler

    return crawler.crawlerMain()

if __name__=="__main__": # 如果以主程式執行
    app.run() # 立刻啟動伺服器