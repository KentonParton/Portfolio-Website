'''
@file:		utils.py
@author: 	Kenton Parton
@function:	Page has generic functions that we can re-use
'''

def buildCheckBox(request,title, display):
	
	#Builds  HTML
	html = ' \
		<div class="inputCont"> \
			<h4>' + str(title) + '</h4> \
			<div class="windowSizeCont"> '
	
	for data in display:
		html += ' \
			<div class="windowSizes"> \
				<div class="checkbox"> \
					<input type="checkbox" id="' + data[0] + '" title="' + data[1] + '"> \
				</div> \
				<h6>' + str(data[1]) + '</h6> \
			</div>'
	html += ' \
		</div> \
	</div> '	
	
	return html
		
def buildWindowDropdown(request, title, inputID, divID, dropdownData):
	
	# Builds HTML
	html = '\
		<div class="windowCont" id="' + inputID + '"> \
			<div class="inputCont" > \
				<h4>' + str(title) + '</h4> \
					<select id="' + divID + '" title="' + title + '"> \
						<option value="">Select an option.</option>'
					
	# loops through the data
	for data in dropdownData:
		
		# Builds HTML
		html += '<option value="' + data[0] + '">' + data[1] + '</option>'
		
	# Builds HTML
	html += ' \
				</select> \
			</div>\
		</div> '
	
	#returns html for window dropdowns
	return html
	
# Builds textbox based on input
def buildTextbox(request, title, divID, placeholder=''):
	
	# Builds HTML
	html = '\
		<div class="inputCont"> \
			<h4>' + str(title) + '</h4> \
			<input type="text" id="' + divID + '" name ="' + divID + '" placeholder="' + placeholder + '"> \
		</div>'

	# Returns HTML for the newly constructed dropdown
	return html

# Builds Dropdown lists based on input
def buildDropdown(request, title, divID, dropdownData):
	
	# Builds HTML
	html = '\
		<div class="inputCont"> \
			<h4>' + str(title) + '</h4> \
				<select id="' + divID + '" title="' + title + '"> \
					<option value="">Select an option.</option>'
					
	# loops through the data
	for data in dropdownData:
		
		# Builds HTML
		html += '<option value="' + data[0] + '">' + data[1] + '</option>'
		
	# Builds HTML
	html += ' \
			</select> \
		</div>'

	# Returns HTML for the newly constructed dropdown
	return html