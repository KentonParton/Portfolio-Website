from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from about_me.mrbm import utils
from about_me.mrbm import compute

# Importing json for python
import json

def index(request):

	# Gets the left side HTML
	leftHTML = buildLeftSection(request)

	# Gets the playground HTML
	playgroundHTML = buildPlaygroundSection(request)

	# Gets the right side HTML
	rightHTML = buildRightSection(request)

	# Renders the base.html file and substitues the vairable in the template with our new variables
	return render(request, 'mrbm.html', { 'leftSect' : leftHTML, 'playground' : playgroundHTML, 'rightSect' : rightHTML })

# Builds the left side HTML
def buildLeftSection(request):

	# Initializes the data for the first wall type
	wallTypeData1 = [
		['compWall', 'Complete Wall'],
		['incompWall', 'Incomplete Wall']
	]

	# Initializes the data for the second wall type
	wallTypeData2 = [
		['0', '0'],
		['1', '1'],
		['2', '2'],
	]

	# Initializes the data for the count
	countData = [
		['0', '0'],
		['1', '1'],
		['2', '2'],
		['3', '3'],
		['4', '4'],
		['5', '5'],
		['6', '6'],
		['7', '7'],
		['8', '8']
	]

	display = [
		['window1','600 mm'],
		['window2','900 mm'],
		['window3','1200 mm'],
		['window4','1500 mm'],
		['window5','1800 mm'],
	]

	# Builds HTML
	html = ' \
		<div class="leftSect"> \
			<div class="logoSect"></div> \
			<div class="compuSect"> \
				<div class="header"> \
					<h1>Create Your Structure</h1> \
				</div> \
				' + utils.buildTextbox(request, 'Enter Your Wall Length. (mm)', 'wallLength', 'Please enter your wall length here. (millimeters)') + ' \
				' + utils.buildDropdown(request, 'Is it a Complete or Incomplete Wall?', 'wallType1', wallTypeData1) + ' \
				' + utils.buildDropdown(request, 'Number of Corner Juctions', 'wallType2', wallTypeData2) + ' \
				' + utils.buildDropdown(request, 'Number of T-Junctions', 'wallType3', countData) + ' \
				' + utils.buildDropdown(request, 'Number of Doors?', 'doors', countData) + ' \
				' + utils.buildCheckBox(request, 'Select your window lengths', display) + ' \
				' + utils.buildWindowDropdown(request, 'Select the number of 600 mm windows', 'window1Cont', 'window1Val' , countData) + ' \
				' + utils.buildWindowDropdown(request, 'Select the number of 900 mm windows', 'window2Cont', 'window2Val' , countData) + ' \
				' + utils.buildWindowDropdown(request, 'Select the number of 1200 mm windows', 'window3Cont', 'window3Val' , countData) + ' \
				' + utils.buildWindowDropdown(request, 'Select the number of 1500 mm windows', 'window4Cont', 'window4Val' , countData) + ' \
				' + utils.buildWindowDropdown(request, 'Select the number of 1800 mm windows', 'window5Cont', 'window5Val' , countData) + ' \
				<div class="buttonCont"> \
					<div class="button"> \
						<span>Show Results</span> \
					</div> \
				</div> \
			</div> \
		</div>'

	# Returns HTML
	return html

# Builds the playground HTML
def buildPlaygroundSection(request):

	# Builds HTML
	html = ' \
		<div class="playground"> \
			<div class = "zoom"> \
			<img src="../static/images/mrbm/zoomOut.svg"> \
			<img src="../static/images/mrbm/zoomIn.svg"> \
			</div> \
			<div class="popup"> \
				<span></span> \
			</div> \
		</div>'

	# Returns HTML
	return html

# Builds the Key HTML on right side of page
def buildRightSection(request):

	# Initializes a list for the shutters
	shutter_key = [
		['600 mm', 'shutterXl', 'Shutters'],
		['400 mm', 'shutterL'],
		['350 mm', 'shutterM'],
		['300 mm', 'shutterS'],
		['250 mm', 'shutterXs'],
	]

	junction_key = [
		['Corner-Junction', 'shutterC', 'cornerJunc', 'cPieceJunc', 'Junctions'],
		['T-Junction', 'shutterT', 'tJunc', 'tPieceJunc'],
	]

	window_key = [
		['1800 mm', 'windowXl' , 'Windows'],
		['1500 mm', 'windowL'],
		['1200 mm', 'windowM'],
		['900 mm', 'windowS'],
		['600 mm', 'windowXs'],
	]

	other_key = [
		['Door 900 mm', 'shutterD', 'Other']
	]

	key_list = [shutter_key, junction_key, window_key, other_key]


	# Builds HTML
	html = ' \
		<div class="rightSect"> \
			<div class="key"> '


	for key in key_list:

		html += ' \
			<div class="keyCont"> \
				<h2>' + str(key[0][-1]) + '</h2>'

		# Loops through shutter_key
		for element in key:	

			# Builds HTML for shutter_key
			html += ' \
				<div class="shutterCont"> '

			if key == window_key or key == other_key:

				html += '<h4>' + str(element[0]) + '</h4> '

			else:
				html += ' \
					<h3>' + str(element[0]) + '</h3> '

			html += '<div class="keyOutline"> '


			if key == junction_key:

				html += ' \
						<div class="' + element[1] + '"> \
							<div class="' + element[2] + '"></div> \
							<div class="' + element[3] + '"></div> \
						</div> \
					</div> \
				</div> '

			else:
				html += ' \
						<div class="' + str(element[1]) + '"></div> \
					</div> \
				</div>'

		html += '</div>'

	html += ' \
			</div> \
		</div>'

	return html

