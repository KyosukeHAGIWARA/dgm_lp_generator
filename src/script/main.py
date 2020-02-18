import csv
import json
import re
import datetime

# if __name__ == '__main__':



# グローバルで使うクライアントの識別子(ディレクトリ,LPのパスとか)
client_key = 'test_client'

# inputデータのファイルパス
input_csv = '../../input/' + 'order_test_client_20200218.csv'

now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


# inputからデータを読み込み
input_data = {}
with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    # header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        input_data[row[0]] = row[1] 

# print(input_data)


# base_defaultを読み込んで、今回の分のdefault.jsonを新規作成
default_data = {}
with open(input_data['base_default'], 'r', encoding='utf-8') as f:
    default_data = json.load(f)

default_data['title'] = input_data['title']

default_data['sale']['main_img_path'] = {
    'pc': input_data['pc_image'],
    'sp': input_data['sp_image']
}

default_data['sale']['period'] = {
    'start': {
        'yyyy': "2020",
        'mm': re.findall(r'[0-9]+', input_data['start'])[0],
        'dd': re.findall(r'[0-9]+', input_data['start'])[1],
        'wd': re.findall(r'（.）', input_data['start'])[0][1:2],
        'time': re.findall(r'[0-9]+:[0-9]+', input_data['start'])[0]
    },
    'end': {
        'yyyy': "2020",
        'mm': re.findall(r'[0-9]+', input_data['end'])[0],
        'dd': re.findall(r'[0-9]+', input_data['end'])[1],
        'wd': re.findall(r'（.）', input_data['end'])[0][1:2],
        'time': re.findall(r'[0-9]+:[0-9]+', input_data['end'])[0]
    },
}
print(default_data)

savepath = '../../src/resource/default/test_client/' + 'default_extend_{}.json'.format(now_str)
with open(savepath, 'w', encoding='utf-8') as outfile:
    json.dump(default_data, outfile,ensure_ascii=False)