var get_data_and_make_stats_plot = function (chart_parent) {
	args = parse_input();

	return fetch('/stats' + args , { method: 'GET' })
			.then(function (response) { return response.json(); })
			.then(function (full_data) {
				var data = {
					name: 'title',
					x: [],
					y: [],
					text: [],
					type: 'bar',
					marker: {
						color: '#343a40',
						line: {
							color: '#0069d9',
							width: 2.0
						}
					}
				};
				var i;
				var category = get_radio_value("category");
				for (i = 0; i < full_data.length; i++) {
					data.x.push(full_data[i].title);
					if (category == "total") {
						data.y.push(full_data[i].total);
						data.text.push(int_seconds_to_timestamp(full_data[i].total));
					}
					if (category == "times") {
						data.y.push(full_data[i].times);
					}
					if (category == "average") {
						data.y.push(full_data[i].average);
						data.text.push(int_seconds_to_timestamp(full_data[i].average));
					}
					if (category == "median") {
						data.y.push(full_data[i].median);
						data.text.push(int_seconds_to_timestamp(full_data[i].median));
					}
				}
				return plot_data(data, chart_parent);
			}).catch(function (error) { return console.log(error); });
};

var get_data_and_make_schedules_plot = function (chart_parent) {
	args = parse_input();
	day_names = ['Monday','Tuesday', 'Wednesday',
		'Thursday', 'Friday', 'Saturday', 'Sunday'];

	return fetch('/schedule' + args , { method: 'GET' })
			.then(function (response) { return response.json(); })
			.then(function (full_data) {
				var data = {
					name: 'title',
					x: [],
					y: [],
					z: [],
					type: 'heatmap',
					colorscale: [[0, '#343a40'], [1, '#0069d9']]
				};
				var i;
				data.x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23];
				for (i = 6; i >= 0; i--) {
					data.y.push(day_names[i]);
					var j;
					var day_data = [];
					for (j = 0; j < 24; j++) {
							day_data.push(full_data[i][j]);
					}
					data.z.push(day_data);
				}
				return plot_data(data, chart);
			}).catch(function (error) { return console.log(error); });
};

var plot_data = function (data, parent_element) {
	var text = [];
	var vals = [];
	var i;
	for (i=0; i<1200; i++) {
		var days = Math.floor(i / 24);
		var hours = i - days * 24;
		text.push(days + "d, " + hours + "hrs");
		vals.push(i * 3600);
	}
	var layout = {
		autosize: false,
		xaxis: {
			color: '#0069d9',
		},
		yaxis: {
			ticktext: text,
			tickvals: vals,
			tickmode: 'array',
			automargin: true,
			color: '#0069d9',
			font: { size:30 },
		},
		paper_bgcolor: '#343a40',
		plot_bgcolor: '#343a40'
	};
	Plotly.newPlot(parent_element, [data], layout);
};

var update_form_visibility = function (chart_selection) {
	if (chart_selection == 'bar') {
		document.getElementById('sys_group').style.display = "initial";
		document.getElementById('sysex_group').style.display = "initial";
		document.getElementById('skip_group').style.display = "initial";
		document.getElementById('lkbk_group').style.display = "initial";
		document.getElementById('num_entries_group').style.display = "initial";
		document.getElementById('category_group').style.display = "initial";
	} else if (chart_selection == 'sched') {
		document.getElementById('sys_group').style.display = "initial";
		document.getElementById('sysex_group').style.display = "initial";
		document.getElementById('skip_group').style.display = "initial";
		document.getElementById('lkbk_group').style.display = "initial";
		document.getElementById('num_entries_group').style.display = "none";
		document.getElementById('category_group').style.display = "none";
	}
};

var register_chart_listener = function () {
	var radios = document.getElementsByName("chart_selection");
	for (var i = 0; i < radios.length; i++) {
			radios[i].addEventListener('change', function() {
					var radio_value = this.value;
					update_form_visibility(radio_value);
			});
	}
};

var parse_input = function() {
	var args = ""
	var category = get_radio_value("category");
	args += '?criteria=' + category;

	var systems = document.getElementById("sys").value
	if (systems != '')
		args += '&systems=' + systems;

	var exclude_systems = document.getElementById("sysex").value
	if (exclude_systems != '')
		args += '&exclude_systems=' + exclude_systems;

	var skip_shorter_than = document.getElementById("skip").value
	if (skip_shorter_than != '')
		args += '&skip_shorter_than=' + skip_shorter_than;

	var lookback = document.getElementById("lkbk").value
	if (lookback != '')
		args += '&lookback=' + lookback;

	var num_entries = document.getElementById("num_entries").value
	if (num_entries != '')
		args += '&num_entries=' + num_entries;
	return args;
};

var get_radio_value = function (radio_name) {
	var radios = document.getElementsByName(radio_name);

	for (var i = 0, length = radios.length; i < length; i++) {
		if (radios[i].checked) {
			return radios[i].value;
		}
	}
};

var int_seconds_to_timestamp = function (seconds) {
	var days = Math.floor(seconds / 86400);
	seconds -= days * 86400;
	var hours = Math.floor(seconds / 3600);
	seconds -= hours * 3600;
	var minutes = Math.floor(seconds / 60);
	seconds -= minutes * 60;
	seconds = Math.floor(seconds);
	result = "";
	if (days > 0) result += days + "d ";
	if (hours < 10) result += "0";
	result += hours + ":";
	if (minutes < 10) result += "0";
	result += minutes + ":";
	if (seconds < 10) result += "0";
	result += seconds;
	return result;
};

var on_update = function(chart_parent) {
	var chart = document.getElementById('chart')
	var chart_type = get_radio_value('chart_selection');
	if (chart_type == "bar") {
		get_data_and_make_stats_plot(chart);
		return;
	}
	if (chart_type == "sched") {
		get_data_and_make_schedules_plot(chart);
		return;
	}
	if (chart_type == "history") {
		get_data_and_make_history_plot();
		return;
	}
};
