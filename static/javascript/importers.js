$(document).ready(function(){

	checkPage();
});

function checkPage() {

	var currentPage = getCurrentPage();

	if (currentPage === 'orders') {

		inputTransfer(currentPage);
	}
}

// gets the current page
function getCurrentPage() {

	// Gets the URL of the current page
	var linkUrl = document.URL;
	// splits on '/'
	var temp = linkUrl.split('/');

	// gets the page label || need to check when live
	var currentPage = temp[3];

	return currentPage;
}

// adds orders to orders page
function inputTransfer(currentPage) {

	// AJAX Call
	$.ajax({
		url:'/GETvalues/', //name of the function in views.py
		type : "POST", //POST to send information to views.py, OR GET to retrieve information
		data : {
			currentPage : currentPage
		},
		complete : function(data) {  //allows us to return the value from views.py

			// Gets the returned string from python and split's to determine the status of the value
			var output = data.responseText.split(' || ');

			// appends the html from views.py to #row4 .orderCont
			$('#row4 .orderCont').append(output[1]);
			showProducts();
			$('.ordCont').hide();


			// number of orders that have been created
			var orderCount = output[2];

			//list of each order due date
			//changes timer times from a JSON string into a list
			var orderTimes = $.parseJSON(output[3]);

			//list of order Id's
			var orderId = $.parseJSON(output[4]);

			// used as a 2nd iterator like i in the for loop below
			var iterator = 0;

			// loops though incomplete orders
			for ( var i = 0; i < orderCount; i++){

				// adds timer plugin
				$('#timer-' + orderId[i]).countdown(orderTimes[i], {elapse: true})

				//code is run when timer is updated (every second)
				.on('update.countdown', function(event) {

					//if time has passed due date set timer to negative
			    	if (event.elapsed) { // Either true or false
						//negative timer
			      		$(this).html(event.strftime('- %I:%M:%S'));
			    	} else {
						//positive timer
			      		$(this).html(event.strftime('%I:%M:%S'));
			    	}


					// gets the time for each order
					var pointInTime = $(this).text();

					// removes letters, spaces and leaves digits and hyphens
					pointInTime = pointInTime.replace(/[^0-9\-]/g,'');

					//gets Id of each timer
					var timerId = '#' + $(this).attr('id');

					//number of times executed = number of orders
					if (iterator < orderCount) {
						//sets orders in correct rows on page load
						rowSwitch(orderCount, timerId, pointInTime);
						//increases iterator by 1
						iterator ++;

					//if the time of any orders = the string below rowSwitch
					//is run to move order to correct row
					} else {

						var timeCheck = ['25:00:00', '13:00:00', '07:00:00', '03:00:00', '- 00:00:00']
						// checks of any order times are equal to the above times
						for ( k = 0; k < timeCheck.length; k++) {
							if ($(timerId).text() === timeCheck[k]){
								// run rowSwitch if times are equal
								rowSwitch(orderCount, timerId, pointInTime);
								break;
							}
						}
					}
				});
			}
			// removes order on completion
			displayPrompt(orderTimes);

			//hides complete order prompt
			$('.promptCont').hide();

			//gets last refresh time
			getTime();

			//refreshes page
			lastRefresh();

			//refresh page every 5 min
			refreshOnTimer();

		}
	});
}

function formatTime(pointInTime) {

	if (pointInTime[0] === '-') {
		return '-0'
	}

	for (i = 0; i < pointInTime.length; i++) {

		if (pointInTime[i] === '0') {
			pointInTime = pointInTime.replace('0','');
			i--;
		} else {
			return pointInTime;
		}
	}
}



// puts orders in correct row
function rowSwitch(orderCount, timerId, pointInTime){

	pointInTime = formatTime(pointInTime);

	// order Id
	var getOrderId = timerId.split('-');
	getOrderId = getOrderId[1];

	// column Id
	var columnId = $('#' + getOrderId).attr('column');

	//need to change this
	// array or times as numerical value
	var tRange = [ 0, 30000, 70000, 130000, 250000];
	// row Id's
	var rows = ['#row0', '#row1', '#row2', '#row3', '#row4', '#row5']

	// loops through rows
	for ( k = 0; k < rows.length; k++){

		// checks which row the order must be moved to
		if (parseInt(pointInTime) <= tRange[k]) {

			if (pointInTime[0] === '-'){
				moveOrders(getOrderId, columnId, rows, k);
				break;
			}
			moveOrders(getOrderId, columnId, rows, k);
			break;

		} else if(parseInt(pointInTime) > tRange[tRange.length - 1]) {
			moveOrders(getOrderId, columnId, rows, 5);
			break;
		}
	}

	// //displays orders
	$('.ordCont').show();
}

function moveOrders(getOrderId, columnId, rows, k) {

	// colors for each row
	var colors = ['#EF2A00', '#EF8900', '#EFBC00', '#9EE100', '#008A91', '#C11DD2'];

	$('#' + getOrderId).appendTo( rows[k] + ' .orderCont' + ' #' + columnId);
	$('#timer-' + getOrderId).css('color', '' + colors[k] + '');
	$('#block-' + getOrderId).css('background', '' + colors[k] + '');
	$('#digit-' + getOrderId).css('background', '' + colors[k] + '');
}

