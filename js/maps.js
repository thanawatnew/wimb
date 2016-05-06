function smoothZoom (map, level, cnt, mode) {
		//alert('Count: ' + cnt + 'and Max: ' + level);

		// If mode is zoom in
		if(mode == true) {

			if (cnt >= level) {
				return;
			}
			else {
				var z = google.maps.event.addListener(map, 'zoom_changed', function(event){
					google.maps.event.removeListener(z);
					smoothZoom(map, level, cnt + 1, true);
				});
				setTimeout(function(){map.setZoom(cnt)}, 350);
			}
		} else {
			if (cnt <= level) {
				return;
			}
			else {
				var z = google.maps.event.addListener(map, 'zoom_changed', function(event) {
					google.maps.event.removeListener(z);
					smoothZoom(map, level, cnt - 1, false);
				});
				setTimeout(function(){map.setZoom(cnt)}, 350);
			}
		}
	}   
/*
// the smooth zoom function
function smoothZoom (map, max, cnt) {
    if (cnt >= max) {
            return;
        }
    else {
        z = google.maps.event.addListener(map, 'zoom_changed', function(event){
            google.maps.event.removeListener(z);
            smoothZoom(map, max, cnt + 1);
        });
        setTimeout(function(){map.setZoom(cnt)}, 500); // 80ms is what I found to work well on my system -- it might not work well on all systems
    }
}//*/
function reg(input) {
    var flags;
    //could be any combination of 'g', 'i', and 'm'
    flags = 'gi';
    return new RegExp(input,flags)//('ReGeX' + input + 'ReGeX', flags);
}
String.prototype.matchAll = function(regexp) {
// By Chris West
  var matches = [];
  this.replace(regexp, function() {
    var arr = ([]).slice.call(arguments, 0);
    var extras = arr.splice(-2);
    arr.index = extras[0];
    arr.input = extras[1];
    matches.push(arr);
  });
  return matches.length ? matches : null;
};


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

function setUserAgent(window, userAgent) {
    if (window.navigator.userAgent != userAgent) {
        var userAgentProp = { get: function () { return userAgent; } };
        try {
            Object.defineProperty(window.navigator, 'userAgent', userAgentProp);
        } catch (e) {
            window.navigator = Object.create(navigator, {
                userAgent: userAgentProp
            });
        }
    }
}
var isTouch = (('ontouchstart' in window) || (navigator.msMaxTouchPoints > 0));
if(isTouch)
{
var userAgent='Mozilla/5.0 (Linux; Android 5.1.1; Nexus 4 Build/LMY48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.105 Mobile Safari/537.36';//'Mozilla/5.0 (Linux; U; Android 4.2; en-us; Nexus 4 Build/JOP24G) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30';
setUserAgent(window, userAgent);
//setUserAgent(document.querySelector('map-canvas').contentWindow, userAgent);
//setUserAgent(document.querySelector('iframe').contentWindow, 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36');
console.log('this device is touch-enabled');
}
console.log(navigator.userAgent); // returns 'agent'
function fnChangeBorder(index){
	document.getElementById(index).children[0].children[0].children[0].src="/html/wimb/img/black.jpg";//.style.borderColor="#00FF00";
}
function initialize()
{
	var map = 
	    new google.maps.Map(document.getElementById('map-canvas'));
	var bounds = new google.maps.LatLngBounds();
	var infowindow = new google.maps.InfoWindow();
	//getLocation(map);
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
		content+='<br><a href="#" onclick="setFlipbook('+i+",'normal','0'"+')">Real time feed</a>';
		
		//content+='<br><div id="listContainer"><ul id="expList">';
		content+='<div class="ui-widget-content accordion-resizer"><div  class="accordion">';
		for(var j in p[8])
		{
			
    
			//content+='<li><a href="#" class="hide" data-toggle="#list">'+j+'</a><ul class="out" id="list">';
			content+='<h3><a href="#" onclick="'+"setFlipbook("+i+",'big','"+i+'_'+j+"')"+'"'+">"+"Full picture: "+j+'</a></h3><div><ul>';
			for(var k in p[8][j])
			{
				
				content+='<li><a href="#" onclick="'+"setFlipbook("+i+",'haar','"+i+'_'+j+'_result_'+k+"')"+'"'+">"+"Cropped picture: "+j+'</a></li>';
				for(var l in p[8][j][k])
				{
					content+='<li><a href="#" onclick="'+"setFlipbook("+i+",'ocr','"+i+'_'+j+'_result_'+k+'_result_number_'+l+"')"+'"'+">Result picture: "+j+'_'+k+'_'+l+': ';
var str = p[9][0][4]+','+p[9][1][4];
var regexp = reg('[^,]\w{0,5}5\w{0,5}[^,]') 
var bus_number_list = str.matchAll(regexp);
//console.log(bus_number_list);
is_first_bus_number=true;
for (var count_bus_number=0;count_bus_number<Object(bus_number_list).length;count_bus_number++)
{
console.log(bus_number_list[count_bus_number]);
if(count_bus_number>0) content+=',';
content+=bus_number_list[count_bus_number][0];
is_first_bus_number=false;
}
content+='</li>';
//+p[8][j][k][l]+'<ul>';
				} 
			}
			content+='</div>';
		}
		content+='</div></div>';
		if(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0]=="a" || parseInt(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0])<5 && moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[1]=="minutes" || moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[1]=="minute"  || moment(j, "YYYYMMDD_hhmmss").fromNow()=="a few seconds ago" ||  moment(j, "YYYYMMDD_hhmmss").fromNow()=="in a few seconds" ||  moment(j, "YYYYMMDD_hhmmss").fromNow()=="in a minute") feature_type = 'bus_green.png';
		else if(parseInt(moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[0])<10 && moment(j, "YYYYMMDD_hhmmss").fromNow().split(' ')[1]=="minutes") feature_type = 'bus_yellow.png';
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
	var listener = google.maps.event.addListener(map, "idle", function() { 
  	//if (map.getZoom() > 16) map.setZoom(16);
	smoothZoom(map, 15, map.getZoom(),true); 
  	//map.setZoom(15);
	google.maps.event.removeListener(listener); 
	});
	//if (map.getZoom() < 16) map.setZoom(16); 
	
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
innerDiv.innerHTML =  '<a href="#map-canvas"><img src="/html/wimb/images_haar/'+i+'_'+j+'_result_'+k+'.jpg" <!--onClick="'+"fnChangeBorder('"+i+'_'+j+'_result_'+k+".jpg')"+'" --></a>';
  //li.innerHTML = title;
//carousel.appendChild(innerDiv);

var carousel = document.getElementById(i+'_'+j+'_result_'+k+'.jpg');
try
{
carousel.appendChild(innerDiv);
}
catch(err)
{
//location.reload();

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
