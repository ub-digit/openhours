#!/usr/bin/perl

use CGI;
# use DBI;

$cgi = new CGI;

$typ = $cgi->param('t');
$id = $cgi->param('i');
if ($typ == 1 || $typ == 2 || $typ == 3) { 

    $lokal = $cgi->param('l');
    $namn = $cgi->param('namn');
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
}

#Saknas det uppgifter?
#if (!$typ || !$lokal || !$namn || !$plats || !$kvitteras || !$intern || !$aktiv) {
if (! ($typ && $lokal && $namn && $plats && $kvitteras && $intern && $aktiv)) {
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
}
else {
    print <<_SLUT_;
<html><head><title>Spara nytt bokningsobjekt</title></head>
<body>
<table cellpading = 1 cellspacing = 10 border = 0>
<tr><td align = right>Typ av bokningsobjekt</td><td>$typ_namn</td></tr>
<tr><td align = right>Namn</td><td>$namn</td></tr>
<tr><td align = right>Bibliotek</td><td>$lokal</td></tr>
<tr><td align = right>Kommentar till bokningsobjektet</td><td>$komm</td></tr>
<tr><td align = right>Plats</td><td>$plats</td></tr>
<tr><td align = right>Objektet m&aring;ste kvitteras</td><td>$kvitteras</td></tr>
<tr><td align = right>Objektet &auml;r aktivt</td><td>$aktiv</td></tr>
<tr><td align = right>Objektet &auml;r endast f&ouml;r internt bruk</td><td>$intern</td></tr>
<form action = store_objekt.cgi method = post>
_SLUT_
    if ($id) {
	print "<input type = hidden name = i value = $id>\n\r";
    }
    if ($typ == 1) {
	print <<_SLUT_;
<tr><td align = right>Antal platser i rummet</td><td>$antal_platser</td></tr>
<tr><td align = right>Dator finns i rummet</td><td>$dator</td></tr>
<tr><td align = right>Whiteboard/tavla finns i rummet</td><td>$tavla</td></tr>
<input type = hidden name = antal_platser value = $antal_platser>
<input type = hidden name = dator value = $dator>
<input type = hidden name = tavla value = $tavla>
_SLUT_
}
    elsif ($typ == 2) {
	print <<_SLUT_;
<tr><td align = right>Internetuppkopplad dator</td><td>$webb</td></tr>
<tr><td align = right>Ordbehandlingsprogram p&aring; datorn</td><td>$ord</td></tr>
<tr><td align = right>Tillg&aring;ng till skrivare</td><td>$webb</td></tr>
<tr><td align = right>Datorn har diskettstation</td><td>$diskett</td></tr>
<tr><td align = right>Datorn har ut&ouml;kat tangentborsst&ouml;d (skriv vilka i kommentar)</td><td>$tangent</td></tr>
<input type = hidden name = webb value = $webb>
<input type = hidden name = ord value = $ord>
<input type = hidden name = printer value = $printer>
<input type = hidden name = diskett value = $diskett>
<input type = hidden name = tangent value = $tangent>
_SLUT_
}
    elsif ($typ == 3) {
	print <<_SLUT_;
<tr><td align = right>Datorn har braille</td><td>$braille</td></tr>
<input type = hidden name = braille value = $braille>
_SLUT_
}
    print <<_SLUT_;
<input type = hidden name = t value = $typ>
<input type = hidden name = l value = $lokal>
<input type = hidden name = n value = \"$namn\">
<input type = hidden name = komm value = \"$komm\">
<input type = hidden name = plats value = \"$plats\">
<input type = hidden name = kvitteras value = $kvitteras>
<input type = hidden name = intern value = $intern>
<input type = hidden name = aktiv value = $aktiv>
<tr><td>&nbsp;</td><td align = rigth>
<input type = submit value = Spara>
</td></tr><tr><td>&nbsp;</td><td align = rigth>
<i>Kan ta lite tid...<br>Ha t&aring;lamod...</i></td></tr>
</form>
</table></body></html>
_SLUT_
}