def inputAccept (request):

	# stores number of walls created
	wallCount = request.POST['wallCount']

	# request the array inputArray from jquery file general.js
	inputArray = request.POST['inputArray']
	inputArray = json.loads(inputArray)

	#Computes the list of shutters needed to create the wall
	containerList = compute.runFunctions(inputArray)

	# if the errorMsg list is empty(there is no error) run compute.countShutters
	if containerList[-2] == []:
		# Adds up the number or each shutter type needed
		countShutterList = compute.countShutters(inputArray, containerList)


		# Builds the HTML for the wall
		html = buildWallHTML(request, wallCount, countShutterList)

		# Returns Success followed by the correct html
		return HttpResponse('SUCCESS || ' + html)

	# this will return an error message which will be used in general.js function.
	else:

		# Error List
		errorList = [
			['invalidInput', 'The wall length is shorter than the length of the doors and windows entered'],
			['indexError', 'This value cannot be computed, please try a slightly different number'],
			['multiple', 'The wall length entered is not a multiple of 50']
		]

		# Initialize the error message - Default message
		errorMsg = 'There has been an error encountered.'

		# Loops through the error list
		for error in errorList:

			# Checks if the error exists in the list
			if str(error[0]) == str(containerList[-2][0]):
				# Gets the error message
				errorMsg = str(error[1])

		# Returns Error followed by the error
		return HttpResponse('ERROR || ' + errorMsg)

# Builds the HTML for the wall here
def buildWallHTML(request, wallCount, countShutterList):

	cCount = 0
	tCount = 0

	control_array = [
		['1', 'rotate', '../static/images/mrbm/toolbar/rotate.svg', 'Rotate Wall'],
		['2', 'delete', '../static/images/mrbm/toolbar/delete.svg', 'Delete Wall'],
		['3', 'sort', '../static/images/mrbm/toolbar/sort.svg', 'Sort Shutters'],
		['4', 'switch', '../static/images/mrbm/toolbar/switch.svg', 'Switch Corner-junction, click it!'],
		['5', 'flip', '../static/images/mrbm/toolbar/flip.svg', 'Flip Corner/T Junction, click it!'],
		['6', 'drag', '../static/images/mrbm/toolbar/drag.svg', 'Drag Wall'],
	]

	# Builds HTML
	html = ' \
		<div class="mainBlock" id="draggable-' + wallCount + '"> \
			<div class="toolbar"> '

	# constructs the control-bar for each wall.
	for controls in control_array:

		html += ' \
				<div id="control-' + controls[0] + '" title="' + controls[3] + '" class="controls" data-type="' + controls[1] + '" data-id="' + wallCount + '"> \
					<div class="' + controls[1] + '" > \
						<img src="' + controls[2] + '"> \
					</div> \
				</div> '

	html += ' \
			</div> \
			<div class="arrow"></div> \
			<div class="dragBlock"> \
				<div id="wall-' + str(wallCount) + '" class="wallCont">'

	# Builds shutters in each wall
	for shutter in countShutterList:

		for shutterCount in xrange(shutter[1]):

			if shutter[0] == 'shutterC':

				cCount = cCount + 1

				html += ' \
					<div id="shutC-'+ str(cCount) +'" class="' + str(shutter[0])+ '" >\
						<div class="cornerJunc"></div>\
						<div class="cPieceJunc"></div>\
					</div>'

			elif shutter[0] == 'shutterT':

				tCount = tCount + 1

				html += ' \
					<div id="shutT-'+ str(tCount) +'" class="' + str(shutter[0])+ '" >\
						<div class="tJunc"></div>\
						<div class="tPieceJunc"></div>\
					</div>'

			else:
				# Builds HTML
				html += '<div class="' + str(shutter[0])+ '" ></div>'

	# Builds HTML
	html += '\
				</div> \
			</div> \
		</div>'

	return html
