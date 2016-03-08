// JavaScript Document

//ストライプ（奇数行）
$(document).ready(function(){
    $('.information td:even').addClass('even');
});




//ページ内スムーススクロール
$(function(){
	$('a[href^=#]').click(function(){
		var speed = 500;
		var href= $(this).attr("href");
		var target = $(href == "#" || href == "" ? 'html' : href);
		var position = target.offset().top;
		$("html, body").animate({scrollTop:position}, speed, "swing");
		return false;
	});
});




//メニューバートップに固定
jQuery(function($) {

var nav    = $('#navi'),
    offset = nav.offset();

$(window).scroll(function () {
  if($(window).scrollTop() > offset.top - 1) {
    nav.addClass('fixed');
  } else {
    nav.removeClass('fixed');
  }
});

});
