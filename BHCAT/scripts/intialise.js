var grid;

var columns = [
	{id: "id", name: "ID", field: "ID",sortable: true, formatter:pslink, minWidth:180},
	{id: "radec", name: "RA-DEC", field: "RADEC",sortable: true, minWidth:180},
	{id: "source", name: "Source", field: "SOURCE"},
	{id: "pspin", name: "Spin P", field: "PSPIN"},
	{id: "porbit", name: "Orb P", field: "PORB"},
	{id: "m2", name: "M2", field: "M2"},
	{id: "dist", name: "Dist", field: "D"},
	{id: "type", name: "Type", field: "TYPE"},
	{id: "av", name: "Av", field: "AV"}
];

var options = {
	enableCellNavigation: true,
	enableColumnReorder: false,
	multiColumnSort: true
};

$(function () {
	$.getJSON('spicat.json',function(data){
		grid = new Slick.Grid("#myGrid", data, columns, options);
		grid.onSort.subscribe(function (e, args) {
	      		var cols = args.sortCols;
	      		data.sort(function (dataRow1, dataRow2) {
				for (var i = 0, l = cols.length; i < l; i++) {
			  		var field = cols[i].sortCol.field;
			  		var sign = cols[i].sortAsc ? 1 : -1;
			  		var value1 = dataRow1[field], value2 = dataRow2[field];
			  		var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
			  		if (result != 0) {
			    			return result;
			  		}
				}
				return 0;
	      		});
	      		grid.invalidate();
	      		grid.render();
	    	});
	});
})

//Add a link to the wdid column
var pslink = function(row, cell, value, columnDef, dataContext){
		temp_str = value.split(' ').join(''); //Removing spaces from path name
    return '<a href="spiders/' +temp_str+ "/" +temp_str+'.html" target="_blank">' +value+ '</a>'
}
