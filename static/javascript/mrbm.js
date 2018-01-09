/*
	Author: Kenton Parton
	Function: Javascript for handling all general events
*/
$(document).ready(function(){
 	//Unchecks checkboxes on page load
  var checkboxes = $(':checkbox');
	checkboxes.prop('checked', false);

	var windowIds = ['#window1Val', '#window2Val', '#window3Val', '#window4Val', '#window5Val'];
	//loops through windowIds array
	for ( var i = 0; i < windowIds.length; i++)
		// Resets the value of the dropdown on page load
		$(windowIds[i] ).val('');

		// Remove the selected attribute on the dropdown on page load
		$(windowIds[i] ).prop('selected', false);

	//Hides windowCont on page load
	$('.windowCont').hide();

	var wallType1Val = $('#wallType1' ).val();

	//If incomplete wall is selected remove the Corner junction option from user
	if (wallType1Val === 'incompWall'){

		$(".inputCont:eq(2)").hide();
		$("#wallType2").val('0');
	}


	cornerHide();
	ToggleCheckboxes();
    numValidate();
    userInputs();


});

function cornerHide() {


	$('#wallType1').click(function(){

		//gets value of #wallType1
		var wallType1Val = $('#wallType1' ).val();

		//If incomeplete wall value is selected
		if (wallType1Val === 'incompWall'){

			//console.log('Incomplete Selected');

			//HIde 2nd child of .inputCont
			$(".inputCont:eq(2)").hide();

			// sets #wallType value to 0
			$("#wallType2").val('0');

		}else {
			// console.log('Complete Selected');
			//if a complete wall is selected, show corner junction option
			$(".inputCont:eq(2)").show();
		}
	});
}

//toggles the div of the checkbox between show() and hide()
function ToggleCheckboxes() {

	// gets the input id of the checkbox that is clicked
	$('input').click(function(){
		//setting idTitle to the id of the element clicked
		idTitle = this.id;

		//Toggles between .show and .hide
		$('#' + idTitle + 'Cont' ).toggle(this.checked);
		selectReset(idTitle);
	});
}

// trying to change the <option value=""> to the first option value=""
function selectReset(idTitle){

	// Resets the value of the dropdown
	$('#' + idTitle + 'Val' ).val('');

	// Remove the selected attribute on the dropdown
	$('#' + idTitle + 'Val' ).prop('selected', false);
}

function numValidate () {

    //Prevents non-numerics from being displayed in wallLength input box
    $('#wallLength').keypress(function(event){

        if(event.which != 8 && isNaN(String.fromCharCode(event.which))){
            event.preventDefault();
			//alert("Only numbers will be accepted");
        }
	});
}

function userInputs() {

	// array of id's
    var idArray = [
		['#wallLength'],
		['#wallType1'],
		['#wallType2'],
		['#wallType3'],
		['#doors'],
		['#window1Val', '#window1'],
		['#window2Val', '#window2'],
		['#window3Val', '#window3'],
		['#window4Val', '#window4'],
		['#window5Val', '#window5'],
	];
	// Will keep track of the the value of the draggable block added to .playground when button is clicked
	var wallCount = 0;

    // When button is clicked function will be initiated
    $('.button').click(function(){

		// wallCount will be incrmented by 1 each time button is clicked
		wallCount = wallCount + 1;

        //this array will be used to store the user inputs
		var inputArray = [];

		//Looping through the list of id's
        for ( var i = 0; i < idArray.length; i++){

			//Sets wallParams = to the value of specific element id
            var wallParams = $(idArray[i][0]).val();

			//If there is an empty string in any of the id inputs something will be alerted
            if (wallParams === '') {
				// checks if the length if the list being checked it length 2
				if (idArray[i].length === 2){
					//if idArray is checked then alert the user that information needs to be enter, change background color
					if ($(idArray[i][1]).is(':checked')){
						$(idArray[i][0]).css('background', '#CF7171');
					}else{
						// if it isn't checked, then push a value of 0 to inputArray
						inputArray.push(0);
						// alert("working");
					}
				}else{
					//if idArray[i] isn't length 2 alert user
					$(idArray[i][0]).css('background', '#CF7171');
				}
            } else {
				//Push the wallParams value to inputArray
                inputArray.push(wallParams);
				$(idArray[i][0]).css('background', 'white');
            }
        }

		// if the length of the array(inputArray) is != to length of idArray, empty the list
        if (inputArray.length != idArray.length ) {
            inputArray = [];
        }else {
			// If inputArray and idArray are the same length, transfer values to inputTransfer.
            inputTransfer( inputArray, wallCount);
        }
    });
}

