import keepa
import requests
from urllib.parse import quote
import time
import random
import json
import sys

#待機関数
def wait():
    time.sleep(random.uniform(2,3))


#ライセンスキー照合関数
def cheack_license(license_key, license_url):
    res = requests.get(license_url + str('?license=') + license_key)
    res_json = res.json()
    flag_message = res_json['message']
    if flag_message == 'pass':
        return True
    else:
        return False

# LINE通知用関数
def notify_to_line(token, text):
    line_notify_token = token
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': text}
    requests.post(line_notify_api, headers = headers, data = data)

# 設置値読込関数
def read_setting():
    with open("./setting/setting.json", "r", encoding="utf-8") as read:
        data_dict = json.load(read)
    license_key = data_dict["general-setting"]["license-key"]
    license_url = data_dict["general-setting"]["license-url"]
    notice_flag = data_dict["general-setting"]["notice"]
    line_token = data_dict["general-setting"]["notify-token"]
    keepa_token = data_dict["general-setting"]["keepa-token"]
    rakten_token = data_dict["general-setting"]["rakten-token"]
    rate = data_dict["search-setting"]["rate"]
    return license_key, license_url, notice_flag, line_token, keepa_token, rakten_token, rate

# 対象ストアURL読込関数
def read_store_urls():
    store_urls = []
    with open("./data/urls.txt", "r", encoding="utf-8") as read:
        el = read.readlines()
    for row in el:
        word = str(row).strip()
        store_urls.append(word)
    return store_urls

# NGワード読込関数
def read_ng_words():
    ng_words = []
    with open("./data/NGwords.txt", "r", encoding="utf-8") as read:
        el = read.readlines()
    for row in el:
        word = str(row).strip()
        ng_words.append(word)
    return ng_words

# ストア商品取得関数
def get_store_products(rakten_token, store_url, ng_words):
    # 情報の取り出し
    shopCode = str(store_url).split('/')[3]
    # NGワードの整形
    ng_in = quote(" ".join(ng_words))
    # ストアコードでの検索
    base_url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json'
    parms = {
        # ストアコード
        "shopCode": shopCode,
        # Token
        "applicationId": rakten_token,
        # NG word oRFlag　は複数のNGワード対等の為設定
        "NGKeyword": ng_in,
        "orFlag": "1",
        # 出力されるJSONのフォーマット指定
        "formatVersion": "2",
        # 取得ページ数（最大の100を指定）
        "page": "100"
    }
    # Make Requests URL
    for key in parms:
            base_url += '&' + str(key) + '=' + parms[key]
    # Requests
    res = requests.get(base_url)
    time.sleep(1)
    res_json = res.json()
    print(res_json)
    # 【楽天の1枚⽬の商品写真】
    # 【楽天の商品名】
    # 【楽天の価格】
    # 【楽天のURL】※（別タブで表⽰設定）
    return_list = []
    res_products = res_json["Items"]
    for res_product in res_products:
        return_list.append([res_product["mediumImageUrls"][0], res_product["itemName"], res_product["itemPrice"], res_product["itemUrl"]])
    return return_list

# keepaデータ取得関数
def get_keepa_data(return_list, rate):
    result_list = []
    for return_item in return_list:
        search_keyword = return_item[1]
        rakuten_price = return_item[2]
        # keepaでのキーワード検索
        # 価格比較
        # dev
        keepa_price = 100
        if compare(rakuten_price, keepa_price, rate):
            # result_listに格納
            result_list.append()
        else:
            pass
    return result_list

# 比較関数
def compare(rakuten_price, keepa_price, rate):
    # dev
    if rakuten_price*float(rate) >= keepa_price:
        return True
    else:
        return False

# HTML出力関数
def output_html(result_list):
    pass

if __name__ == "__main__":
    # init
    print("[INFO]:設定ファイルの読み込み")
    license_key, license_url, notice_flag, line_token, keepa_token, rakten_token, rate = read_setting()
    # license
    license_flag = cheack_license(license_key, license_url)
    if license_flag:
        pass
    else:
        print("[WARNING]:ライセンス認証に失敗しました。")
        time.sleep(10)
        sys.exit()
    # read URL
    store_urls = read_store_urls()
    # read NG Words
    ng_words = read_ng_words()
    # main
    result_list = []
    for store_url in store_urls:
        pass
    output_html(result_list)
    notify_to_line(line_token, "検索終了")
    print("[INFO]:検索終了")
    print("[INFO]:10秒後にプログラムを終了します")
    time.sleep(10)
    sys.exit()

# 【楽天の1枚⽬の商品写真】
# 【楽天の商品名】
# 【楽天の価格】
# 【楽天のURL】※（別タブで表⽰設定）
# 【Amazonの1枚⽬の商品写真】
# 【Amazonの商品名】
# 【Amazonの価格】
# 【AmazonのURL】※（別タブで表⽰）
