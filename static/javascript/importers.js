$(document).ready(function(){


	if ($(window).width() > 854) {
		
	}

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
	var link_url = document.URL;
	// splits on '/'
	var temp = link_url.split('/');

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
			//changes timer times from a string into a list
			var orderTimes = $.parseJSON(output[3]);

			//list of order ID's
			var orderID = $.parseJSON(output[4]);

			// used as a 2nd iterator like i in the for loop below
			var iterator = 0;

			// loops though incomplete orders
			for ( var i = 0; i < orderCount; i++){

				// adds timer plugin
				$('#timer-' + orderID[i]).countdown(orderTimes[i], {elapse: true})

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
					//console.log(pointInTime);

					//gets ID of each timer
					var timerID = '#' + $(this).attr('id');


					//number of times executed = number of orders
					if (iterator < orderCount) {

						//sets orders in correct rows on page load
						rowSwitch(orderCount, timerID, pointInTime);
						//moveToColumn();
						//increases iterator by 1
						iterator ++;

					//if the time of any orders = the string below rowSwitch
					//is run to move order to correct row
					} else {

						var timeCheck = ['12:00:00', '06:00:00', '02:00:00', '- 00:00:00']

						// checks of any order times are equal to the above times
						for ( k = 0; k < timeCheck.length; k++){

							if ($(timerID).text() === timeCheck[k]){

								// run rowSwitch if times are equal
								rowSwitch(orderCount, timerID, pointInTime, currentPage);
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

// moves order to correct column
function moveToColumn() {

	$('.ordCont').each(function (index, value){

		var columnID = $(this).attr('column');

		$(this).appendTo('#' + columnID);
	});
}


// puts orders in correct row
function rowSwitch(orderCount, timerID, pointInTime, currentPage){

	// order ID
	var getOrderID = timerID.split('-');
	getOrderID = getOrderID[1];

	// column ID
	var columnID = $('#' + getOrderID).attr('column');

	// colors for each row
	var colors = ['#008A91', '#9EE100', '#EFBC00', '#EF8900', '#EF2A00' ];
	// row ID's
	var rows = [ '#row4', '#row3', '#row2', '#row1']

	//need to change this
	// array or times as numerical value
	var colomnRange = ['24', '12', '06', '02', '01'];

	pointInTime = pointInTime.substring(0, 2);
	console.log(pointInTime);

	// loops thorugh colors
	for ( k = 0; k < colors.length; k++){

		// checks which row the order must be moved to
		if (colomnRange[k] > pointInTime) {

			$('#' + getOrderID).appendTo( rows[k] + ' .orderCont' + ' #' + columnID);

			$('#timer-' + getOrderID).css('color', '' + colors[k] + '');
			$('#block-' + getOrderID).css('background', '' + colors[k] + '');
			$('#digit-' + getOrderID).css('background', '' + colors[k] + '');
		}
	}

	// // if time is above 12 hours move to #row4
	// if (colomnRange[1] < pointInTime){

	// 	$('#' + getOrderID).appendTo('#row4 .orderCont' + ' #' + columnID);

	// 	$('#timer-' + getOrderID).css('color', '#008A91');
	// 	$('#block-' + getOrderID).css('background', '#008A91');
	// 	$('#digit-' + getOrderID).css('background', '#008A91');
	// }

	// if (pointInTime[0] === '-'){

	// 	$('#' + getOrderID).appendTo('#row0 .orderCont' + ' #' + columnID);

	// 	$('#timer-' + getOrderID).css('color', '#EF2A00');
	// 	$('#block-' + getOrderID).css('background', '#EF2A00');
	// 	$('#digit-' + getOrderID).css('background', '#EF2A00');

	// }

	// //displays orders
	$('.ordCont').show();
}

function showProducts() {

	// hide divs on page load
	$(".prodDetails").hide();
	$('.pageOverlay').hide();

	// un-binds click
	$('.ordOverlay').unbind('click');
	//binds click
	$('.ordOverlay').bind('click', function(){

		var overlayID = $(this).attr('id').split('-');
		overlayID = overlayID[1];
		// checks if overlay is visiable (bool)
		var visible = $('#' + overlayID + ' .prodDetails').is(":visible");

		// hides all product information first
		$('.promptCont').hide();
		$('.prodDetails').hide();
		$('.triangle').hide();

		// toggles clicked divs product information
		if (visible === false){

			$('#' + overlayID + ' .prodDetails').toggle();
			$('#' + overlayID + ' .triangle').toggle();

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

		//gets the ID of the "complete" button that is clicked
		var buttonID = $(this).attr('id').split('-');
		buttonID = buttonID[1];
		var visible = $('#' + buttonID + ' .promptCont').is(":visible");

		$('.prodDetails').hide();
		$('.promptCont').hide();

		if (visible === false){

			$('#' + buttonID + ' .promptCont').toggle();

			// KP || hide pageOverlay
			$('.pageOverlay').show();
			$(".triangle").hide();

		} else if (visible === true) {

			$('.pageOverlay').hide();
			$(".triangle").hide();
		}

		// runs removeOrder
		changeOrderStatus(buttonID, orderTimes);

		//  KP || Un-binds the pageOverlay
		$('.pageOverlay').unbind('click');

		// KP ||  Binds the pageOverlay
		$('.pageOverlay').bind('click', function(){

			$('.promptCont').hide();

			// KP || hide pageOverlay
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

	//displays actual time
	var currentTime = "Last Refreshed at: " + hours.slice(-2) + ":" + minutes.slice(-2) + ":" + seconds.slice(-2);

	//removes text inside div
	$('.lastRefresh').empty();

	//appends new time to div
	$('.lastRefresh').append(currentTime);

}

function lastRefresh() {

	$('.refresh').unbind('click');

	$('.refresh').bind('click', function() {

		//refreshes the page
		removeDivs();
   		checkPage();
		getTime();
	});
}

function refreshOnTimer() {

	//will refresh the page every 5 minutes(300000)
	setTimeout(function(){
		removeDivs();
   		checkPage();
   		getTime();

	}, 300000);
}

function removeDivs () {

	$('.pageOverlay').remove();
	$('.ordCont').remove();
}

// user has option to remove order or not
function changeOrderStatus(buttonID, orderTimes){

	$('.yes, .no').unbind('click');

	$('.yes, .no').bind('click', function() {

		// KP || hide pageOverlay
		$('.pageOverlay').hide();

		// class of div clicked (yes or no)
		var promptClass = $(this).attr('class');

		// if class is = 'yes'
		if (promptClass === 'yes'){

			// gets the current time of that timer
			var timePastDue = $('#timer-' + buttonID).text();

			// removes letters, symbols except numbers and hyphens
			timePastDue = timePastDue.replace(/[^0-9\-]/g,'');

			// used to calculate total time overdue. Wiil be used for statistics
			if (timePastDue[0] === '-') {
				var totalTimeOverdue = totalTimeOverdue + timePastDue;
			}

			// removes the order when 'yes' is cliced
			$('#' + buttonID).remove();
			var removeOrderID = parseInt(buttonID);
			changeDB(removeOrderID);

		// hides prompt when 'no' is clicked
		} else if (promptClass === 'no') {

			//console.log('#prompt-' + buttonID);
			$('#prompt-' + buttonID).hide();
		}
	});
}

// request to change db
function changeDB(removeOrderID) {
	//console.log(removeOrderID);

	// AJAX Call
	$.ajax({
		url:'/changeDB/', //name of the function in views.py
		type : "POST", //POST to send information to views.py, OR GET to retrieve information
		data : {
			removeOrderID : removeOrderID
		},
		complete : function(data) {

			var status = data.responseText;
			removeDivs();
	   		checkPage();
			getTime();
		}
	});
}
