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


$(document).ready(function () {
    // Initialize datetime picker
    $('.datetimepicker').datetimepicker({
        format: 'd-m-Y H:i',
        step: 30,
        mask: true
    });

    // Initialize DataTables with server-side processing
    $('#taskTable').DataTable({
        processing: true,
        serverSide: true,
        responsive: true,
        ajax: {
            url: '/tasks', // The URL to fetch data
            type: 'GET',
            data: function (d) {
                // Optional: you can add filters here if needed, e.g.:
                // d.category = $('#filterCategory').val();
            }
        },
        columns: [
            { data: 'id', title: 'ID', visible: false },
            { data: 'sl_no', title: 'S.No', orderable: false },
            { data: 'name', title: 'Task', orderable: false },
            {
                data: 'category',
                title: 'Category',
                orderable: false,
                render: function (data, type, row) {
                    if (row.priority === 'High') {
                        return `<span class="badge bg-danger">${data} (${row.priority})</span>`;
                    } else if (row.priority === 'Medium') {
                        return `<span class="badge bg-warning text-black">${data} (${row.priority})</span>`;
                    }
                    return `<span class="badge bg-primary">${data} (${row.priority})</span>`;
                }
            },
            { data: 'due_date', title: 'Due Date', orderable: false },
            {
                data: 'id',
                title: 'Actions',
                orderable: false,
                render: function (data, type, row) {
                    if (row.is_completed) {
                        return `<button class="btn btn-sm btn-danger delete-task" data-task-id="${data}" title="Delete task"><i class="fa fa-trash"></i></button>`;
                    }
                    return `
                        <div class="d-flex gap-2" role="group">
                            <button class="btn btn-sm btn-primary complete-task" data-task-id="${data}" title="Mark as complete"><i class="fa fa-check"></i></button>
                            <button class="btn btn-sm btn-danger delete-task" data-task-id="${data}" title="Delete task"><i class="fa fa-trash"></i></button>
                        </div>
                    `;
                }
            },
        ],
        rowCallback: function (row, data) {
            if (data.is_completed) {
                $(row).addClass('table-success');
            } else if (new Date(data.due_date) < new Date()) {
                $(row).addClass('table-danger');
            } else if (data.priority === 'high') {
                $(row).addClass('table-danger');
            } else if (data.priority === 'medium') {
                $(row).addClass('table-warning');
            } else {
                $(row).addClass('table-light');
            }
        }
    });

    // Handle form submission to add a new task
    $("#addTaskForm").submit(function (event) {
        event.preventDefault();
        $form = $(this);
        var formData = {
            name: $("#taskName").val(),
            priority: $("#taskPriority").val(),
            category: $("#taskCategory").val(),
            due_date: $("#dueDate").val()
        };

        $.ajax({
            url: '/add',
            type: 'POST',
            data: formData,
            beforeSend: function () {
                $("#taskFeedback").html('');
                $form.find('button').prop('disabled', true);
            },
            success: function (response) {
                $("#taskName").val('');
                $("#taskPriority").val('low');
                $("#taskCategory").val('personal');
                $("#dueDate").val('');
                toastr.success(response.message);
                // Reload DataTable to reflect the new task
                $('#taskTable').DataTable().draw(false)
                rerender();
            },
            error: function (xhr, status, error) {
                var errorMsg = xhr.responseJSON ? xhr.responseJSON.error : "An error occurred.";
                toastr.error(errorMsg);
            },
            complete: function () {
                $form.find('button').prop('disabled', false);
            }
        });
    });

    // Handle task completion
    $(document).on('click', '.complete-task', function (event) {
        var taskId = $(this).data('task-id');
        $.ajax({
            url: '/complete/' + taskId,
            type: 'POST',
            success: function (response) {
                toastr.success('Task completed successfully');
                rerender();
                $('#taskTable').DataTable().draw(false)
            },
            error: function (xhr, status, error) {
                toastr.error('Error completing task');
            }
        });
    });

    $(document).on('click', '.delete-task', function (event) {
        var taskId = $(this).data('task-id');
        $.ajax({
            url: '/delete/' + taskId,
            type: 'POST',
            success: function (response) {
                toastr.success('Task deleted successfully');
                rerender();
                $('#taskTable').DataTable().draw(false)
            },
            error: function (xhr, status, error) {
                toastr.error('Error deleting task');
            }
        });
    });
});
