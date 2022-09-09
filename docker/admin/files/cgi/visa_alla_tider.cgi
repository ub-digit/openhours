#!/usr/bin/perl

use DBI;
use CGI;

require "./connect_string.pl";

$cgi = new CGI;

$typ = $cgi->param('t');
$l = $cgi->param('l');

@lokal = split /\|/, $l;

print "Content-type: text/html\n\n";
print "<html><head><title>Administrera &ouml;ppettider</title></head><body>\n\r";

&connect_db;
if (!$dbh) { &connect_error; }

if ($l) {

########################

    $alla_query = "select o.oid, o.day, o.open, o.close, o.from_dag from openhours o, dag_ordning d where o.lokal_id = $lokal[0] and o.prioritet = 2 and o.day = d.day and d.ordning > 0 and $lokal[0] in (select id from lokal_sort where sort_order is not null or id = 90) order by o.from_dag, d.ordning";
    
    $sth = $dbh->prepare($alla_query);
    $rv = $sth->execute;
    print "<form action = radera_tider.cgi method = get>\n\r";
    print "<input type = hidden name = l value = $lokal[0]>\n\r";
    print "<center><h2>&Ouml;ppettider f&ouml;r $lokal[1]</h2>\n\r";
    print "T&auml;nk p&aring; att det alltid m&aring;ste finnas minst en post f&ouml;r varje veckodag d&auml;r fr&aring;n-och-med datumet <b>m&aring;ste</b> vara <b>mindre</b> &auml;n dagens datum.<br>Det kan d&auml;rf&ouml;r vara bra att <b>f&ouml;rst</b> skapa en ny tid innan man tar bort en gammal felaktig eller inte l&auml;ngre aktuell tid.";
    print "<p><table border = 0><tr><td>\n\r";
    print "<h3>V&auml;lj veckodagar att radera.</h3>Veckodag &#124 &Ouml;ppnar &#124 St&auml;nger &#124 g&auml;ller fr.o.m<br>\n\r";
    # print "$alla_query<p>\n\r";
    
    
    #print "<select name = di size = 8 multiple>\n\r";
     print "<select name = di size = 8 multiple STYLE='font-family : monospace; font-size : 12pt'>\n\r";
    #print "<font face='monospace'>"; 

    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
	if ($i == 0) {
	    $pelle = $info[4];
	}
	if ($pelle ne $info[4]) {
	    print "<option>-----";
	    $pelle = $info[4];
	}

	if ($info[2] != $info[3]) {
	    print "<option value = $info[0]|$info[4]>$info[1] &#124; $info[2] &#124 $info[3] &#124 $info[4]";
	}
	else {
	    print "<option value = $info[0]|$info[4]>$info[1] &#124; St&auml;ngt &#124 &#124 $info[4]";
	}
    }
    print "</select></td></tr><tr><td align = right>\n\r";
    print " &nbsp; <input type = submit name = d value = Radera>\n\r";
    print "</td></tr></table>\n\r";

########

    $alla_query = "select oid, day, open, close from openhours where lokal_id = $lokal[0] and prioritet = 1 order by from_dag, day";
    
    $sth = $dbh->prepare($alla_query);
    $rv = $sth->execute;
    print "<form action = radera_tider.cgi method = get>\n\r";
#    print "<input type = hidden name = e value = 1>\n\r";
    print "<center><table><tr><td>\n\r";
    print "<h3>V&auml;lj dagar att radera.</h3>\n\r";
    print "&nbsp; &nbsp;Dag&nbsp; &nbsp; &#124 &nbsp; &nbsp;&Ouml;ppnar &nbsp; &nbsp;&#124 St&auml;nger <br>\n\r";
    print "<select name = ei size = 5 multiple>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
        print "<option value = $info[0]|$info[1]>$info[1] &#124; $info[2] &#124 $info[3] ";
    }
    print "</select></td></tr><tr><td align = right>\n\r";
    print " &nbsp; <input type = submit name = e value = Radera>\n\r";
    print "</form></td></tr></table>\n\r";
    print "<a href = add_date.cgi>Skapa ny &ouml;ppettid f&ouml;r generell veckodag</a><p>\n\r";
    print "<a href = add_one_day.cgi>Skapa ny &ouml;ppettid f&ouml;r specifikt datum</a><p>\n\r";

