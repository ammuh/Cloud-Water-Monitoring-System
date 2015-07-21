var menuMap = {
    "Dashboard": "../Partials/dashboard_p.html",
    "Sensors": "../Partials/sensors_p.html",
    "Settings": "../Partials/settings_p.html",
    "Water": "../Partials/dash_water_p.html",
    "Cost": "../Partials/dash_cost_p.html",
    "Carbon Emissions": "../Partials/dash_ce_p.html"
};
$(document).ready(function(e) {
    var i = sessionStorage.getItem("page");
    if (i == null) {
        sessionStorage.setItem("page", "Dashboard");
    }
    loadPage(sessionStorage.getItem("page"));
});

function loadPage(page) {
    console.log(page);
    c = $('.content-wrapper').attr('style');
    z = $('.content-wrapper fa fa-refresh fa-spin fa-5x');
    console.log(c);
    console.log(z);
    if (c === undefined || c == null || c === false) {
        $('.content-wrapper').empty();
        h = $(window).height();
        prp = "padding:" + h / 2 + "px; text-align:center;";
        $('.content-wrapper').attr('style', prp);
        $('.content-wrapper').html('<i class="fa fa-refresh fa-spin fa-5x"></i>');
    } else {
        $('.content-wrapper').empty();
        h = $(window).height();
        prp = "padding:" + h / 3 + "px; text-align:center;";
        $('.content-wrapper').attr('style', c + prp);
        $('.content-wrapper').html('<i class="fa fa-refresh fa-spin fa-5x"></i>');
    }
    $.get(menuMap[page], function(data) {
        $('.content-wrapper').empty();
        $('.content-wrapper').html(data).promise().done(function() {
            d = "min-height: " + ($(window).height() - ($('.main-footer').outerHeight() + $('.main-header').outerHeight())) + "px;";
            $('.content-wrapper').attr('style', d);
            sessionStorage.setItem("page", page);
            pageInit(page);
        });
    });

}

