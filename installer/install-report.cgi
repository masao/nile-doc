#!/usr/local/bin/perl -w
# -*-CPerl-*-
use IO::File;
use CGI qw(:all);
use POSIX qw(:time_h);

$| = 1;

$title = "Software Installation Report Submission Page";
$my_address = 'admin@nile.ulis.ac.jp';
$filename = "softlist.shtml";
$real_filename = "/usr/local/apache/htdocs/nile/installer/softlist.shtml";
$index_filename = "/usr/local/apache/htdocs/nile/installer/softindex";

# �ʲ��Υ�٥��Ȥ���
$label_name = 		"���󥹥ȡ��뤷����Ρ�������";
$label_version = 	"�С������ʥѥå���٥�ˡ�";
$label_description = 	"��ñ������������������������";
$label_prefix = 	"���󥹥ȡ����衡������������";
$label_who = 		"���󥹥ȡ��뤷���͡���������";
$label_date = 		"���ա�����������������������";
$label_manual = 	"�ޥ˥奢�롡����������������";
$label_origin = 	"�����ϩ��������������������";
$label_src = 		"���������֤���ꡡ����������";
$label_related = 	"��Ϣ�ե����롡��������������";
$label_at_install = 	"���󥹥ȡ���κݤ��ѹ�������";
$label_misc = 		"[ ����¾ ]";
$label_attention = 	"[ ��ջ��� ]";

$text_width = 40;		# ���ϥե�����ɤ�Ĺ��
$text_rows=3;			# �ƥ�����������ι⤵

$query = CGI->new();

print $query->header(), $query->start_html($title), h1($title), "\n";

# �Ǹ�ˤ���Ǥ�Ԥ�̾����ɽ�������ޤ��礦��
sub print_tail() {
    print <<EOF
<HR>
<ADDRESS>Administration group for nile.ulis.ac.jp<BR>
<A HREF="mailto:$my_address">$my_address</A>
</ADDRESS>
EOF
}

if ($query->param("submit")) {	# ��Ͽ������

    open(HTMLFILE, ">>$real_filename") ||
	die "can't append data to $filename : $!";
    open(INDEXFILE, ">>$index_filename") ||
	die "can't append data to $filename : $!";

    $day   = sprintf("%02d", (localtime)[3]);
    $month = sprintf("%02d", (localtime)[4] + 1);
    $year = (localtime)[5] + 1900;

    $anchor = $name = $query->param("name");
    $name =~ s/[\xa1-\xfe]//g;    # 2-byteʸ���Ϻ�롣
    $name .= ".$year-$month-$day";
    
    my $report =
	h2("<a name=\"$name\">��</a> ", $query->param("name"), " ��", $query->param("description"), "�� By ", $query->param("who")).
	ul(li($label_name, $query->param("name")).
	   li($label_version, $query->param("version")).
	   li($label_description, $query->param("description")).
	   li($label_prefix, $query->param("prefix")).
	   li($label_who, $query->param("who")).
	   li($label_date, POSIX::strftime("%D",localtime)).
	   #$query->param("date", scalar localtime).
	   li($label_manual, $query->param("manual")).
	   li($label_origin, $query->param("origin")).
	   li($label_src, $query->param("src")).
	   li($label_related, $query->param("related")).
	   li($label_at_install, pre($query->param("at_install"))).
	   li($label_misc, pre($query->param("misc"))).
	   li($label_attention, pre($query->param("attention"))));

    print HTMLFILE "<hr>\n$report\n";

    print INDEXFILE  "<li>$year-$month-$day: <a href=\"#$name\">$anchor</a>\n";

    print $report;
    print p("�ʾ�����Ƥ���Ͽ����ޤ�����");

    my $msg = html2txt($report);
    my $subject = $query->param("name");
    open(SENDMAIL, "| /usr/local/bin/nkf | /usr/lib/sendmail -oi -t") ||
	die "sendmail open failed: $!";
    print SENDMAIL <<EOF;
From: "Installer" <masao\@ulis.ac.jp>
To: "Nile Administrators" <$my_address>
Subject: [nile-install] $subject

$msg

URL: http://nile.ulis.ac.jp/nile/installer/$filename#$name
EOF

    close(SENDMAIL) || warn "sendmail didn't close nicely";
} else {			# ���줫����Ͽ���롣
    print p("nile �˲������եȥ������򥤥󥹥ȡ��뤷���顢��������Ͽ���ޤ��礦��"), "\n";
    print $query->startform();
    print $label_name, $query->textfield(-name=>"name",-size=>$text_width), br(), "\n";
    print $label_version, $query->textfield(-name=>"version",-size=>$text_width), br(), "\n";
    print $label_description, $query->textfield(-name=>"description",-size=>$text_width), br(), "\n";
    print $label_prefix, $query->textfield(-name=>"prefix",-size=>$text_width), br(), "\n";
    print $label_who, $query->textfield(-name=>"who",-size=>$text_width), br(), "\n";
#    print $label_date, $query->textfield(-name=>"date",-size=>$text_width), br(), "\n";
    print $label_manual, $query->textfield(-name=>"manual",-size=>$text_width), br(), "\n";
    print $label_origin, $query->textfield(-name=>"origin",-size=>$text_width), br(), "\n";
    print $label_src, $query->textfield(-name=>"src",-size=>$text_width), br(), "\n";
    print $label_related, $query->textfield(-name=>"related",-size=>$text_width), br(), "\n";
    print $label_at_install, br(), $query->textarea(-name=>"at_install",-rows=>$text_rows,-columns=>$text_width+30), br(), "\n";
    print $label_misc, br(), $query->textarea(-name=>"misc",-rows=>$text_rows,-columns=>$text_width+30), br(), "\n";
    print $label_attention, br(), $query->textarea(-name=>"attention",-rows=>$text_rows,-columns=>$text_width+30), br(), "\n";
    print $query->submit("submit","��Ͽ");
    print $query->end_form();

    print $query->p("�� ��ա� ��Ͽ��Ʊ���˴����Ԥ˥᡼�뤬������褦�ˤ��ޤ�����");
}
print hr();
print p(a({href=>$filename},"����ޤǤ���Ͽ���줿���"));
print_tail();
print end_html();

sub html2txt {
    my ($html) = @_;
    my $tmpfile = "/tmp/.inst-rep.$$";
    open(W3M, "|/usr/local/bin/w3m -dump -T text/html > $tmpfile") || 
	die "w3m open fail: $!";
    print W3M $html;
    close(W3M);
    my $result = readfile($tmpfile);
    unlink($tmpfile);
    return $result;
}
# ��Ψ�褯�ե��������Ȥ��ɤ߹��ࡣ
sub readfile ($) {
    my ($fname) = @_;

    my $fh = new IO::File;
    $fh->open($fname) || die "readfile: $fname: $!";
    my $cont = '';
    my $size = -s $fh;
    read $fh, $cont, $size;
    $fh->close;
    return $cont;
}
