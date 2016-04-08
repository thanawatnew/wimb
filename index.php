<html>
<head>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
<script src="data.json"></script>
<script>
var data =[];
function getData() {
	var data2;
    $.ajax({
        url: "/html/wimb/buses.json",//"/Home/GetData/",
        type: "GET",
        contentType: 'json',
	dataType:'json',
        success: function (data){
            //console.log(data.key1); // value for key1
            //or to list all values
            for(var key in data){
		 locations[data[key][0]][8][data[key][1]+'_'+data[key][2]+'_'+data[key][3]+'_'+data[key][4]]=data[key][5]
                 console.log(data[key]);
            }
		data2=data;
		console.log('test');
		 setTimeout(getData, 5000);	
        },
	error: function(xhr,status,error){
		console.log(status);
		console.log(error);
		//console.log(data.responseText);
	}
    });
		//console.log(data2);
		//return data2;
	
}
var data3 = setInterval(getData, 5000);

</script>
</head>
<body>
</body>
</html>

