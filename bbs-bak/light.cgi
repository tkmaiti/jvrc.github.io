#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LIGHT BOARD
#│ light.cgi - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require './init.cgi';
require $jcode;

&decode;
&setfile;
if ($in{'regist'}) {
	require $registpl;
	&regist;
} elsif ($mode eq "editlog") {
	require $editpl;
	&editlog;
} elsif ($mode eq "delelog") {
	require $editpl;
	&delelog;
} elsif ($mode eq "past" && $pastkey) {
	require $pastpl;
	require $searchpl;
	&pastlog;
} elsif ($mode eq "check") {
	require $checkpl;
	&check;
} elsif ($mode eq "howto") {
	&howto;
} elsif ($mode eq "find") {
	&find;
}
&viewlog;

#-------------------------------------------------
#  記事表示
#-------------------------------------------------
sub viewlog {
	# レス数＆ページ数を認識
	my ($res, $page);
	foreach ( keys(%in) ) {
		if (/^res(\d+)$/) {
			$res = $1;
			last;
		} elsif (/^page(\d+)$/) {
			$page = $1;
			last;
		}
	}

	# クッキー取得
	my ($cnam, $ceml, $curl, $cpwd) = &get_cookie;
	if (!$curl) { $curl = "http://"; }

	# タイトル表示
	&header;
	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" alt=\"$title\">\n";
	} else {
		print "<b style=\"color:$t_col; font-size:$t_size";
		print "px; font-family:'$t_face'\">$title</b>\n";
	}

	# 表示開始
	print <<"EOM";
<hr width="90%">
[<a href="$home" target="_top">トップに戻る</a>]
[<a href="$bbscgi?mode=howto">留意事項</a>]
[<a href="$bbscgi?mode=find">ワード検索</a>]
EOM

	# 過去ログリンク
	print "[<a href=\"$bbscgi?mode=past\">過去ログ</a>]\n" if ($pastkey);

	# ログ編集機能のリンク
	print "[<a href=\"$admincgi\">管理用</a>]\n";

	# 返信モード
	my ($resub, $recom);
	if ($res) {

		# 引用記事抽出
		open(IN,"$logfile");
		while (<IN>) {
			my ($no,$dat,$nam,$eml,$sub,$com) = split(/<>/);

			if ($res == $no) {

				# コメントに引用符付加
				$recom = "&gt; $com";
				$recom =~ s/<br>/\n&gt; /g;

				# 題名に引用項目付加
				$sub =~ s/^Re://;
				$resub = "Re:[$res] $sub";

				last;
			}
		}
		close(IN);
	}

	# 投稿フォーム
	print <<EOM;
<hr width="90%"></div>
<form method="post" action="$bbscgi">
<blockquote>
<table cellpadding="1" cellspacing="1">
<tr>
  <td><b>おなまえ</b></td>
  <td><input type="text" name="name" size="28" value="$cnam"></td>
</tr>
<tr>
  <td><b>Ｅメール</b></td>
  <td><input type="text" name="email" size="28" value="$ceml"></td>
</tr>
<tr>
  <td><b>タイトル</b></td>
  <td><input type="text" name="sub" size="36" value="$resub">
	<input type="submit" name="regist" value="投稿する"><input type="reset" value="リセット"></td>
</tr>
<tr>
  <td colspan="2"><b>コメント</b><br>
  <textarea cols="56" rows="7" name="comment">$recom</textarea></td>
</tr>
<tr>
  <td><b>参照先</b></td>
  <td><input type="text" size="50" name="url" value="$curl"></td>
</tr>
EOM

	# 投稿キー
	if ($regist_key) {
		require $regkeypl;
		my ($str_plain,$str_crypt) = &pcp_makekey;

		print qq|<tr><td><b>投稿キー</b></td>|;
		print qq|<td><input type="text" name="regikey" size="6" style="ime-mode:inactive" value="">\n|;
		print qq|（投稿時 <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="投稿キー"> を入力してください）</td></tr>\n|;
		print qq|<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
	}

	print <<EOM;
<tr>
  <td><b>パスワード</b></td>
  <td><input type="password" name="pwd" size="8" maxlength="8" value="$cpwd">
  （記事メンテ用）</td>
