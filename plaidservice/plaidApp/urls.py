from django.urls import path
from . import views

app_name = 'plaid'
urlpatterns = [
    path('',views.index,name='index'),
    path('log_in', views.log_in, name='log-in'),
    path('log_in_form', views.log_in_form, name='log-in-form'),
    path('log_out', views.log_out, name='log-out'),
    path('signup', views.signup, name="signup"),
    path('create_user', views.create_user, name='create-user'), 
    path('transactions', views.transactions, name='transactions'),
    path('create_link_token', views.create_link_token, name='create-link-token'),
    path('refresh_accounts', views.refresh_accounts, name='refresh-accounts'),
    


]

#    path('auth', views.get_auth, name="get-auth"),       