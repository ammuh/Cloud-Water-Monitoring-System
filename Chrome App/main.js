 chrome.bluetooth.getAdapterState(function(adapter) {
  	console.log("Adapter " + adapter.address + ": " + adapter.name);
  	chrome.bluetooth.getDevices(function (deviceInfos) {
  		console.log(deviceInfos);
  	});
	});