from django.shortcuts import render, redirect
from .models import Lead
from django.db.models import Q
import math

#shows the initial page
def leads(request):
	
	leads = Lead.objects.all()

	# determine the number of results
	number = int(math.ceil(len(leads)/10.0))

	# create an array called pages that we can iterate through to create the right number of links
	pages = []
	for i in range(0, number):
		pages.append(i+1)

	context = {'leads': leads[0:10], 'pages': pages}
	return render(request, 'ajax_leads/leads.html', context)

# search with pagination
def search(request, id):

	# first we'll get all the objects
	leads = Lead.objects.all()

	# if we have a "to" date, we'll filter the results with the "to" date
	if request.POST['to']:
		leads = leads.filter(register_date__lte = request.POST['to'])
	
	# if we have a "from" date, we'll filter the results with the "from" date
	if request.POST['from']:
		leads = leads.filter(register_date__gte = request.POST['from'])

	# if a text search is enterred, we'll filter for that text within first_name and last_name
	if request.POST['search']:
		first_name_match = Q(first_name__icontains = request.POST['search'])
		last_name_match = Q(last_name__icontains = request.POST['search'])
		leads = leads.filter(first_name_match | last_name_match)

	# determine the number of results
	number = int(math.ceil(len(leads)/10.0))
	# create an array called pages that we can iterate through to create the right number of links
	pages = []
	for i in range(0, number):
		pages.append(i+1)

	# if id == 0 then we will show the first ten results
	if int(id) == 0:
		start = 0
		end = 10
	# otherwise show the corresponding page of results
	else:
		end = int(id)*10
		start = end-10

	context = {'leads': leads[start:end], 'pages': pages}
	return render(request, 'ajax_leads/partials/lead_partial.html', context)

# for adding new leads to my database
def new(request):
	context = {'leads': Lead.objects.all()}
	return render(request, 'ajax_leads/new.html', context)

# handles creating new leads
def create(request):
	Lead.objects.create(
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		register_date = request.POST['register_date'],
		email = request.POST['email'])
	return redirect('/new')