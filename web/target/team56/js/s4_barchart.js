function loadOneColumn() {
	var myChart = echarts.init(document.getElementById('BarChartforS4'));

	var xAxisData = [ 'abbotsford', 'albert park', 'brunswick',
			'brunswick east', 'carlton', 'carlton north', 'collingwood',
			'cremorne', 'docklands', 'east melbourne', 'fitzroy',
			'fitzroy north', 'flemington', 'kensington', 'maribyrnong',
			'melbourne', 'newport', 'north melbourne', 'northcote', 'parkville' ];

	var mor_t = [ 5, 4, 6, 6, 11, 1, 4, 2, 11, 1, 8, 3, 3, 24, 1, 217, 1, 2, 6,
			7 ];
	var aft_t = [ 1, 0, 5, 1, 6, 0, 0, 0, 7, 3, 5, 2, 0, 44, 0, 83, 0, 0, 0, 1 ];
	var nig_t = [ 5, 1, 10, 7, 14, 2, 4, 1, 19, 3, 19, 3, 3, 43, 1, 320, 1, 4,
			4, 4 ];

	var mor_in = [ -71, -67, -139, -23, -333, -15, -60, -25, -212, -69, -256,
			-43, -45, -15, -13, -1554, -11, -62, -49, -66 ];
	var aft_in = [ -131, -122, -289, -62, -730, -25, -180, -29, -370, -155,
			-550, -53, -101, -36, -32, -2889, -28, -134, -82, -198 ];
	var nig_in = [ -37, -86, -124, -28, -647, -13, -96, -17, -384, -91, -301,
			-27, -15, -15, -19, -2102, -8, -118, -42, -123 ];

	var itemStyle = {
		normal : {},
		emphasis : {
			barBorderWidth : 1,
			shadowBlur : 10,
			shadowOffsetX : 0,
			shadowOffsetY : 0,
			shadowColor : 'rgba(0,0,0,0.5)'
		}
	};

	myChart.setOption({
		//backgroundColor : '#eee',
		legend : {
			data : [ 'abbotsford', 'albert park', 'brunswick',
					'brunswick east', 'carlton', 'carlton north',
					'collingwood', 'cremorne', 'docklands', 'east melbourne',
					'fitzroy', 'fitzroy north', 'flemington', 'kensington',
					'maribyrnong', 'melbourne', 'newport', 'north melbourne',
					'northcote', 'parkville' ],
			align : 'left',
			left : 10
		},
		brush : {
			toolbox : [ 'rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear' ],
			xAxisIndex : 0
		},
		toolbox : {
			feature : {
				magicType : {
					type : [ 'stack', 'tiled' ]
				},
				dataView : {}
			}
		},
		tooltip : {},
		xAxis : {
			data : xAxisData,
			name : 'X Axis',
			silent : false,
			axisLine : {
				onZero : true
			},
			splitLine : {
				show : false
			},
			splitArea : {
				show : false
			}
		},
		yAxis : {
			inverse : true,
			splitArea : {
				show : false
			}
		},
		grid : {
			left : 100
		},
		visualMap : {
			type : 'continuous',
			dimension : 1,
			text : [ 'High', 'Low' ],
			inverse : true,
			itemHeight : 200,
			calculable : true,
			min : -2,
			max : 6,
			top : 60,
			left : 10,
			inRange : {
				colorLightness : [ 0.4, 0.8 ]
			},
			outOfRange : {
				color : '#bbb'
			},
			controller : {
				inRange : {
					color : '#2f4554'
				}
			}
		},
		series : [ {
			name : 'Morning tweeter',
			type : 'bar',
			stack : 'one',
			itemStyle : itemStyle,
			data : mor_t
		}, {
			name : 'afternoon tweeter',
			type : 'bar',
			stack : 'one',
			itemStyle : itemStyle,
			data : aft_t
		}, {
			name : 'night tweeter',
			type : 'bar',
			stack : 'two',
			itemStyle : itemStyle,
			data : nig_t
		}, {
			name : 'morning instagram',
			type : 'bar',
			stack : 'two',
			itemStyle : itemStyle,
			data : mor_in
		}, {
			name : 'afternoon instagram',
			type : 'bar',
			stack : 'two',
			itemStyle : itemStyle,
			data : aft_in
		}, {
			name : 'night instagram',
			type : 'bar',
			stack : 'two',
			itemStyle : itemStyle,
			data : nig_in
		} ]
	});
	myChart.on('brushSelected', renderBrushed);

	function renderBrushed(params) {
		var brushed = [];
		var brushComponent = params.batch[0];

		for (var sIdx = 0; sIdx < brushComponent.selected.length; sIdx++) {
			var rawIndices = brushComponent.selected[sIdx].dataIndex;
			brushed.push('[Series ' + sIdx + '] ' + rawIndices.join(', '));
		}

		myChart.setOption({
			title : {
				backgroundColor : '#333',
				text : 'SELECTED DATA INDICES: \n' + brushed.join('\n'),
				bottom : 0,
				right : 0,
				width : 100,
				textStyle : {
					fontSize : 12,
					color : '#fff'
				}
			}
		});
	}
};

loadOneColumn();