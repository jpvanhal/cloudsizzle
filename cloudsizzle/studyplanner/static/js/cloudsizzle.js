$(document).ready(function(){
	$('#courses table').addClass('tablesorter');
	$('#courses table').tablesorter({sortList:[[0,0],[2,1]], cssDesc: 'headerSortDown', widgets: ['zebra']});
});
