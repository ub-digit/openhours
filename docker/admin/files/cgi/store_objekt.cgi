#!/usr/bin/perl

use CGI;
use DBI;
use POSIX qw(strftime);

require "./connect_string.pl";

$cgi = new CGI;

$typ = $cgi->param('t');
$id = $cgi->param('i');

my $datum1 = strftime("%Y-%m-%d", localtime(time + 86400 * $dagar));

if ($typ == 1 || $typ == 2 || $typ == 3) { 

    $lokal = $cgi->param('l');
    $namn = $cgi->param('n');
    $plats = $cgi->param('plats');
    $komm = $cgi->param('komm');
    $kvitteras = $cgi->param('kvitteras');
    $intern = $cgi->param('intern');
    $aktiv = $cgi->param('aktiv');

    if ($typ == 1) {
	$antal_platser = $cgi->param('antal_platser');
	$dator = $cgi->param('dator');
	$tavla = $cgi->param('tavla');
    }
    elsif ($typ == 2) {
	$webb = $cgi->param('webb');
	$ord = $cgi->param('ord');
	$printer = $cgi->param('printer');
	$diskett = $cgi->param('diskett');
	$tangent = $cgi->param('tangent');
    }
    elsif ($typ == 3) {
	$braille = $cgi->param('braille');
    }
}
else {
    # Fel typ
    $fel = 1;
    $pelle = 0;	
}

#Saknas det uppgifter?
if (!$typ || !$lokal || !$namn || !$plats || !$kvitteras || !$intern || !$aktiv) {
#if (! ($typ && $lokal && $namn && $plats && $kvitteras && $intern && $aktiv)) {
    $fel = 1;
    $pelle = 1;
}
elsif ($typ == 1) {
    $typ_namn = "Grupprum";
    if (!$antal_platser || !$dator || !$tavla) {
	$fel = 1;
	$pelle = 2;
    }
}
elsif ($typ == 2) {
    $typ_namn = "Datorarbetsplats";
    if (!$webb || !$ord || !$printer || !$diskett || !$tangent) {
	$fel = 1;
	$pelle = 3;
    }
}
elsif ($typ == 3) {
    $typ_namn = "L&auml;sstudio";
    if (!$braille) {
	$fel = 1;
	$pelle = 4;
    }
}

print "Content-type: text/html\n\n";

if ($fel == 1) {
    print "<html><body>Uppgifter saknas $pelle </body></html>\n\r";
    exit();
}

