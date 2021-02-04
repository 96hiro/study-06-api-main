import requests
import urllib
import os
import pandas as pd
import datetime

#csv出力保存関数
def write_cvs(Gnl_Rank_List,Gnl_Item_List,gnr_ID):
    
    df = pd.DataFrame({"ランキング":Gnl_Rank_List,
        "商品名":Gnl_Item_List})
    #ファイル存在チェック
    if os.path.isfile('./Rakuten_Gnl_Rank({}).csv' .format(gnr_ID)):
        
        today = datetime.date.today()
        df.to_csv('./Rakuten_Gnl_Rank({})-{}.csv' .format(gnr_ID,today), encoding="utf-8_sig", mode='w', header=True, index=True)
    else:
        df.to_csv('./Rakuten_Gnl_Rank({}).csv' .format(gnr_ID), encoding="utf-8_sig", mode='w', header=True, index=True)




#商品検索(リクエストURL)
REQUEST_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
#商品の最小価格と最高価格(リクエストURL)
Product_RQ_URL = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
#任意のジャンルのランキングを取得(リクエストURL)
Product_Ranking_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?"

#アプリID
APP_ID="1019079537947262807"

#検索キーワード
serch_keyword = "鬼滅"

#商品検索
serch_params={
    "format" : "json",
    "keyword" : serch_keyword,
    "hits" : 5,
    "applicationId" : [APP_ID],
    "availability" : 0
}
print("----------商品名と価格を取得し出力する--------------------")
#serch_paramsの内容でリクエストを送信
response = requests.get(REQUEST_URL, serch_params)
result = response.json()

for i in range(0, len(result['Items'])):
    #商品名と価格を取得し出力する
    print(result['Items'][i]['Item']['itemName'])
    print(result['Items'][i]['Item']['itemPrice'])

#janコードを指定
serch_ID = 4953980840578

#対象商品の最小価格と最高価格の取得
serch_params2={
    "format" : "json",
    "keyword" : serch_ID,
    "applicationId" : [APP_ID],
    "availability" : 1
}

print("----------最小価格と最大価格を取得し出力する--------------------")
#serch_params2の内容でリクエストを送信
response = requests.get(Product_RQ_URL, serch_params2)
result2 = response.json()

for c in range(0, len(result2['Products'])):
    #最小価格と最大価格を取得し出力する
    print(result2['Products'][c]['Product']['minPrice'])
    print(result2['Products'][c]['Product']['maxPrice'])
# print(result2)

gnr_ID = 100804

#任意のジャンルのランキングを取得
serch_params3={
    "format" : "json",
    "applicationId" : [APP_ID],
    "genreId" : gnr_ID #インテリア
}

response = requests.get(Product_Ranking_URL, serch_params3)
result3 = response.json()
Gnl_Rank_List = []
Gnl_Item_List = []
for a in range(0, len(result3['Items'])):
    #ランキングと商品名を取得
    gnl_rank = result3['Items'][a]['Item']['rank']
    gnl_item = result3['Items'][a]['Item']['itemName']

    Gnl_Rank_List.append(gnl_rank)
    Gnl_Item_List.append(gnl_item)
# print(result3)

write_cvs(Gnl_Rank_List,Gnl_Item_List,gnr_ID)