function pageInit(page) {
    switch (page) {
        case "Dashboard":
            h = $('.box-body.dailyReport').height();
            $('.box-body.dailyReport').empty();
            prp = "padding:" + h / 2 + "px; text-align:center;";
            $('.box-body.dailyReport').attr('style', prp);
            $('.box-body.dailyReport').html('<i class="fa fa-refresh fa-spin fa-3x"></i>');
            $.get(menuMap[$('.nav.dailyReport > li.active > a').html()], function(data) {
                $('.box-body.dailyReport').attr('style', '');
                $('.box-body.dailyReport').html(data).promise().done(function() {});
            });
            $('.nav.dailyReport > li').click(function() {
                console.log($(this));
                h = $('.box-body.dailyReport').height();
                $('.box-body.dailyReport').empty();
                prp = "padding:" + h / 2 + "px; text-align:center;";
                $('.box-body.dailyReport').attr('style', prp);
                $('.box-body.dailyReport').html('<i class="fa fa-refresh fa-spin fa-3x"></i>');
                $.get(menuMap[$(this).children('a').html()], function(data) {
                    $('.box-body.dailyReport').empty();
                    $('.box-body.dailyReport').attr('style', '');
                    $('.box-body.dailyReport').html(data).promise().done(function() {});
                });
            });
             var areaChartCanvas = $("#stat-master").get(0).getContext("2d");
        // This will get the first returned node in the jQuery collection.
        var areaChart = new Chart(areaChartCanvas);

        var areaChartData = {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
            {
              label: "Electronics",
              fillColor: "rgba(210, 214, 222, 1)",
              strokeColor: "rgba(210, 214, 222, 1)",
              pointColor: "rgba(210, 214, 222, 1)",
              pointStrokeColor: "#c1c7d1",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
              label: "Digital Goods",
              fillColor: "rgba(60,141,188,0.9)",
              strokeColor: "rgba(60,141,188,0.8)",
              pointColor: "#3b8bba",
              pointStrokeColor: "rgba(60,141,188,1)",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(60,141,188,1)",
              data: [28, 48, 40, 19, 86, 27, 90]
            }
          ]
        };

        var areaChartOptions = {
          //Boolean - If we should show the scale at all
          showScale: true,
          //Boolean - Whether grid lines are shown across the chart
          scaleShowGridLines: false,
          //String - Colour of the grid lines
          scaleGridLineColor: "rgba(0,0,0,.05)",
          //Number - Width of the grid lines
          scaleGridLineWidth: 1,
          //Boolean - Whether to show horizontal lines (except X axis)
          scaleShowHorizontalLines: true,
          //Boolean - Whether to show vertical lines (except Y axis)
          scaleShowVerticalLines: true,
          //Boolean - Whether the line is curved between points
          bezierCurve: true,
          //Number - Tension of the bezier curve between points
          bezierCurveTension: 0.3,
          //Boolean - Whether to show a dot for each point
          pointDot: false,
          //Number - Radius of each point dot in pixels
          pointDotRadius: 4,
          //Number - Pixel width of point dot stroke
          pointDotStrokeWidth: 1,
          //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
          pointHitDetectionRadius: 20,
          //Boolean - Whether to show a stroke for datasets
          datasetStroke: true,
          //Number - Pixel width of dataset stroke
          datasetStrokeWidth: 2,
          //Boolean - Whether to fill the dataset with a color
          datasetFill: true,
          //String - A legend template
          legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
          //Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
          maintainAspectRatio: false,
          //Boolean - whether to make the chart responsive to window resizing
          responsive: true
        };

        //Create the line chart
        areaChart.Line(areaChartData, areaChartOptions);
        $('#button1').click(function(){
            areaChartData = {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
            {
              label: "Electronics",
              fillColor: "rgba(210, 214, 222, 1)",
              strokeColor: "rgba(210, 214, 222, 1)",
              pointColor: "rgba(210, 214, 222, 1)",
              pointStrokeColor: "#c1c7d1",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
              label: "Digital Goods",
              fillColor: "rgba(60,141,188,0.9)",
              strokeColor: "rgba(60,141,188,0.8)",
              pointColor: "#3b8bba",
              pointStrokeColor: "rgba(60,141,188,1)",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(60,141,188,1)",
              data: [28, 48, 40, 19, 86, 27, 90]
            }
            
          ]
        };
        areaChart.Line(areaChartData, areaChartOptions);
        });
        $('#button2').click(function(){
            areaChartData = {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
            {
              label: "Electronics",
              fillColor: "rgba(210, 214, 222, 1)",
              strokeColor: "rgba(210, 214, 222, 1)",
              pointColor: "rgba(210, 214, 222, 1)",
              pointStrokeColor: "#c1c7d1",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: [52, 552, 25, 245, 78, 70, 40]
            },
            {
              label: "Digital Goods",
              fillColor: "rgba(60,141,188,0.9)",
              strokeColor: "rgba(60,141,188,0.8)",
              pointColor: "#3b8bba",
              pointStrokeColor: "rgba(60,141,188,1)",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(60,141,188,1)",
              data: [124, 453, 353, 24, 324, 23, 124]
            }
            
          ]
        };
        areaChart.Line(areaChartData, areaChartOptions);
        });
        $('#button3').click(function() {
            areaChartData = {
          labels: ["January", "February", "March", "April", "May", "June", "July"],
          datasets: [
            {
              label: "Electronics",
              fillColor: "rgba(210, 214, 222, 1)",
              strokeColor: "rgba(210, 214, 222, 1)",
              pointColor: "rgba(210, 214, 222, 1)",
              pointStrokeColor: "#c1c7d1",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: [1459, 23, 812, 246, 55, 434]
            },
            {
              label: "Digital Goods",
              fillColor: "rgba(60,141,188,0.9)",
              strokeColor: "rgba(60,141,188,0.8)",
              pointColor: "#3b8bba",
              pointStrokeColor: "rgba(60,141,188,1)",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(60,141,188,1)",
              data: [434, 23, 50, 19, 236, 27, 90]
            }
          ]
            }
          areaChart.Line(areaChartData, areaChartOptions);
        });
            $('#daterange-btn').daterangepicker({
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
                function(start, end) {
                    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                }
            );
            $("#powerplant").auderoSmokeEffect({
                imagePath: "dist/img/smoke.png",
                posX: 0,
                posY: 0
            });
            $("#powerplant").auderoSmokeEffect('toggle');
            $.get("/fp/user/data", function(data){
                console.log(data);
            });
            break;
        case "Sensors":
            $(function() {
                $("#sensorst").dataTable({
                    "pageLength": 5,
                    "lengthChange": false,
                    "searching": false,
                    "language": {
                        "emptyTable": "You have no sensors in your profile."
                    }
                });
                $("#sensorsl").dataTable({
                    "data": {},
                    "language": {
                        "emptyTable": "Select a sensor to view the data."
                    }
                });
            });
            $('#world-map').vectorMap();
            $('#daterange-btn').daterangepicker({
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
                function(start, end) {
                    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                }
            );
            var gdata = null;
            if (gdata != null) {
                Chart.defaults.global.responsive = true;
                var ctx = $('#stat-master').get(0).getContext("2d");
                new Chart(ctx).Line(data, {
                    bezierCurve: false
                });
            } else {
                $('.graph-container').empty();
                $('.graph-container').html("<p>Select a sensor above to view data</p>");
            }
            $.get( "/fp/user/sensors/form", function( data ) {
                console.log(data.locations);
                for (var i in data.locations){
                    var c1 = '<option>'+data.locations[i]+'</option>';
                    var c2 = '<option>' + data.locations[i] + '</option>';
                    $('.loc-container-1').append(c1);
                    $('.loc-container-2').append(c2);
                }
            });
            $('#bt1').click(function(){
                console.log($('#sensId').val());
                db = { 'id': $('#sensId').val()};
                $.ajax({
                  type: "POST",
                  url: "/fp/user/sensors/form",
                  data: db,
                  success: function(data){
                    console.log
                  },
                  contentType: "application/json"
                });               
            });
            break;
        case "Settings":
            break;
    }
}