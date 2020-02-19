import generateHtml
import os
import json
import csv
import shutil
from datetime import datetime

def create_lp_folder(folder_path):

    if not os.path.isfile(folder_path):
        os.makedirs(folder_path + 'PC')
        os.makedirs(folder_path + 'SP')
        print('create folder : {}'.format(folder_path))
    else:
        print('This folder is already exist.')

if __name__ == '__main__':
    
    # secretなデータを読み込む
    secret = {}
    with open('secret.json', 'r', encoding='utf-8') as f:
        secret = json.load(f)

    # inputなデータを読み込む
    input_data = {}
    with open('../input/{}'.format(secret['input_csv']), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # header = next(reader)  # ヘッダーを読み飛ばしたい時
        for row in reader:
            input_data[row[0]] = row[1] 


    now_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    # LPを置いとくフォルダをローカルに生成
    lp_path = '{}{}_{}/'.format(secret['local_lp_path'], secret['client_key'], now_str)
    create_lp_folder(lp_path)


    # フォルダに画像を引っ張ってくる
    shutil.copy2('{}{}'.format(secret['image_downloads_path'], input_data['pc_image']), '{}PC/{}'.format(lp_path, input_data['pc_image']))
    shutil.copy2('{}{}'.format(secret['image_downloads_path'], input_data['sp_image']), '{}SP/{}'.format(lp_path, input_data['sp_image']))


    # LPhtmlを生成してフォルダに置く
    generateHtml.generate_lp(lp_path, input_data)


    # FTPで送信する 
    # シェルスクリプトの引数をセッティング
    arg_list = [
        secret['local_lp_path'],
        '{}_{}/'.format(secret['client_key'], now_str),
        secret['ftp_address'],
        secret['ftp_remote_path'],
        secret['ftp_id'],
        secret['ftp_pass']
    ]

    
    os.system('./lp_folder_up.sh {0[0]} {0[1]} {0[2]} {0[3]} {0[4]} {0[5]}'.format(arg_list))