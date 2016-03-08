#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LIGHT BOARD
#│ admin.cgi - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require './init.cgi';
require $jcode;

&decode;
&setfile;
&auth_check;
if ($in{'log_mente'}) { &log_mente; }
elsif ($in{'set_up'}) { &set_up; }
elsif ($in{'aprv_log'}) { &aprv_log; }
elsif ($in{'chg_pwd'}) { &chg_pwd; }
&admin_menu;

#-------------------------------------------------
#  管理モード
#-------------------------------------------------
sub admin_menu {
	&header;
	print <<EOM;
<div align="right">
<form action="$bbscgi">
<input type="submit" value="▲掲示板へ">
</form>
</div>
<div align="center">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<table border="1" cellpadding="5" cellspacing="0">
<tr>
	<th bgcolor="#b5b5ff">選択</th>
	<th width="220" bgcolor="#b5b5ff">処理項目</th>
</tr><tr>
	<th><input type="submit" name="set_up" value="選択"></th>
	<td>設定内容の変更</td>
</tr><tr>
	<th><input type="submit" name="log_mente" value="選択"></th>
	<td>記事メンテナンス</td>
EOM

	if ($conf_log) {

		print qq|</tr><tr>\n|;
		print qq|<th><input type="submit" name="aprv_log" value="選択"></th>\n|;
		print qq|<td>未承認記事の承認アップ</td>|;
	}

	print <<EOM;
</tr><tr>
	<th><input type="submit" name="chg_pwd" value="選択"></th>
	<td>パスワードの変更</td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  記事のメンテナンス
#-------------------------------------------------
sub log_mente {


	# 削除
	if ($in{'job'} eq "dele" && $in{'no'}) {

		# 削除情報
		my %del;
		foreach ( split(/\0/, $in{'no'}) ) {
			$del{$_} = 1;
		}

		# 削除記事抜き取り
		my @data;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no) = split(/<>/);

			if (!defined($del{$no})) {
				push(@data,$_);
			}
		}

		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# 修正フォーム
	} elsif ($in{'job'} eq "edit" && $in{'no'}) {

		# 記事は１つのみ
		if ($in{'no'} =~ /\0/) { &error("修正記事の選択は１つのみです"); }

		local($no,$dat,$nam,$eml,$sub,$com,$url);
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);

			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);

	# 修正実行
	} elsif ($in{'job'} eq "edit2") {

		# 入力チェック
		if ($in{'url'} eq "http://") { $in{'url'} = ""; }

		# データオープン
		my @data;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);

			if ($in{'no'} == $no) {
				$_ = "$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@data,$_);
		}

		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	# 管理画面
	&header;
	&back_btn;
	print <<EOM;
<p>処理を選択して送信ボタンを押してください。</p>
<form action="$admincgi" method="post">
<input type="hidden" name="log_mente" value="1">
<input type="hidden" name="pass" value="$in{'pass'}">
処理：
<select name="job">
<option value="edit">修正
<option value="dele">削除</select>
<input type="submit" value="送信する">
<dl>
EOM

	# 記事展開
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70) . "...";
		}

		print qq|<dt><hr><input type="checkbox" name="no" value="$no">|;
		print qq|[<b>$no</b>] <b style="color:$subcol">$sub</b> - <b>$nam</b> - $dat|;
		print qq|<dd>$com <font color="$subcol" size="-1">&lt;$hos&gt;</font>\n|;
	}
	close(IN);

	print <<EOM;
