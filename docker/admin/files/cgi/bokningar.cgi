#!/usr/bin/perl

use CGI;
use DBI;
use POSIX qw(strftime);

require "./connect_string.pl";

$cgi = new CGI;

$datum = $cgi->param('d');
$lokal = $cgi->param('l');
$typ = $cgi->param('t');
$start = $cgi->param('st');
$slut = $cgi->param('sl');
@id = $cgi->param('i');
$kommentar = $cgi->param('k');

&connect_db;

print "content-type: text/html\n\n";

if ($datum && $lokal && $typ && !$start && !$slut) {

    print "<form action = bokningar.cgi method = post>\n\r";
    print "<center><table border='0'>\n\r";
    print "<tr><td><b>Starttid:</b> </td><td>\n\r";
    
    print "<select name = st>\n\r";
    for ($i = 7; $i < 22; $i++) {
	print "<option value = $i>$i.00";
    }

    print "</select>\n\r";
    print "</td></tr><tr><td><b>Sluttid:</b> </td><td>\n\r";
    
    print "<select name = sl>\n\r";
    for ($i = 7; $i < 22; $i++) {
	print "<option value = $i>$i.00";
    }
    print "</select></td></tr>\n\r";

    print "<input type = 'hidden' name = 'd' value = '$datum'>";    

    $alla_query = "select obj_id, namn from boknings_objekt where typ = $typ and lokal_id = $lokal order by namn";
    
    $sth = $dbh->prepare($alla_query);
    $rv = $sth->execute;
    if ($rv > 10) { $antal = 10; } else { $antal = $rv; }
    print "<tr><td>";
    print "<b>V&auml;lj objekt att boka:</b><p><br>";
    print "V&auml;lj flera datorarbetsplatser <br> eller grupprum genom att ";
    print "<br>h&aring;lla ner Ctrl-knappen.";
    print "</td><td>";
    print "<select name = i multiple size = $antal>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
        if ($antal == 1) {
            print "<option value = $info[0] selected=true>$info[1]";
        }
        else {
            print "<option value = $info[0]>$info[1]";
        }
    }
    print "</select></td></tr><tr><td align = right>\n\r";
    print "<tr><td><b>Bokningsbeskrivning:</b> </td><td>";
    print "<input type = 'text' name = k maxlength = 20></td></tr>";

    print "<tr><td>&nbsp;</td><td align=right>\n\r";
    print "<input type=submit value = \"Boka\">\n\r";
    print "</td></tr></table></form>\n\r";
    
    print "</center>\n\r";
}

elsif ($datum && $id[0] && $start && $slut && $kommentar) {
    # print "@id $datum $start $slut<p>";
    foreach $id (@id) {
	$in .= "$id,";
    }
    chop $in;
    $update = "update bokning set bokad = true, bokad_barcode = '1122334455', status = 5, kommentar = '$kommentar' where dag = '$datum' and obj_id in ($in) and slut > $start and start < $slut and bokad = false and status = 1";

    $rv = $dbh->do($update);
    # $rc = $dbh->commit;
    if ($rv > 0) {
	# ok
	print "<h2>Bokning klar.</h2>";
	print "Kontrollera g&auml;rna bokningarna via det vanliga gr&auml;nssnittet<p>";
	print "Alla bokningar g&ouml;rs med l&aring;nekortsnummer 1122334455.<br>";
	print "Anv&auml;nd det numret om n&aring;gon av bokningarna ska avbokas.";
	print "<p>Dessa bokningar beh&ouml;ver <b>inte</b> kvitteras.";
    }
    else {
	# Fel
	print "FEL. Ingen bokning har skett";
	print "<p>$update<p>";
    }

}

else {
    print "Uppgifter saknas";
}













