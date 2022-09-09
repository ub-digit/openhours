#! /bin/ksh

PATH=/usr/local/postgres/bin:/usr/local/bin:$PATH
LD_LIBRARY_PATH=/usr/local/postgres/lib:/usr/local/lib
export LD_LIBRARY_PATH PATH

cd /export/home/gubmail

./skicka_aktiveringsmail.pl >> ./aktivering.log 2>&1