//Function will transfer inputArray to view.py
function inputTransfer(inputArray, wallCount) {
	// console.log(inputArray);

	// AJAX Call
	$.ajax({
		url:'/inputAccept/', //name of the function in views.py
		type : "POST", //POST to send information to views.py, OR GET to retrieve information
		data : {
			wallCount : wallCount,
			inputArray : JSON.stringify(inputArray)//turns inputArray into a string
		},
		complete : function(data) {  //allows us to return the value from views.py

			// Gets the returned string from python and split's to determine the status of the value
			var output = data.responseText.split(' || ');

			// Checks if it was a SUCCESS
			if (output[0] == 'SUCCESS') {

				// Adds the HTML to the playground
				$('.playground').append(output[1]);

				// $('#wall-' + wallCount).sortable({});
				// $('#wall-' + wallCount).sortable('disable');

				$('.wallCont').sortable({});
				$('.wallCont').sortable('disable');

				// Activates the draggable boxes
				$('.mainBlock').draggable({ containment: 'parent' });
				//$('.mainBlock').draggable('disable');

				// Reset all toolbar styles to default
				$('.toolbar .controls').css('background', '#B3B3B3');
		
				// Adds the active style only on the selected div
				$('.toolbar' + ' #control-6').css('background', '#888888' );
				activateDrag();

				//calls activateToolbar
				activateToolbar();

				//determines which function needs to be run based on which feature is selected in toolbar controls
				//trigger();

			} else {
				// Adds the message to the span tag
				$('.playground .popup span').html(output[1]);

				// Displays the popup div
				$('.playground .popup').show();

				// Add's the timeout function
				setTimeout(function() {
					// Hide's the popup div
					$('.playground .popup').hide();
				}, 5000);
			}
		}
	});
}


function activateToolbar(){
	// Un-binds the toolbar controls
	$('.toolbar .controls').unbind('click');

	// Binds the toolbar controls
	$('.toolbar .controls').bind('click', function(){



		//gets the id of the toolbar control that is clicked
		var clickedID = $(this).attr('id');

		//gets the type of the clicked toolbar control
		var divType = $(this).attr('data-type');

		// changes the control bar colors
		if (clickedID != 'control-1') {

			// Reset all toolbar styles to default
			$('.toolbar .controls').css('background', '#B3B3B3');

			// Adds the active style only on the selected div
			$('.toolbar' + ' #' + clickedID).css('background', '#888888' );
		}


		// Switch checks for the divType
		switch(divType) {
			case 'rotate':
				//gets data-id of the clicked toolbar control
				var divDataID = $(this).attr('data-id');

				//calls activateRotate function (rotates wall)
				activateRotate(divDataID);

				break;
			case 'delete':

				//gets data-id of the clicked toolbar control
				var divDataID = $(this).attr('data-id');
				//removes the #draggable id div
				$('#draggable-' + divDataID).remove();

				break;
			case 'sort':

				// Run function Sort
				activateSort();

				break;
			case 'switch':

				// Run function Switch
				activateSwitch();


				break;
			case 'flip':

				//gets data-id of the clicked toolbar control
				var divDataID = $(this).attr('data-id');

				// Run function Sort
				activateFlip();

				break;
			case 'drag':

				// Run function Sort
				activateDrag();

				break;
		}
	});
}