else { # Alla uppgifter finns
    # Kolla om det ska vara update eller insert (finns id?)
    # Skicka vidare till resultatsida.

    &connect_db;
    $dbh->{AutoCommit} = 0;

    if ($aktiv eq 'Ja') {$aktiv = t;} else {$aktiv = f;}
    if ($intern eq 'Ja') {$intern = t;} else {$intern = f;}
    if ($kvitteras eq 'Ja') {$kvitteras = t;} else {$kvitteras = f;}
    
    if ($id) {
	#
	# UPDATE 
	# 
	$obj_update = "update boknings_objekt set lokal_id=$lokal, namn=\'$namn\', plats=\'$plats\', ska_kvitteras=\'$kvitteras\', kommentar=\'$komm\', aktiv=\'$aktiv\', intern_bruk=\'$intern\' where obj_id = $id";
	$rv = $dbh->do($obj_update);
	if ($rv != 1) {
	    $uppdaterings_fel = 1;
	    $str = $dbh->errstr;
	}
	else {
	    if ($typ == 1) {
		# grupprumsinsert
		if ($dator eq 'Ja') {$dator = t;} else {$dator = f;}
		if ($tavla eq 'Ja') {$tavla = t;} else {$tavla = f;}
		$typ_update = "update typ_1_grupprum set antal_platser = $antal_platser, finns_dator = \'$dator\', finns_tavla = \'$tavla\' where obj_id = $id";
	    }
	    elsif ($typ == 2) {
		# datorinsert
		if ($webb eq 'Ja') {$webb = 1;} else {$webb = 0;}
		if ($ord eq 'Ja') {$ord = 1;} else {$ord = 0;}
		if ($printer eq 'Ja') {$printer = t;} else {$printer = f;}
		if ($diskett eq 'Ja') {$diskett = 1;} else {$diskett = 0;}
		if ($tangent eq 'Ja') {$tangent = 1;} else {$tangent = 0;}
		$typ_update = "update typ_2_datorer set diskettstation = \'$diskett\', extra_tangentbord = \'$tangent\', webb = \'$webb\', ordbehandling = \'$ord\', skrivare = \'$printer\' where obj_id = $id";
	    }
	    elsif ($typ == 3) {
		# lasstudio
		if ($braille eq 'Ja') {$braille = 1;} else {$braille = 0;}
		$typ_update = "update typ_3_lasstudio set braille = \'$braille\' where obj_id = $id";
	    }
	    $rv = $dbh->do($typ_update);
	    if ($rv != 1) {
		$uppdaterings_fel = 1;
		$str = $dbh->errstr;
	    }
	}
    }
    elsif (!$id) { 
	# 
	# INSERT
	# 
	$get_id_query = "select nextval(\'obj_id\')\;";
	$sth = $dbh->prepare($get_id_query);
	$rv = $sth->execute;
	@pelle = $sth->fetchrow_array;
	$id = $pelle[0];

	$obj_insert = "insert into boknings_objekt values ($id, $typ, $lokal, \'$namn\', \'$plats\', \'$kvitteras\', \'$komm\', \'$aktiv\', \'$intern\')";
	$rv = $dbh->do($obj_insert);
	if ($rv != 1) {
	    $uppdaterings_fel = 1;
	    $str = $dbh->errstr;
	}
	else {
	    if ($typ == 1) {
		# grupprumsinsert
		if ($dator eq 'Ja') {$dator = t;} else {$dator = f;}
		if ($tavla eq 'Ja') {$tavla = t;} else {$tavla = f;}
		$typ_insert = "insert into typ_1_grupprum values ($id, $antal_platser, \'$dator\', \'$tavla\','')";
	    }
	    elsif ($typ == 2) {
		# datorinsert
		if ($webb eq 'Ja') {$webb = t;} else {$webb = f;}
		if ($ord eq 'Ja') {$ord = t;} else {$ord = f;}
		if ($printer eq 'Ja') {$printer = t;} else {$printer = f;}
		if ($diskett eq 'Ja') {$diskett = 1;} else {$diskett = 0;}
		if ($tangent eq 'Ja') {$tangent = 1;} else {$tangent = 0;}
		$typ_insert = "insert into typ_2_datorer values ($id, \'$webb\', \'$ord\', \'$printer\', '', \'$tangent\', \'$diskett\')";
	    }
	    elsif ($typ == 3) {
		# lasstudio
		if ($braille eq 'Ja') {$braille = 1;} else {$braille = 0;}
		$typ_insert = "insert into typ_3_lasstudio values ($id,\'$braille\')";
	    }
	    $rv = $dbh->do($typ_insert);
	    if ($rv != 1) {
		$uppdaterings_fel = 1;
		$str = $dbh->errstr;
	    }
	    else {
		#if ($aktiv == 1) {
		$dagar_fram_query = "select dagar_fram from typ_info where typ = $typ and from_dag < \'$datum1\' order by from_dag desc";
		$sth = $dbh->prepare($dagar_fram_query);
		$rv = $sth->execute;
		undef $dagar_fram;
		$dagar_fram = $sth->fetchrow_array;
		
		if (!$dagar_fram) {
		    print "<html><head><title>Spara bokningsobjekt misslyckades</title></head>\n\r<body>$dagar_fram_query";
		    next;
		} 
		for ($j = 0; $j < $dagar_fram; $j++) {
		    $dagar = $j;
		    &skapa_bokningar;
		    #}
		}
	    }
	}
    } # slut insert
    if ($uppdaterings_fel) {
	$rc = $dbh->rollback;
	$rc = $dbh->disconnect;
	
#	    print <<_SLUT_;
	print "<html><head><title>Spara bokningsobjekt misslyckades</title></head>\n\r";
	print "<body>\n\r";
	print "<h2>Felmeddelande\: $str <br>| $typ_insert | $obj_insert | </h2>\n\r";
	print "Inget objekt har sparats. Du kan f&ouml;rs&ouml;ka igen genom att ladda om sidan, eller ";
	print "skapa ett nytt objekt. Kontakta <a href = mailto:it\@ub.gu.se>IT-avdelningen</a> (Lars Prytz) om detta ";
	print "problem kvarst&aring;r, och meddela vad som st&aring;r i felmeddelanden som visas p&aring; denna sida. ";
	print "</body></html>\n\r";
#_SLUT_
    }
    else {
	#Det har lyckats
	$rc = $dbh->commit;
	$rc = $dbh->disconnect;
	print "<html><head>\n\r";
	print "<meta http-equiv=Refresh content=\"1; URL=update_ok.cgi?antal=$rv\">\n\r";
	print "</head></html>\n\r";
#	print "<html><body>BRA<p>$obj_update $obj_insert<p>$typ_update $typ_insert</body></html>\n\r";
    }
}

########################################

sub skapa_bokningar {

    $datum = strftime("%Y-%m-%d", localtime(time + 86400 * $dagar));
    $dag = strftime("%A", localtime(time + 86400 * $dagar));

    $query_open = "select open, close from openhours where lokal_id = $lokal and (day = \'$datum\' or (day = \'$dag\' and from_dag < \'$datum\')) order by prioritet, from_dag desc";
    $sth = $dbh->prepare($query_open);
    $rv = $sth->execute;
    undef @open_close;
    @open_close = $sth->fetchrow_array;
    
    $open = $open_close[0];
    $close = $open_close[1];
    if (!$close) {
    print "<html><head><title>Spara bokningsobjekt misslyckades 2</title></head>\n\r<body>$query_open Det fanns inga tider i basen.</body></html>";
	exit;
    }
    $typ_query = "select timmar_pass from typ_info where typ = $typ and from_dag < \'$datum\' order by from_dag desc";
    $sth = $dbh->prepare($typ_query);
    $rv = $sth->execute;
    undef $timmar_pass;
    $timmar_pass = $sth->fetchrow_array;
    if (!timmar_pass) {
	print "<html><head><title>Spara bokningsobjekt misslyckades 2</title></head>\n\r<body>$typ_query Det fanns inga tidsangivelser i basen.</body></html>";
	exit;
    }
#$typ = $lista[0];
#$timmar_pass = $lista[1];
    
# Nu vet vi allt... open, close samt antal timmar per pass.
# Nu ska alla objekt faa nya tider beroende paa om de aer aktiva och vilken typ de aer.

    $start_tid = $open;
    while ($start_tid <= ($close - ($timmar_pass / 2))) {
	$slut_tid = $start_tid + $timmar_pass;
	if ($slut_tid > $close) {
	    $slut_tid = $close;
	}
	# Detta aer alla bokningar som ska skapas. Antingen kan de skrivas till fil eller direkt in i databasen.
#	printf "insert into bokning values ($id, $typ, \'$datum\', %2.2f, %2.2f)\;\n", $start_tid, $slut_tid;
	$ins = "insert into bokning values ($id, $typ, \'$datum\', $start_tid, $slut_tid)\;\n";
	$rv = $dbh->do($ins);
	$start_tid = $start_tid + $timmar_pass;
    }    

    
}




