#!/usr/bin/perl

use DBI;
use CGI;

require "./connect_string.pl";

$cgi = new CGI;

$lokal = $cgi->param('l');
$d = $cgi->param('d');
@di = $cgi->param('di');
$e = $cgi->param('e');
@ei = $cgi->param('ei');
$radera = $cgi->param('r');

print "Content-type: text/html\n\n";

if ($d && $di[0] && $lokal) { #
    $ok = 1;
}
if ($e && $ei[0] && $lokal) { #
    $ok = 1;
}
if ($radera == 1) {
    $ok = 2;
}

if ($ok == 1) {
    print "<br><p><blockquote>\n\r";
    print "&Auml;r du s&auml;ker p&aring; att du ska radera dessa tider?<br>\n\r";
    print "<form action = radera_tider.cgi method = get>\n\r";
    print "<input type = hidden name = l value = $lokal>\n\r";
    print "<input type = hidden name = d value = $d>\n\r";

    foreach $di (@di) {
	print "<input type = hidden name = di value = $di>\n\r";
    }
    foreach $ei (@ei) {
	print "<input type = hidden name = ei value = $ei>\n\r";
    }

    print "<input type = hidden name = e value = $e>\n\r";
    print "<input type = hidden name = r value = 1>\n\r";

    print "<br><table border = 0><tr><td valign = top>\n\r";
    print "<input type = submit name = Skicka value = Radera>\n\r";
    print "</form></td><td width = 70>&nbsp;</td><td valign = top>\n\r";
    
    print "<form action = ./ method = get>\n\r";
    print "<input type = submit name = Avbryt value = Avbryt>\n\r";
    print "</td></tr></table>\n\r";
    print "</blockquote>\n\r";    
}

elsif ($ok == 2) {

    $pelle = 0;

    # Om $d saa ska prioritet 2 raderas (generell dag)
    # Om $e saa ska prioritet 1 raderas (enskild dag)
    &connect_db;

    if ($d) {
	foreach $di (@di) {
	    # $lista[0] = oid, $lista[1] = from_dag
	    @lista = split /\|/, $di;
	    $del_query = "delete from openhours where prioritet = 2 and oid = $lista[0] and from_dag = \'$lista[1]\' and lokal_id = $lokal\;";
	    $sth = $dbh->prepare($del_query);
	    $rv = $sth->execute;
	    print "antal = $rv <br>\n\r";
	    $pelle += $rv;
	}
	print "<p>Antal raderade dagar $pelle";
    }
    #$alla_query = "select obj_id, namn, kommentar from boknings_objekt where typ = $typ and lokal = $lokal";
    
    elsif ($e) {
	foreach $ei (@ei) {
	    # $lista[0] = oid, $lista[1] = from_dag
	    @lista = split /\|/, $ei;
	    $del_query = "delete from openhours where oid = $lista[0] and prioritet = 1 and day = \'$lista[1]\' and lokal_id = $lokal\;";
	    $sth = $dbh->prepare($del_query);
	    $rv = $sth->execute;
	    print "antal = $rv <br>\n\r";
	    $pelle += $rv;
	}
	print "<p>Antal raderade dagar $pelle";
    }
    else { # Ska inte kunna haenda...
	print "<html><body>Fel uppgifter</body></html>\n\r";
    }
    print "<p>Kontrollera att antalet raderade poster st&auml;mmer med antalet dagar som ni hade markerat.<p>\n\r";
    print "Om detta inte st&auml;mmer, <a href = visa_alla_tider.cgi?l=$l\&t=$typ>tryck h&auml;r</a> och prova igen";
    print "<p>Om ni trots flera f&ouml;rs&ouml;k inte lyckas radera en dag/tid, kontakta it-avdelningen / Lars Prytz";
    print "<p><h2>OBS</h2>Kontrollera <b>alltid</b> att det finns minst en post per veckodag med from-datum mindre &auml;n ";
    print "dagen datum kvar efter att ni har raderat tider. <br>Detta kan ni g&ouml;ra ";
    print "<a href = visa_alla_tider.cgi?l=$l\&t=$typ>h&auml;r</a>.";
}
else { # uppgifter saknas
    print <<_SLUT_;
<html><body>
Uppgifter saknas
</body></html>
_SLUT_
}
