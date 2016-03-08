#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);

require 'cgi-lib.pl';
require 'jcode.pl';

&ReadParse(*in);

$name = $in{'name'};
$kinmu = $in{'kinmu'};
$yakushoku = $in{'yakushoku'};
$todoufuken = $in{'todoufuken'};
$jusho_1 = $in{'jusho_1'};
$jusho_2 = $in{'jusho_2'};
$tel = $in{'tel'};
$fax = $in{'fax'};
$mail = $in{'mail'};
$date = $in{'date'};
$ip = $in{'ip'};

$owFlag = 0;

$etr_log = "\"$date\",\"$ip\",\"$name\",\"$kinmu\",\"$yakushoku\",\"$todoufuken\",\"$jusho_1\",\"$jusho_2\",\"$tel\",\"$fax\",\"$mail\",,,,\n";

open(FILE,"./jvrc_log/jvrc_etr_en.csv")||die "Can't open file";
flock(FILE,2);
@etr_log_body=<FILE>;
flock(FILE,8);
close(FILE);

foreach $line(@etr_log_body){
	if($line eq $etr_log){
		$owFlag = 1;
	}
}

if($owFlag == 0){

	$num = unshift (@etr_log_body, $etr_log);

	open(FILE, ">./jvrc_log/jvrc_etr_en.csv")||die "Can't open file";
	flock(FILE,2);
	print FILE @etr_log_body;
	flock(FILE,8);
	close(FILE);

	$printdate = " ■ Application date ■ $date \n";
	$printname = " ■        Name      ■ $name \n";
	$printkinmu = " ■Department/Company■ $kinmu \n";
	$printyakushoku = " ■       Title      ■ $yakushoku \n";
	$printtodoufuken = " ■      Country     ■ $todoufuken \n";
	$printjusho_1 = " ■     Address１    ■ $jusho_1 \n";
	$printjusho_2 = " ■     Address２    ■ $jusho_2 \n";
	$printtel = " ■ Telephone Number ■ $tel \n";
	$printfax = " ■        FAX       ■ $fax \n";
	$printmail = " ■  E-mail address  ■ $mail \n";			

	$topbody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nJapan Virtual Robotics Challenge (JVRC)\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nYour application has been received successfully as follows.\n\n";	
	$middlebody = "$printdate$printname$printkinmu$printyakushoku$printtodoufuken$printjusho_1$printjusho_2$printtel$printfax$printmail\n\n";
	$bottombody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nDate ：Beginning of October 2015. We will inform you on the website.\nPlace：CEATEC (plan)\nApplication Fee：free\n\nWe will contact the procedure of participation from the secretariat later.\n\n\nJapan Virtual Robotics Challenge (JVRC) Secretariat\n\nhttp://www.jvrc.org/en/\n\noffice\@jvrc.org\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n*Personal customer information will only be used for our registration management.\n All of our site and transactions are based on SSL protection.";
	$send = "\"Japan Virtual Robotics Challenge(JVRC) Secretariat\"<office\@jvrc.org>";
	$subject = "Japan Virtual Robotics Challenge (JVRC) Application";
	$body = "$topbody$middlebody$bottombody";

	jcode::convert(\$subject,'jis');
	jcode::convert(\$body,'jis');
	jcode::convert(\$send,'jis');

	open(MAIL,"| /usr/sbin/sendmail -t");
	print MAIL "To: $mail\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);
#上は入力者宛、下は事務局宛★☆★☆★☆★☆★☆★☆★☆★☆
	open(MAIL,"| /usr/sbin/sendmail -t");
	print MAIL "To: office\@jvrc.org\n";
#	print MAIL "To: mmm\@s-vivid.com\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);


}

print "Content-type: text/html\n\n";

	print <<EOM;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS" />
<title>Japan Virtual Robotics Challenge(JVRC)</title>
<meta http-equiv="content-style-type" content="text/css" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="keywords" content="Japan Virtual Robotics Challenge,JVRC,NEDO," />
<meta name="description" content="'Japan Virtual Robotics Challenge' (JVRC for short) is a competition of disaster response robots by computer simulations. It will be held as a part of 'R & D project on Disaster-response Robots' by New Energy and Industrial Technology Development Organization (NEDO)." />

