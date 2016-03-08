#┌─────────────────────────────────
#│ LIGHT BOARD
#│ pastmake.pl - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

#-------------------------------------------------
#  過去ログ生成
#-------------------------------------------------
sub past_make {
	# 過去ログファイル名を定義
	open(NO,"+< $pastno") || &error("Open Error: $pastno");
	eval "flock(NO, 2);";
	my $count = <NO>;
	$count = sprintf("%04d", $count);

	# 過去ログを開く
	my $i = 0;
	my ($flg, @data);
	open(LOG,"+< $pastdir/$count.cgi") || &error("Open Error: $count.cgi");
	eval "flock(LOG, 2);";
	while (<LOG>) {
		$i++;
		push(@data,$_);

		# 最大件数を超えると中断
		if ($i >= $pastmax) {
			$flg++;
			last;
		}
	}

	# 最大件数をオーバーすると次ファイルを自動生成
	if ($flg) {

		# 過去ログを一旦閉じる
		close(LOG);

		# カウントファイルをアップ
		$count = sprintf("%04d", $count+1);

		# カウントファイル更新
		seek(NO, 0, 0);
		print NO $count;
		truncate(NO, tell(NO));
		close(NO);

		# 新過去ログ
		open(LOG,"+> $pastdir/$count.cgi") || &error("Write Error: $count.cgi");
		eval "flock(LOG, 2);";
		print LOG @past;
		close(LOG);

		chmod(0666, "$pastdir/$count.cgi");

	# 現有過去ログのまま
	} else {

		unshift(@data,@past);
		seek(LOG, 0, 0);
		print LOG @data;
		truncate(LOG, tell(LOG));
		close(LOG);
	}
}


1;

