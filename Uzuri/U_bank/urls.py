from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('learn/', views.learn, name='learn'),
    path('register/', views.register, name='register'),
    path('admin_page/', views.admin_page, name='admin_page'),  # Name matches the view
    path('client_page/', views.client_page, name='client_page'),  # Name matches the view
    path('login/', views.login, name='login'),
    
    #client urls
    path('account/', views.account, name='account'),
    path('clientLoan/', views.clientLoan, name='clientLoan'),
    path('clientprofile/', views.clientprofile, name='clientprofile'),
    path('transaction', views.transaction, name='transaction'),
    
    #admin urls
    path('accounts/', views.accounts, name='Accounts'),
    path('logs/', views.logs, name='Logs'),
    path('loans/', views.admin_loans, name='Loans'),
    path('clients/', views.clients, name='Clients'),
    path('adminprofile/',views.adminprofile, name='adminprofile'),
]
