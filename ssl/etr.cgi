#!/usr/bin/perl

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
$kana = $in{'kana'};
$kinmu = $in{'kinmu'};
$yakushoku = $in{'yakushoku'};
$yubin = $in{'yubin'};
$todoufuken = $in{'todoufuken'};
$jusho_1 = $in{'jusho_1'};
$jusho_2 = $in{'jusho_2'};
$tel = $in{'tel'};
$fax = $in{'fax'};
$mail = $in{'mail'};



($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$month = $mon+1;
$year+=1900;
$date = "$year年$month月$mday日$hour時$min分$sec秒";
$ip = $ENV{"REMOTE_ADDR"};


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
<a href="http://jvrc.org/index.html">
<img src="../images/img-main.png" alt="メインイメージ" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/en/ssl/etr.html"><img src="../images/en_flag.png" alt="english" width="21" height="14" />English</a>
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
<li><a href="http://jvrc.org/rule.html">競技ルール</a></li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">チュートリアル</a></li>
<li><a href="http://jvrc.org/team.html">チーム紹介</a></li>
<li><a href="http://jvrc.org/download.html">ダウンロード</a></li>
<li><a href="http://jvrc.org/result.html">進行状況・結果</a></li>
<li><a href="http://jvrc.org/faq.html">よくあるご質問(FAQ)</a></li>
<li class="current-page"><a href="https://jvrc.org/ssl/contact.html"><img src="../images/inquiry-icon.png" alt="" width="22" height="16" />&nbsp;お問い合わせ&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6" /></a>
  <ul>
  <li><a href="https://jvrc.org/ssl/etr.html"><img src="../images/sanka-icon.png" alt="" width="26" height="23" />&nbsp;参加申込み</a></li>
  </ul>
</li>
</ul>
<!-- / #navi --></div>

<div id="contents" class="clearfix">
<div id="main2">

<!--form ここから-->
<h2>参加\申\込み確認</h2><br />

<div class="need2">
<span class="red">以下の内容にお間違いがなければ【お\申\し込みを完了する】ボタンを押してください。</span><br />
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
<!--<tr>
<th nowrap="nowrap">案内</th>
<td><span class="need" style="vertical-align: middle;">必須</span></td>
<td>今後「ジャパンバーチャルロボティクスチャレンジ（JVRC）」からの案内を&nbsp;
$kibou
</td>
</tr>-->
</table>
<br />

<div class="t-center">
<form method="post" action="etr_fn.cgi" name="thisform" onsubmit='return checkForm()'>
<input type=button value=" 戻 る " onClick="javascript:history.back()">　<input type=submit value="お\申\し込みを完了する">
<input type=hidden name="name" value="$name">
<input type=hidden name="kana" value="$kana">
<input type=hidden name="kinmu" value="$kinmu">
<input type=hidden name="yakushoku" value="$yakushoku">
<input type=hidden name="yubin" value="$yubin">
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
<div class="line">　</div>

<div>
<dl class="sign" id="ssl">
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>

<dd style="height:50px;">※ご記入頂いた個人情報は、弊社責任の下で管理し、本大会以外の目的では使用致しません。
</dd></dl>
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