function showProducts() {

	// hide divs on page load
	$(".prodDetails").hide();
	$('.pageOverlay').hide();

	// un-binds click
	$('.ordOverlay').unbind('click');
	//binds click
	$('.ordOverlay').bind('click', function(){

		var overlayId = $(this).attr('id').split('-');
		overlayId = overlayId[1];
		// checks if overlay is visiable (bool)
		var visible = $('#' + overlayId + ' .prodDetails').is(":visible");

		// hides all product information first
		$('.promptCont').hide();
		$('.prodDetails').hide();
		$('.triangle').hide();

		// toggles clicked divs product information
		if (visible === false){

			$('#' + overlayId + ' .prodDetails').toggle();
			$('#' + overlayId + ' .triangle').toggle();

			// KP || hide pageOverlay
			$('.pageOverlay').show();

		} else if (visible === true) {

			$('.pageOverlay').hide();
		}

		//  KP || Un-binds the pageOverlay
		$('.pageOverlay').unbind('click');

		// KP ||  Binds the pageOverlay
		$('.pageOverlay').bind('click', function(){

			$(".prodDetails").hide();
			$(".triangle").hide();

			// KP || hide pageOverlay
			$('.pageOverlay').hide();
		});
	});
}


//displays "Are you sure?" prompt
function displayPrompt(orderTimes){

	$('.btn-complete').unbind('click');

	$('.btn-complete').bind('click', function(){

		//gets the Id of the "complete" button that is clicked
		var buttonId = $(this).attr('id').split('-');
		buttonId = buttonId[1];
		var visible = $('#' + buttonId + ' .promptCont').is(":visible");

		$('.prodDetails').hide();
		$('.promptCont').hide();

		if (visible === false){

			$('#' + buttonId + ' .promptCont').toggle();

			// KP || hide pageOverlay
			$('.pageOverlay').show();
			$(".triangle").hide();

		} else if (visible === true) {

			$('.pageOverlay').hide();
			$(".triangle").hide();
		}

		// runs removeOrder
		changeOrderStatus(buttonId, orderTimes);

		// Un-binds the pageOverlay
		$('.pageOverlay').unbind('click');

		// Binds the pageOverlay
		$('.pageOverlay').bind('click', function(){

			$('.promptCont').hide();

			// hide pageOverlay
			$('.pageOverlay').hide();
		});
	});
}

// Gets time for last refresh
function getTime() {

	//gets current date
	var timeNow = new Date();

	var hours = '00' + timeNow.getHours();

	var minutes = '00' + timeNow.getMinutes();

	var seconds = '00' + timeNow.getSeconds();

	// displays actual time
	var currentTime = "Last Refreshed at: " + hours.slice(-2) + ":" + minutes.slice(-2) + ":" + seconds.slice(-2);

	// removes text inside div
	$('.lastRefresh').empty();

	// appends new time to div
	$('.lastRefresh').append(currentTime);

}

function refreshOnTimer() {

	// will refresh the page every 5 minutes(300000)
	setTimeout(function(){
		removeDivs();
   		checkPage();
   		getTime();

	}, 300000);
}

function lastRefresh() {

	$('.refresh').unbind('click');

	$('.refresh').bind('click', function() {

		// refreshes the page
		removeDivs();
   		checkPage();
		getTime();
	});
}

function removeDivs () {

	$('.pageOverlay').remove();
	$('.ordCont').remove();
}

// user has option to remove order or not
function changeOrderStatus(buttonId, orderTimes){

	$('.yes, .no').unbind('click');

	$('.yes, .no').bind('click', function() {

		// hide pageOverlay
		$('.pageOverlay').hide();

		// class of div clicked (yes or no)
		var promptClass = $(this).attr('class');

		// if class is = 'yes'
		if (promptClass === 'yes'){

			// gets the current time of that timer
			var timePastDue = $('#timer-' + buttonId).text();

			// removes letters, symbols except numbers and hyphens
			timePastDue = timePastDue.replace(/[^0-9\-]/g,'');

			// used to calculate total time overdue. Wiil be used for statistics
			if (timePastDue[0] === '-') {
				var totalTimeOverdue = totalTimeOverdue + timePastDue;
			}

			// removes the order when 'yes' is cliced
			$('#' + buttonId).remove();
			var removeOrderId = parseInt(buttonId);
			changeDB(removeOrderId);

		// hides prompt when 'no' is clicked
		} else if (promptClass === 'no') {

			//console.log('#prompt-' + buttonId);
			$('#prompt-' + buttonId).hide();
		}
	});
}

// request to change db
function changeDB(removeOrderId) {
	// AJAX Call
	$.ajax({
		url:'/changeDB/', //name of the function in views.py
		type : "POST", //POST to send information to views.py, OR GET to retrieve information
		data : {
			removeOrderId : removeOrderId
		},
		complete : function(data) {

			var status = data.responseText;
			removeDivs();
	   		checkPage();
			getTime();
		}
	});
}