<dt><hr>
</dl>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  設定処理
#-------------------------------------------------
sub set_up {

	# 編集実行
	if ($in{'submit'}) {

		# チェック
		if (!$in{'home'}) { &error('戻り先の入力がありません'); }
		if (!$in{'max'}) { &error('最大記事数の入力がありません'); }
		if (!$in{'plog'}) { &error('表示件数の入力がありません'); }
		if (!$in{'b_size'}) { &error('本文文字サイズの入力がありません'); }
		if ($in{'t_img'} eq "http://") { $in{'t_img'} = ""; }
		if ($in{'bg'} eq "http://") { $in{'bg'} = ""; }
		$in{'no_wd'} =~ s/　/ /g;

		# 更新
		open(OUT,"+> $setfile") || &error("Write Error : $setfile");
		print OUT "$in{'title'}<>$in{'t_col'}<>$in{'t_size'}<>$in{'t_face'}<>$in{'t_img'}<>$in{'bg'}<>$in{'bc'}<>$in{'tx'}<>$in{'li'}<>$in{'vl'}<>$in{'al'}<>$in{'home'}<>$in{'max'}<>$in{'subcol'}<>$in{'refcol'}<>$in{'plog'}<>$in{'b_size'}<>$in{'mail'}<>$in{'deny'}<>$in{'link'}<>$in{'wait'}<>$in{'no_wd'}<>$in{'jp_wd'}<>$in{'urlnum'}<>";
		close(OUT);

		# 完了メッセージ
		&header;
		print qq|<div align="center"><h3>設定が完了しました</h3>\n|;
		print qq|<form action="$admincgi" method="post">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="管理TOPに戻る"></form>\n|;
		print qq|</div>\n</body></html>\n|;
		exit;
	}

	$t_img ||= "http://";
	$bg    ||= "http://";
	$home  ||= "http://";
	$b_size =~ s/\D//g;

	&header;
	&back_btn;
	print <<EOM;
<ul>
<li>修正する部分のみ変更してください。
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="set_up" value="1">
<table border="0">
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>タイトル名</td>
  <td><input type="text" name="title" size="30" value="$title"></td>
</tr><tr>
  <td>タイトル色</td>
  <td>
	<input type="text" name="t_col" size="12" value="$t_col" style="ime-mode:inactive">
	<font color="$t_col">■</font>
  </td>
</tr><tr>
  <td>タイトルサイズ</td>
  <td>
	<input type="text" name="t_size" size="5" value="$t_size" style="ime-mode:inactive">
	ピクセル
  </td>
</tr><tr>
  <td>タイトルフォント</td>
  <td><input type="text" name="t_face" size="30" value="$t_face" style="ime-mode:inactive"></td>
</tr><tr>
  <td>タイトル画像</td>
  <td>
	<input type="text" name="t_img" size="40" value="$t_img" style="ime-mode:inactive">
	（任意）
  </td>
</tr><tr><td colspan="2"><hr></td></tr>
<tr>
  <td>壁紙</td>
  <td>
	<input type="text" name="bg" size="40" value="$bg" style="ime-mode:inactive">
	（任意）
  </td>
</tr><tr>
  <td>背景色</td>
  <td><input type="text" name="bc" size="12" value="$bc" style="ime-mode:inactive">
	<font color="$bc">■</font></td>
</tr>
<tr>
  <td>文字色</td>
  <td><input type="text" name="tx" size="12" value="$tx" style="ime-mode:inactive">
	<font color="$tx">■</font></td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type="text" name="li" size="12" value="$li" style="ime-mode:inactive">
	<font color="$li">■</font> （未訪問）</td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type="text" name="vl" size="12" value="$vl" style="ime-mode:inactive">
	<font color="$vl">■</font> （訪問済）</td>
</tr>
<tr>
  <td>リンク色</td>
  <td><input type="text" name="al" size="12" value="$al" style="ime-mode:inactive">
	<font color="$al">■</font> （訪問中）</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>記事題名色</td>
  <td><input type="text" name="subcol" size="12" value="$subcol" style="ime-mode:inactive">
	<font color="$subcol">■</font></td>
</tr>
<tr>
  <td>引用符色</td>
  <td><input type="text" name="refcol" size="12" value="$refcol" style="ime-mode:inactive">
	<font color="$refcol">■</font></td>
</tr>
<tr>
  <td>戻り先</td>
  <td><input type="text" name="home" size="40" value="$home" style="ime-mode:inactive"></td>
</tr>
<tr>
  <td>最大記事数</td>
  <td><input type="text" name="max" size="5" value="$max" style="ime-mode:inactive"></td>
</tr>
<tr>
  <td>表\示件数</td>
  <td><input type="text" name="plog" size="5" value="$plog" style="ime-mode:inactive">
	（1ページ当りの記事表\示数）</td>
</tr>
<tr>
  <td>本文文字</td>
  <td><input type="text" name="b_size" size="5" value="$b_size" style="ime-mode:inactive">
	ピクセル</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>URLリンク</td>
  <td>
EOM

	my @ox = ("しない","する");
	foreach (0,1) {
		if ($link == $_) {
			print "<input type=\"radio\" name=\"link\" value=\"$_\" checked>$ox[$_]\n";
		} else {
			print "<input type=\"radio\" name=\"link\" value=\"$_\">$ox[$_]\n";
		}
	}

	print <<EOM;
	&nbsp;（記事中のURLを自動リンク）
  </td>
</tr>
<tr>
  <td>URL制限</td>
  <td><input type="text" name="urlnum" size="5" value="$urlnum" style="ime-mode:inactive">
	（投稿時、本文に含まれるURLの個数制限。0にすると機能\オフ）</td>
</tr>
<tr>
  <td>投稿間隔</td>
  <td><input type="text" name="wait" size="5" value="$wait" style="ime-mode:inactive"> 秒
	（同一ホストの連続投稿制御）</td>
</tr>
<tr>
  <td>英文制限</td>
  <td>
EOM

	foreach (0,1) {
		if ($jp_wd == $_) {
			print "<input type=\"radio\" name=\"jp_wd\" value=\"$_\" checked>$ox[$_]\n";
		} else {
			print "<input type=\"radio\" name=\"jp_wd\" value=\"$_\">$ox[$_]\n";
		}
	}

	print <<EOM;
	&nbsp;（題名・本文に日本語が含まれない場合投稿拒否）
</tr>
EOM

	if ($sendmail) {
		print "<tr><td colspan=\"2\"><hr></td></tr>\n";
		print "<tr><td>Ｅメール</td>";
		print "<td><input type=\"text\" name=\"mail\" size=\"30\" value=\"$mail\"><br>\n";
		print "（メール通知する場合）</td></tr>\n";
	}

	print <<"EOM";
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>拒否ホスト</td>
  <td><input type="text" name="deny" size="50" value="$deny">
	（スペースで区切る）</td>
</tr>
<tr>
  <td>禁止ワード</td>
  <td><input type="text" name="no_wd" size="50" value="$no_wd">
	（スペースで区切る）</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
</table>
<input type="submit" name="submit" value="設定を修正する"></form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  未承認記事の承認
#-------------------------------------------------
sub aprv_log {
	# 承認
	if ($in{'job'} eq "aprv" && $in{'no'}) {

		# 該当ログ
		my @log;
		foreach ( split(/\0/, $in{'no'}) ) {
			open(DB,"$tmpdir/$_.cgi");
			my $log = <DB>;
			close(DB);

			unshift(@log,$log);
		}

		# 本番ログ
		local($i, $top, @data, @past);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			$i++;
			if ($i == 1) { $top = $_; }

			# 現行ログ
			if ($i < $max - @log) {
				push(@data,$_);

			# 過去ログ
			} elsif ($pastkey) {
				push(@past,$_);
			}
		}

		# 採番
		my $num = (split(/<>/, $top))[0];

		# 本番データ更新
		foreach (@log) {
			$num++;
			unshift(@data,"$num<>$_\n");
		}

		# 本番データ更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 過去ログ更新
		if (@past > 0) {
			require $pastmkpl;
			&past_make;
		}

		# 一時ログ削除
		foreach ( split(/\0/, $in{'no'}) ) {
			unlink("$tmpdir/$_.cgi");
		}

	# 削除
	} elsif ($in{'job'} eq "dele" && $in{'no'}) {

		# ログ削除
		foreach ( split(/\0/, $in{'no'}) ) {
			unlink("$tmpdir/$_.cgi");
		}
	}

	opendir(DIR,"$tmpdir");
	my @dir = readdir(DIR);
	closedir(DIR);

	my @log;
	foreach (@dir) {
		if (/^(\d+)\.cgi$/) {
			push(@log,$1);
		}
	}
	@log = sort{ $b <=> $a }@log;

	# 管理画面
	&header;
	&back_btn;
	print <<EOM;
<p>処理を選択して送信ボタンを押してください。</p>
<form action="$admincgi" method="post">
<input type="hidden" name="aprv_log" value="1">
<input type="hidden" name="pass" value="$in{'pass'}">
処理：
<select name="job">
<option value="aprv">承認
<option value="dele">削除
</select>
<input type="submit" value="送信する">
<dl>
EOM

	foreach (@log) {

		open(DB,"$tmpdir/$_.cgi");
		my $log = <DB>;
		close(DB);

		my ($dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/, $log);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70) . "...";
		}

		print qq|<dt><hr><input type="checkbox" name="no" value="$_">|;
		print qq|<b style="color:$subcol">$sub</b> - <b>$nam</b> - $dat|;
		print qq|<dd>$com <font color="$subcol" size="-1">&lt;$hos&gt;</font>\n|;
	}

	print <<EOM;
