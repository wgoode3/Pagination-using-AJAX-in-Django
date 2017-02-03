from django.shortcuts import render, redirect
from .models import Lead
from django.db.models import Q
import math

#shows the initial page
def leads(request):
	leads = Lead.objects.all()
	number = int(math.ceil(len(leads)/10.0))
	pages = []
	for i in range(0, number):
		pages.append(i+1)
	context = {
		'leads': leads[0:10],
		'pages': pages}
	return render(request, 'ajax_leads/leads.html', context)

# search with pagination
def search(request, id):

	# if id == 0 then we show the first ten results
	if int(id) == 0:
		start = 0
		end = 10
	else:
		end = int(id)*10
		start = end-10

	# get all objects
	leads = Lead.objects.all()

	# to date
	if request.POST['to']:
		leads = leads.filter(register_date__lte = request.POST['to'])
	
	# from date
	if request.POST['from']:
		leads = leads.filter(register_date__gte = request.POST['from'])

	# search
	if request.POST['search']:
		first_name_match = Q(first_name__icontains = request.POST['search'])
		last_name_match = Q(last_name__icontains = request.POST['search'])
		leads = leads.filter(first_name_match | last_name_match)

	number = int(math.ceil(len(leads)/10.0))
	pages = []
	for i in range(0, number):
		pages.append(i+1)

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

'''
# The way I built the query string when I was using raw SQL for search

	# build the query string
	query = "SELECT * FROM ajax_leads_lead"
		# both from and to dates
	if request.POST['to'] and request.POST['from']:
		f = "'"+request.POST['from']+"'"
		t = "'"+request.POST['to']+"'"
		query += " WHERE register_date BETWEEN {} AND {}".format(f, t)
		if request.POST['search']:
			s = "'%%"+request.POST['search']+"%%'"
			query += " AND first_name LIKE {} OR last_name LIKE {}".format(s, s)
	# to date
	elif request.POST['to']:
		t = "'"+request.POST['to']+"'"
		query += " WHERE register_date < {}".format(t)
		if request.POST['search']:
			s = "'%%"+request.POST['search']+"%%'"
			query += " AND first_name LIKE {} OR last_name LIKE {}".format(s, s)
	# from date
	elif request.POST['from']:
		f = "'"+request.POST['from']+"'"
		query += " WHERE register_date > {}".format(f)
		if request.POST['search']:
			s = "'%%"+request.POST['search']+"%%'"
			query += " AND first_name LIKE {} OR last_name LIKE {}".format(s, s)
	# just search
	elif request.POST['search']:
		leads = Lead.objects.filter(first_name_match | last_name_match)
		s = "'%%"+request.POST['search']+"%%'"
		query += " WHERE first_name LIKE {} OR last_name LIKE {}".format(s, s)

	query += " LIMIT 0, 10"
	print query
'''

