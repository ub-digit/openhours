#!/bin/bash

. /usr/local/etc/dbsettings.sh

DIR=/www/gundarutiner/boknings_admin

cd $DIR
>userlist
psql -h $DATABASE_HOST_ALIAS_DB $DATABASE_NAME_ALIAS_DB > /dev/null 2>&1 <<EOF
\t
\o $DIR/userlist
select anv_id from anv_namn where anv_nr in (select anv from anv_grupp where grupp in ( 511,602,508 ) );
EOF

# SB: Vi har filen lokalt i /etc/roxenshadow
# scp root@130.241.16.11:/etc/shadow . > /dev/null 2>&1

>$DIR/.htpasswd

echo ' xgaddc' >> userlist
echo ' xstrae' >> userlist

for i in $(cat userlist)
do
    grep "^$i:" /etc/roxenshadow | cut -d: -f1-2 >> $DIR/.htpasswd
done

# SB: Ingen mening att rota med en fil vi inte kopierat.
# chmod 700 $DIR/shadow 
# rm $DIR/shadow

touch $DIR/getuser.log
