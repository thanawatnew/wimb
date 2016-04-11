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
		
        content+='</ul></li></ul></div>';
		var marker = new google.maps.Marker({
			position: latlng,
			map: map,
			title: p[0]+' '+p[1],
			content: content
		});
	
		google.maps.event.addListener(marker, 'click', function() {
			infowindow.setContent(this.title+'<br>'+this.content);
			infowindow.open(map, this);
			map.setCenter(marker.getPosition());
			
		});
		
	}
	
	map.fitBounds(bounds);
	
}

google.maps.event.addDomListener(window, 'load', initialize);
