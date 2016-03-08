#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);

require 'cgi-lib.pl';
require 'jcode.pl';

&ReadParse(*in);

$name = $in{'name'};
$kana = $in{'kana'};
$team = $in{'team'};
$kinmu = $in{'kinmu'};
$yakushoku = $in{'yakushoku'};
$yubin = $in{'yubin'};
$todoufuken = $in{'todoufuken'};
$jusho_1 = $in{'jusho_1'};
$jusho_2 = $in{'jusho_2'};
$tel = $in{'tel'};
$fax = $in{'fax'};
$mail = $in{'mail'};
$date = $in{'date'};
$ip = $in{'ip'};

$owFlag = 0;

$etr_log = "\"$date\",\"$ip\",\"$name\",\"$kana\",\"$team\",\"$kinmu\",\"$yakushoku\",\"$yubin\",\"$todoufuken\",\"$jusho_1\",\"$jusho_2\",\"$tel\",\"$fax\",\"$mail\",,,,\n";

open(FILE,"./jvrc_log/jvrc_etr.csv")||die "Can't open file";
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

	open(FILE, ">./jvrc_log/jvrc_etr.csv")||die "Can't open file";
	flock(FILE,2);
	print FILE @etr_log_body;
	flock(FILE,8);
	close(FILE);

	$printdate = " ■お\申\し込み日時■ $date \n";
	$printname = " ■   お 名 前   ■ $name \n";
	$printkana = " ■   フリガナ   ■ $kana \n";
	$printteam = " ■   チーム名   ■ $team \n";
	$printkinmu = " ■   ご 所 属   ■ $kinmu \n";
	$printyakushoku = " ■    役 職     ■ $yakushoku \n";
	$printyubin = " ■   郵便番号   ■ $yubin \n";
	$printtodoufuken = " ■   都道府県   ■ $todoufuken \n";
	$printjusho_1 = " ■   住 所 １   ■ $jusho_1 \n";
	$printjusho_2 = " ■住所２（アパート、ビル名など）■ $jusho_2 \n";
	$printtel = " ■   電話番号   ■ $tel \n";
	$printfax = " ■    ＦＡＸ    ■ $fax \n";
	$printmail = " ■メールアドレス■ $mail \n";			

	$topbody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nジャパンバーチャルロボティクスチャレンジ(JVRC)\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n以下の内容が「ジャパンバーチャルロボティクスチャレンジ」事務局に送信されました。\n\n";
	$middlebody = "$printdate$printname$printkana$printteam$printkinmu$printyakushoku$printyubin$printtodoufuken$printjusho_1$printjusho_2$printtel$printfax$printmail\n\n";
	$bottombody = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n日　 時：2015年（平成27年）10月上旬 詳しくはホームページでお知らせします。\n会　 場：CEATEC（\予\定）\n参加費：無料\n\n参加手続きの詳細については後日、運営事務局よりご連絡致します。\n\nジャパンバーチャルロボティクスチャレンジ事務局\　\株式会社アドスリー内\nhttps://jvrc.org/\nＴＥＬ 03(5925)2840\　\ＦＡＸ 03(5925)2913\nＥメール office\@jvrc.org\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n※入力された個人情報は、当大会参加\申\し込み以外では使用しません。\n\　\送信はＳＳＬ（暗号化通信）で保護されています。";
	$send = "\"「ジャパンバーチャルロボティクスチャレンジ」事務局\"<office\@jvrc.org>";
	$subject = "「ジャパンバーチャルロボティクスチャレンジ」参加\申\込";
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
#	print MAIL "To: e.imabayashi\@adthree.com\n";
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
<a href="../index.html">
<img src="../images/img-main.png" alt="メインイメージ" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/en/ssl/etr.html"><img src="../images/en_flag.png" alt="english" width="21" height="14" />English</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<div id="naviArea">
<ul id="gNav">
<li><a href="../index.html">TOP</a></li>
<li><a href="../rule.html">競技ルール</a></li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">チュートリアル</a></li>
<li><a href="../team.html">チーム紹介</a></li>
<li><a href="../download.html">ダウンロード</a></li>
<li><a href="../result.html">進行状況・結果</a></li>
<li class="current-page"><a href="etr.html"><img src="../images/sanka-icon.png" alt="" width="26" height="25" /> 参加\申\込み</a></li>
<li><a href="contact.html"><img src="../images/inquiry-icon.png" alt="" width="22" height="16" /> お問い合わせ</a></li>
</ul>
<!-- / #naviArea --></div>
<!-- / #navi --></div>


<div id="contents" class="clearfix">
<div id="main2">

<h2>参加\申\込み完了</h2>
<br />

<div class="need2">
<span class="red">以下の内容を送信しました。控えのメールをご確認ください。</span><br />
<br /> 
</div>
                 
<table class="form" summary="お\申\込み">
<tr>
<th nowrap="nowrap" class="t_top">お名前</th>
<td width="6%" class="aqua"><div class="need">必須</div></td>
<td class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">フリガナ</th>
<td><div class="need">必須</div></td>
<td>$kana</td>
</tr>
<tr>
<th nowrap="nowrap">チーム名</th>
<td>&nbsp;</td>
<td>$team</td>
</tr>
<tr>
<th nowrap="nowrap">ご所属</th>
<td>&nbsp;</td>
<td>$kinmu</td>
</tr>
<tr>
<th nowrap="nowrap">役職</th>
<td>&nbsp;</td>
<td>$yakushoku</td>
</tr>
<tr>
<th nowrap="nowrap">郵便番号</th>
<td>&nbsp;</td>
<td>$yubin</td>
</tr>
<tr>
<th nowrap="nowrap">都道府県</th>
<td>&nbsp;</td>
<td>$todoufuken</td>
</tr>
<tr>
<th nowrap="nowrap">住所１</th>
<td>&nbsp;</td>
<td>$jusho_1</td>
</tr>
<tr>
<th nowrap="nowrap">住所２<br />（ビル名など）</th>
<td>&nbsp;</td>
<td>$jusho_2</td>
</tr>
<tr>
<th nowrap="nowrap">電話番号</th>
<td>&nbsp;</td>
<td>$tel</td>
</tr>
<tr>
<th nowrap="nowrap">ＦＡＸ</th>
<td>&nbsp;</td>
<td>$fax</td>
</tr>
<tr>
<th nowrap="nowrap">メールアドレス</th>
<td><div class="need">必須</div></td>
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

<dd style="height:50px;">※ご記入頂いた個人情報は、弊社責任の下で管理し、本大会以外の目的では使用致しません。
</dd>
</dl>
</div>


</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../images/go-top.png" alt="トップへ" width="88" height="38" /></a></div>

<div id="footer">
<div class="sponsor alpha">主催：<a href="http://www.nedo.go.jp/" target="_blank"><img src="../images/nedo-logo.png" alt="国立研究開発法人　新エネルギー・産業技術総合開発機構" width="60" height="31"/></a>　国立研究開発法人　新エネルギー・産業技術総合開発機構 　　　　共催：<a href="http://www.meti.go.jp/" target="_blank"><img src="../images/keizai-logo.png" alt="経済産業省" width="111" height="33" /></a>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>

</body>
</html>

EOM
exit;