#!/usr/local/bin/perl -w
# ���󥹥ȡ��뤷�����եȤ��ܼ���ư�������롣
# (�����θ������ܼ��ե����뤬���줿��Ȥ�����)

# ����ˡ��
#  % ./makeindex.pl softlist.shtml > softindex

use strict;

main();
sub main {
    while (my $line = <>) {
	if ($line =~ /\<a\s+name=\"([^\"]+)\"\>([^\<]+)\<\/a\>/) {
	    my $name = $1;
	    $name =~ /([\d\-]+)$/;
	    my $date = $1;
	    $line =~ /���󥹥ȡ��뤷����Ρ������� ([^\<]+)\<\/LI\>/;
	    my $realname = $1;
	    print "<li>$date: <a href=\"#$name\">$realname</a>\n";
	}
    }
}
