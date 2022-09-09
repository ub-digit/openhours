#!/usr/bin/perl

use CGI;
use DBI;
use POSIX qw(strftime);

require "./connect_string.pl";

$cgi = new CGI;

$dagar = $cgi->param('d');
$lokal = $cgi->param('l');
$typ = $cgi->param('t');
$pers = $cgi->param('p');

&connect_db;

print "content-type: text/html\n\n";

print "<form action = bokningar.cgi method = post>\n\r";
print "<center>";
print "<h2>Boka en eller flera datorer/grupprum del av dag/hel dag</h2>";
print "<table border='0'>\n\r";
print "<tr><td colspan = '2'>";
print "<b>OBS</b> Redan&nbsp;gjorda&nbsp;bokningar&nbsp;kommer&nbsp;<b>inte</b>&nbsp;att&nbsp;skrivas&nbsp;&ouml;ver.<br>Endast lediga pass kommer att bokas.<br><br>";
print "<tr><td>Bibliotek</td><td>\n\r";
	
# Lista med bibliotek
$query_info = "select id, namn from lokal where id in (40,42,43,44,47,48,50,60,61,66,92) order by namn";
$sth = $dbh->prepare($query_info);
$rv = $sth->execute;
print "<select name = l>\n\r";
if (!$lokal) {
    print "<option value = >V&auml;lj bibliotek";
}
for ($i = 0; $i < $rv; $i++) {
    @info = $sth->fetchrow_array;
    if ($lokal == $info[0]) {
	print "<option value = $info[0] selected>$info[1]";
    }
    else {
	print "<option value = $info[0]>$info[1]";
    }
}
print "</select>\n\r";
print "</td></tr><tr><td>Datum</td><td>\n\r";

# Lista med dagar
print "<select name = d>\n\r";
for ($i = 0; $i < 14; $i++) {
    my $nicedate = strftime("%Y-%m-%d", localtime(time + 86400 * $i));	
    print "<option value='$nicedate'>$nicedate";
}
print "</select>\n\r";
print "</td></tr><tr><td>Typ</td><td>\n\r";

# Lista med typer (grupprum, datorarbetsplats)
$query_info = "select distinct typ, typ_namn from typ_info where typ in (1,2,3) order by typ";
$sth = $dbh->prepare($query_info);
$rv = $sth->execute;
print "<select name = t>\n\r";
for ($i = 0; $i < $rv; $i++) {
    @info = $sth->fetchrow_array;
    if ($typ == $info[0]) {
	print "<option value=$info[0] selected>$info[1]";
    }
    else {
	print "<option value=$info[0]>$info[1]";
    }
}
print "</select>\n\r";

print "</td></tr><tr><td>&nbsp;</td><td align=right>\n\r";
print "<input type=submit value = \"Visa tider\">\n\r";
print "</td></tr></table></form>\n\r";

print "</center>\n\r";
