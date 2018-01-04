from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
import sqlite3
import json
from about_me.importers.orders.models import Order, ProductItem, Client, Product


@login_required(login_url='../')
@csrf_protect
def index(request):

	status = displayAdmin(request)

	status = displayAdmin(request)

	status = displayAdmin(request)

	# Gets the playground HTML
	playgroundHTML = buildPlaygroundSection(request)

	# Renders the base.html file and pwdsubstitues the vairable in the template with our new variables
	return render(request, 'orders/base.html', { 'displayAdmin' : status, 'playground' : playgroundHTML })


def getBaseURL(request):

	# gets full url
	URL = request.get_full_path().split('/')
	# gets url extension
	URL = URL[0]

	return URL

def displayAdmin(request):

	# checks if user has is_staff status
	status = is_staff(request)

	if status == True:

		# runs getBase URL function
		URL = getBaseURL(request)

		# displays ADMIN section button if 'is_staff = True'
		html = ' \
			<div class="btnCont" > \
				<a class="headBtn" title="Admin" href="' + URL + '/admin"></a> \
			</div> '

		return html

	else:

		html = ''

		return html


# Builds the playground HTML
def buildPlaygroundSection(request):

	times = [
		['Past Due'],
		['2 hrs'],
		['6 hrs'],
		['12 hrs'],
		['24 hrs'],
	]

	# Builds HTML
	html = ' \
		<div class="playground"> \
		<div class="block"></div> '

	for i in range(len(times)):

		html += ' \
			<div id="row' + str(i) + '" class="row"> \
				<div class="timesCont"> \
					<div class="times"> \
						<h4>' + str(times[i][0]) + '</h4> \
					</div> \
				</div> \
				<div class="orderCont"> \
					<div class="column" id="column-1"></div> \
					<div class="column" id="column-2"></div> \
					<div class="column" id="column-3"></div> \
				</div> \
			</div> '

	html += '<div class="notice">Please note that all product and client information has been randomly created and are purely for demonstration purposes.</div>'

	# Returns HTML
	return html

# orders and products query
def GETvalues(request):

	currentPage = request.POST['currentPage']

	if currentPage == '':
		return HttpResponse('SUCCESS')

	#connects to db
	conn = sqlite3.connect('db.sqlite3')

	sql_orders = """SELECT orders_order.id,
			orders_order.client_id,
			orders_client.client,
			orders_order.order_number,
			orders_order.due
		FROM orders_order
		INNER JOIN orders_client ON orders_order.client_id = orders_client.id
		WHERE orders_order.status = ''"""

	sql_products = """SELECT orders_productitem.order_number_id,
			orders_product.name,
			orders_product.description,
			orders_product.product_code,
            orders_product.volume,
			orders_productitem.quantity
		FROM orders_productitem
		INNER JOIN orders_product ON orders_productitem.product_id = orders_product.id"""


	# connects to the section that was selected in each query
	orders = conn.execute(sql_orders)
	products = conn.execute(sql_products)

	#will contain ID's of each order
	countID = []

	#will contain times of each order
	times = []

	# counts number of orders
	countOrders = 0
	static_list = []
	product_list = []

	for order in orders:

		static_list.append(order)
		times.append(order[4])
		countID.append(order[0])

		countOrders += 1

	for product in products:

		product_list.append(product)


	times = json.dumps(times)
	countID = json.dumps(countID)
	conn.commit()

	# checks if user is a super user
	superUser = is_superuser(request)
	# checks if is_staff = True
	staff = is_staff(request)


	if currentPage == 'orders':

		html = buildOrdersHTML(request, static_list, product_list)

		# Returns Success followed by the correct html
		return HttpResponse('SUCCESS || ' + html + ' || ' + str(countOrders) + ' || ' + str(times) + ' || ' + str(countID))


	elif currentPage == 'preview':

		html = buildPreviewPage(request, static_list, product_list)

		return HttpResponse('SUCCESS || ' + html + ' || ' + str(countOrders) + ' || ' + str(times) + ' || ' + str(countID))

# checks if user is a super user
def is_superuser(request):

	current_user = request.user

	return current_user.is_superuser

# checks if is_staff
def is_staff(request):

	current_user = request.user

	return current_user.is_staff

# builds the HTML for all incompleted orders
def buildOrdersHTML(request, static_list, product_list):
	#print 'build = '+str(order_list)
	html = '<div class="pageOverlay"></div> '

	counter = 1

	for static in static_list:

		divID = str(static[0])
		notSure = str(static[1])
		client = str(static[2])
		ordNum = str(static[3])
		dateDue = str(static[4])
		numItems = int(0)

		# places orders in correct column
		if counter % 3 == 1:

			html += '<div class="ordCont" id="'+ divID + '" column="column-1">'

		if counter % 3 == 2:

			html += '<div class="ordCont" id="'+ divID + '" column="column-2">'

		if counter % 3 == 0:

			html += '<div class="ordCont" id="'+ divID + '" column="column-3">'


		counter += 1

		# Builds HTML
		html += ' \
				<div id="block-' + divID + '" class="colorBlock"></div> \
				<div class="ordHeader" id="header-'+ divID +'"> \
					<div class="timer" id="timer-'+ divID +'" data-countdown="' + dateDue + '"> </div> \
					<div class="title" id="info3">' + client + '</div> \
					<div class="orderNum"> \
						<div id="digit-' + divID + '" class="digit">' + ordNum + '</div> \
					</div> \
					<div class="buttonCont"> \
						<div id="overlay-' + divID + '" class="ordOverlay"></div> '

		staff = is_staff(request)

		# displays complete button based on staff staus
		if staff is True:

			html += ' \
				<div id="button-'+ divID +'" data-id="'+ divID +'" class="btn-complete"></div> \
				<div class="background"></div> '


		for product in product_list:

			if divID == str(product[0]):

				numItems = numItems + int(product[5])

		html += '<div class="numItems" id="items-' + divID + '">'+ str(numItems) +' Items</div> '

		html += ' \
						<div class="promptCont" id="prompt-'+ divID +'"> \
							<div class="decision"> \
								<p class="yes">Yes</p> \
							</div> \
							<div class="decision"> \
								<p class="no">No</p> \
							</div> \
						</div> \
					</div> \
				</div> \
				<div class="prodDetails"> \
					<div class="prodRow header"> \
						<div class="col" >Product</div> \
						<div class="col" >Code</div> \
						<div class="col" >Volume</div> \
						<div class="col" >Qty</div> \
					</div>'

		# builds product information
		for product in product_list:

			if divID == str(product[0]):

				html += ' \
					<div class="prodRow" > \
						<div class="col">' + str(product[1]) + ' ' + str(product[2]) + '</div> \
						<div class="col">' + str(product[3]) + '</div> \
						<div class="col">' + str(product[4]) + '</div> \
						<div class="col">' + str(product[5]) + '</div> \
					</div> '

		html += '\
			</div> \
		</div>'

	return html


#updates complete bool in db when order is completed
def changeDB(request):

	#gets removeOrderID variable from jQuery
	removeOrderID = request.POST["removeOrderID"]

	#connects to db
	createDb = sqlite3.connect('db.sqlite3')

	#selects timeStamp_order table
	queryCurs = createDb.execute("SELECT * FROM orders_order")

	sql = """
	UPDATE orders_order
	SET status = 0
	WHERE id = ?
	"""

	queryCurs.execute(sql, (removeOrderID,))

	createDb.commit()


	return HttpResponse('SUCCESS')
