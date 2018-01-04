from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from about_me.importers.orders.models import Order, ProductItem


def send_intransit_email(sender, **kwargs):
	order = kwargs["instance"]

	if order.status == '1' and order.old_status == '0':
		client = order.client
		products = order.products()

		context = {
			"order": order,
			"client": client,
			"products": products,
		}
		message_text = render_to_string("email/intransit.txt", context)
		message_html = render_to_string("email/intransit.html", context)
		send_mail(
			"Your order is on its way!",
			message_text,
			"tom.masojada@gmail.com",
			["tom.masojada@gmail.com"],
			html_message=message_html
		)
  	else:
  		pass

post_save.connect(send_intransit_email, sender=Order)





