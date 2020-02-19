import csv
import json
import re
import datetime
import os
from jinja2 import Template, Environment, FileSystemLoader


def generate_default_file(input_file_path, timestamp_str):
    # inputからデータを読み込み
    input_data = {}
    with open(input_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # header = next(reader)  # ヘッダーを読み飛ばしたい時

        for row in reader:
            input_data[row[0]] = row[1] 

    print(input_data)


    # base_defaultを読み込んで、今回の分のdefault.jsonを新規作成
    default_data = {}
    with open(input_data['base_default'], 'r', encoding='utf-8') as f:
        default_data = json.load(f)

    default_data['sale']['title'] = input_data['title']

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

    default_savepath = '../src/resource/default/test_client/' + 'default_extend_{}.json'.format(timestamp_str)
    with open(default_savepath, 'w', encoding='utf-8') as outfile:
        json.dump(default_data, outfile,ensure_ascii=False)

    return default_savepath



def generate_html(output_folder_path, default_file_path, template_folder_path,  timestamp_str):
    
    default_data = {}
    # 今回の分のdefault.jsonを読み込んで、outputのhtmlを生成
    with open(default_file_path, 'r', encoding='utf-8') as f:
        default_data = json.load(f)

    env = Environment(loader=FileSystemLoader('.', encoding='utf_8'))
    tpl = env.get_template(template_folder_path)
    render = tpl.render(default_data)

    output_savepath = output_folder_path + 'output_{}.html'.format(timestamp_str)
    with open(output_savepath, 'w', encoding='utf_8') as stream:
            stream.write(render)


if __name__ == '__main__':

    # secretなデータを読み込む
    secret = {}
    with open('secret.json', 'r', encoding='utf-8') as f:
        secret = json.load(f)


    # グローバルで使うクライアントの識別子(ディレクトリ,LPのパスとか)
    client_key = secret['client_key']

    # inputデータのファイルパス
    input_csv = '../input/' + secret['input_csv'] 

    now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    default_file_path = generate_default_file(input_csv, now_str)

    generate_html('../output/{}/pc/'.format(client_key), default_file_path, './template/PC/general_template.html', now_str)
    generate_html('../output/{}/sp/'.format(client_key), default_file_path, './template/SP/general_template.html', now_str)