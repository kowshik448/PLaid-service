from django.shortcuts import render
from django.http import  HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Transaction, Account
from django.views.decorators.csrf import  ensure_csrf_cookie
import json
import plaid
from plaid import Client
import os

plaid_client_id = os.environ.get('PLAID_CLIENT_ID')
plaid_secret = os.environ.get('PLAID_SECRET')

client = Client(client_id=plaid_client_id,
				secret=plaid_secret,
				environment='sandbox')
logged_in = False
access_token=None
def index(request):
	
	username = latest_transactions = accounts = None
	user = request.user
	global logged_in

	if user.is_authenticated:
		latest_transactions = user.transaction_set.order_by('-date')[:5]
		logged_in = user.is_authenticated
		accounts = user.account_set.order_by('name')
		username = user.username

	data = {
		'latest_transactions': latest_transactions,
		'logged_in': logged_in,
		'accounts': accounts,
		'username': username
	}
	return render(request, 'index.html', data)

def log_in(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		print('invalid credentials')
	return HttpResponseRedirect('/', {'username': username})

def log_in_form(request):
	return render(request, 'log-in.html',)

def log_out(request):
	logout(request)
	return HttpResponseRedirect('/')

def signup(request):
	
	return render(request, 'signup.html',)

def create_user(request):
	username = request.POST.get('username')
	email = request.POST.get('email','user@gmail.com')
	password = request.POST.get('password')
	user = User(email = email, username= username, password =password)

	
	user.save()
	print('User created successfully')
	return HttpResponseRedirect('/log_in_form')

def transactions(request):
	global logged_in

	username = all_transactions = None
	user = request.user

	if user.is_authenticated:
		all_transactions = user.transaction_set.order_by('-date')
		paginator = Paginator(all_transactions, 50)

		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)

		logged_in = user.is_authenticated
		username = user.username

	data = {
		'all_transactions': all_transactions,
		'logged_in': logged_in,
		'username': username,
		'page_obj': page_obj,
	}
	return render(request, 'transactions.html', data)

def refresh_accounts(request):
	user = request.user
	items = user.plaiditem_set.all()
	print(items)

	for item in items:
		access_token = item.access_token
		response = client.Accounts.get(access_token)

		accounts = response['accounts']
		print(response)
		for account in accounts:
			acc = Account.objects.get(plaid_account_id=account['account_id'])
			acc.balances = account['balances']
			acc.mask = account['mask']
			acc.name = account['name']
			acc.official_name = account['official_name']
			acc.subtype = account['subtype']
			acc.account_type = account['type']
			acc.save()


	return HttpResponseRedirect('/')

@ensure_csrf_cookie
def create_link_token(request):
	user = request.user

	if user.is_authenticated:
		data = {
			'user': {
				'client_user_id': str(user.id)
			},
			'products': ["transactions"],
			'client_name': "John's Finance App",
			'country_codes': ['US'],
			'language': 'en'
		}

		response = { 'link_token': client.post('link/token/create', data) }

		link_token = response['link_token']
		return JsonResponse(link_token)
	else:
		return HttpResponseRedirect('/')

def get_access_token(request):
    global access_token

    public_token = request.POST['public_token']
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']
    
    return JsonResponse(exchange_response)

# def get_auth(request):
# 	user = request.user

# 	try:
# 		auth_response = client.post('auth/get', access_token)
# 	except plaid.errors.PlaidError as e:
# 		return JsonResponse({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } })
# 	json.dumps(auth_response, sort_keys=True, indent=4)
# 	print(auth_response)
# 	return JsonResponse({'error': None, 'auth': auth_response})