</tr>
</table>
</blockquote>
<dl>
EOM

	# 記事展開
	my $i = 0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { next; }

		my ($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);

		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color="$refcol">$2<\/font>/g;
		$com .= "<p><a href=\"$url\" target=\"_blank\">$url</a>" if ($url);

		# 記事編集
		print "<dt><hr>[<b>$no</b>] <b style=\"color:$subcol\">$sub</b> ";
		print "投稿者：<b>$nam</b> 投稿日：$dat &nbsp;";
		print "<input type=\"submit\" name=\"res$no\" value=\"返信\"><br><br>\n";
		print "<dd>$com<br><br>\n";
	}
	close(IN);

	print "<dt><hr></dl>\n";

	# 繰り越しページ定義
	my $next = $page + $plog;
	my $back = $page - $plog;

	my $flg;
	if ($back >= 0) {
		$flg = 1;
		print qq|<input type="submit" name="page$back" value="前ページ">\n|;
	}
	if ($next < $i) {
		$flg = 1;
		print qq|<input type="submit" name="page$next" value="次ページ">\n|;
	}

	# ページ移動ボタン表示
	if ($flg) {
		my ($x, $y) = (1, 0);
		while ( $i > 0 ) {
			if ($page == $y) {
				print "<b>[$x]</b>\n";
			} else {
				print "[<a href=\"$bbscgi?page$y=val\">$x</a>]\n";
			}
			$x++;
			$y += $plog;
			$i -= $plog;
		}
	}
	print <<"EOM";
</form>
<div align="center">
<form action="$bbscgi" method="post">
処理 <select name="mode">
<option value="editlog">修正
<option value="delelog">削除</select>
記事No<input type="text" name="no" size="3" style="ime-mode:inactive">
暗証キー<input type="password" name="pwd" size="6" maxlength="8">
<input type="submit" value="送信"></form>
<!-- 著作権表\記:削除禁止($ver) -->
<span style="font-size:10px;font-family:Verdana,Helvetica">
- <a href="http://www.kent-web.com/" target="_top">LightBoard</a> -
</span></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  留意事項
#-------------------------------------------------
sub howto {
	&header;
	print <<EOM;
<div align="center">
<table border="1" width="85%" cellpadding="15">
<tr><td class="r">
<h3>掲示板利用上の注意</h3>
<ol>
<li>この掲示板は<b>クッキー対応</b>です。1度記事を投稿いただくと、おなまえ、Ｅメール、ＵＲＬ、暗証キーの情報は2回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）
<li>投稿内容には、<b>タグは一切使用できません。</b>
<li>記事を投稿する上での必須入力項目は<b>「おなまえ」</b>と<b>「メッセージ」</b>です。Ｅメール、ＵＲＬ、題名、暗証キーは任意です。
<li>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。
<li>記事の投稿時に<b>暗証キー</b>（英数字で8文字以内）を入れておくと、その記事は次回暗証キーによって削除することができます。
<li>記事の保持件数は最大<b>$max件</b>です。それを超えると古い順に自動削除されます。
<li>既存の記事に簡単に<b>「返信」</b>することができます。各記事にある<b>「返信」ボタン</b>を押すと投稿フォームが返信用となります。
<li>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$bbscgi?mode=find">「ワード検索」</a>のリンクをクリックすると検索モードとなります。
<li>管理者が著しく不利益と判断する記事や他人を誹謗中傷する記事は予\告なく削除することがあります。
</ol>
</td></tr>
</table>
<form>
<input type="button" value="掲示板に戻る" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  検索画面
#-------------------------------------------------
sub find {
	&header;
	print <<EOM;
<form action="$bbscgi">
<input type="submit" value="掲示板に戻る">
</form>
<ul>
<li>検索したい<b>キーワード</b>を入力し、「条件」「表\示」を選択して「検索」ボタンを押して下さい。
<li>キーワードは半角スペースで区切って複数指定することができます。
</ul>
<table>
<tr>
EOM

	require $searchpl;
	&search($logfile);
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  クッキー取得
#-------------------------------------------------
sub get_cookie {
	# クッキーを取得
	my $cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	my %cook;
	foreach ( split(/;/, $cook) ) {
		my ($key, $val) = split(/=/);

		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	my @cook;
	foreach ( split(/<>/, $cook{'LIGHT_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		push(@cook,$_);
	}
	return @cook;
}

#-------------------------------------------------
#  自動リンク
#-------------------------------------------------
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_top\">$2<\/a>/g;
}


