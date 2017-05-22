from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Application, ApplicationForm

def application(request):
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


def application_status(request, id):
	application = Application.objects.get(id=id)
	status_str = [s for s in Application.APPLICATION_STEPS if s[0] == application.step][0][1]
	return render(request, "shoppers/application_status.html", {'application': application, 'status': status_str})


def index(request):
	if request.method == "POST":
		email = request.POST['email']
		request.session['email'] = email
		application = Application.objects.filter(email=email)
		if application:
			application = application[0]
			return redirect('application_status', id=application.id)
		else:
			return redirect('application')
	else:
		return render(request, "shoppers/index.html")
