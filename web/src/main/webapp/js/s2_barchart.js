function loadOneColumn() {
	var myChart = echarts.init(document.getElementById('BarChartforS2'));
	var data1 = [ 2, 3, 1, 1, 0, 1, 2, 2, 1, 1 ];
	var data2 = [ 0, 1, 1, 1, 2, 1, 3, 1, 1, 2 ];
	var data3 = [ 3, 2, 1, 1, 6, 1, 1, 1, 1, 1 ];

	var path1 = "data/s2/positive.json";
	$.ajax({
		type : 'get',
		url : path1,
		dataType : "json",
		success : function(result) {
			data1 = result.data;
			console.log(data1);
		},
		error : function(errorMsg) {
			alert("failure of loading data!");
		}
	});

	var path2 = "data/s2/negative.json";
	$.ajax({
		type : 'get',
		url : path2,
		dataType : "json",
		success : function(result) {
			data2 = result.data;
		},
		error : function(errorMsg) {
			alert("failure of loading data!");
		}
	});

	var path3 = "data/s2/neutral.json";
	$.ajax({
		type : 'get',
		url : path3,
		dataType : "json",
		success : function(result) {
			data3 = result.data;
		},
		error : function(errorMsg) {
			alert("failure of loading data!");
		}
	});

	myChart.setOption({
		title : {
			text : 'Melbourne',
			subtext : '',
			x : '300'
		},tooltip : {
			trigger : 'axis',
			axisPointer : { // 坐标轴指示器，坐标轴触发有效
				type : 'shadow' // 默认为直线，可选为：'line' | 'shadow'
			}
		},
		legend : {
			data : [ 'positive', 'negative', 'neutral' ]
		},
		grid : {
			left : '3%',
			right : '4%',
			bottom : '3%',
			containLabel : true
		},
		xAxis : {
			type : 'value'
		},
		yAxis : {
			type : 'category',
			data : [ 'docklands', 'carlton', 'carlton north', 'east melbourne',
					'melbourne', 'north melbourne', 'south melbourne',
					'south yarra', 'southbank', 'west melbourne' ]
		},
		series : [ {
			name : 'positive',
			type : 'bar',
			stack : '总量',
			label : {
				normal : {
					show : true,
					position : 'insideRight'
				}
			},
			data : data1
		}, {
			name : 'negative',
			type : 'bar',
			stack : '总量',
			label : {
				normal : {
					show : true,
					position : 'insideRight'
				}
			},
			data : data2
		}, {
			name : 'neutral',
			type : 'bar',
			stack : '总量',
			label : {
				normal : {
					show : true,
					position : 'insideRight'
				}
			},
			data : data3
		} ]
	});
};

loadOneColumn();
