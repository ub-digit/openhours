#!/usr/bin/perl

use POSIX qw(strftime);
use DBI;

$dagar = $ARGV[0] || 7;
$obj_id = $ARGV[1];
$lokal = $ARGV[2];
$dagar--;

$datum = strftime("%Y-%m-%d", localtime(time + 86400 * $dagar));
$dag = strftime("%A", localtime(time + 86400 * $dagar));

&connect_db;

$query_open = "select open, close from openhours where lokal_id = $lokal and (day = \'$datum\' or (day = \'$dag\' and from_dag <= \'$datum\')) order by prioritet, from_dag desc";    
$sth = $dbh->prepare($query_open);
$rv = $sth->execute;
undef @open_close;
@open_close = $sth->fetchrow_array;

$open = $open_close[0];
$close = $open_close[1];

$typ_query = "select b.typ, timmar_pass from typ_info t, boknings_objekt b where b.obj_id = $obj_id and t.typ = b.typ";
$sth = $dbh->prepare($typ_query);
$rv = $sth->execute;
undef $timmar_pass;
@lista = $sth->fetchrow_array;

$typ = $lista[0];
$timmar_pass = $lista[1];

# Nu vet vi allt... open, close samt antal timmar per pass.
# Nu ska alla objekt faa nya tider beroende paa om de aer aktiva och vilken typ de aer.

$start_tid = $open;
while ($start_tid <= ($close - ($timmar_pass / 2))) {
    $slut_tid = $start_tid + $timmar_pass;
    if ($slut_tid > $open_close[1]) {
	$slut_tid = $open_close[1];
    }
    # Detta aer alla bokningar som ska skapas. Antingen kan de skrivas till fil eller direkt in i databasen.
    printf "insert into bokning values ($obj_id, $typ, \'$datum\', %2.2f, %2.2f)\;\n", $start_tid, $slut_tid;
    $ins = "insert into bokning values ($obj_id, $typ, \'$datum\', $start_tid, $slut_tid)\;\n";
    $start_tid = $start_tid + $timmar_pass;
}





