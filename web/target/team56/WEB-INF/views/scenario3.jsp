<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Scenario one</title>
<script src="js/echarts.js"></script>
<script src="js/jquery-3.3.1.min.js"></script>
<link rel="stylesheet" href="css/navigation.css" type="text/css" />
</head>
<body>

	<div class="nav">
		<ul>
			<li><a style="font-size: 14px" href="melbmap">Melb Map</a></li>
			<li><a style="font-size: 14px" href="sydneymap">Sydney Map</a></li>
			<li><a style="font-size: 14px" href="scenario1">Scenario 1</a></li>
			<li><a style="font-size: 14px" href="scenario2">Scenario 2</a></li>
			<li><a style="font-size: 14px" href="scenario3">Scenario 3</a></li>
			<li><a style="font-size: 14px" href="scenario4">Scenario 4</a></li>
			<li><a style="font-size: 14px" href="scenario5">Scenario 5</a></li>
		</ul>
	</div>

	<div style="width: 100%; height: 100%;">
		<div id="PieChartforCrimeTweet" class="piechart"
			style="width: 710px; height: 900px;"></div>

		<div id="PieChartforCrimeCSV" class="piechart"
			style="width: 710px; height: 900px;"></div>
	</div>

	<script type="text/javascript" src="js/s3_piechart_tweet.js"></script>
	<script type="text/javascript" src="js/s3_piechart_csv.js"></script>

</body>
</html>
