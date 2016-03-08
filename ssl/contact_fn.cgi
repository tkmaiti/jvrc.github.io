#!/usr/bin/perl

require 'cgi-lib.pl';
require 'jcode.pl';

&ReadParse(*in);

$name = $in{'name'};
$shozoku = $in{'shozoku'};
$mail = $in{'mail'};
$naiyo = $in{'naiyo'};

$date = $in{'date'};
$ip = $in{'ip'};

$owFlag = 0;

$etr_log = "\"$date\",\"$ip\",\"$name\",\"$shozoku\",\"$mail\",\"$naiyo\",,,,\n";

open(FILE,"./jvrc_log/jvrc_con.csv")||die "Can't open file";
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

	open(FILE, ">./jvrc_log/jvrc_con.csv")||die "Can't open file";
	flock(FILE,2);
	print FILE @etr_log_body;
	flock(FILE,8);
	close(FILE);

	$printdate = " ■  お問合せ日時  ■ $date \n";
	$printname = " ■     氏  名     ■ $name \n";
	$printshozoku = " ■ご所属（勤務先）■ $shozoku \n";
	$printmail = " ■ メールアドレス ■ $mail \n";
	$printnaiyo = " ■  お問合せ内容  ■ $naiyo \n";

	$topbody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nジャパンバーチャルロボティクスチャレンジ(JVRC)\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nお問合せ、ありがとうございました。\n\n以下の内容が「ジャパンバーチャルロボティクスチャレンジ」事務局に送信されました。\n\n";$middlebody = "$printdate$printname$printshozoku$printmail$printnaiyo\n\n";
	
	$bottombody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n日　時：2015年（平成27年）10月7日～10月10日\n会　場：CEATEC JAPAN 2015\n参加費：無料\n\nジャパンバーチャルロボティクスチャレンジ事務局\nhttp://www.jvrc.org/\ninquiry\@jvrc.org\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n※入力された個人情報は、当大会のお問い合せ以外では使用致しません。\n\　\送信はＳＳＬ（暗号化通信）で保護されています。";
	$send = "\"「Japan Virtual Robotics Challenge(JVRC)」事務局\"<inquiry\@jvrc.org>";
	$subject = "「ジャパンバーチャルロボティクスチャレンジ」お問合せ";
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
	print MAIL "To: inquiry\@jvrc.org\n";
#	print MAIL "To: e.imabayashi\@adthree.com\n";
#	print MAIL "To: mmm\@s-vivid.com\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);

}

print "Content-type: text/html\n\n";
#print "Content-type: text/html; charset=Shift_JIS\n\n";

	print <<EOM;


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">
<head>
<meta http-equiv="content-type" content="text/html; charset=Shift_JIS" />
<title>ジャパンバーチャルロボティクスチャレンジ</title>
<meta http-equiv="content-style-type" content="text/css" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="keywords" content="ジャパンバーチャルロボティクスチャレンジ,Japan Virtual Robotics Challenge,JVRC,国立研究開発法人新エネルギー・産業技術総合開発機構,NEDO," />
<meta name="description" content="「ジャパンバーチャルロボティクスチャレンジ（Japan Virtual Robotics Challenge）」（略称JVRC）は国立研究開発法人新エネルギー・産業技術総合開発機構 (NEDO) が実施中の「環境・医療分野の国際研究開発・実証プロジェクト／ロボット分野の国際研究開発・実証事業／災害対応ロボット研究開発（アメリカ）」プロジェクトの一環として実施する災害対応ロボットのコンピュータシミュレーションによる競技会です。" />

<link rel="shortcut icon" href="../images/favicon.ico" />

<link href="../css/import.css" rel="stylesheet" type="text/css" media="all" />
<link href="style_info.css" rel="stylesheet" type="text/css" media="all" />
<script type="text/javascript" src="../js/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="../js/base.js"></script>

</head>


<body>

<div id="page">

<div id="header">
<div class="imgArea">
<a href="http://jvrc.org/index.html">
<img src="../images/img-main.png" alt="メインイメージ" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/en/ssl/contact.html"><img src="../images/en_flag.png" alt="english" width="21" height="14" />English</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<ul id="dropmenu">
<li><a href="http://jvrc.org/index.html">TOP&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/about.html">ＪＶＲＣについて</a></li>
  </ul>
</li>
<li><a href="http://jvrc.org/rule.html">競技ルール&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/tech-guide.html">JVRCテクニカルガイド</a></li>
  </ul>
</li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">チュートリアル</a></li>
<li><a href="http://jvrc.org/team.html">チーム紹介</a></li>
<li><a href="http://jvrc.org/download.html">ダウンロード</a></li>
<li><a href="http://jvrc.org/result.html">進行状況・結果</a></li>
<li><a href="http://jvrc.org/faq.html">よくあるご質問(FAQ)</a></li>
<li class="current-page"><a href="https://jvrc.org/ssl/contact.html"><img src="../images/inquiry-icon.png" alt="" width="22" height="16" />&nbsp;お問い合わせ&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6" /></a>
  <ul>
  <li><a href="https://jvrc.org/ssl/etr.html"><img src="../images/sanka-icon.png" alt="" width="26" height="21" />&nbsp;参加申込み</a></li>
  </ul>
</li>
</ul>
<!-- / #navi --></div>

<div id="contents" class="clearfix">
<div id="main2">


<h2>お問い合せ完了</h2>
<br />
<div class="need2">
<span class="red">以下の内容を送信しました。</span></div>
  
                    
<table class="form" summary="お問い合わせ">
<tr>
<th width="17%" nowrap="nowrap" class="t_top">お名前</th>
<td width="6%" class="aqua"><div class="need">必須</div></td>
<td width="77%" class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">ご所属先（勤務先）</th>
<td><div class="need">必須</div></td>
<td>$shozoku</td>
</tr>
<tr>
<th nowrap="nowrap">メールアドレス</th>
<td><div class="need">必須</div></td>
<td>$mail</td>
</tr>
<tr>
<th nowrap="nowrap">お問い合わせ内容</th>
<td><div class="need">必須</div></td>
<td>$naiyo</td>
</tr>
</table>

<br />


<div class="line">　</div>

<div>
<dl class="sign" id="ssl">
<!--
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja"><a href="http://jp.globalsign.com/" target="_blank"><img alt="SSL　グローバルサインのサイトシール" border="0" id="ss_img" src="//seal.globalsign.com/SiteSeal/images/gs_noscript_100-50_ja.gif"></a></span><script type="text/javascript" src="//seal.globalsign.com/SiteSeal/gs_flash_100-50_ja.js"></script></dt>
-->
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>
<dd style="height:50px;">※ご記入頂いた個人情報は、弊社責任の下で管理し、本大会以外の目的では使用致しません。</dd>
</dl>
</div>

</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../images/go-top.png" alt="トップへ" width="88" height="38" /></a></div>

<div id="footer">
<div class="sponsor alpha">主催：<a href="http://www.nedo.go.jp/" target="_blank"><img src="../images/nedo-logo.png" alt="国立研究開発法人　新エネルギー・産業技術総合開発機構" width="60" height="31"/></a>　国立研究開発法人　新エネルギー・産業技術総合開発機\構\ 　　　　共催：<a href="http://www.meti.go.jp/" target="_blank"><img src="../images/keizai-logo.png" alt="経済産業省" width="111" height="33" /></a>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>

</body>
</html>

EOM
exit;