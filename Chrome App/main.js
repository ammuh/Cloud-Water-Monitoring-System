var openConn;
var device_list = {};
var data = {"datatype":"JSON", "uniqueId":"m136efsrTy-1000001", "rawData":null};
var csv = "";

chrome.bluetooth.getDevices(function(devices) {
	console.log(devices);
  for (var i = 0; i < devices.length; i++) {
  	$('body > ul.dev-list').append('<li id="port"><a href="#" id="connect">'+devices[i].name+'</a> <a id="disconnect"> Disconnect </a></li>').promise().done(function(){
  		$("a").unbind("click").click(function(){
				console.log("click");
  			startPort(device_list[$(this).html()].address, device_list[$(this).html()].uuids[0]);
			});
  	});
  	device_list[devices[i].name] = {"address": devices[i].address, "uuids":devices[i].uuids};
  }
});


$('button.send').click(function(){
	chrome.bluetoothSocket.send(openConn, str2ab($('input.console').val()), function(bytes_sent) {
	  if (chrome.runtime.lastError) {
	    console.log("Send failed: " + chrome.runtime.lastError.message);
	  } else {
	    console.log("Sent " + bytes_sent + " bytes")
	  }
	})
	setTimeout(function (){newResp();}, 1500);
});

$('button.websend').click(function(){
	console.log("click");
	
	Papa.parse(csv,{
		header: true,
		complete: function(results){
			console.log(results);
			data.rawData = results.data;
			postData();
		},
	});
});

function startPort(addr, uuid) {
	console.log(addr);
	console.log(uuid);
	chrome.bluetoothSocket.create(function(createInfo) {
		console.log(createInfo)
		openConn = createInfo.socketId;
		chrome.bluetoothSocket.onReceive.addListener(function(receiveInfo) {
				console.log('recieved');
				console.log(receiveInfo.data);
				console.log(ab2str(receiveInfo.data));
				csv += ab2str(receiveInfo.data);
  			// receiveInfo.data is an ArrayBuffer.
			});
  	chrome.bluetoothSocket.connect(createInfo.socketId,	addr, uuid, function() {
		  if (chrome.runtime.lastError) {
		    console.log("Connection failed: " + chrome.runtime.lastError.message);
		  } else {
		    console.log("success");// Profile implementation here.
		  }
		});
	});

	}


function stopPort(cPort){
	chrome.serial.disconnect(cPort, function(result){
			console.log(result);
	});
}

function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}

function str2ab(str) {
  var buf = new ArrayBuffer(str.length*2); // 2 bytes for each char
  var bufView = new Uint16Array(buf);
  for (var i=0, strLen=str.length; i<strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

function newResp() {
	$('.responses').append("<li>"+ resp + "</li>");
	resp="";

}
function postData() {
	var jstring = JSON.stringify(data);
	console.log(data);
	console.log(jstring);
	var xhr = new XMLHttpRequest();
	xhr.open("POST", 'http://flux-plant.appspot.com/device/DataSubmit', true);
	xhr.setRequestHeader('Content-type', 'application/json, charset=utf-8');
	xhr.onreadystatechange = function () {
		$('p.webresp').html(xhr.responseText);
		}; // Implemented elsewhere.
	
	xhr.send(jstring);
}