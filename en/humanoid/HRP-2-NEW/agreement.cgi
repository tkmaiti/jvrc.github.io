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
		$value =~ s/,/、/g;
        $in{$x} = $value;
    }
}




$name = $in{'name'};
$shozoku = $in{'shozoku'};
$mail = $in{'mail'};



($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$month = $mon+1;
$year+=1900;
$date = "$month/$mday/$year $hour:$min:$sec";
$ip = $ENV{"REMOTE_ADDR"};


print "Content-type: text/html\n\n";

	print <<EOM;


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">
<head>
<meta http-equiv="content-type" content="text/html; charset=Shift_JIS" />
<title>Japan Virtual Robotics Challenge(JVRC)</title>
<meta http-equiv="content-style-type" content="text/css" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="keywords" content="Japan Virtual Robotics Challenge,JVRC,NEDO," />
<meta name="description" content="'Japan Virtual Robotics Challenge' (JVRC for short) is a competition of disaster response robots by computer simulations. It will be held as a part of 'R & D project on Disaster-response Robots' by New Energy and Industrial Technology Development Organization (NEDO)." />

<link rel="shortcut icon" href="../../../images/favicon.ico" />

<link href="../../../css/import.css" rel="stylesheet" type="text/css" media="all" />
<script type="text/javascript" src="../../../js/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="../../../js/base.js"></script>
<link href="style_agreement.css" rel="stylesheet" type="text/css" media="all" />

</head>
<body>

<div id="page">

<div id="header">
<div class="imgArea">
<a href="http://jvrc.org/en/index.html">
<img src="../../../images/en/img-main.png" alt="" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/download.html"><img src="../../../images/ja_flag.png" alt="Japan" width="21" height="14" />Japanese</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<ul id="dropmenu-en">
<li><a href="http://jvrc.org/en/index.html">TOP&nbsp;<img src="../../../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/en/about.html">About JVRC</a></li>
  </ul>
</li>
<li><a href="http://jvrc.org/en/rule.html">Rule&nbsp;<img src="../../../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/en/tech-guide.html">Technical Guide</a></li>
  </ul>
</li>
<li><a href="http://jvrc.github.com/tutorials/html/index.html" target="_blank">Tutorial</a></li>
<li><a href="http://jvrc.org/en/team.html">Team</a></li>
<li class="current-page"><a href="http://jvrc.org/en/download.html">Download</a></li>
<li><a href="http://jvrc.org/en/result.html">Result</a></li>
<li><a href="http://jvrc.org/en/faq.html">FAQs</a></li>
<li><a href="https://jvrc.org/en/ssl/contact.html"><img src="../../../images/inquiry-icon.png" alt="" width="22" height="16" />&nbsp;Contact Us&nbsp;<img src="../../../images/sankaku.png" alt="" width="8" height="6" /></a>
  <ul>
  <li><a href="https://jvrc.org/en/ssl/etr.html"><img src="../../../images/sanka-icon.png" alt="" width="26" height="21" />&nbsp;Application</a></li>
  </ul>
</li>
</ul>
<!-- / #navi --></div>


<div id="contents" class="clearfix">
<div id="main2">

<h2>Confirm Download application</h2>
<br />

<div class="need2 MG-B10">
<!--<p>
<span class="red">Please check your input contents, before you click Downroad button.</span>
</span>
</p> -->
</div>
                 
<table class="form" summary="Download application">
<tr>
<th width="17%" nowrap="nowrap" class="t_top">Name</th>
<td width="10%" class="aqua"><div class="need">Mandatory</div></td>
<td width="77%" class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">Department/Company</th>
<td><div class="need">Mandatory</div></td>
<td>$shozoku</td>
</tr>
<tr>
<th nowrap="nowrap">E-mail address</th>
<td><div class="need">Mandatory</div></td>
<td>$mail</td>
</tr>
</table>

<br />

<div class="t-center">
<form method="post" action="https://jvrc.org/en/humanoid/HRP-2-NEW/agreement_fn.cgi" name="thisform" onsubmit='return checkForm()'>
<input type=button value=" Back " onClick="javascript:history.back()">&nbsp;&nbsp;&nbsp;&nbsp;<input type=submit value=" Downroad ">
<input type=hidden name="name" value="$name">
<input type=hidden name="shozoku" value="$shozoku">
<input type=hidden name="mail" value="$mail">								
<input type=hidden name="date" value="$date">
<input type=hidden name="ip" value="$ip">
</form>
</div>
<br />


<div class="line">&nbsp;</div>
<br />
<br />
<div>
<dl class="sign" id="ssl">
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>
<dd style="height:50px;">*The personal information you provide in this downroad is strictly managed and used only for this event.</dd>
</dl>
</div>

</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../../../images/go-top.png" alt="to TOP" width="88" height="38" /></a></div>

<div id="footer">
<div class="alpha sponsor2">
<table>
<tr>
<td>
Organizers：<a href="http://www.nedo.go.jp/english/index.html" target="_blank"><img src="../../../images/nedo-logo.png" alt="New Energy and Industrial Technology Development Organization" width="60" height="31"/></a></td>
<td>New Energy and Industrial Technology <br />
Development Organization</td>
<td class="space">&nbsp;</td>
<td>Co-Organizer：<a href="http://www.meti.go.jp/english/index.html" target="_blank"><img src="../../../images/keizai-logo.png" alt="Ministry of Economy, Trade and Industry" width="111" height="33" /></a></td>
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