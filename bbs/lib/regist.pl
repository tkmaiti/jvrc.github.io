#┌─────────────────────────────────
#│ LIGHT BOARD
#│ regist.pl - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  投稿受付
#-------------------------------------------------
sub regist {
	# 入力チェック
	if (!$post_flag) { &error("不正なアクセスです"); }
	if ($in{'name'} eq "") { &error("名前が入力されていません"); }
	if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
	if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("e-mailの入力内容が正しくありません");
	}
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }
	if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }
	if ($no_wd) { &no_wd; }
	if ($jp_wd) { &jp_wd; }
	if ($urlnum > 0) { &urlnum; }

	# 投稿キーチェック
	if ($regist_key) {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("投稿キーが入力不備です。<br>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}

		# 投稿キーチェック
		# -1 : キー不一致
		#  0 : 制限時間オーバー
		#  1 : キー一致
		my $chk = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("投稿キーが制限時間を超過しました。<br>投稿フォームに戻って再読込み後、指定の数字を再入力してください");
		} elsif ($chk == -1) {
			&error("投稿キーが不正です。<br>投稿フォームに戻って再読込み後、指定の数字を入力してください");
		}
	}

	# 削除キー暗号化
	local($pwd, $time, $date);
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# 時間取得
	$time = time;
	my ($min,$hour,$mday,$mon,$year,$wday) = (localtime($time))[1..6];
	my @wk = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
				$year+1900,$mon+1,$mday,$wk[$wday],$hour,$min);

	# 一時ファイル収容のとき
	if ($conf_log == 1) {
		&conf_log;

	# 即反映のとき
	} else {
		&add_log;
	}

	# クッキーを発行
	&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'});

	# メール処理
	if ($sendmail && $mail && $in{'email'} ne $mail) { &mailto; }

	# 完了メッセージ
	&message("投稿は正常に処理されました");
}

#-------------------------------------------------
#  記事追加
#-------------------------------------------------
sub add_log {
	# ログを開く
	local($i, @data, @past);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;

	# 二重投稿禁止
	my ($no,$dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $top);
	if ($host eq $ho && $wait > $time - $tim) {
		close(DAT);
		&error("連続投稿はもうしばらく時間を置いてください");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		close(DAT);
		&error("二重投稿は禁止です");
	}

	# 記事数調整
	$data[0] = $top;
	while (<DAT>) {
		$i++;

		# 現行ログ
		if ($i < $max-1) {
			push(@data,$_);

		# 過去ログ
		} elsif ($pastkey) {
			push(@past,$_);
		}
	}

	# 記事No
	$no++;

	# 更新
	seek(DAT, 0, 0);
	print DAT "$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>\n";
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 過去ログ更新
	if (@past > 0) {
		require $pastmkpl;
		&past_make;
	}
}

#-------------------------------------------------
#  クッキー発行
#-------------------------------------------------
sub set_cookie {
	my @cook = @_;

	my @t = gmtime(time + 60*24*60*60);
	my @m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	my @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	my $gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	my $cook;
	foreach (@cook) {
		# タグ排除
		s/&gt;//g;
		s/&lt;//g;
		s/&quot;//g;
		s/&amp;//g;

		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: LIGHT_BOARD=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  メール送信
#-------------------------------------------------
sub mailto {
	# 記事の改行・タグを復元
	my $com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/＜/g;
	$com =~ s/&gt;/＞/g;
	$com =~ s/&quot;/”/g;
	$com =~ s/&amp;/＆/g;

	# メール本文を定義
	my $mbody = <<"EOM";
投稿日時：$date
ホスト名：$host
ブラウザ：$ENV{'HTTP_USER_AGENT'}

投稿者名：$in{'name'}
Ｅメール：$in{'email'}
ＵＲＬ  ：$in{'url'}
タイトル：$in{'sub'}

$com
EOM

	# 題名をBASE64化
	my $msub = &base64("[$title : $no] $in{'sub'}");

	# メールアドレスがない場合
	my $email;
	if ($in{'email'} eq "") { $email = $mail; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t -i") || &error("メール送信失敗");
	print MAIL "To: $mail\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";

	foreach ( split(/\n/, $mbody) ) {
		&jcode::convert(\$_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}

	close(MAIL);
}

#-------------------------------------------------
#  BASE64変換
#-------------------------------------------------
#	とほほのWWW入門で公開されているルーチンを参考にしました。
#	http://www.tohoho-web.com/
sub base64 {
	my ($sub) = @_;
	&jcode::convert(\$sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	my $ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	my ($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i = 0; $y = substr($x,$i,6); $i += 6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  完了メッセージ
#-------------------------------------------------
sub message {
	local($msg) = @_;

	&header;
	print <<EOM;
<blockquote>
<h3>$msg</h3>
<form action="$bbscgi">
<input type="submit" value="掲示板へ戻る">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  禁止ワードチェック
#-------------------------------------------------
sub no_wd {
	my $flg;
	foreach ( split(/\s+/, $no_wd) ) {
		if (index("$in{'name'} $in{'sub'} $in{'comment'}", $_) >= 0) {
			$flg = 1;
			last;
		}
	}
	if ($flg) { &error("禁止ワードが含まれています"); }
}

#-------------------------------------------------
#  日本語チェック
#-------------------------------------------------
sub jp_wd {
	if ($in{'comment'} !~ /[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC]/) {
		&error("コメントに日本語が含まれていません");
	}
}

#-------------------------------------------------
#  URL個数チェック
#-------------------------------------------------
sub urlnum {
	my $com = $in{'comment'};
	my $num = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("コメント中のURLアドレスは最大$urlnum個までです");
	}
}

#-------------------------------------------------
#  一時ファイル保存
#-------------------------------------------------
sub conf_log {
	# 前ログ
	open(TMP,"+< $tmplog") || &error("Open Error: $tmplog");
	eval "flock(TMP, 2);";
	my $data = <TMP>;

	# 二重投稿禁止
	my ($dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $data);
	if ($host eq $ho && $wait > $time - $tim) {
		close(TMP);
		&error("連続投稿はもうしばらく時間を置いてください");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		close(TMP);
		&error("二重投稿は禁止です");
	}

	# 書き換え
	seek(TMP, 0, 0);
	print TMP "$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>";
	truncate(TMP, tell(TMP));
	close(TMP);

	# 採番
	open(NO,"+< $tmpnum") || &error("Open Error: $tmpnum");
	eval "flock(NO, 2);";
	my $num = <NO> + 1;
	seek(NO, 0, 0);
	print NO $num;
	truncate(NO, tell(NO));
	close(NO);

	# ファイル生成
	open(TMP,"+> $tmpdir/$num.cgi");
	eval "flock(TMP, 2);";
	print TMP "$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>";
	close(TMP);
}


1;