function activateRotate (divDataID) {

	/*
		New approach!!!!!!!!

		For loop to
			get child div[i].....increse i therefore going down lift of children
			need to check if it is shutterC or T because we will use ID's iinstead
			get height and width and change css ....will need if statement for shutterC and T
			if wall rotated change margin
				change margins
			else
				change margin

	*/

	//gives the id of the wall that the toolbar is attached to
	var wallCont = '#wall-' + divDataID;

	//toggles wallRotate (class) and wallCont (class)
	$(wallCont).toggleClass('wallRotate');

	//array which will contain the child classes of wallCont being rotated.
	var shutterArray = [];
	var idArray = [];

	//adds shutter classes to shutterArray
	$(wallCont + ' > div').each(function () {

		//gets the child div class names inside wallCont
		var classSplit = this.className.split(' ');
		//console.log(classSplit);

		var shutterID = $(this).attr('id');

		// checks if className is in dragClassArray
		if (jQuery.inArray(classSplit[0], shutterArray) =='-1') {
			//pushes className to dragClassArray
			shutterArray.push(classSplit[0]);
		}

		// checks if the shutterC or shutterT ID is in idArray
		if (typeof shutterID === 'undefined') {
			// console.log("typeof shutterID === string(undefined) approx line 344");
		} else {
			//pushes shutterC and shutterT ID's into
			idArray.push(shutterID);
			// console.log("push shutterC and T");

		}
	});

	//checks if wall has been rotated
	var wallContSplit = $(wallCont).attr('class').split(' ');
	//rotated = 'wallRotate' if wall has been rotated
	var rotated = wallContSplit[3];

	//loops through the shutterArray and changes heights and widths of divs
	shutterArray.forEach(function(item) {

		//gets height of each class
		var height = $( wallCont + ' .' + item ).height();
		//gets width of each class
		var width = $( wallCont +  ' .' + item ).width();

		//sets height to width and width to height of classes inside wallCont div
		$( wallCont + ' .' + item ).css('width', height);
		$( wallCont + ' .' + item).css('height', width);

		if (rotated === 'wallRotate') {

			//changes margins when rotated
			$( wallCont + ' .' + item).css('margin', '0px 1px 1px 1px');

		} else {
			//changes margins back to original
			$( wallCont + ' .' + item).css('margin', '1px 1px 1px 0px');
		}
	});
	//loops through idArray allowing for divs to be rotated
	idArray.forEach(function(item) {
		//console.log(item);

		// path to specific div
		var pieceJuncPath = wallCont + ' #' + item;

		// gets full class name attached to cPieceJunc or tPieceJunc div
		var pieceJunc = $(pieceJuncPath).children().last().attr('class');

		// split version of pieceJunc variable
		var pieceJuncSplit = $(pieceJuncPath).children().last().attr('class').split(' ');

		// path to the either the cPieceJunc or tPieceJunc div
		var pieceJuncFinal = pieceJuncPath + ' .' + pieceJuncSplit[0];

		// possible class combination
		var classOptions = [
			['cPieceJunc', 'cRotate'],
			['cPieceJunc cFlipped', 'cCombo'],
			['cPieceJunc cSwitched', 'cRotSwitched'],
			['cPieceJunc cHorCombo', 'cVertCombo'],
			['cPieceJunc cCombo', 'cFlipped'],
			['cPieceJunc cRotSwitched', 'cSwitched'],
			['cPieceJunc cVertCombo', 'cHorCombo'],
			['cPieceJunc cRotate', ''],
			['tPieceJunc tFlipped', 'tCombo'],
			['tPieceJunc', 'tRotate'],
			['tPieceJunc tCombo', 'tFlipped'],
			['tPieceJunc tRotate', ''],
		];

		//Looping through the list of classes
		for (var l = 0; l < classOptions.length; l++){

			//checks if cPieceJunc or tPiecejunc class matches class name in classOptions
			if (pieceJunc === classOptions[l][0]) {

				//adds new class from classOptions
				$(pieceJuncFinal).toggleClass(classOptions[l][1]);

				//remove the class after pieceJuncFinal class
				$(pieceJuncFinal).removeClass(pieceJuncSplit[1]);
			}
		}

		var childClassArray = [
			[' .cornerJunc', ' .cPieceJunc'],
			[' .tJunc', ' .tPieceJunc'],
		];

		//Changes height and width of corner
		for ( j = 0; j < 2; j++){

			for ( k = 0; k < childClassArray.length; k++){

				//gets height of each class
				height = $( wallCont + ' #' + item + childClassArray[j][k] ).height();
				//gets width of each class
				width = $( wallCont +  ' #' + item + childClassArray[j][k] ).width();

				//sets height to width and width to height of classes inside wallCont div
				$( wallCont + ' #' + item + childClassArray[j][k] ).css('width', height);
				$( wallCont + ' #' + item + childClassArray[j][k] ).css('height', width);

			}
		}
	});
}


//Activates sort plugin and changes background color of sort icon in toolbar
function activateSort() {

	//enables sortable plugin
	$('.wallCont').sortable('enable');

	//disables draggable plugin
	$( '.mainBlock' ).draggable('disable');
	//unbinds click function for activateSwitch function
	$('.shutterC').unbind('click');
	//unbinds click function for activateSwitch function
	$('.shutterT, .shutterC').unbind('click');

}