<link rel="shortcut icon" href="../images/favicon.ico" />

<link href="../../css/import.css" rel="stylesheet" type="text/css" media="all" />
<link href="style_info.css" rel="stylesheet" type="text/css" media="all" />
<script type="text/javascript" src="../../js/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="../../js/base.js"></script>


</head>

<body>


<div id="page">

<div id="header">
<div class="imgArea">
<a href="http://jvrc.org/en/index.html"><img src="../../images/en/img-main.png" alt="" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/ssl/contact.html"><img src="../../images/ja_flag.png" alt="Japan" width="22" height="14" />Japanese</a>
</div><!--/ english-->

</div><!-- / #imgArea-en -->
</div><!-- / #header -->


<div id="navi">
<div id="naviArea">
<ul id="gNav">
<li><a href="../index.html">TOP</a></li>
<li><a href="../rule.html">Rule</a></li>
<li><a href="http://jvrc.github.com/tutorials/html/index.html" target="_blank">Tutorial</a></li>
<li><a href="../team.html">Team</a></li>
<li><a href="../download.html">Download</a></li>
<li><a href="../result.html">Result</a></li>
<li class="current-page"><a href="https://jvrc.org/en/ssl/etr.html"><img src="../../images/sanka-icon.png" alt="" width="26" height="25" />Application</a></li>
<li><a href="https://jvrc.org/en/ssl/contact.html"><img src="../../images/inquiry-icon.png" alt="" width="22" height="16" /> Contact Us</a></li>
</ul>
<!-- / #naviArea --></div>
<!-- / #navi --></div>


<div id="contents" class="clearfix">
<div id="main2">

<h2>Application complete</h2>
<br />

<div class="need2">
<span class="red">It has sent E-Mail to your E-Mail address. Please check E-Mail.</span><br />
<br /> 
</div>
                 
<table class="form" summary="お\申\込み">
<tr>
<th nowrap="nowrap" class="t_top">Name</th>
<td width="6%" class="aqua"><div class="need">Mandatory</div></td>
<td class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">Department/Company</th>
<td>&nbsp;</td>
<td>$kinmu</td>
</tr>
<tr>
<th nowrap="nowrap">Title</th>
<td>&nbsp;</td>
<td>$yakushoku</td>
</tr>
<tr>
<th nowrap="nowrap">Country</th>
<td>&nbsp;</td>
<td>$todoufuken</td>
</tr>
<tr>
<th nowrap="nowrap"Address１</th>
<td>&nbsp;</td>
<td>$jusho_1</td>
</tr>
<tr>
<th nowrap="nowrap">Address２</th>
<td>&nbsp;</td>
<td>$jusho_2</td>
</tr>
<tr>
<th nowrap="nowrap">Telephone Number</th>
<td>&nbsp;</td>
<td>$tel</td>
</tr>
<tr>
<th nowrap="nowrap">FAX</th>
<td>&nbsp;</td>
<td>$fax</td>
</tr>
<tr>
<th nowrap="nowrap">E-mail address</th>
<td><div class="need">Mandatory</div></td>
<td>$mail</td>
</tr>
</table>
<br />

<div class="line">　</div>

<div>
<dl class="sign" id="ssl">
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>

<dd style="height:50px;">*Personal customer information will only be used for our management. All of our site and transactions are based on SSL protection.
</dd>
</dl>
</div>


</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../../images/go-top.png" alt="to TOP" width="88" height="38" /></a></div>

<div id="footer">
<div class="alpha sponsor2">
<table>
<tr>
<td>
Organizers：<a href="http://www.nedo.go.jp/english/index.html" target="_blank"><img src="../../images/nedo-logo.png" alt="New Energy and Industrial Technology Development Organization" width="60" height="31"/></a></td>
<td>New Energy and Industrial Technology <br />
Development Organization</td>
<td class="space">&nbsp;</td>
<td>Co-Organizer：<a href="http://www.meti.go.jp/english/index.html" target="_blank"><img src="../../images/keizai-logo.png" alt="Ministry of Economy, Trade and Industry" width="111" height="33" /></a></td>
<td>Ministry of Economy, <br />
Trade and Industry</td>
</tr>
</table>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>

</body>
</html>

EOM
exit;