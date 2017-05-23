import datetime
import random
import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from .models import Application, ApplicationForm

from django.db.models.functions import ExtractYear, ExtractWeek, ExtractMonth

def application(request):
	if not request.session.get('email'):
		return redirect('index')

	if request.method == "POST":
		form = ApplicationForm(request.POST)
		if form.is_valid():
			for field in form.fields:
				request.session[field] = form.cleaned_data[field]
			return redirect('background_check')
	else:
		form = ApplicationForm()

	return render(request, 'shoppers/application.html', {'form': form, 'email': request.session['email']})


def background_check(request):
	if not request.session.get('email'):
		return redirect('index')

	if request.method == "POST":
		application = Application(email=request.session['email'], name=request.session['name'],
				phone=request.session['phone'], zipcode=request.session['zipcode'])
		application.save()

		# delete user information from session
		del request.session['name']
		del request.session['email']
		del request.session['zipcode']
		del request.session['phone']

		return redirect('application_status', id=application.id)
	else:
		return render(request, "shoppers/background_check.html", 
				{'email': request.session['email'], 'name': request.session['name']})


def application_status(request, id, new_application=True):
	application = Application.objects.get(id=id)
	status_str = Application.step_str(application.step)
	return render(request, "shoppers/application_status.html", 
		{'application': application, 'status': status_str, 'existing_application': request.session.get('existing_application')})


def index(request):
	request.session.pop('existing_application', None)
	if request.method == "POST":
		email = request.POST['email']
		request.session['email'] = email
		application = Application.objects.filter(email=email)
		if application:
			application = application[0]
			request.session['existing_application'] = True
			return redirect('application_status', id=application.id)
		else:
			return redirect('application')
	else:
		return render(request, "shoppers/index.html")


def _convert_data_to_funnel(data):
	# Create a funnel from the buckets of data.
	num_hired = data.get(Application.step_str(6), 0)
	num_rejected = data.get(Application.step_str(7), 0)
	curr_sum = num_hired + num_rejected + data.get(Application.step_str(5), 0)
	data[Application.step_str(5)] = curr_sum
	curr_sum += data.get(Application.step_str(4), 0)
	data[Application.step_str(4)] = curr_sum
	curr_sum += data.get(Application.step_str(3), 0)
	data[Application.step_str(3)] = curr_sum
	curr_sum += data.get(Application.step_str(2), 0)
	data[Application.step_str(2)] = curr_sum
	curr_sum += data.get(Application.step_str(1), 0)
	data[Application.step_str(1)] = curr_sum
	return data		


def applicant_analysis(request):
	try:
		from_dt = datetime.datetime.strptime(request.GET.get('from', ''), "%Y-%m-%d").date()
		to_dt = datetime.datetime.strptime(request.GET.get('to', ''), "%Y-%m-%d").date()
	except ValueError:
		return HttpResponseBadRequest()
	if not from_dt or not to_dt:
		return HttpResponseBadRequest()

	applications = Application.objects \
			.filter(created_dt__gte=from_dt, created_dt__lte=to_dt) \
			.annotate(week=ExtractWeek('created_dt'), year=ExtractYear('created_dt'), month=ExtractMonth('created_dt')) \
			.values_list('week', 'year', 'step', 'month')

	# group data by year+week+step
	data = {}
	for application in applications:
		week = application[0]
		year = application[1]
		step = Application.step_str(application[2])
		month = application[3]

		# special stuff for last week of year / first week of year..
		if week == 52 and month == 1:
			year -= 1
		elif week == 1 and month == 12:
			year += 1
		key = (week, year) # key is a (week, year) tuple
		curr = data.get(key, {})
		curr[step] = curr.get(step, 0) + 1
		data[key] = curr

	# convert year-week to date ranges and data into funnel
	new_data = {}
	for ((week, year), value) in data.iteritems():
		d = "%s-W%s" % (year, week)
		from_date = datetime.datetime.strptime("%s-1" % d, "%Y-W%W-%w")
		to_date = datetime.datetime.strptime("%s-0" % d, "%Y-W%W-%w")
		new_key = "%s-%s" % (from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")) 
		new_data[new_key] = _convert_data_to_funnel(value)

	return HttpResponse(simplejson.dumps(new_data), content_type="application/json")