function activateSwitch() {

	$('.shutterT, .shutterC').unbind('click');

	//disables sortable plugin
	$('.wallCont').sortable('disable');
	//disables draggable plugin
	$( '.mainBlock' ).draggable('disable');

	//binds click funtion to .shutterC div
	$('.shutterC').unbind('click');
	$('.shutterC').bind('click', function(){

		// console.log('switch Activated');

		//gets id of parent div
		var parentID = $(this).parent().attr('id');
		//gets id of clicked div
		var clickedID = $(this).attr('id');
		//gets path of cPieceJunc
		var cPieceClass = $('#' + parentID + ' #' + clickedID + ' .cPieceJunc').attr('class');
		//gets cPieceJunc toggled classes
		var toggledClasses = $('#' + parentID + ' #' + clickedID).children().last().attr('class').split(' ');
		//divs that point to t cPieceJunc
		var cPieceJunc = $('#' + parentID + ' #' + clickedID + ' .cPieceJunc');

		var testVariable = '#' + parentID + ' #' + clickedID + ' .cPieceJunc';


		var switchedArrayClass = [

			['cPieceJunc cFlipped', 'cHorCombo'],
			['cPieceJunc cRotate', 'cRotSwitched'],
			['cPieceJunc cCombo', 'cVertCombo'],
			['cPieceJunc cHorCombo', 'cFlipped'],

		];
		//adds and removes css classes for styles when divs are switched
		if (cPieceClass === 'cPieceJunc' || cPieceClass === 'cPieceJunc cSwitched') {

			//toggles cSwitched class
			$(cPieceJunc).toggleClass('cSwitched');

		} else {
			//checks current class name of div and changes it accordingly
			for (var i = 0; i < switchedArrayClass.length; i++){

				//if class name clicked matches class in switchedArrayClass change it
				if (cPieceClass === switchedArrayClass[i][0]) {

					//adds class name
					$(cPieceJunc).toggleClass(switchedArrayClass[i][1]);

					//removes specific class
					$(cPieceJunc).removeClass(toggledClasses[1]);

					break;
				}
			}
		}
	});
}

function activateFlip() {

	//disables sortable plugin
	$('.wallCont').sortable('disable');

	//unbinds click function for activateSwitch function
	$('.shutterC').unbind('mouseup');
	//disables draggable plugin
	$( '.mainBlock' ).draggable('disable');

	//binds click function to .shutterT and .shutterC classes
	$('.shutterT, .shutterC').unbind('click');
	$('.shutterT, .shutterC').bind('click', function() {

		//gives the id of the wall that the toolbar is attached to
		var wallCont = $(this).parent().attr('id');

		// path to specific div
		var thisID = $(this).attr('id');

		var pieceJuncPath = '#' + wallCont + ' #' + thisID;


		// gets full class name attached to cPieceJunc or tPieceJunc div
		var pieceJunc = $(pieceJuncPath).children().last().attr('class');

		// split version of pieceJunc variable
		var pieceJuncSplit = $(pieceJuncPath).children().last().attr('class').split(' ');

		// path to the either the cPieceJunc or tPieceJunc div
		var pieceJuncFinal = pieceJuncPath + ' .' + pieceJuncSplit[0];

		// possible class combination
		var flipClassOptions = [
			['cPieceJunc cCombo', 'cRotate'],
			['cPieceJunc cRotate', 'cCombo'],
			['cPieceJunc cSwitched', 'cHorCombo'],
			['cPieceJunc cHorCombo', 'cSwitched'],
			['cPieceJunc cRotSwitched', 'cVertCombo'],
			['cPieceJunc cVertCombo', 'cRotSwitched'],
			['cPieceJunc cFlipped', ''],
			['cPieceJunc', 'cFlipped'],
			['tPieceJunc tCombo', 'tRotate'],
			['tPieceJunc tRotate', 'tCombo'],
			['tPieceJunc', 'tFlipped'],
			['tPieceJunc tFlipped', ''],

		];

		//Looping through the list of classes
		for (var l = 0; l < flipClassOptions.length; l++){

			//checks if cPieceJunc or tPiecejunc class matches class name in flipClassOptions
			if (pieceJunc === flipClassOptions[l][0]) {

				//adds new class from flipClassOptions
				$(pieceJuncFinal).toggleClass(flipClassOptions[l][1]);

				//remove the class after pieceJuncFinal class
				$(pieceJuncFinal).removeClass(pieceJuncSplit[1]);
			}
		}
	});
}

//Activates drag plugin and changes background color of drag icon in toolbar
function activateDrag() {

	// console.log('drag Activated');

	//disables sortable plugin
	$('.wallCont').sortable('disable');

	// //disables click function for activateSwitch
	$('.shutterC').unbind('mouseup');

	// //disables click function for activateFlip
	$('.shutterT, .shutterC').unbind('mouseup');

	//enables draggable plugin
	$( '.mainBlock' ).draggable('enable');

}
