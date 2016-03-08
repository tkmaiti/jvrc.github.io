#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);

require 'cgi-lib.pl';

&ReadParse(*in);


if (&MethPost()) {
    foreach $x (%in) {
        $value = $in{$x};
        $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$value =~ s/&/&amp;/g;
		$value =~ s/"/&quot;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/,/ÅA/g;
        $in{$x} = $value;
    }
}



$name = $in{'name'};
#$kana = $in{'kana'};
$team = $in{'team'};
$kinmu = $in{'kinmu'};
$yakushoku = $in{'yakushoku'};
#$yubin = $in{'yubin'};
$todoufuken = $in{'todoufuken'};
$jusho_1 = $in{'jusho_1'};
$jusho_2 = $in{'jusho_2'};
$tel = $in{'tel'};
$fax = $in{'fax'};
$mail = $in{'mail'};



($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$month = $mon+1;
$year+=1900;
$date = "$yearîN$monthåé$mdayì˙$houréû$minï™$secïb";
$ip = $ENV{"REMOTE_ADDR"};


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
<a href="../index.html"><img src="../../images/en/img-main.png" alt="" width="1115" height="313" /></a>

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

<!--form Ç±Ç±Ç©ÇÁ-->
<h2>Confirm Application</h2><br />

<div class=
"need2">
<span class="red">Please check your input contents, before you click SUBMIT button.</span><br />
<br /> 
</div>
                      
<table class="form" summary="Ç®\ê\\çûÇ›">
<tr>
<th nowrap="nowrap" class="t_top">Name</th>
<td width="6%" class="aqua"><div class="need">Mandatory</div></td>
<td class="t_top">$name</td>
</tr>
<!--<tr>
<th nowrap="nowrap">ÉtÉäÉKÉi</th>
<td><div class="need">ïKê{</div></td>
<td>$kana</td>
</tr>-->
<tr>
<th nowrap="nowrap">Team Name</th>
<td>&nbsp;</td>
<td>$team</td>
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
<!--<tr>
<th nowrap="nowrap">óXï÷î‘çÜ</th>
<td>&nbsp;</td>
<td>$yubin</td>
</tr>-->
<tr>
<th nowrap="nowrap">Country</th>
<td>&nbsp;</td>
<td>$todoufuken</td>
</tr>
<tr>
<th nowrap="nowrap">AddressÇP</th>
<td>&nbsp;</td>
<td>$jusho_1</td>
</tr>
<tr>
<th nowrap="nowrap">AddressÇQ</th>
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

<div class="t-center">
<form method="post" action="etr_fn.cgi" name="thisform" onsubmit='return checkForm()'>
<input type=button value=" Back " onClick="javascript:history.back()">&nbsp;&nbsp;&nbsp;&nbsp;<input type=submit value=" Submit ">
<input type=hidden name="name" value="$name">
<input type=hidden name="team" value="$team">
<input type=hidden name="kinmu" value="$kinmu">
<input type=hidden name="yakushoku" value="$yakushoku">
<input type=hidden name="todoufuken" value="$todoufuken">
<input type=hidden name="jusho_1" value="$jusho_1">
<input type=hidden name="jusho_2" value="$jusho_2">
<input type=hidden name="tel" value="$tel">
<input type=hidden name="fax" value="$fax">
<input type=hidden name="mail" value="$mail">
<input type=hidden name="date" value="$date">
<input type=hidden name="ip" value="$ip">
</form>
</div>
<div class="line">Å@</div>

<div>
<dl class="sign" id="ssl">
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>

<dd style="height:50px;">*Personal customer information will only be used for our management. All of our site and transactions are based on SSL protection.
</dd></dl>
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
OrganizersÅF<a href="http://www.nedo.go.jp/english/index.html" target="_blank"><img src="../../images/nedo-logo.png" alt="New Energy and Industrial Technology Development Organization" width="60" height="31"/></a></td>
<td>New Energy and Industrial Technology <br />
Development Organization</td>
<td class="space">&nbsp;</td>
<td>Co-OrganizerÅF<a href="http://www.meti.go.jp/english/index.html" target="_blank"><img src="../../images/keizai-logo.png" alt="Ministry of Economy, Trade and Industry" width="111" height="33" /></a></td>
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