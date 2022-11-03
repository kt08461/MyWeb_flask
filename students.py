import pandas as pd
import base64
from matplotlib import pyplot as plt
from flask import Flask, render_template
from io import BytesIO

TitleFont = {'fontsize':16, 'fontweight':'bold'}

def pandasMain():
    # 統計國立、私立學校數量
    cntSchools()

    # 統計男、女學生人數
    cntGender()

    # 統計各縣市有多少學校
    cntSchoolsByCity()

    return render_template("students.html", text=text)

def init_data():
    def setImgFont():
        plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False

    setImgFont()

    file_path="data/110_student.csv"
    df = pd.read_csv(file_path, header=0,dtype={'學校代碼':str})
    df = df.applymap(lambda x: x.replace(',',''))
    df = df.applymap(lambda x: x.replace('-','0'))

    for c in df.columns[4:-2]:
        df[c] = df[c].astype('int')

    return df

# 統計國立、私立學校數量
def cntSchools():
    df = df110.groupby(by='學校名稱', as_index=False).sum(numeric_only=True)
    df_n = df[df['學校名稱'].str.contains('國立')]
    df_p = df[~df['學校名稱'].str.contains('國立')]
    text["sch_pub"] = len(df_n)
    text["sch_pri"] = len(df_p)
    text["sch_total"] = len(df_n)+len(df_p)

# 統計各縣市有多少學校
def cntSchoolsByCity():
    df_city_u = df110.groupby(by=['縣市名稱','學校名稱'],
                            as_index=False).sum(numeric_only=True)
    df_city = df_city_u.groupby(by='縣市名稱').count()
    df_city = pd.DataFrame(df_city['學校名稱'])
    df_city.columns=['學校數量']

    imgSchoolsByCity(df_city)

# 長條圖: 各縣市學校數量
def imgSchoolsByCity(df):
    X = [i for i in range(len(df))]
    Y = list(df['學校數量'])

    # 長條圖
    fig = plt.figure(figsize=(10, 5))
    ax = plt.gca()
    ax.set_title('各縣市學校數量', TitleFont)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # 加文字
    plt.bar(X, Y)
    for x, y in zip(X, Y):
        plt.text(x, y+0.05, '%d' % y, ha='center', va='bottom')

    plt.xticks(X,df.index.str[3:], rotation=90)
    plt.ylabel('學校數量')

    # 圖檔轉Base64
    text["plot"]["city_schools"] = imgBase64(fig)

# 統計男、女學生人數
def cntGender():
    text["stud_male"] = df110[df110.columns[5]].sum()
    text["stud_female"] = df110[df110.columns[6]].sum()
    text["stud_total"] = format(text["stud_male"] + text["stud_female"], ',')
    text["stud_male"] = format(text["stud_male"], ',')
    text["stud_female"] = format(text["stud_female"], ',')

# 圖檔轉Base64
def imgBase64(fig):
    img_fp = BytesIO()
    fig.savefig(img_fp, format='png', bbox_inches='tight')
    img_b64 = base64.encodebytes(img_fp.getvalue()).decode()
    img_b64 = 'data:image/png;base64,' + str(img_b64)

    return img_b64

text = {'plot':{}}
df110 = init_data()
pandasMain()