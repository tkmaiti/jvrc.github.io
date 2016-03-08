#┌─────────────────────────────────
#│ LIGHT BOARD v7.0
#│ init.cgi - 2009/01/17
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'LIGHT BOARD v7.0';
#┌─────────────────────────────────
#│[ 注意事項 ]
#│ 1.このスクリプトはフリーソフトです。このスクリプトを使用した
#│   いかなる損害に対して作者はその責任を一切負いません。
#│ 2.設置に関する質問はサポート掲示板にお願いいたします。メールに
#│   よる質問にはお答えできません。
#└─────────────────────────────────

#===========================================================
#  ▼設定項目
#===========================================================

# 外部ファイル【サーバパス】
$jcode    = 'jcode.pl';
$regkeypl = './lib/registkey.pl';
$registpl = './lib/regist.pl';
$editpl   = './lib/editlog.pl';
$searchpl = './lib/search.pl';
$pastpl   = './lib/pastlog.pl';
$checkpl  = './lib/check.pl';
$pastmkpl = './lib/pastmake.pl';

# 本体ファイルCGI【URLパス】
$bbscgi = './light.cgi';

# 管理ファイルCGI【URLパス】
$admincgi = './admin.cgi';

# ログファイル【サーバパス】
$logfile = './data/data.cgi';

# 設定ファイル【サーバパス】
$setfile = './data/light.dat';

# パスワードファイル【サーバパス】
$pwdfile = './data/pwd.cgi';

# sendmailパス（メール通知する場合）
# → 例 /usr/lib/sendmail
$sendmail = '/usr/sbin/sendmail';

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 1;

# １回当りの最大投稿サイズ (bytes)
$maxData = 51200;

# ログを確認後表示させる（0=no 1=yes）
# → 投稿されたログを管理者が表示前に確認する場合（スパム＆イタズラ対策）
$conf_log = 0;

# 一時ログディレクトリ【サーバパス】
$tmpdir = './tmp';

# 一時ログNOファイル【サーバパス】
$tmpnum = './data/tmpnum.dat';

# 一時ログ用前ログファイル【サーバパス】
$tmplog = './data/tmplog.cgi';

## --- <以下は「投稿キー」機能（スパム対策）を使用する場合の設定です> --- ##
#
# 投稿キーの使用（スパム対策）
# → 0=no 1=yes
$regist_key = 1;

# 投稿キー画像生成ファイル【URLパス】
$registkeycgi = './registkey.cgi';

# 投稿キー暗号用パスワード（英数字で８文字）
$pcp_passwd = 'pass7777';

# 投稿キー許容時間（分単位）
#   投稿フォームを表示させてから、実際に送信ボタンが押される
#   までの可能時間を分単位で指定
$pcp_time = 30;

# 投稿キー画像の大きさ（10ポ or 12ポ）
# 10pt → 10
# 12pt → 12
$regkey_pt = 10;

# 投稿キー画像の文字色
# → $textと合わせると違和感がない。目立たせる場合は #dd0000 など。
$moji_col = '#dd0000';

# 投稿キー画像の背景色
# → $bgcolorと合わせると違和感がない
$back_col = '#f0f0f0';

#---(以下は「過去ログ」機能を使用する場合の設定です)---#
#
# 過去ログ機能 (0=no 1=yes)
$pastkey = 0;

# 過去ログディレクトリ【サーバパス】
$pastdir = './past';

# 過去ログカウントファイル【サーバパス】
$pastno = './data/pastno.dat';

# 過去ログ１ファイル当りの最大件数
$pastmax = 400;

#===========================================================
#  ▲設定完了
#===========================================================

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub decode {
	my $buf;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag = 1;
		if ($ENV{'CONTENT_LENGTH'} > $maxData) {
			&error("投稿量が大きすぎます");
		}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag = 0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in);
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JISコード変換
		&jcode::convert(\$val, "sjis", "", "z");

		# エスケープ
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$mode = $in{'mode'};
	$headflag = 0;
	$ENV{'TZ'} = "JST-9";
}

#-------------------------------------------------
#  設定ファイル認識
#-------------------------------------------------
sub setfile {
	# 設定ファイル読み込み
	open(IN,"$setfile") || &error("Open Error: $setfile");
	my $file = <IN>;
	close(IN);

	# 設定内容認識
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait,$no_wd,$jp_wd,$urlnum) = split(/<>/, $file);

	# IP&ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	# アクセス拒否
	if ($deny) {
		local($flag);
		foreach ( split(/\s+/, $deny) ) {
			s/\./\\\./g;
			s/\*/\.*/g;
			if ($host =~ /$_/i) { $flag = 1; last; }
		}
		if ($flag) { &error("ただ今ご利用できません"); }
	}
	$b_size .= "px";
}

#-------------------------------------------------
#  HTMLヘッダ
#-------------------------------------------------
sub header {
	if ($headflag) { return; }

	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th {
	font-size: $b_size;
	font-family: "MS UI Gothic","ＭＳ Ｐゴシック",Osaka;
}
.num { font-family:Verdana,Helvetica,Arial; }
.l { background-color: #666666; color: #ffffff; }
.r { background-color: #ffffff; color: #000000; }
-->
</style>
<title>$title</title></head>
EOM

	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	}
	$headflag = 1;
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	&header;
	print <<"EOM";
<div align="center">
<hr width="400">
<h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<p>
<form>
<input type="button" value="前画面に戻る" onclick="history.back()">
</form>
<p>
<hr width="400">
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  パスワード暗号
#-------------------------------------------------
sub encrypt {
	my $inp = shift;

	# 候補文字列を定義
	my @char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# 乱数で種を抽出
	srand;
	my $salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# 暗号化
	crypt($inp, $salt) || crypt ($inp, '$1$' . $salt);
}

#-------------------------------------------------
#  パスワード照合
#-------------------------------------------------
sub decrypt {
	my ($inp, $log) = @_;

	# 種抽出
	my $salt = $log =~ /^\$1\$(.*)\$/ && $1 || substr($log, 0, 2);

	# 照合
	if (crypt($inp, $salt) eq $log || crypt($inp, '$1$' . $salt) eq $log) {
		return 1;
	} else {
		return 0;
	}
}


1;

