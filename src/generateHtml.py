import csv
import json
import re
import datetime
import os
from jinja2 import Template, Environment, FileSystemLoader


def generate_default_file(input_data, timestamp_str):
    '''
    input_dataを基にdefaultファイルを生成。
    下地となるモノを一旦呼び出し、上書き更新してから、timestampを付けて別名保存。
    '''
    
    # base_defaultを読み込み
    default_data = {}
    with open(input_data['base_default'], 'r', encoding='utf-8') as f:
        default_data = json.load(f)

    # 以下、今回用に上書き
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
    
    # 名前を付けて、別名保存
    default_savepath = '../src/resource/default/{}/default_{}.json'.format(input_data['client_key'], timestamp_str)
    with open(default_savepath, 'w', encoding='utf-8') as outfile:
        json.dump(default_data, outfile,ensure_ascii=False)

    print('Generated Default File : {}'.format(default_savepath))
    return default_savepath


def generate_html(output_file_path, default_file_path, template_folder_path):
    '''
    html生成をハンドリング
    defaultファイルをtmplファイルにimplementしたものを、output_fileとして吐き出す
    '''

    # 今回の分のdefault.jsonを読み込んで、outputのhtmlを生成
    default_data = {}
    with open(default_file_path, 'r', encoding='utf-8') as f:
        default_data = json.load(f)

    # tmplを呼び出してrender
    tpl = Environment(loader=FileSystemLoader('.', encoding='utf_8')).get_template(template_folder_path)
    render = tpl.render(default_data)

    # render内容をhtmlファイルとして保存
    with open(output_file_path, 'w', encoding='utf_8') as stream:
        stream.write(render)
    
    print('Generated HTML : {}'.format(output_file_path))


def generate_lp(output_file_path, input_data):
    '''
    inputのdictを基にlpを生成ハンドリング。
    output_file_pathを親に、PC版とSP版をそれぞれ作る
    '''
    
    now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    default_file_path = generate_default_file(input_data, now_str)

    generate_html('{}PC/index.html'.format(output_file_path), default_file_path, input_data['pc_template'])
    generate_html('{}SP/index.html'.format(output_file_path), default_file_path, input_data['sp_template'])



if __name__ == '__main__':

    print('This is generateHtml')