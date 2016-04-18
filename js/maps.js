
function prepareList() {
  $('#expList').find('li:has(ul)')
  	.click( function(event) {
  		if (this == event.target) {
  			$(this).toggleClass('expanded');
  			$(this).children('ul').toggle('medium');
  		}
  		return false;
  	})
  	.addClass('collapsed')
  	.children('ul').hide();
  };
 
  $(document).ready( function() {
      prepareList();
  });
function initialize()
{
	var map = 
	    new google.maps.Map(document.getElementById('map-canvas'));
	var bounds = new google.maps.LatLngBounds();
	var infowindow = new google.maps.InfoWindow();
	var count=0;
	for (var i in locations)
	{
		var p = locations[i];
		if(p[5]==0 && p[6]==0) continue;
		if(Object.keys(locations[i][8]).length<=0) continue;
		var latlng = new google.maps.LatLng(p[5], p[6]);
		bounds.extend(latlng);
		content='<div class="popup-img" id="flipbook-'+i+'">\
		<iframe src="http://www.bmatraffic.com/PlayVideo.aspx?ID='+p[0]+'" scrolling="no" frameborder="0" \
		style="width: 400px; height: 266px; display: block; padding: 0px; margin-top:0px;"></iframe>\
		<img src="http://www.bmatraffic.com/images/logo-bkk-small.png"> camera by bmatraffic.com\
		</div>';
		content+='<br><a href="#" onclick="setFlipbook('+i+",'normal','0'"+')">normal</a>';
		
		content+='<br><div id="listContainer"><ul id="expList">';
		for(var j in p[8])
		{
			
    
			//content+='<li><a href="#" class="hide" data-toggle="#list">'+j+'</a><ul class="out" id="list">';
			content+='<li><a href="#" onclick="'+"setFlipbook("+i+",'big','"+i+'_'+j+"')"+'"'+">"+j+'<ul>';
			for(var k in p[8][j])
			{
				
				content+='<li><a href="#" onclick="'+"setFlipbook("+i+",'haar','"+i+'_'+j+'_result_'+k+"')"+'"'+">"+j+'<ul>';
				for(var l in p[8][j][k])
					content+='<li><a href="#" onclick="'+"setFlipbook("+i+",'ocr','"+i+'_'+j+'_result_'+k+'_result_number_'+l+"')"+'"'+">"+j+'_'+k+'_'+l+': '+p[8][j][k][l]+'<ul>';
				 
			}
		}
		if(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0]=="a" || parseInt(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0])<5) feature_type = 'bus_green.png';
		else if(parseInt(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0])<10) feature_type = 'bus_yellow.png';
		else feature_type = 'bus_red.png';
        content+='</ul></li></ul></div>';
		var marker = new google.maps.Marker({
			position: latlng,
			map: map,
			title: p[0]+' '+p[1],
			content: content,
			icon: '/html/wimb/img/' + feature_type
		});
	
		google.maps.event.addListener(marker, 'click', function() {
			infowindow.setContent(this.title+'<br>'+this.content);
			infowindow.open(map, this);
			map.setCenter(marker.getPosition());
			
		});
		
		createMarkerButton(marker,i);	
	}
	map.fitBounds(bounds);
	
}
function createMarkerButton(marker,i) {
//
  //Creates a sidebar button
 // var ul = document.getElementById("marker_list");
  //var li = document.createElement("li");
//var carousel= document.getElementById("gallery");
//var carousel= document.getElementsByClassName("owl-stage")[0];
var p = locations[i];
for(var j in p[8])
{
for(var k in p[8][j])
{
/*
var owl = $('.owl-carousel');

var html = '<img src="/html/wimb/images_haar/'+i+'_'+j+'_result_'+k+'.jpg" height="15%" width="15%" onclick="#map-canvas">';//'<div class="item"><h4>N1</h4></div>';
var content = '<div class="owl-item" id="'+j+'">' + html + '</div>';
    owl.trigger('add.owl.carousel', [$(content)])
        .trigger('refresh.owl.carousel').trigger('next.owl.carousel');
		var innerDiv = document.getElementById(j);
//*/	
var innerDiv = document.createElement('div');
  //var title = marker.getTitle();
innerDiv.className = 'owl-item';
innerDiv.innerHTML =  '<a href="#map-canvas"><img src="/html/wimb/images_haar/'+i+'_'+j+'_result_'+k+'.jpg"></a>';
  //li.innerHTML = title;
//carousel.appendChild(innerDiv);

var carousel = document.getElementById(i+'_'+j+'_result_'+k+'.jpg');
try
{
carousel.appendChild(innerDiv);
}
catch(err)
{
location.reload();
}

  //ul.appendChild(li);
  //*/
  //Trigger a click event to marker when the button is clicked.
  google.maps.event.addDomListenerOnce(innerDiv, "click", function(){
    google.maps.event.trigger(marker, "click");
  });
  }
}
  
}
google.maps.event.addDomListener(window, 'load', initialize);
