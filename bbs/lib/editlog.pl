#┌─────────────────────────────────
#│ LIGHT BOARD
#│ edit.pl - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  記事修正
#-------------------------------------------------
sub editlog {
	# 入力チェック
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("記事No又はパスワードが入力されていません");
	}

	# 修正実行
	if ($in{'submit'}) {

		# チェック
		if ($no_wd) { &no_wd; }
		if ($jp_wd) { &jp_wd; }
		if ($urlnum > 0) { &urlnum; }

		# 未入力チェック
		if ($in{'name'} eq "") { &error("名前が入力されていません"); }
		if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
		if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
			&error("Ｅメールの入力内容が正しくありません");
		}
		if ($in{'url'} eq "http://") { $in{'url'} = ""; }
		if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }

		# 差し替え
		my ($flg, @data);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);

			if ($in{'no'} == $no) {

				# 認証チェック
				if ($pwd eq "" || &decrypt($in{'pwd'}, $pwd) != 1) {
					$flg = -1;
					last;
				}

				$flg = 1;
				$_ = "$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@data,$_);
		}

		if ($flg != 1) {
			close(DAT);
			&error("不正な処理です");
		}

		# 更新
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

		# 完了メッセージ
		&message("記事の修正を完了しました");
	}

	# 記事抽出
	my ($flg, @edit);
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		if ($in{'no'} == $no) {

			# パスワードなし
			if ($pwd eq "") {
				$flg = 2;
			}

			# パスワード一致
			if (&decrypt($in{'pwd'}, $pwd) == 1) {
				$flg = 1;
				@edit = ($no,$dat,$nam,$eml,$sub,$com,$url);

			# パスワード不一致
			} else {
				$flg = 3;
			}
			last;
		}
	}
	close(IN);

	if (!$flg) {
		close(DAT);
		&error("該当記事が見当たりません");
	} elsif ($flg == 2) {
		close(DAT);
		&error("この記事にはパスワードが設定されていません");
	} elsif ($flg == 3) {
		close(DAT);
		&error("パスワードが違います");
	}

	# 修正フォーム
	&edit_form(@edit);
}

#-------------------------------------------------
#  記事削除
#-------------------------------------------------
sub delelog {
	# 入力チェック
	if (!$post_flag) { &error("不正なアクセスです"); }
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("記事No又はパスワードが入力されていません");
	}

	# ログを読み込む
	my ($flg, @data);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		if ($in{'no'} == $no) {

			# パスワードなし
			if ($pwd eq "") {
				$flg = 2;
				last;
			}

			# パスワード一致
			if (&decrypt($in{'pwd'}, $pwd) == 1) {
				$flg = 1;
				next;

			# パスワード不一致
			} else {
				$flg = 3;
				last;
			}
		}
		push(@data,$_);
	}

	if (!$flg) {
		close(DAT);
		&error("該当記事が見当たりません");
	} elsif ($flg == 2) {
		close(DAT);
		&error("この記事にはパスワードが設定されていません");
	} elsif ($flg == 3) {
		close(DAT);
		&error("パスワードが違います");
	}

	# ログ更新
	seek(DAT, 0, 0);
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	# 完了メッセージ
	&message("記事は正常に削除されました");
}

#-------------------------------------------------
#  編集フォーム
#-------------------------------------------------
sub edit_form {
	my ($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	if (!$url) { $url = "http://"; }
	$com =~ s/<br>/\n/g;

	# 編集画面
	&header;
	print <<EOM;
[<a href="javascript:history.back()">前画面に戻る</a>]
<h3>編集フォーム</h3>
<ul>
<li>修正する部分のみ変更してください。
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="pwd" value="$in{'pwd'}">
投稿者名<br><input type="text" name="name" size="28" value="$nam"><br>
Ｅメール<br><input type="text" name="email" size="28" value="$eml"><br>
タイトル<br><input type="text" name="sub" size="36" value="$sub"><br>
参照先<br><input type="text" name="url" size="45" value="$url"><br>
コメント<br><textarea name="comment" cols="58" rows="7">$com</textarea><br>
<input type="submit" name="submit" value="送信する">
</form>
</ul>
</body>
</html>
EOM
	exit;
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


1;

