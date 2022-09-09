#!/usr/bin/perl

use CGI;

$cgi = new CGI;

print "Content-type:text/html\n\n";

@dagar = $cgi->param('dagar');
@loc = $cgi->param('loc');
$open = $cgi->param('open');
$close = $cgi->param('close');
$datum = $cgi->param('datum');

$i = 0;
if ($dagar[0] && $loc[0] && $open && $close && $datum) {

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
    }
    else {
	# Skriv ut alla variabler foer kontroll samt submit-knapp.
	print "<html><head></head><body>\n\r";
	print "<h2>Nya &ouml;ppetider som kommer att sparas</h2>\n\r";
	$i = 0;
	print "<form action = store_openhours.cgi method = post>\n\r";
	foreach (@loc) {
	    $j = 0;
	    @lista = split /\|/, $loc[$i];
	    print "<b>$lista[1]</b><br>\n\r";
	    print "<input type = hidden name = loc value = $lista[0]>\n\r";
	    foreach (@dagar) {
		@lista = split /\-/, $dagar[$j];
		if ($open != $close) {
		    print "&nbsp; &nbsp; $lista[1] $open - $close<br>\n\r";
		}
		else {
		    print "&nbsp; &nbsp; $lista[1] St&auml;ngt <br>\n\r";
		}
		$j++;
	    }
	    $i++;
	}
	$i = 0;
	foreach (@dagar) {
	    print "<input type = hidden name = dagar value = $dagar[$i]>\n\r";
	    $i++;
	}
	print "<p>Dessa tider kommer att g&auml;lla <b>fr&aring;n och med $datum</b>\n\r";
#	print "open = $open<br>close = $close<p>\n\r";
	print "<input type = hidden name = open value = $open>\n\r";
	print "<input type = hidden name = close value = $close>\n\r";
	print "<input type = hidden name = datum value = $datum>\n\r";
	print "<p><input type = submit value = Spara>\n\r";
	print "</form>\n\r";
    }
}

else {
    print <<SLUT;
    <html><body>
    <table border = 0><tr><td width = 200>
       <b>V&auml;lj dag eller dagar.</b><br> Du kan markera flera alternativ genom 
       att h&aring;lla ner 'kontroll' (Ctrl) p&aring; tangentbordet samtidigt som du
       v&auml;ljer dagar. <i>(kommand-tangenten om du anv&auml;nder Mac)</i>.
    </td>
    <td>
    <form action=add_date.cgi method=post>
    <select name=dagar size=7 multiple>
     <option value=Monday-M&aring;ndag>M&aring;ndag
     <option value=Tuesday-Tisdag>Tisdag
     <option value=Wednesday-Onsdag>Onsdag
     <option value=Thursday-Torsdag>Torsdag
     <option value=Friday-Fredag>Fredag
     <option value=Saturday-L&ouml;rdag>L&ouml;rdag
     <option value=Sunday-S&ouml;ndag>S&ouml;ndag
    </select>
    </td></tr>
    <tr><td width = 200>
    <b>V&auml;lj bibliotek</b><br>Ett eller flera p&aring; samma s&auml;tt som ovan.
    </td><td>
    <select name=loc size=9 multiple>
    <option value=40|Biomedicinska>Biomedicinska
    <option value=42|Samh&auml;llsvetenskapliga_biblioteket>Samh&auml;llsvetenskapliga_biblioteket
    <option value=92|Samh&auml;llsvetenskapliga_biblioteket_f&ouml;reningsgatan>Samh&auml;llsvetenskapliga_biblioteket_f&ouml;reningsgatan
    <option value=44|Humanistiska_biblioteket>Humanistiska_biblioteket
    <option value=47|Pedagogiska_biblioteket>Pedagogiska_biblioteket
    <option value=48|Ekonomiska_biblioteket>Ekonomiska_biblioteket
    <option value=60|H&auml;lsovetarbackens_bibliotek>H&auml;lsovetarbackens_bibliotek
    <option value=61|Konstbiblioteket>Konstbiblioteket
    <option value=62|Biblioteket_f&ouml;r_musik_och_dramatik>Biblioteket_f&ouml;r_musik_och_dramatik
    <option value=90|KvinnSam>KvinnSam
    <option value=50|Campus_Linne>Campus_Linne
    </select>
    </td></tr>
    <tr><td width = 200>
    &Ouml;ppnar <i>(ex.vis 09.00)</i><br>Ange samma tid p&aring; &ouml;ppnar som p&aring; st&auml;nger om biblioteket ska vara st&auml;ngt hela dagen, ex.vis 10.00 och 10.00</td>
    <td><input type = text name=open size = 5 maxlength = 5>
    </td></tr>
    <tr><td width = 200>
    St&auml;nger <i>(ex.vis 20.00)</i><br>eller samma som &ouml;ppettiden om biblioteket ska vara st&auml;ngt hela dagen.
    </td><td><input type = text name=close size = 5 maxlength = 5>
    </td></tr>
    <tr><td width = 200>
    Datum som &auml;ndringen ska g&auml;lla fr&aring;n och med <i>ex.vis 2002-01-01</i></td>
    <td><input type = text name=datum size = 10 maxlength = 10>
    </td></tr>
    <tr><td>&nbsp;</td>
    <td><input type=submit value = Skicka>
    </td></tr>
</form>
</table>
</body></html>

SLUT
    
}

