(function ($) {
    var hexToRGB = function (hex, alpha) {
        var r = parseInt(hex.slice(1, 3), 16),
            g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
        if (alpha) {
            return "rgba(" + r + ", " + g + ", " + b + ", " + alpha + ")";
        } else {
            return "rgb(" + r + ", " + g + ", " + b + ")";
        }
    }

    var initChartAjax = function (trackingViewDay) {
        var $this = $('#tracking-view-chart');
        var ctx = $this.get(0);
        themePrimaryColor = $(":root").css('--theme-primary-color');
        if (ctx != null) {
            $.ajax({
                url: dashboard_variables.ajax_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    action: 'dashboard_chart_ajax',
                    nonce: dashboard_variables.nonce,
                    tracking_view_day: trackingViewDay
                },
                success: function (response) {
                    setTimeout(() => {
                        ctx = ctx.getContext('2d');
                        window['gradient'] = ctx.createLinearGradient(0, 0, 0, 300);
                        window['gradient'].addColorStop(0, hexToRGB(themePrimaryColor, '0.33'));
                        window['gradient'].addColorStop(0.5, hexToRGB(themePrimaryColor, '0.15'));
                        window['gradient'].addColorStop(1, hexToRGB(themePrimaryColor, '0'));
                        var chartConfig = {
                            type: response.chart_type,
                            data: {
                                labels: response.chart_labels,
                                datasets: [{
                                    label: response.chart_label,
                                    data: response.chart_data,
                                    pointBackgroundColor: themePrimaryColor,
                                    pointBorderColor: '#fff',
                                    pointBorderWidth: 4,
                                    pointRadius: 6,
                                    backgroundColor: window['gradient'],
                                    borderColor: hexToRGB(themePrimaryColor, '1'),
                                    borderWidth: 2,
                                    fill: true,
                                    tension: 0.2,
                                }]
                            },
                            options: {
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                },
                                //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                                scaleBeginAtZero: true,
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
                                //Boolean - If there is a stroke on each bar
                                barShowStroke: false,
                                //Number - Pixel width of the bar stroke
                                barStrokeWidth: 2,
                                //Number - Spacing between each of the X value sets
                                barValueSpacing: 5,
                                //Number - Spacing between data sets within X values
                                barDatasetSpacing: 1,
                                legend: { display: false },
                                tooltips: {
                                    enabled: true,
                                    mode: 'x-axis',
                                    cornerRadius: 4
                                },
                            }
                        };
                        if (typeof (dashboardChart) !== 'undefined') {
                            dashboardChart.destroy();
                        }
                        // Create the chart
                        dashboardChart = new Chart(ctx, chartConfig);
                    }, 200);
                },
                error: function (error) {
                    console.log(error);
                },
            });
        }
    }

    var onChangeFilterDashboardChart = function () {
        var $this = $('#tracking-view-chart');
        if ($this.length <= 0) {
            return;
        }
        $('.tfcl-page-insight-filter .tfcl-page-insight-filter-button select[name="tracking_view_day"]').on('change', function (event) {
            event.preventDefault();
            var trackingViewDay = $('.tfcl-page-insight-filter .tfcl-page-insight-filter-button select[name="tracking_view_day"]').val();
            initChartAjax(trackingViewDay);
        });
    }

    $(document).ready(function ($) {
        initChartAjax();
        onChangeFilterDashboardChart();
    })
})(jQuery);