<dt><hr>
</dl>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<h4>パスワードを入力してください</h4>
<form action="$admincgi" method="post">
<input type="radio" name="mode" value="admin" checked>記事
<input type="radio" name="mode" value="setup">設定<br><br>
<input type="password" name="pass" size="10">
<input type="submit" value=" 認証 ">
</form>
</div>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  入室画面
#-------------------------------------------------
sub back_btn {
	print <<EOM;
<div align="right">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; メニュー">
</form>
</div>
EOM
}

#-------------------------------------------------
#  編集フォーム
#-------------------------------------------------
sub edit_form {
	local($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	$url ||= "http://";
	$com =~ s/<br>/\n/g;

	&header;
	print <<EOM;
[<a href="javascript:history.back()">前画面に戻る</a>]
<h3>編集フォーム</h3>
<ul>
<li>修正する部分のみ変更してください。
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="log_mente" value="1">
<input type="hidden" name="job" value="edit2">
投稿者名<br><input type="text" name="name" size="28" value="$nam"><br>
Ｅメール<br><input type="text" name="email" size="28" value="$eml"><br>
タイトル<br><input type="text" name="sub" size="36" value="$sub"><br>
参照先<br><input type="text" name="url" size="45" value="$url"><br>
コメント<br><textarea name="comment" cols="58" rows="7">$com</textarea><br>
<input type="submit" value=" 修正を行う "></form>
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  パスワード認証
#-------------------------------------------------
sub auth_check {
	# パスワードファイルが空の場合は設定画面へ
	if (-z $pwdfile) {
		&chg_pwd;
	}

	# パスワード未入力の場合は入力画面へ
	if ($in{'pass'} eq "") {
		&pwd_form;
	}

	# パスワード読み込み
	open(IN,"$pwdfile");
	my $data = <IN>;
	close(IN);

	# 認証
	if (&decrypt($in{'pass'}, $data) != 1) {
		&error("認証できません");
	}
}

#-------------------------------------------------
#  パスワード入力画面
#-------------------------------------------------
sub pwd_form {
	&header;
	print <<EOM;
<div align="center">
<p>管理パスワードを入力してください</p>
<form action="$admincgi" method="post">
<input type="password" name="pass" size="20">
<input type="submit" value="認証">
</form>
</div>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  パスワード変更
#-------------------------------------------------
sub chg_pwd {
	# 変更
	if ($in{'submit'}) {

		my $err;
		if ($in{'pass1'} eq "" || $in{'pass2'} eq "") {
			$ere .= "新パスワードが未入力です<br>";
		}
		if ($in{'pass1'} ne $in{'pass2'}) {
			$err .= "再度入力したパスワードが違います<br>";
		}
		if ($err) { &error($err); }

		open(DAT,"+> $pwdfile") || &error("Write Error: $pwdfile");
		print DAT &encrypt($in{'pass1'});
		close(DAT);

		# 完了メッセージ
		&header;
		print qq|<div align="center"><h3>変更が完了しました</h3>\n|;
		print qq|<form action="$admincgi" method="post">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass1'}">\n|;
		print qq|<input type="submit" value="管理TOPに戻る"></form>\n|;
		print qq|</div>\n</body></html>\n|;
		exit;
	}

	&header;
	&back_btn;
	print <<EOM;
<blockquote>
新パスワードを入力してください
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="chg_pwd" value="1">
<table>
<p>■新パスワード（英数字で8文字以内）<br>
<input type="password" name="pass1" size="20">
</p>
<p>■再度入力<br>
<input type="password" name="pass2" size="20">
</p>
<input type="submit" name="submit" value="送信する">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}


