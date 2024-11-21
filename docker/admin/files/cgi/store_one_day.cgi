#!/usr/bin/perl

use CGI;
use DBI;

require "./connect_string.pl";

$cgi = new CGI;

#@dagar = $cgi->param('dagar');
@loc = $cgi->param('loc');
$open = $cgi->param('open');
$close = $cgi->param('close');
$datum = $cgi->param('datum');

print "Content-type:text/html\n\n";

$i = 0;
if ($loc[0] && $open && $close && $datum) {

#    print "Content-type:text/html\n\n";
    
    if ( $open !~ /[0-2][0-9]\.[0-5][0-9]/) {
	print "fel tidsformat (&ouml;ppnar)<p>\n\r";
	$fel = 1;
    }
    if ( $close !~ /[0-2][0-9]\.[0-5][0-9]/) {
	print "fel tidsformat (st&auml;nger)<p>\n\r";
	$fel = 1;
    }
    # OBS datum som aer tillatna aer from 2002-**-** - 2009-**-**
    # Vissa felaktiga datum kan slinka igenom som 2002-19-39 osv
    if ( $datum !~ /20[0-9][0-9]\-[0-1][0-9]\-[0-3][0-9]/) {
	print "fel datumformat<p>\n\r";
	$fel = 1;
    }
    if ($fel) {
	print "<a href = add_date.cgi>Tillbaka</a>\n\r";
#	print "</body></html>\n\r";
    }
    else {
	# Spara ner till DB.
#	print "<html><head></head><body>\n\r";
#	print "<h2>Nya &ouml;ppetider som har sparats</h2>\n\r";

#	$antal_dagar = @dagar;
	$antal_loc = @loc;
#	$tot = $antal_dagar * $antal_loc;

	&connect_db;
	$dbh->{AutoCommit} = 0;
	$i = 0;
	$update_ok = 0;
	foreach $loc (@loc) {
	    #@loc_lista = split /\-/, $loc[$i];
	    $insert = "insert into openhours values ($loc, \'$datum\', $open, $close, 1)\;";
	    $rv = $dbh->do($insert);
	    if ($rv) {
		$update_ok++;
	    }
	    else {
		print "uppdateringsfel<br>\n\r";
	    }
	}
	$i++;
#	print "<p>Antal poster = $tot, Antal insert = $update_ok<br>\n\r";
	if ($antal_loc == $update_ok) {
	    $rc = $dbh->commit;
	    $rc = $dbh->disconnect;
	    print "<html><head>\n\r";
	    print "<meta http-equiv=Refresh content=\"1; URL=update_ok.cgi?antal=$antal_loc\">\n\r";
	    print "</head></html>\n\r";
	}
	else {
	    $rc = $dbh->rollback;
	    print "<b>Ingen uppdatering har skett.</b>\n\r";
	}
    }
}
else {
    print <<SLUT;
    <html><body>
Uppgifter saknas.<p>
<a href = add_date.cgi>Tillbaka</a>
</body></html>

SLUT
    
}

