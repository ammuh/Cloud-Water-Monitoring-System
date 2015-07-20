var menuMap = {
	"Dashboard": "Partials/dashboard_p.html",
	"Statistics": "Partials/statistics_p.html",
	"Sensors": "Partials/sensors_p.html",
	"Settings": "settings_p"
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
		$('.content-wrapper').html(data).promise().done(function(){
			d = "min-height: "+($(window).height() - ($('.main-footer').outerHeight()+$('.main-header').outerHeight()))+"px;";
		$('.content-wrapper').attr('style', d);
		sessionStorage.setItem("page", page);
		pageInit(page);
		});
		});
	
}

function pageInit(page) {
	switch(page){
		case "Dashboard":
			  
			break;
		case "Statistics":
			Chart.defaults.global.responsive = true;
			var data = {
					labels: ["January", "February", "March", "April", "May", "June", "July"],
					datasets: [
						{
							label: "My First dataset",
							fillColor: "rgba(220,220,220,0.2)",
							strokeColor: "rgba(220,220,220,1)",
							pointColor: "rgba(220,220,220,1)",
							pointStrokeColor: "#fff",
							pointHighlightFill: "#fff",
							pointHighlightStroke: "rgba(220,220,220,1)",
							data: [65, 59, 80, 81, 56, 55, 40]
						},
						{
							label: "My Second dataset",
							fillColor: "rgba(151,187,205,0.2)",
							strokeColor: "rgba(151,187,205,1)",
							pointColor: "rgba(151,187,205,1)",
							pointStrokeColor: "#fff",
							pointHighlightFill: "#fff",
							pointHighlightStroke: "rgba(151,187,205,1)",
							data: [28, 48, 40, 19, 86, 27, 90]
						}
					]
				};
			var ctx = $('#stat-master').get(0).getContext("2d");
			new Chart(ctx).Line(data, {bezierCurve: false});
			$('#daterange-btn').daterangepicker(
                {
                  ranges: {
                    'Today': [moment(), moment()],
                    'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
                    'Last 7 Days': [moment().subtract('days', 6), moment()],
                    'Last 30 Days': [moment().subtract('days', 29), moment()],
                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                    'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
                  },
                  startDate: moment().subtract('days', 29),
                  endDate: moment()
                },
			function (start, end) {
			  $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
			}
			);
			break;
		case "Sensors":
			  $(function () {
				$("#sensorst").dataTable({
                    "pageLength": 5,
                    "lengthChange": false,
                    "searching": false,
                    "language": {
                      "emptyTable": "You have no sensors in your profile."
                    }
                });
                $("#sensorsl").dataTable({
                    "data":{},
                    "language": {
                    "emptyTable": "Select a sensor to view the data."
                    }
                });
			  });
            $('#world-map').vectorMap();
			break;
		case "Settings":
			break;
		}
	}