#############################

}
else { # uppgifter saknas

    print "<form action = visa_alla_tider.cgi method = post>\n\r";
    print "<br><center><h2>V&auml;lj bibliotek vars tider ska listas.</h2>\n\r";
    print "<table width = 400 border = 0>\n\r";
    $query_info = "select id, namn from lokal where id in (select id from lokal_sort where sort_order is not null or id = 90)";
    $sth = $dbh->prepare($query_info);
    $rv = $sth->execute;
    print "<tr><td>V&auml;lj bibliotek</td><td><select name = l>\n\r";
    for ($i = 0; $i < $rv; $i++) {
        @info = $sth->fetchrow_array;
	$info[1] =~ tr/ /_/;
        print "<option value = $info[0]|$info[1]>$info[1]";
    }
    print "</select></td></tr>\n\r";

    print "<tr><td></td><td align = right><input type = submit value = V&auml;lj></td></tr></table>\n\r";
    &instruktioner;
}

print "<a href = ./>Tillbaka till admin-sidan</a><p>\n\r";
print "</body></html>\n\r";

#######################################

sub instruktioner {
    print <<_SLUT_;
<table width = 600 border = 0><tr><td>
	P&aring; denna sida kan man se vilka &ouml;ppettider som g&auml;ller f&ouml;r ett enskilt bibliotek.<br>
Det finns tv&aring; typer av &ouml;ppettider, det som g&auml;ller en enskild dag och de som g&auml;ller f&ouml;r en generell
veckodag.<p>
Den generella &ouml;ppettiden g&auml;ller fr&aring;n och med ett visst datum. Dessa anges per veckodag och kommer att g&auml;lla
tills dess att det l&auml;ggs in nya tider f&ouml;r den veckodagen och den nya tidens "fr&aring;n och med" datum passeras. 
 Om b&aring;da tiderna &auml;r samma s&aring; inneb&auml;r det att biblioteket kommer att vara st&auml;ngt den dagen.
<br>Ex:<i><blockquote>Ett visst bibliotek har tv&aring; tider f&ouml;r fredagar, en som ser ut som 
<br></i>Friday | 09.00 | 21.00 | 2002-01-02<i> 
<br>och en som ser ut som 
<br></i>Friday | 10.00 | 18.00 | 2002-04-01<i>
<br>
Detta inneb&auml;r att alla fredagar fram till 2002-04-01 kommer &ouml;ppettiden f&ouml;r det biblioteket vara 9.00-21.00 p&aring;
fredagar. Efter 2002-04-01 kommer &ouml;ppettiden p&aring; fredagar att vara 10.00-18.00. Den tiden kommer att g&auml;lla tills dess att en ny tid f&ouml;r fredagar l&auml;ggs in i databasen med ett nytt "fr&aring;n och med" -datum. 
</blockquote></i>
Det &auml;r inte n&ouml;dv&auml;ndigt att radera gamla tider, men det kan hj&auml;lpa till s&aring; att det &auml;r enkelt att 
se vilka tider som &auml;r aktuella just nu. T&auml;nk p&aring; att det alltid m&aring;ste finnas minst en post f&ouml;r varje 
veckodag d&auml;r fr&aring;n-och-med datumet <b>m&aring;ste</b> vara mindre &auml;n dagens datum.
<p>
<hr><br>
Man kan &auml;ven ha speciella &ouml;ppettider f&ouml;r en enskild dag, oavsett veckodag. De dagar som har egna &ouml;ppettider 
listas i den nedre listan. F&ouml;r det datum som st&aring;r i den listan kommer dessa tider att g&auml;lla. Om b&aring;da 
tiderna &auml;r samma s&aring; inneb&auml;r det att biblioteket kommer att vara st&auml;ngt den dagen.<br>
Ex:<i><blockquote>En dag i listan med dag och tid 
<br></i>2002-12-24 | 12.00 | 12.00<i>
<br> inneb&auml;r att biblioteket kommer att vara st&auml;ngt den dagen, medan en post med dag och tid 
<br></i>2002-03-28 | 09.00 | 13.00<i>
<br> inneb&auml;r att biblioteket kommer att vara &ouml;ppet 9-13 den dagen. 
</blockquote></i> 

Gamla &ouml;ppettider f&ouml;r specifika dagar raderas per automatik n&auml;r det datumet har passerats.
</td></tr></table><p>
_SLUT_
}






