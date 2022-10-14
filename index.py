from flask import Flask, render_template
app=Flask(__name__) # __name__ 代表目前執行的模組

@app.route("/") # 函式的裝飾 (Decorator): 以函式為基礎，提供附加功能
def home():
    return render_template("index.html")

@app.route("/p1") # 代表我們要處理的網站路徑
def p1():
    return render_template("p1.html")

@app.route("/p2")
def p2():
    return render_template("p2.html")

if __name__=="__main__": # 如果以主程式執行
    app.run() # 立刻啟動伺服器