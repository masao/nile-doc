#!/usr/local/bin/perl -w
# インストールしたソフトの目次を自動生成する。
# (何かの原因で目次ファイルが壊れたら使おう。)

# 使用法：
#  % ./makeindex.pl softlist.shtml > softindex

use strict;

main();
sub main {
    while (my $line = <>) {
	if ($line =~ /\<a\s+name=\"([^\"]+)\"\>([^\<]+)\<\/a\>/) {
	    my $name = $1;
	    $name =~ /([\d\-]+)$/;
	    my $date = $1;
	    $line =~ /インストールしたもの　　　： ([^\<]+)\<\/LI\>/;
	    my $realname = $1;
	    print "<li>$date: <a href=\"#$name\">$realname</a>\n";
	}
    }
}
