import numpy as np
import base64
from flask import Flask, render_template
from matplotlib import pyplot as plt
from io import BytesIO

def pandasMain():
    x = np.arange(0, 10, 0.1)
    y = np.sin(x)
    plt.plot(x, y)
    # plt.show()

    # 轉 Base64
    img_fp = BytesIO()
    plt.savefig(img_fp, format='png')
    img_fp.seek(0)
    img_b64 = base64.b64encode(img_fp.getvalue()) # 將圖片轉為base64
    img_b64 = str(img_b64, "utf-8") # 提取base64字符串，不然會是-->b'xxxxx

    # 產生html Code
    return render_template("students.html").format(img_b64)

pandasMain()