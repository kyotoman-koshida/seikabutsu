
$('.slider').slick({
    centerMode: true,
    centerPadding: '50px',
    autoplay:true,
    autoplaySpeed:5000,
    dots:true,
    arrows:true,
    
});

$(function(){
    $("nav").hide();
    $(".menubtn").click(function(){//メニューボタンをクリックしたとき
        $("nav").toggle(300);//0.3秒で表示したり非表示にしたりする
    });
});
