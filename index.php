<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="/html/wimb/assets/owl.carousel.min.css">
<link rel="stylesheet" href="/html/wimb/assets/owl.theme.default.min.css">
<link rel="stylesheet" href="/html/wimb/assets/docs.theme.min.css">
  <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<style>
#accordion-resizer {
    padding: 10px;
    width: 350px;
    height: 220px;
  }
#listContainer{
  margin-top:15px;
}
 
#expList ul, li {
    list-style: none;
    margin:0;
    padding:0;
    cursor: pointer;
}
#expList p {
    margin:0;
    display:block;
}
#expList p:hover {
    background-color:#121212;
}
#expList li {
    line-height:140%;
    text-indent:0px;
    background-position: 1px 8px;
    padding-left: 20px;
    background-repeat: no-repeat;
}
</style>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
<script src="result_data_aggregate_bus_station_siamtraffic.js" charset="UTF-8"></script><!---->
<!--<script src="data.json" charset="UTF-8"></script>--->
<script type="text/javascript" src="http://maps.google.com/maps/api/js?libraries=geometry"></script>
<script src="/html/wimb/js/maps.js" type="text/javascript"></script>
<script src="/html/wimb/bus_station.js" type="text/javascript" charset="UTF-8"></script>
<script src="/html/wimb/js/owl.carousel.min.js"></script>
<script src="/html/wimb/js/moment.min.js"></script>

 <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
<script>
//var data =[];
var is_debug = false;
$(function() {
    $( ".accordion" ).accordion({
      heightStyle: "fill"
    });
  });
  $(function() {
    $( ".accordion-resizer" ).resizable({
      minHeight: 140,
      minWidth: 200,
      resize: function() {
        $( ".accordion" ).accordion( "refresh" );
      }
    });
  });
function setFlipbook(id,type,image_path)
{
	if(type=="normal")
	content='<iframe src="http://www.bmatraffic.com/PlayVideo.aspx?ID='+id+'" scrolling="no" frameborder="0" \
		style="width: 400px; height: 266px; display: block; padding: 0px; margin-top:0px;"></iframe>\
		<img src="http://www.bmatraffic.com/images/logo-bkk-small.png">\
		';
	else if(type=="big")
		content = '<img src="/html/wimb/images_haar_result/'+image_path+'_result.jpg" width="400px" height="266px">';
	else if(type=="haar")
		content = '<img src="/html/wimb/images_number_result/'+image_path+'_result.jpg">';
	else if(type=="ocr")
		content = '<img src="/html/wimb/images_number/'+image_path+'.jpg">';
	$('#flipbook-'+id).html(content);
		
}

function getData() {
	//var data2;
    $.ajax({
        url: "/html/wimb/buses.json",//"/Home/GetData/",
        type: "GET",
        contentType: 'json',
	dataType:'json',
        success: function (data){

            //console.log(data.key1); // value for key1
            //or to list all values
            for(var key in data){
				if(is_debug)
				{
					console.log('key = ');
					console.log(key);
					console.log('data[key] = ');
					console.log(data[key]);
				}
				 if(!(data[key][0] in Object(locations)))
				 {
					console.log("error: not found cam_id = "+data[key][0]);
					continue;
					//locations[data[key]]={};
					 //locations[data[key][0]][8][data[key][1]+'_'+data[key][2]]={data[key][3]:{data[key][4]:data[key][5]}};

				 }
				 else if(!(data[key][1]+'_'+data[key][2] in Object(locations[data[key][0]][8])))
				 {
					locations[data[key][0]][8][data[key][1]+'_'+data[key][2]]={};
					locations[data[key][0]][8][data[key][1]+'_'+data[key][2]][data[key][3]]={};
					locations[data[key][0]][8][data[key][1]+'_'+data[key][2]][data[key][3]][data[key][4]]=data[key][5];
				 }
				 else if(!(data[key][3] in Object(locations[data[key][0]][8][data[key][1]+'_'+data[key][2]])))
				 {
					 locations[data[key][0]][8][data[key][1]+'_'+data[key][2]][data[key][3]]={};
					locations[data[key][0]][8][data[key][1]+'_'+data[key][2]][data[key][3]][data[key][4]]=data[key][5];
				 }
				 else locations[data[key][0]][8][data[key][1]+'_'+data[key][2]][data[key][3]][data[key][4]]=data[key][5];
						 //console.log(data[key]);
				
				/*
				var bus_station_nearest = null;
				var distance_nearest = 999999999;
				for(var i=0;i<bus_station.length;i++)
				{
					if(is_debug) 
					{
						console.log('key = ');
						console.log(key);
						console.log('i = ');
						console.log(i);
					}
					var distance_between = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(bus_station[i][2],bus_station[i][3]), new google.maps.LatLng(locations[data[key][0]][5],locations[data[key][0]][6]));
					if( distance_between < distance_nearest )
					{
						bus_station_nearest = bus_station[i];
						distance_nearest = distance_between;
					}
				}
				locations[data[key][0]].push(bus_station_nearest)
				//*/
            }
		//data2=data;
		console.log('downloaded data');
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


getData();
//setInterval(getData, 5000);
$(document).ready(function() {
	
              $('.owl-carousel').owlCarousel({
                loop: false,
                margin: 10,
				//autoWidth:true,
                responsiveClass: true,
                responsive: {
                  0: {
                    items: 1,
                    nav: true
                  },
                  600: {
                    items: 3,
                    nav: false
                  },
                  1000: {
                    items: 5,
                    nav: true,
                    loop: false,
                    margin: 20
                  }
                }
              })
            })

</script>
</head>
<body>
<iframe src="http://www.bmatraffic.com" width="0" height="0"></iframe>
<!--<div id="map-canvas" style="width: auto; height: 75%; width: 100%; border: 2px solid #73AD21"></div>-->
<div id="map-canvas" style="height: 65%; width: 100%; "></div>
<div class="row">
        <div class="large-12 columns">
          <div class="owl-carousel" id="gallery" style="width:100%;">
		  <?php
		  
		  if ($handle = opendir('images_haar')) {
$count_picture = 0;
    while (false !== ($entry = readdir($handle))) {

        if ($entry != "." && $entry != ".." && $entry != "g.php") {
			echo '<div class="item" id="'.$entry.'" onclick='."'".'$(".owl-carousel").trigger("to.owl.carousel", ['.$count_picture.', 1000000, true])'."'".'>'."\n";
			//echo "<img src='./images_haar/$entry' height='15%' width='15%'>\n";
			echo "</div>\n";
            //echo "$entry\n";
        }
	$count_picture+=1;
    }

    closedir($handle);
}

//*/
?>
<!--
            <div class="item">
              <h4>1</h4>
            </div>
            <div class="item">
              <h4>2</h4>
            </div>
            <div class="item">
              <h4>3</h4>
            </div>
            <div class="item">
              <h4>4</h4>
            </div>
            <div class="item">
              <h4>5</h4>
            </div>
            <div class="item">
              <h4>6</h4>
            </div>
            <div class="item">
              <h4>7</h4>
            </div>
            <div class="item">
              <h4>8</h4>
            </div>
            <div class="item">
              <h4>9</h4>
            </div>
            <div class="item">
              <h4>10</h4>
            </div>
            <div class="item">
              <h4>11</h4>
            </div>
            <div class="item">
              <h4>12</h4>
            </div>
			-->
          </div>
		</div>
</div>
<iframe src="/html/wimb/images_haar/g.php" scrolling="no" frameborder="0" \
		style="width: 100%; height: 100%; display: block; padding: 0px; margin-top:0px;"></iframe>
</body>
</html>

