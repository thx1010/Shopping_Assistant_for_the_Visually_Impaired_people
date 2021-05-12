# -*- coding: utf-8 -*- 
import sys
import time
import asyncio
from Script_tts import script_tts, script_tts_f
from Mecab_test import Q_1, do_mecab, Q_2
import random
import json
import os

def greeting():
    line = input()
    g_list = ['에코야', '에코', '백호야', '아이고야']
    if line in g_list:
        print({"message": "안녕하세요. 당신의 AI 패션 메이트 에코입니다. 어떤 옷을 찾고 계신가요?", "Imgurl": "null"})
        sys.stdout.flush()
    else:
        print({"message": "제가 잘 이해한건지 모르겠네요.", "Imgurl": "null"})
        sys.stdout.flush()
        greeting()

global Clo_Key
global Clo_Value
def clo_Id():
    line = input()
    me_list = do_mecab(line)
    fin = Q_1(me_list)
    keys = fin.keys()
    global Clo_Key
    Clo_Key = list(keys)
    values = fin.values()
    global Clo_Value
    Clo_Value = list(values)
    try:
        Clo_Key[0]
        #print(fin)
        
    except IndexError:
        print({"message":"잘 못 알아들었습니다. 다시 한번 말씀해주세요", "Imgurl": "null"})
        sys.stdout.flush()
        clo_Id()

global Pat_Key
global Pat_Value
def Pat_Id():
    line = input()
    me_list = do_mecab(line)
    fin = Q_1(me_list)
    keys = fin.keys()
    global Pat_Key
    Pat_Key = list(keys)
    values = fin.values()
    global Pat_Value
    Pat_Value = list(values)
    try:
        Pat_Key[0]
        #print(fin)
    except IndexError:
        print({"message":"잘 못 알아들었습니다. 다시 한번 말씀해주세요", "Imgurl": "null"})
        sys.stdout.flush()
        Pat_Id()

global Len_Key
global Len_Value
def Len_Id():
    line = input()
    me_list = do_mecab(line)
    fin = Q_1(me_list)
    keys = fin.keys()
    global Len_Key
    Len_Key = list(keys)
    values = fin.values()
    global Len_Value
    Len_Value = list(values)
    try:
        Len_Key[0]
        #print(fin)
        
    except IndexError:
        print({"message":"잘 못알아들었습니다. 다시 한번 말씀해주세요", "Imgurl": "null"})
        sys.stdout.flush()
        Len_Id()

global Price_ID
def pri_Id():
    line = input()
    me_list = do_mecab(line)
    global Price_ID
    Price_ID = Q_2(me_list)

    try:
        Price_ID[0]
        #print(Price_ID[0], type(Price_ID[1][0]))
        
    except IndexError:
        print({"message": "잘 못알아들었습니다. 다시 한번 말씀해주세요", "Imgurl": "null"})
        sys.stdout.flush()
        pri_Id()


#Mysql Connection
import pymysql
conn = pymysql.connect(
    host= '211.214.181.77',
    user= 'daye',
    password = '1234',
    db='ClothesInfo',
    charset='utf8'
)
cursor = conn.cursor()

