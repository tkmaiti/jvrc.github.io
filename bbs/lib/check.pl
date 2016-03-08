#┌─────────────────────────────────
#│ LIGHT BOARD
#│ check.pl - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<ul>
EOM

	# ログチェック
	foreach ( $logfile, $setfile, $pwdfile, $tmpnum, $tmplog ) {
		if (-f $_) {
			print "<li>パス：$_ → OK\n";

			if (-r $_ && -w $_) {
				print "<li>パーミッション：$_ → OK\n";
			} else {
				print "<li>パーミッション：$_ → NG\n";
			}
		} else {
			print "<li>パス：$_ → NG\n";
		}
	}

	# ディレクトリ
	if (-d $tmpdir) {
		print "<li>ディレクトリパス：$tmpdir → OK\n";
		if (-r $tmpdir && -w $tmpdir && -x $tmpdir) {
			print "<li>ディレクトリパーミッション：$_ → OK\n";
		} else {
			print "<li>ディレクトリパーミッション：$_ → NG\n";
		}
	} else {
		print "<li>ディレクトリパス：$_ → NG\n";
	}

	# 過去ログ
	@yn = ('なし', 'あり');
	print "<li>過去ログ：$yn[$pastkey]\n";
	if ($pastkey) {
		if (-f $pastno) {
			print "<li>パス：$pastno → OK\n";
			if (-r $pastno && -w $pastno) {
				print "<li>パーミッション：$pastno → OK\n";
			} else {
				print "<li>パーミッション：$pastno → NG\n";
			}
		} else {
			print "<li>パス：$pastno → NG\n";
		}
		if (-d $pastdir) {
			print "<li>パス：$pastdir → OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<li>パーミッション：$pastdir → OK\n";
			} else {
				print "<li>パーミッション：$pastdir → NG\n";
			}
		} else {
			print "<li>パス：$pastdir → NG\n";
		}
	}
	print "</ul>\n</body></html>\n";
	exit;
}



1;

