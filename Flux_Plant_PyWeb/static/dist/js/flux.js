var menuMap = {
	"Dashboard":"AjaxPartials/Partials/dashboard_p.html",
	"Statistics":"AjaxPartials/Partials/statistics_p.html",
	"Sensors":"AjaxPartials/Partials/sensors_p.html",
	"Settings":"settings_p"
	};
$(document).ready(function(e) {
	var i = sessionStorage.getItem("page");
    if (i == null) {
		sessionStorage.setItem("page", "Dashboard");
	}
	loadPage(sessionStorage.getItem("page"));
});

function loadPage(page) {
	console.log("Entered Load Page Function");
	console.log(page);
	c = $('.content-wrapper').attr('style');
	z = $('.content-wrapper fa fa-refresh fa-spin fa-5x');
	console.log(c);
	console.log(z);
	if (c === undefined || c == null || c === false) {
		console.log("EnteredIf Block");
		$('.content-wrapper').empty();
		h = $(window).height();
		prp = "padding:"+h/2+"px; text-align:center;";
		$('.content-wrapper').attr('style', prp);
		$('.content-wrapper').html('<i class="fa fa-refresh fa-spin fa-5x"></i>');
	}
	else {
		$('.content-wrapper').empty();
		h = $(window).height();
		prp = "padding:"+h/3+"px; text-align:center;";
		$('.content-wrapper').attr('style', c+prp);
		$('.content-wrapper').html('<i class="fa fa-refresh fa-spin fa-5x"></i>');
	}
	$.get(menuMap[page], function(data) {
		$('.content-wrapper').empty();
		$('.content-wrapper').html(data);
		d = "min-height: "+($(window).height() - ($('.main-footer').outerHeight()+$('.main-header').outerHeight()))+"px;";
		$('.content-wrapper').attr('style', d);
		sessionStorage.setItem("page", page);
		});
	pageInit(page);
}

function pageInit(page) {
	case "Dashboard":
		break;
	case "Statistics":
		break;
	case "Sensors":
		break;
	case "Settings":
		break;
	}