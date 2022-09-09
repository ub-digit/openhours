#!/usr/bin/perl

sub grupprum;
sub dator;

use CGI;
use DBI;

require "./connect_string.pl";

$cgi = new CGI;
$typ = $cgi->param('t');
$id = $cgi->param('i');

&connect_db;

if ($id) {
    $objekt_query = "select * from boknings_objekt where obj_id = $id";
    $sth = $dbh->prepare($objekt_query);
    $rv = $sth->execute;
    @bo = $sth->fetchrow_array;
    $typ = $bo[1];
    if ($typ == 1) {
	$typ_query = "select * from typ_1_grupprum where obj_id = $id";
    }
    elsif ($typ == 2) {
	$typ_query = "select * from typ_2_datorer where obj_id = $id";
    }
    elsif ($typ == 3) {
	$typ_query = "select * from typ_3_lasstudio where obj_id = $id";
    }
    $sth = $dbh->prepare($typ_query);
    $rv = $sth->execute;
    @specifik = $sth->fetchrow_array;    
}
print "Content-type: text/html\n\n";
if ($typ == 1 || $typ == 2 || $typ == 3 || $id) { # Om nya typer tillkommer saa ska detta aendras.

    $query = "select distinct lower(typ_namn) from typ_info where typ = $typ";
    $sth = $dbh->prepare($query);
    $rv = $sth->execute;
    @typ = $sth->fetchrow_array;
    if (!$id) {
	print "<html><head><title>Skapa nytt bokningsobjekt av typ $typ[0]</title></head>\n\r";
	print "<body><h2>Skapa nytt bokningsobjekt av typ $typ[0]</h2>\n\r";
    }
    else {
	print "<html><head><title>Editera bokningsobjekt av typ $typ[0]</title></head>\n\r";
	print "<body><h2>Editera bokningsobjekt av typ $typ[0]</h2>\n\r";
    }
    print <<_SLUT_;
<table cellpadding = 3 cellspacing = 10 border = 1><tr>
<form action=lagra_objekt.cgi method = post>
<input type = hidden name = t value = $typ>
_SLUT_
    if ($id) { print "<input type=hidden name = i value = $id>\n\r"; }
    print "<td>Bibliotek</td>\n\r";
    print "<td><select name = l>\n\r";

    $query = "select * from lokal order by id";
    $sth = $dbh->prepare($query);
    $rv = $sth->execute;

    for ($i = 0; $i < $rv; $i++) {
        @bib = $sth->fetchrow_array;
	if ($bib[0] == $bo[2]) {
	    print "<option value = $bib[0] selected >$bib[1]";
	}
	else {
	    print "<option value = $bib[0]>$bib[1]";
	}
    }
    print "</select>\n\r";
    print <<_SLUT_;
</td>
<td rowspan = 7>
_SLUT_
    &anvisningar;
    print <<_SLUT_;
</td>
</tr>
<tr><td>
Namn p&aring; $typ[0] <br>(max 100 tecken)</td><td>
<input type=text name = namn size = 30 maxlength = 99 value = \"$bo[3]\">
</td></tr>
<tr><td>
Plats f&ouml;r detta objekt<br>(max 30 tecken)</td><td>
<input type=text name = plats size = 30 maxlength = 30 value = \"$bo[4]\">
_SLUT_
#    for ($i=1; $i < 10; $i++) {
#	if ($i == $bo[4]) {
#	    print "<option selected>$i";
#	}
#	else {
#	    print "<option>$i";
#	}
#}
#    print "</select>\n\r";
    print <<_SLUT_;
</td></tr>
<tr><td>
<i>Allm&auml;n info om detta objekt <br>(max 200 tecken)<br>ej obligatorisk uppgift</i>
</td><td>
<input type = text name = komm size = 30 maxlength = 199 value = \"$bo[6]\">
</td></tr>
<tr><td>
Ska detta objekt kvitteras ut<br> innan bokningen g&auml;ller
</td><td>
_SLUT_
    if (!$id || $bo[5] == 1) {
	print "<input type=radio name = kvitteras value = Ja checked = true>Ja";
	print "<input type=radio name = kvitteras value = Nej>Nej";
    }
    else {
	print "<input type=radio name = kvitteras value = Ja>Ja";
	print "<input type=radio name = kvitteras value = Nej checked = true>Nej";
    }
	    print <<_SLUT_;
</td></tr>
<tr><td>
Vad f&ouml;r typ av objekt &auml;r detta 
</td><td>
_SLUT_
    if (!$id || $bo[8] == 0) {
	print "<input type=radio name = intern value = Nej checked = true>offentlig";
	print "<input type=radio name = intern value = Ja>intern";
    }
    else {
	print "<input type=radio name = intern value = Nej>offentlig";
	print "<input type=radio name = intern value = Ja checked = true>intern";
    }
    print <<_SLUT_;
</td></tr>
<tr><td>
Ska detta objekt vara aktivt? 
</td><td>
_SLUT_
    if (!$id || $bo[7] == 1) {
	print "<input type=radio name = aktiv value = Ja checked = true>Ja";
	print "<input type=radio name = aktiv value = Nej>Nej";
    }
    else {
	print "<input type=radio name = aktiv value = Ja>Ja";
	print "<input type=radio name = aktiv value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>
<!-- <tr><td colspan = 3><hr width = 400 size = 1>
</td></tr> -->
_SLUT_

    if ($typ == 1) {
	&grupprum;
    }
    elsif ($typ == 2) {
	&dator;
    }
    elsif ($typ == 3) {
	&lasstudio;
    }
    print <<_SLUT_;
<tr><td>&nbsp;</td><td align = right>
<input type = submit value = Spara>
</table></form>
</body></html>
_SLUT_



}

else {
# ingen typ
    print "<html><body>Uppgifter saknas</body></html>\n\r";
}


####################################################

sub grupprum {
    print <<_SLUT_;
<tr><td>
Hur m&aring;nga platser finns det i rummet
</td><td>
<input type = text name = antal_platser size = 4 maxlength = 4 value = $specifik[1]> 
</td>
<td rowspan = 3>
_SLUT_
    &grupprumsanvisningar;
    print <<_SLUT_;
</td>
</tr>
<tr><td>
Finns det dator i rummet
</td><td>
_SLUT_
    if ($specifik[2] == 1) {
	print "<input type = radio name = dator value = Ja checked = true>Ja";
	print "<input type = radio name = dator value = Nej>Nej";
    }
    elsif ($id && $specifik[2] == 0) {
	print "<input type = radio name = dator value = Ja>Ja";
	print "<input type = radio name = dator value = Nej checked = true>Nej";
    }
    else {
	print "<input type = radio name = dator value = Ja>Ja";
	print "<input type = radio name = dator value = Nej>Nej";
    }
    print "</td></tr>\n\r";
    print <<_SLUT_;
<tr><td>
Finns det whiteboard/tavla i rummet
</td><td>
_SLUT_
    if ($specifik[3] == 1) {
	print "<input type = radio name = tavla value = Ja checked = true>Ja";
	print "<input type = radio name = tavla value = Nej>Nej";
    }
    elsif ($id && $specifik[3] == 0) {
	print "<input type = radio name = tavla value = Ja>Ja";
	print "<input type = radio name = tavla value = Nej checked = true>Nej";
    }
    else {
	print "<input type = radio name = tavla value = Ja>Ja";
	print "<input type = radio name = tavla value = Nej>Nej";
    }
    print "</td></tr>\n\r";
}

####################################################

sub dator {
    print <<_SLUT_;
<tr><td>
&Auml;r datorn kopplad till Internet 
</td><td>
_SLUT_
    if (!$id || $specifik[1] == 1) {
	print "<input type = radio name = webb value = Ja checked = true>Ja";
	print "<input type = radio name = webb value = Nej>Nej";
    }
    else {
	print "<input type = radio name = webb value = Ja>Ja";
	print "<input type = radio name = webb value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td>
<td rowspan = 3>
_SLUT_
    &datoranvisningar;
    print <<_SLUT_;
</td>
</tr>
<tr><td>
Finns det ordbehandlingsprogram p&aring; datorn (office)  
</td><td>
_SLUT_
    if (!$id) {
	print "<input type = radio name = ord value = Ja>Ja";
	print "<input type = radio name = ord value = Nej>Nej";
    }
    elsif ($specifik[2] == 1) {
	print "<input type = radio name = ord value = Ja checked = true>Ja";
	print "<input type = radio name = ord value = Nej>Nej";
    }
    else {
	print "<input type = radio name = ord value = Ja>Ja";
	print "<input type = radio name = ord value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>
<tr><td>
&Auml;r datorn kopplad till en skrivare 
</td><td>
_SLUT_
    if (!$id) {
	print "<input type = radio name = printer value = Ja>Ja";
	print "<input type = radio name = printer value = Nej>Nej";
    }
    elsif ($specifik[3] == 1) {
	print "<input type = radio name = printer value = Ja checked = true>Ja";
	print "<input type = radio name = printer value = Nej>Nej";
    }
    else {
	print "<input type = radio name = printer value = Ja>Ja";
	print "<input type = radio name = printer value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>

<tr><td>
Har datorn diskettstation 
</td><td>
_SLUT_
    if (!$id) {
	print "<input type = radio name = diskett value = Ja>Ja";
	print "<input type = radio name = diskett value = Nej>Nej";
    }
    elsif ($specifik[6] == 1) {
	print "<input type = radio name = diskett value = Ja checked = true>Ja";
	print "<input type = radio name = diskett value = Nej>Nej";
    }
    else {
	print "<input type = radio name = diskett value = Ja>Ja";
	print "<input type = radio name = diskett value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>


<tr><td>
Har datorn extra spr&aring;kst&ouml;d<br><i>Skriv vilka i kommentar</i> 
</td><td>
_SLUT_
    if (!$id) {
	print "<input type = radio name = tangent value = Ja>Ja";
	print "<input type = radio name = tangent value = Nej>Nej";
    }
    elsif ($specifik[5] == 1) {
	print "<input type = radio name = tangent value = Ja checked = true>Ja";
	print "<input type = radio name = tangent value = Nej>Nej";
    }
    else {
	print "<input type = radio name = tangent value = Ja>Ja";
	print "<input type = radio name = tangent value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>



_SLUT_
}

###########################

sub lasstudio {
    print <<_SLUT_;
<tr><td>
Har datorn braille 
</td><td>
_SLUT_
    if ($id && $specifik[1] == 1) {
	print "<input type = radio name = braille value = Ja checked = true>Ja";
	print "<input type = radio name = braille value = Nej>Nej";
    }
    else {
	print "<input type = radio name = braille value = Ja>Ja";
	print "<input type = radio name = braille value = Nej checked = true>Nej";
    }
    print <<_SLUT_;
</td></tr>
_SLUT_
}

##########################


sub anvisningar {
    print <<_SLUT_;
<ul>
    <li>
	<b>Alla f&auml;lten</b> g&aring;r att &auml;ndra /editera om n&aring;got blir fel.
    </li>
    <p>
    <li><b>Namn</b> &auml;r det som kommer att visas ut&aring;t. T&auml;nk p&aring; att vara konsekventa i namngivningen.<br>
	Om namnen blir f&ouml;r l&aring;nga s&aring; &auml;r det risk att inte hela namnet f&aring;r plats p&aring; en rad, 
	vilket kan g&ouml;ra sidan med alla tider on&ouml;digt r&ouml;rig. 
    </li>
    <p>
    <li><b>Plats</b> kan vara vara v&aring;ning, balkong eller likn som beskriver var p&aring; de respektive biblioteken 
	objektet finns.<br>
	S&aring; l&auml;nge det &auml;r konsekvent inom resp. bibl. med uttryck och med versaler/gemener s&aring; kan ni skriva 
	    vad ni vill. <br><i>(ex.vis V&aring;ning, v&aring;n. Balkong, balkong osv.</i>
    </li>
    <p>
    <li>
    Objekt som inte beh&ouml;ver <b>kvitteras</b> kommer aldrig att bli gula p&aring; sidan med bokningstiderna, och 
    kommer s&aring;ledes inte heller bli lediga efter att tiden har b&ouml;rjat tillsammans med de andra som inte har kvitterats.  
    </li>
    <p>
    <li>Objekt som skapas kommer att f&aring; bokningsdatum med en g&aring;ng, men <b>ej aktiva objekt</b> kommer att bli bokningsbara
        f&ouml;rst efter att de har aktiverats. <br>
	Ej aktiva objekt syns <a target=_blank href=http://www.ub.gu.se/bokningar/bokning_test.html>h&auml;r</a> (Sidan &ouml;ppnas i nytt f&ouml;nster)  
	<br>Objekt kan g&ouml;ras inaktiva pga att dator ska repareras, arbete utf&ouml;ras i rummet eller likn. Inaktiva objekt kommer inte med i listan med bokningsbara tider. 
    </li> 
</ul>
_SLUT_
}

###########

sub datoranvisningar {

}

###########

sub grupprumsanvisningar {

    print <<_SLUT_;
<ul><li>
    Antal <b>platser</b> ska skrivas med <b>siffror</b>
</li></ul>
_SLUT_
}









