// Define chart objects globally
let taskDistribution, weeklyProgress, productivityHours;

// Fetch Task Distribution Data and Initialize Chart
$.get('/api/task-distribution', function (response) {
    const taskDistributionOptions = {
        series: response.distribution, // Use API-provided data
        chart: {
            type: 'donut',
            height: 250
        },
        labels: ['Personal', 'Work', 'Health', 'Learning'], // Ensure API returns matching labels
        colors: ['#4361ee', '#f44336', '#4CAF50', '#ff9800'],
        plotOptions: {
            pie: {
                donut: {
                    size: '70%'
                }
            }
        },
        legend: {
            position: 'bottom'
        },
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    };

    taskDistribution = new ApexCharts(
        document.querySelector("#task-distribution"),
        taskDistributionOptions
    );
    taskDistribution.render();
});

// Fetch Weekly Progress Data and Initialize Chart
$.get('/api/weekly-progress', function (response) {
    const weeklyProgressOptions = {
        series: [{
            name: 'Tasks Completed',
            data: response.data // Use API-provided data
        }],
        chart: {
            type: 'area',
            height: 250,
            toolbar: {
                show: false
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        xaxis: {
            categories: response.categories // Use API-provided categories
        },
        colors: ['#4361ee'],
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.9,
                stops: [0, 90, 100]
            }
        }
    };

    weeklyProgress = new ApexCharts(
        document.querySelector("#weekly-progress"),
        weeklyProgressOptions
    );
    weeklyProgress.render();
});

// Fetch Productivity Hours Data and Initialize Chart
$.get('/api/productivity-hours', function (response) {
    const productivityHoursOptions = {
        series: [{
            name: 'Tasks',
            data: response.data // Use API-provided data
        }],
        chart: {
            height: 250,
            type: 'bar',
            toolbar: {
                show: false
            }
        },
        plotOptions: {
            bar: {
                borderRadius: 5,
                columnWidth: '50%',
            }
        },
        colors: ['#4361ee'],
        xaxis: {
            categories: response.categories, // Use API-provided categories
            labels: {
                rotate: -45
            }
        }
    };

    productivityHours = new ApexCharts(
        document.querySelector("#productivity-hours"),
        productivityHoursOptions
    );
    productivityHours.render();
});

// Define the Rerender Function
window.rerender = function () {
    $.get("/api/task-distribution", function (response) {
        taskDistribution.updateSeries(response.distribution);
    });

    $.get("/api/weekly-progress", function (response) {
        weeklyProgress.updateSeries([{
            name: 'Tasks Completed',
            data: response.data
        }]);
        weeklyProgress.updateOptions({
            xaxis: {
                categories: response.categories
            }
        });
    });

    $.get("/api/productivity-hours", function (response) {
        productivityHours.updateSeries([{
            name: 'Tasks',
            data: response.data
        }]);
        productivityHours.updateOptions({
            xaxis: {
                categories: response.categories
            }
        });
    });
};
