#!/bin/sh
lp_path=$1 
lp_pass=$2

ftp_address=$3
ftp_remote_path=$4
ftp_id=$5
ftp_pass=$6


cd ${lp_path}${lp_pass}
pwd

ftp -n << END
open $ftp_address
user $ftp_id $ftp_pass 
bin
prompt

cd $ftp_remote_path
mkdir $lp_pass
cd $lp_pass

lcd PC
mput *

cd ..
cd ..
cd sp/ch
mkdir $lp_pass
cd $lp_pass

lcd ..
lcd SP

mput *

bye
END