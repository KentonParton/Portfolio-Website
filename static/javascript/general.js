/*
	Author: Kenton Parton
	Function: Javascript for handling all general events
*/
$(document).ready(function () {

	$(".computer").attr("src", $("#img-tag-id").attr("src")).load(function () {
		var comp_height = this.height;
		var land_height = $('.landing_container').height() - 50;
		var margin = (land_height - comp_height) / 2;
		$('.position_projects').css('margin', '' + margin + 'px 0px');

		if ($(window).width() <= 854) {
			$('.menus').addClass('dropped');
			$('.drop_down').show();
			$('.dropped').hide();
			mobile_switch();
		} else {
			$('.menus').removeClass('dropped');
			$('.drop_down').hide();
			$('.dropped').show();
		}
	});

	$(window).resize(function () {
		// console.log($(window).width());
		sizeDivs();
		adjust_divs();
	});

	display_dropped();
	check_project();
	scroll_to_div();
});

function sizeDivs() {

	var comp_height = $('.position_projects').height();
	var land_height = $('.landing_container').height() - 50;
	var margin = (land_height - comp_height) / 2;

	$('.position_projects').css('margin', '' + margin + 'px 0px');
}

function display_dropped() {

	$('.drop_down').click(function() {
		$('.dropped').toggle();
	});
}

function adjust_divs() {

	if ($(window).width() > 854) {
		if ($('.menus').hasClass('dropped')) {
			$('.dropped').show();
			$('.menus').removeClass('dropped');
			$('.drop_down').hide();
		}
	} else {
		if ($('.menus').hasClass('dropped')) {
			
		} else {
			$('.menus').addClass('dropped');
			$('.drop_down').show();
			$('.dropped').hide();
			
		}
	}
	mobile_switch();
}

function mobile_switch() {
	
	var class_array = [
		['.landing_container'],
		['.drop_down'],
		['.my_name'],
		['.welcome_container'],
		['#first span'],
		['.projects_container .project .text_container'],
		['.projects_container .project .text_container .demo'],
		['.overlay .description p'],
		['.overlay .description'],
		['.overlay .description .go-to'],
		['#first'],
		['#second'],
		['#second span'],
		['#first'],
		['#info-1'],
		['#info-2'],
		['#info-3'],
		['.text span'],
		['.contact_me'],
		['.comp_container'],
		['.position_projects'],
		['.contents_container .portfolio_container .project .text_container'],
		['.contents_container .portfolio_container .project .text_container span'],
		['h2'],
		['.alternative_container span:nth-child(2)'],
		['.contents_container .portfolio_container .project .img_container'],
		['.contents_container .portfolio_container .project .img_container img'],
		['.contents_container .contact_me_container .form_container .text'],
	]

	if ($(window).width() <= 812) {
		for (i = 0; i < class_array.length; i++) { 
			$(class_array[i][0]).addClass('mobile');
		}

	} else {
		for (i = 0; i < class_array.length; i++) { 
			$(class_array[i][0]).removeClass('mobile');
		}
	}
}

function check_project() {

	$('.project').click(function() {

		var project = $(this).attr('id');
		// console.log(window.location.href);

		if ($(this).hasClass('top')) {
			$('.overlay').show();
			$('.description.' + project).show();
			
			//  KP || Un-binds the pageOverlay
			$('.go-to').unbind('click');
			$('.go-to').bind('click', function(){
				$('.overlay').hide();
				$('.description.' + project).hide();
				redirect(project);
			});

			$('.overlay').unbind('click');
			$('.overlay').bind('click', function(){
				$('.overlay').hide();
				$('.description.' + project).hide();
			});

		} else {
			redirect(project);
		}
	});
}

function redirect(project) {

	if (project == 'importers') {
		// window.location.href = window.location.href + "login/";
		window.open(window.location.href + "login/");
	} else if (project == 'mrbm') {
		window.open(window.location.href + "mrbm/");
	} else if (project == 'gaming') {
		window.open("http://d8emrxif7467f.cloudfront.net/index.html");
	}
}


function scroll_to_div() {

	$('.scroll_to, .contact_me').click(function() {

		var div_id = $(this).attr('id').split('-');
		$(window).scrollTop( $('#position-' + div_id[1]).offset().top);
	});
}





function load_main_page() {

	$(".page_direct_cont").click(function () {

		// AJAX Call
		$.ajax({
			url: '/index/', //name of the function in views.py
			type: "POST", //POST to send information to views.py, OR GET to retrieve information
			data: {
			},
			complete: function (data) {  //allows us to return the value from views.py

				consol.log('yes');
				// Gets the returned string from python and split's to determine the status of the value
				// var output = data.responseText.split(' || ');

				// Checks if it was a SUCCESS
				// if (output[0] == 'SUCCESS') {

				// 	console.log(output[0]);
				// }
			}
		});
	});
}
