#!/usr/bin/perl

use DBI;
use CGI;

require "./connect_string.pl";

$cgi = new CGI;

$typ = $cgi->param('t');
$lokal = $cgi->param('l');

&connect_db;

print "Content-type: text/html\n\n";

if ($lokal && $typ) {
    $alla_query = "select obj_id, namn, substr(kommentar,1,75) from boknings_objekt where typ = $typ and lokal_id = $lokal order by namn";
    
    $sth = $dbh->prepare($alla_query);
    $rv = $sth->execute;
    print "<form action = skapa_objekt.cgi method = post>\n\r";
    print "<center><table><tr><td>\n\r";
    print "<h2>V&auml;lj objekt att editera.</h2><br>Namn &#124 Kommentar <i>(ev. tomt)</i><br><select name = i>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
        print "<option value = $info[0]>$info[1] &#124; $info[2]";
    }
    print "</select></td></tr><tr><td align = right>\n\r";
    print " &nbsp; <input type = submit value = V&auml;lj>\n\r";
    print "</td></tr></table></body></html>\n\r";
}
else { # uppgifter saknas

    print "<html><body>\n\r";
    print "<form action = visa_alla_objekt.cgi method = post>\n\r";
    print "<br><center><h2>V&auml;lj bibliotek och typ som ska listas.</h2>\n\r";
    print "<table width = 400 border = 0>\n\r";
    $query_info = "select id, namn from lokal order by id";
    $sth = $dbh->prepare($query_info);
    $rv = $sth->execute;
    print "<tr><td>V&auml;lj bibliotek</td><td><select name = l>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
        print "<option value = $info[0]>$info[1]";
    }
    print "</select></td></tr>\n\r";

    $query_info = "select distinct typ, typ_namn from typ_info";
    $sth = $dbh->prepare($query_info);
    $rv = $sth->execute;
    print "<tr><td>V&auml;lj typ av bokningsobjekt</td><td><select name = t>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
        print "<option value=$info[0]>$info[1]";
    }
    print "</select></td></tr>\n\r";
    print "<tr><td></td><td align = right><input type = submit value = V&auml;lj></td></tr></table>\n\r";
}
