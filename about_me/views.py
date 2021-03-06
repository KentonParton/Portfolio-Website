from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Importing json for python
import json
import requests
import pprint

def index(request):
	
	# Static section of the page
	mainHTML = build_main_page(request)

	# Renders the base.html file and substitues the vairable in the template with our new variables
	return render(request, 'base.html', { 'mainSect' : mainHTML })


def build_main_page(request):
	
	html = ' \
		<div class="landing_container"> \
			<div class="header_container"> \
				<div class="my_name">Kenton Parton</div> \
				<img class="drop_down" src="./static/images/about_me/drop_down.svg"> \
				<div class="menus"> \
					<div id="scroll_to-2" class="scroll_to">About Me</div> \
					<div id="scroll_to-3" class="scroll_to">Portfolio</div> \
					<div id="scroll_to-4" class="scroll_to">Contact Me</div> \
				</div> \
			</div> \
			<div class="welcome_container"> \
				<div id="info-1" class="information"> \
					<div id="first" class="about_me"> \
						<span>Major:</span> \
						<span>Minor:</span> \
						<span id="gpa">GPA:</span> \
						<span>Graduation:</span> \
						<span>Studying at:</span> \
					</div> \
					<div id="second" class="about_me"> \
						<span>Information Systems</span> \
						<span>Computer Science</span> \
						<span id="font-1">3.7</span> \
						<span id="font-2">Spring</span> \
						<span id="font-3">2019</span> \
						<span>University of Alabama at Birmingham</span> \
					</div> \
				</div> \
				<div id="info-2" class="information"> \
					<div class="languages"> \
						<div class="language"> \
							<span>Python</span> \
							<span>Django</span> \
							<span>Java</span> \
							<span>JavaScipt</span> \
							<span>CSS</span> \
							<span>HTML</span> \
							<span>Cordova</span> \
						</div> \
					</div> \
				</div> \
				<div id="info-3" class="information"> \
					<div class="internship"> \
						<div class="text"> \
							<span>Seeking a 2018 Summer Internship! Give me the opportunity to impact your business.</span> \
						</div> \
						<div id="contact_me-4" class="contact_me">Contact Me</div> \
					</div> \
				</div> \
			</div> \
			<div class="comp_container"> \
				<div class="position_projects"> \
					<img class="computer" src="./static/images/imac.svg"> \
					<div class="projects_container"> \
						<div id="importers" class="project top"> \
							<div class="img_container"> \
								<img src="./static/images/about_me/box.svg"> \
							</div> \
							<div class="text_container"> \
								<span class="demo">Order Tracking System</span> \
							</div> \
						</div> \
						<div id="mrbm" class="project top"> \
							<div class="img_container"> \
								<img src="./static/images/about_me/sketch.svg"> \
							</div> \
							<div class="text_container"> \
								<span class="demo">Modular Building System</span> \
							</div> \
						</div> \
						<div id="gaming" class="project top"> \
							<div class="img_container"> \
								<img src="./static/images/about_me/gaming.svg"> \
							</div> \
							<div class="text_container"> \
								<span class="demo">Gaming Website</span> \
							</div> \
						</div> \
					</div> \
				</div> \
			</div> \
		</div> \
		<div class="contents_container"> \
			<div class="header black" id="position-2">About Me</div> \
			<div class="header_triangle black"></div> \
			<div class="about_me_container"> \
				<!--div class="img_container"> \
					<img src="./static/images/about_me/me.jpg">\
				</div--> \
				<div class="paragraph_container"> \
					<div class="paragraph"> \
						<span>&ldquo;Intuitive design and functionality are how we give the user new superpowers.&rdquo;</span> \
					</div> \
					<div class="paragraph"> \
						<span>I am a skilled developer, who strives to create applications with flawless functionality and a unique user experience. </span> \
					</div> \
					<div class="paragraph"> \
						<span>Through my personal projects and internship experiences, I have realized that I love working with clients directly or with a team to create innovative solutions. Furthermore, my enthusiasm for technology, business, and the future inspires me to learn new things whenever an opportunity arises.</span> \
					</div> \
					<div class="paragraph"> \
						<span>My major in Information Systems and minor in Computer Science have enriched my skills in object modeling and programming, providing me with both the skill-set to communicate between both programmers and non tech related titles. Balancing an undergraduate course load in Information Systems and Computer Science presents challenges as it is; however, with the addition of being a Division-I tennis player at UAB, I have learned how to manage my time between many tasks and commitments.</span> \
					</div> \
				</div> \
			</div> \
			<div class="portfolio_container"> \
				<div class="header white" id="position-3">Portfolio</div> \
				<div class="header_triangle white"></div> \
				<div id="importers" class="project"> \
					<h2>Order Tracking System</h2> \
					<div class="img_container"> \
						<img src="./static/images/about_me/box.svg"> \
					</div> \
					<div class="text_container"> \
						<span>Created a web-application for a company named Importers Coffee Specialists who distribute coffee and coffee related products to retailers throughout South Africa. This web-application bridges the communication gap between employees, who pack the contents of each order, and upper-level employees who enter the orders into the system. The secondary purpose of this web-applicatoin is to track and display customer orders to employees who will pack the necessary items. Each order details the contents and the time remaining for the order to be packed and loaded. An app is currently in progress which displays packed orders to the companies delivery drivers. This will allow Importers Coffee Specialists to oversee a larger portion of their processes. Django is the primary framework used in this project. Please feel free to interact with the web-app by adding new products, clients or orders.</span> \
					</div> \
				</div> \
				<div id="mrbm" class="project"> \
					<h2>Modular Building System</h2> \
					<div class="img_container"> \
						<img src="./static/images/about_me/sketch.svg"> \
					</div> \
					<div class="text_container"> \
						<span>I built a modular building system for a company named Mobile Rapid Building Methods (MRBM), who utilize a building system which reduces the time and labor to build a structure. The building system combine different sized shutters to create the walls of the building. My web-app calculates the most efficient combinations of each shutter to build the various portions of the structure. This process was previously done by hand through trial an error.</span> \
					</div> \
				</div> \
				<div id="gaming" class="project"> \
					<h2>Gaming Website</h2> \
					<div class="img_container"> \
						<img src="./static/images/about_me/gaming.svg"> \
					</div> \
					<div class="text_container"> \
						<span>I love to play first-person shooters when the time permits it. My enjoyment for playing well-built games lead me to create a fun website which displays some of the tools and tweaks I have used and learnt while playing. This is also the first website I built, which I have not changed, as a reminder of where I started.</span> \
					</div> \
				</div> \
			</div> \
			<div class="contact_me_container"> \
				<div class="header green" id="position-4">Contact Me</div> \
				<div class="header_triangle green"></div> \
				<div class="form_container"> \
					<div class="alternative_container"> \
						<a href="mailto:kknoxparton@gmail.com">CLICK HERE TO EMAIL ME.</a> \
					</div> \
				</div> \
				<div class="form_container"> \
					<div class="text"> \
						<span>I am always looking for new opportunities, projects, and things to learn. Feel free to reach out to me if you have something exciting to talk about, job/internship opportunities, or if you just want to talk.</span> \
						<span>I look forward to hearing from you.</span> \
					</div> \
				</div> \
			</div> \
		</div> '

	return html


	