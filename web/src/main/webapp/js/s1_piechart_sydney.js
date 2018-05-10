/**
 *  Xiaolu Zhang 886161
 *  Jianbo Ma 807590
 *  Hongyi Lin 838776
 *  Xiaoyu Wang 799778
 *  Shalitha Weerakoon Karunatilleke 822379
 *  COMP90024 Cluster and Cloud Computing
 *  Social Media Analytics on Melbourne & Sydney
 */

function loadOneColumn() {
	var myChart = echarts.init(document.getElementById('PieChartforSydney'));
	var info = [];

	myChart.setOption({
		title : {
			text : 'Sydney',
			subtext : 'Twitter data analysis on Lifestyle',
			x : 'center'
		},
		tooltip : {
			trigger : 'item',
			formatter : function(params, ticket, callback) {
				var path = "data/s1/syd/" + params.name + ".json";
				var tips = params.name + '<br/>';
				$.ajax({
					type : 'get',
					url : path,
					dataType : "json",
					success : function(result) {
						info = result.data;
					},
					error : function(errorMsg) {
						alert("failure of loading data!");
					}
				});
				tips = tips + "positive: " + info[0] + '<br/>';
				tips = tips + "negative: " + info[1] + '<br/>';
				tips = tips + "neutral: " + info[2] + '<br/>';
				return tips;
			}
		},
		legend : {
			x : 'center',
			bottom : 10,
			data : []
		},
		series : [ {
			name : 'lifestyle rank',
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
		url : 'data/s1/syd/piechart.json',
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
