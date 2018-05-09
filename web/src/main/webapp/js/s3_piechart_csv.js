function loadOneColumn() {
	var myChart = echarts.init(document.getElementById('PieChartforCrimeCSV'));

	var info = [];

	myChart.setOption({
		title : {
			text : 'Correlation between Location of Crime-related Tweets & Real Crime',
			subtext : 'Twitter',
			x : 'center'
		},
		tooltip : {
			trigger : 'item'
		},
		legend : {
			x : 'center',
			bottom : 10,
			data : []
		},
		series : [ {
			name : 'crime number',
			type : 'pie',
			radius : '65%',
			center : [ '50%', '50%' ],
			data : [],
			itemStyle : {
				emphasis : {
					shadowBlur : 10,
					shadowOffsetX : 0,
					shadowColor : 'rgba(0, 0, 0, 0.5)'
				}
			}
		} ]
	});

	myChart.showLoading();
	var names = [];
	var brower = [];
	$.ajax({
		type : 'get',
		url : 'data/s3/tweeter/piechart.json',
		dataType : "json",
		success : function(result) {
			$.each(result.list, function(index, item) {
				names.push(item.department);
				brower.push({
					name : item.department,
					value : item.num
				});
			});
			myChart.hideLoading();
			myChart.setOption({
				legend : {
					data : names
				},
				series : [ {
					data : brower
				} ]
			});
		},
		error : function(errorMsg) {
			alert("failure of loading data!");
			myChart.hideLoading();
		}
	});
};

loadOneColumn();
