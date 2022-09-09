#!/usr/bin/perl


sub connect_db {
    $db = $ENV{'DB_NAME'};
    $host = $ENV{'DB_HOST'};
    $port = $ENV{'DB_PORT'};
    $user = $ENV{'DB_USER'};
    $pass = $ENV{'DB_PASS'};
    $dbh = DBI->connect("dbi:Pg:dbname=$db;host=$host;port=$port", $user, $pass);
    $dbh->do("set client_encoding=latin1;") if(-f "/usr/local/etc/use_latin1.flag");
    $dbh->{AutoCommit} = 1;
}

###

sub connect_error {
    print "FEL. Kunde inte ansluta till databasen.\n\r";
    print "Kontakta it@ub.gu.se om detta problem kvarst&aring;r ";
    exit -1;
}

1;
