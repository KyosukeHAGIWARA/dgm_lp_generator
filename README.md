# 定型LPジェネレータ

## Description

定型LPを毎回差し替えするのは面倒かつ手間かつミスるので作った。
Pyhtonとjinja2が入ってた環境があればどこでも動く。

## usage

`python3 main.py` するだけ。

inputファイルとdefaultファイルとsecretファイルに必要な情報が入っていれば、ローカルで生成、アップロードまで1アクションで完了する。

## Update Plan

+ 設定ファイルが多すぎてごちゃごちゃなのでどうにかしたい
+ inputファイルすら書くのめんどいのでどうにか推測してくれる機能を追加したい