global myresult
def Search_db():
    global myresult
    if (len(Clo_Key) == 1) and (Price_ID[0] == "이하"):
        sql = "select Distinct(ID), Price, Pattern, Material, Neckline, leng, Imgurl, Color, C_sat, C_value from tshirt where ("+Clo_Key[0]+" like '%"+Clo_Value[0][0]+"%') and (Price <= "+str(Price_ID[1][0])+") and ("+Pat_Key[0]+" like '%"+Pat_Value[0][0]+"%') and ("+Len_Key[0]+" like '%"+Len_Value[0][0]+"%') order by rand();"
        cursor.execute(sql)
        myresult = cursor.fetchall()
        #for x in myresult:
            #print(str(x))
    elif (len(Clo_Key) == 1) and (Price_ID[0] == "이상"):
        sql = "select Distinct(ID), Price, Pattern, Material, Neckline, leng, Imgurl, Color, C_sat, C_value from tshirt where ("+Clo_Key[0]+" like '%"+Clo_Value[0][0]+"%') and (Price >= "+str(Price_ID[1][0])+") and ("+Pat_Key[0]+" like '%"+Pat_Value[0][0]+"%') and ("+Len_Key[0]+" like '%"+Len_Value[0][0]+"%') order by rand();"
        cursor.execute(sql)
        myresult = cursor.fetchall()
    elif (len(Clo_Key) == 2) and (Price_ID[0] == "이하"):
        sql = "select Distinct(ID), Price, Pattern, Material, Neckline, leng, Imgurl, Color, C_sat, C_value from tshirt where ("+Clo_Key[0]+" like '%"+Clo_Value[0][0]+"%') and ("+Clo_Key[1]+" like '%"+Clo_Value[1][0]+"%') and (Price <= "+str(Price_ID[1][0])+") and ("+Pat_Key[0]+" like '%"+Pat_Value[0][0]+"%') and ("+Len_Key[0]+" like '%"+Len_Value[0][0]+"%') order by rand();"
        cursor.execute(sql)
        myresult = cursor.fetchall()
    elif (len(Clo_Key) == 2) and (Price_ID[0] == "이상"):
        sql = "select Distinct(ID), Price, Pattern, Material, Neckline, leng, Imgurl, Color, C_sat, C_value from tshirt where ("+Clo_Key[0]+" like '%"+Clo_Value[0][0]+"%') and ("+Clo_Key[1]+" like '%"+Clo_Value[1][0]+"%') and (Price >= "+str(Price_ID[1][0])+") and ("+Pat_Key[0]+" like '%"+Pat_Value[0][0]+"%') and ("+Len_Key[0]+" like '%"+Len_Value[0][0]+"%') order by rand();"
        cursor.execute(sql)
        myresult = cursor.fetchall()
   
    print({"message": script_tts_f(myresult[0][0], myresult[0][1]) + "이 옷에 대해 더 알아보시겠습니까?", "Imgurl": "http:" + myresult[0][6]})

def more():
    line = input()
    a_line = ["응", "네",  "어", "그래"]
    if line in a_line:
        print({"message": script_tts(myresult[0][2], myresult[0][3], myresult[0][4], myresult[0][5], myresult[0][7], myresult[0][8], myresult[0][9]) + "이 옷을 내 옷장에 넣을까요?", "Imgurl": "http:" + myresult[0][6]})
    else:
        print({"message": "다시 한번 말씀해주세요.", "Imgurl": "null"})
        more()

def select():
    global myresult
    i = 1
    while True:
        i = i+1
        line = input()
        a_line = ["응", "네",  "어", "그래"]
        b_line = ["아니", "아니요"]
        if line in a_line:
            print({"message": "네 알겠습니다. 내 옷장에 넣어드렸어요. 쇼핑을 계속하시겠습니까?", "Imgurl": "null"})
            break
        elif line in b_line:
            print({"message": "다음 코디입니다." + script_tts_f(myresult[i][0], myresult[i][1])+ "이 옷에 대해 더 알아보시겠습니까?", "Imgurl": "http:" + myresult[i][6]})
            line2 = input()
            if line2 in a_line:
                print({"message": script_tts(myresult[i][2], myresult[i][3], myresult[i][4], myresult[i][5], myresult[i][7], myresult[i][8], myresult[i][9]) + "이 옷을 선택하시겠습니까?", "Imgurl": "http:" + myresult[i][6]})
                
            elif line2 in b_line:
                print({"message": "이 옷을 내 옷장에 넣을까요?", "Imgurl": "null"})         
        else:
            print({"message": "다시 한번 말씀해주세요.", "Imgurl": "null"})
            select()
             
def check():
    line = input()
    a_line = ["응", "네",  "어", "그래"]
    b_line = ["아니", "아니요"]
    if line in a_line:
        print({"message": "쇼핑을 다시 시작합니다. 무슨 옷을 찾으시나요?", "Imgurl": "null"})
        main()
    elif line in b_line:
        print({"message": "에코가 종료됩니다. 이용해 주셔서 감사합니다.", "Imgurl": "null"}) 
        sys.exit()
    else:
        print({"message": "다시 한번 말씀해주세요.", "Imgurl": "null"})
        check()

def main():
    clo_Id()
    print({"message": "상품 검색이 완료되었습니다. 가격대는 어떻게 설정할까요?", "Imgurl": "null"})
    pri_Id()
    print({"message": "가격대 설정이 완료되었습니다. 좋아하는 패턴이 있나요?", "Imgurl": "null"})
    Pat_Id()
    print({"message": "원하시는 패턴으로 선택했습니다. 어떤 기장을 원하시나요?", "Imgurl": "null"})
    Len_Id()
    Search_db()
    more()
    select()
    check()
    
greeting()
main()

conn.commit()
conn.close()