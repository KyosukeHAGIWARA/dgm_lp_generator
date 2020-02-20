import generateHtml
import os
import json
import csv
import shutil
from datetime import datetime

def create_lp_folder(folder_path):
    '''
    引数folder_pathを親として空フォルダを作成(子供にPC/ SP/を持つ)
    既にあった場合更地にして作り直す
    '''

    if not os.path.isdir(folder_path):
        os.makedirs(folder_path + 'PC')
        os.makedirs(folder_path + 'SP')
        print('create Folder : {}'.format(folder_path))
    else:
        print('Create Folder Warning : This folder is already exist. Will be overwritten.')
        shutil.rmtree(folder_path)
        create_lp_folder(folder_path)

def file_read(file_name):
    '''
    fileを開いて中身をdictとして返す
    csvは横持のinput_fileのみを想定しているためdict。
    json/csvでなければなにもしない
    '''
    
    output = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        if file_name.split('.')[-1] == 'csv':
            reader = csv.reader(f)
            for row in reader:
                output[row[0]] = row[1]
        elif file_name.split('.')[-1] == 'json':
            output = json.load(f)
        else:
            print('file_read Error: File is not csv or json.')
    return output

if __name__ == '__main__':
    

    # 設定ファイル読み込む
    secret = file_read('./secret.json')
    input_data = file_read('../input/{}'.format(secret['input_csv']))


    #各所末尾のタイムスタンプ
    now_str = datetime.now().strftime('%Y%m%d')

    # LPを置いとくフォルダXをローカルに生成
    print('')
    lp_path = '{}{}_{}/'.format(secret['local_lp_path'], input_data['client_key'], now_str)
    create_lp_folder(lp_path)



    # フォルダXに画像を引っ張ってくる
    print('')
    shutil.copy2('{}{}'.format(secret['image_downloads_path'], input_data['pc_image']), '{}PC/{}'.format(lp_path, input_data['pc_image']))
    shutil.copy2('{}{}'.format(secret['image_downloads_path'], input_data['sp_image']), '{}SP/{}'.format(lp_path, input_data['sp_image']))

    # LPhtmlを生成してフォルダXに置く
    print('')
    generateHtml.generate_lp(lp_path, input_data)


    # FTPでフォルダXをリモートに送信する 
    arg_list = [
        secret['local_lp_path'],
        '{}_{}/'.format(input_data['client_key'], now_str),
        secret['ftp_address'],
        secret['ftp_remote_path'],
        secret['ftp_id'],
        secret['ftp_pass']
    ]
    os.system('./lp_folder_up.sh {0[0]} {0[1]} {0[2]} {0[3]} {0[4]} {0[5]}'.format(arg_list))

    # 最終的なURLを表示
    print('')
    print('Upload Completed! Check this url.')
    print('=================================================================')
    print('https://www.digimart.net/ch/{}_{}/'.format(input_data['client_key'], now_str))
    print('=================================================================')

