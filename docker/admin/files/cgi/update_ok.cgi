#!/usr/bin/perl

use CGI;

$cgi = new CGI;

$antal = $cgi->param('antal');

print "Content-type:text/html\n\n";
if ($antal > 1) {
    print "<p>Uppdatering klar. $antal poster har skapats.";
}
else {
    print "<p>Uppdatering klar. $antal post har skapats.";
}
print "<p><a href = ./> Tillbaka till bokningssidan.</a>";
