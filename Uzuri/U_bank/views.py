from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Client, PasswordImage, Account, Loan, TransactionHistory, DepositHistory, Logs
from . forms import ClientForm, LoginForm, DepositForm, LoanApplicationForm, ClientProfileForm
from django.db import IntegrityError
from .utilis import calculate_total_accounts
from .utilis import calculate_grand_total
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from decimal import Decimal
import requests
import json
from django.db.models import Sum

def index(request):
  return render(request, 'home/index.html')

def about(request):
  return render(request, 'home/about.html')

API_KEY = 'a3ade2274dd6810b92f6d404'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

def get_exchange_rate():
    """Fetches exchange rates from the API."""
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()

        if data.get('result') == 'success':
            return data.get('conversion_rates', {})
        else:
            print("API request failed:", data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def learn(request):
    """Handles currency conversion requests."""
    rates = get_exchange_rate()  # Fetch exchange rates

    if request.method == 'POST' and rates:
        from_currency = request.POST.get('from_currency', '').upper()
        to_currency = request.POST.get('to_currency', '').upper()

        try:
            amount = float(request.POST.get('amount', 0))
        except ValueError:
            amount = 0

        # Validate input currencies and perform conversion
        if from_currency in rates and to_currency in rates and amount > 0:
            from_rate = rates[from_currency]
            to_rate = rates[to_currency]
            converted_amount = (amount / from_rate) * to_rate
        else:
            converted_amount = None  # Invalid input case

        return render(request, 'currency/exchange_rate.html', {
            'rates': rates,
            'converted_amount': converted_amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount
        })

    return render(request, 'home/learn.html', {'rates': rates})



def learn(request):
  return render(request, 'home/learn.html')



def register(request):
    # Fetch all PasswordImage objects to display in the template
    password_images = PasswordImage.objects.all()

    context = {
        'client_form': ClientForm(),
        'password_images': password_images,  # Pass images to the template
        'error': None,  # Default error is None
    }

    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)
        selected_image_ids = request.POST.getlist('password_images')  # Get selected image IDs from checkboxes

        if client_form.is_valid():
            try:
                # Check if the client already exists
                id_number = client_form.cleaned_data.get('ID_Number')
                email = client_form.cleaned_data.get('Email')
                username = client_form.cleaned_data.get('Username')
                account_number = client_form.cleaned_data.get('Account_Number')

                if Client.objects.filter(ID_Number=id_number).exists():
                    context['error'] = "Client with this ID Number already exists."
                    context['client_form'] = client_form
                    return render(request, 'home/register.html', context)

                if Client.objects.filter(Email=email).exists():
                    context['error'] = "Client with this Email already exists."
                    context['client_form'] = client_form
                    return render(request, 'home/register.html', context)

                if Client.objects.filter(Username=username).exists():
                    context['error'] = "Client with this Username already exists."
                    context['client_form'] = client_form
                    return render(request, 'home/register.html', context)

                if Client.objects.filter(Account_Number=account_number).exists():
                    context['error'] = "Client with this Account Number already exists."
                    context['client_form'] = client_form
                    return render(request, 'home/register.html', context)

                # Fetch valid PasswordImage objects
                valid_images = PasswordImage.objects.filter(id__in=selected_image_ids)
                valid_image_ids = set(valid_images.values_list('id', flat=True))

                # Identify invalid IDs
                invalid_image_ids = set(map(int, selected_image_ids)) - valid_image_ids
                if invalid_image_ids:
                    context['error'] = f"Invalid images selected: {', '.join(map(str, invalid_image_ids))}"
                    context['client_form'] = client_form
                    return render(request, 'home/register.html', context)

                # Save the client
                client = client_form.save(commit=False)
                client.save()
                # Associate the selected images with the client
                client.Password_Image.set(valid_images)  # Use `set()` to assign images

                return redirect('home:login')  # Redirect to login page on success

            except IntegrityError as e:
                context['error'] = f"Database error: {str(e)}"
            except Exception as e:
                context['error'] = f"An unexpected error occurred: {str(e)}"
        else:
            context['error'] = "Form validation failed."
            context['client_form'] = client_form

    return render(request, 'home/register.html', context)


def login(request):
    password_images = PasswordImage.objects.all()
    context = {
        'form': LoginForm(),  # Initialize the form for GET requests
        'password_images': password_images,
        'error': None,
    }

    if request.method == 'POST':
        form = LoginForm(request.POST)
        selected_image_ids = request.POST.getlist('password_images')

        if form.is_valid():
            username = form.cleaned_data['Username']
            try:
                client = Client.objects.get(Username=username)
                password_images_in_db = client.Password_Image.all().order_by('id')
                selected_image_ids = list(map(int, selected_image_ids))

                # Validate the number of selected images
                if len(selected_image_ids) != len(password_images_in_db):
                    context['error'] = "Invalid number of images selected. Please select the correct number of images."
                # Validate the sequence of selected images
                elif selected_image_ids == [image.id for image in password_images_in_db]:
                    # Log the login action
                    Logs.objects.create(
                        client=client,
                        action='LOGIN',
                        details=f"User {client.Username} logged in."
                    )

                    # Set the client ID in the session
                    request.session['client_id'] = client.Client_ID

                    # Redirect based on user role
                    if username == 'admin':
                        return redirect(reverse('home:admin_page'))  # Redirect admin to admin page
                    else:
                        return redirect(reverse('home:client_page'))  # Redirect regular users to client page
                else:
                    context['error'] = "Invalid password. The selected images do not match the required sequence."

            except Client.DoesNotExist:
                context['error'] = "Invalid username. Please check your credentials."
        else:
            context['error'] = "Form validation failed. Please check your inputs."

        # Update the context with the form and error messages
        context['form'] = form

    return render(request, 'home/login.html', context)

@login_required
def admin_page(request):
    return render(request, 'admin/adminhome.html')


#client views
@login_required
def account(request):
    # Check if the logged-in user is the admin
    if request.user.username == 'admin':
        return redirect(reverse('home:admin_page'))

    # Retrieve the client ID from the session
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect(reverse('home:login'))  # Redirect to login if client ID is not in session

    try:
        # Fetch the logged-in client's details
        client = Client.objects.get(Client_ID=client_id)

        # Check if the client has an account; if not, create one
        account, created = Account.objects.get_or_create(
            Client=client,
            defaults={
                'Fixed_Account': 0.00,
                'Salary_Account': 0.00,
                'Savings_Account': 0.00,
            }
        )

        # Optionally, you can log or handle cases where a new account was created
        if created:
            print(f"New account created for client: {client.Client_ID}")

    except Client.DoesNotExist:
        return redirect(reverse('home:login'))  # Redirect to login if the client is not found

    return render(request, 'client/accounts.html', {
        'client': client,
        'account': account,
    })

@login_required
def clientLoan(request):
    if request.user.username == 'admin':
        return redirect("home:admin_page")

    # Get the client from session
    client = get_object_or_404(Client, Client_ID=request.session.get('client_id'))
    loans = client.loans.all()
    approved_loans = Loan.objects.filter(Client=client, Status="Approved", Balance__gt=0)
    account = get_object_or_404(Account, Client=client)
    total_approved_loans = approved_loans.aggregate(total=Sum('Loan_Amount'))['total'] or Decimal("0.00")

    if request.method == "POST":
        if 'apply_loan' in request.POST:
            loan_amount = request.POST.get("loanAmount")
            reason = request.POST.get("loanReason")

            if loan_amount and reason:
                Loan.objects.create(
                    Client=client,
                    Loan_Amount=Decimal(loan_amount),
                    Balance=Decimal("0.00"),  # Balance remains 0 until approved
                    Reason=reason,
                    Status="Pending"
                )
                messages.success(request, "Loan application submitted successfully.")
            else:
                messages.error(request, "Please provide all required details.")

            return redirect("home:clientLoan")  # Prevents form resubmission on refresh

        elif 'make_payment' in request.POST:
            loan_id = request.POST.get("loan_id")
            payment_amount = request.POST.get("paymentAmount")
            account_type = request.POST.get("account_type")

            if not loan_id or not payment_amount or not account_type:
                messages.error(request, "Please fill in all payment details.")
                return redirect("home:clientLoan")

            try:
                payment_amount = Decimal(payment_amount)
                if payment_amount <= 0:
                    messages.error(request, "Invalid payment amount.")
                    return redirect("home:clientLoan")

                loan = get_object_or_404(Loan, Loan_ID=loan_id, Status="Approved", Balance__gt=0)
                account_map = {
                    "Fixed": "Fixed_Account",
                    "Salary": "Salary_Account",
                    "Savings": "Savings_Account"
                }

                if account_type not in account_map:
                    messages.error(request, "Invalid account type selected.")
                    return redirect("home:clientLoan")

                selected_account = getattr(account, account_map[account_type])

                if payment_amount > selected_account:
                    messages.error(request, f"Insufficient funds in {account_type} Account.")
                    return redirect("home:clientLoan")

                # Deduct from account and reduce loan balance
                setattr(account, account_map[account_type], selected_account - payment_amount)
                loan.Balance -= payment_amount
                loan.save()
                account.save()

                # Log the loan payment action
                Logs.objects.create(
                    client=client,
                    action='LOAN_PAYMENT',
                    details=f"Paid {payment_amount} towards loan {loan.Loan_ID}."
                )

                messages.success(request, f"Payment of {payment_amount} successfully made for Loan {loan.Loan_ID}.")
                return redirect("home:clientLoan")  # Prevents form resubmission on refresh

            except (ValueError, TypeError):
                messages.error(request, "Invalid payment amount.")
            except Loan.DoesNotExist:
                messages.error(request, "Selected loan is not approved or does not exist.")
            except Account.DoesNotExist:
                messages.error(request, "No associated account found.")

    return render(request, 'client/clientLoan.html', {
        'client': client,
        'loans': loans,
        'approved_loans': approved_loans,
        'account': account,
        'total_approved_loans': total_approved_loans,
    })


    
@login_required
def client_page(request):
    # Redirect admin to admin panel
    if request.user.username == 'admin':
        return redirect(reverse('home:admin_page'))

    # Ensure client is logged in
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect(reverse('home:login'))

    client = get_object_or_404(Client, Client_ID=client_id)
    account = get_object_or_404(Account, Client=client)

    # Fetch the latest 3 transactions
    transactions = TransactionHistory.objects.filter(Client=client).order_by('-Time')[:3]

    # Calculate total balance
    total_balance = (
        account.Fixed_Account +
        account.Salary_Account +
        account.Savings_Account
    )

    # Calculate total approved loans
    approved_loans_total = Loan.objects.filter(Client=client, Status='Approved').aggregate(total=Sum('Balance'))['total'] or 0

    form = DepositForm(request.POST or None)

    if request.method == "POST":
        if 'deposit' in request.POST and form.is_valid():
            account_type = form.cleaned_data['account_type']
            deposit_amount = form.cleaned_data['deposit_amount']

            # Update the selected account balance
            if account_type == 'Fixed_Account':
                account.Fixed_Account += deposit_amount
            elif account_type == 'Salary_Account':
                account.Salary_Account += deposit_amount
            elif account_type == 'Savings_Account':
                account.Savings_Account += deposit_amount

            # Save the updated account
            account.save()

            # Save the deposit to DepositHistory table
            DepositHistory.objects.create(
                client=client,
                account_type=account_type,
                amount=deposit_amount
            )

            # Log the deposit action
            Logs.objects.create(
                client=client,
                action='DEPOSIT',
                details=f"Deposited {deposit_amount} to {account_type.replace('_', ' ').title()} account."
            )

            messages.success(request, f"Successfully deposited {deposit_amount} to your {account_type.replace('_', ' ').title()}!")
            return redirect('home:client_page')

        elif 'transaction_type' in request.POST and request.POST['transaction_type'] == "transfer":
            account_type = request.POST.get("account_type")
            recipient_account_number = request.POST.get("recipientAccountNumber")
            amount = request.POST.get("amount")

            # Validate inputs
            if not account_type or not recipient_account_number or not amount:
                messages.error(request, "All fields are required.")
                return redirect("home:client_page")

            try:
                amount = Decimal(amount)
                if amount <= 0:
                    messages.error(request, "Invalid transaction amount.")
                    return redirect("home:client_page")

                account_map = {
                    "fixed": "Fixed_Account",
                    "salary": "Salary_Account",
                    "savings": "Savings_Account"
                }

                if account_type not in account_map:
                    messages.error(request, "Invalid account type selected.")
                    return redirect("home:client_page")

                selected_account = getattr(account, account_map[account_type])

                if amount > selected_account:
                    messages.error(request, f"Insufficient funds in {account_type.title()} Account.")
                    return redirect("home:client_page")

                # Deduct amount from sender's account
                setattr(account, account_map[account_type], selected_account - amount)
                account.save()

                # Credit recipient if they exist
                recipient_account = Account.objects.filter(Account_ID=recipient_account_number).first()
                if recipient_account:
                    setattr(recipient_account, account_map[account_type], getattr(recipient_account, account_map[account_type]) + amount)
                    recipient_account.save()

                # Log the transaction
                TransactionHistory.objects.create(
                    Client=client,
                    Amount=amount,
                    Receipt_Accno=recipient_account_number  # Store recipient number whether they exist or not
                )

                Logs.objects.create(
                    client=client,
                    action='TRANSACTION',
                    details=f"Transferred {amount} to account {recipient_account_number}."
                )

                messages.success(request, f"Successfully transferred {amount} to {recipient_account_number}.")
                return redirect("home:client_page")

            except (ValueError, TypeError):
                messages.error(request, "Invalid amount entered.")
                return redirect("home:client_page")

    return render(request, 'client/clienthome.html', {
        'client': client,
        'total_balance': total_balance,
        'form': form,
        'account': account,
        'transactions': transactions,
        'approved_loans_total': approved_loans_total,
    })
 
    
    
@login_required
def transaction(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    transactions = TransactionHistory.objects.filter(Client=client).order_by('-Time')

    return render(request, 'client/transaction.html', {
        'client': client,
        'transactions': transactions  # Pass transactions to the template
    })
       
@login_required
def clientprofile(request):
    client_id = request.session.get('client_id')
    if not client_id:
        messages.error(request, "Client ID not found in session.")
        return redirect('home')  # Adjust this redirect as needed

    client = get_object_or_404(Client, Client_ID=client_id)
    password_images = PasswordImage.objects.all()

    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            updated_client = form.save(commit=False)

            # Handle profile image upload
            if 'Image_Upload' in request.FILES:
                uploaded_image = request.FILES['Image_Upload']
                uploaded_image.name = f'client_page/{uploaded_image.name.split("/")[-1]}'
                updated_client.Image_Upload = uploaded_image  

            updated_client.save()

            # Handle password image selection
            if 'Password_Image' in request.POST:
                password_images_selected = request.POST.getlist('Password_Image')
                updated_client.Password_Image.set(password_images_selected) 

            # Log the profile update action
            Logs.objects.create(
                client=client,
                action='PROFILE_UPDATE',
                details="Updated profile information."
            )

            print(f"Client profile updated: {updated_client.Name} (ID: {updated_client.Client_ID})")
            messages.success(request, "Profile updated successfully!")
            return redirect('home:clientprofile')  # Prevents resubmission on refresh

        else:
            print("Form errors:", form.errors)
            messages.error(request, "There were errors with your submission. Please try again.")
    
    else:
        form = ClientProfileForm(instance=client)

    context = {
        'form': form,
        'password_images': password_images,
        'client': client,
        'account_number': client.Account_Number,  
        'id_number': client.ID_Number,
    }

    return render(request, 'client/profile.html', context)

#admin views
def adminprofile(request):
    return render(request, 'adminpanel/profile.html')

@login_required
def admin_page(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    # Get the total number of clients
    client_count = Client.objects.count()
    grand_total = calculate_grand_total()
    approved_loans_total = Loan.objects.filter(Status='Approved').aggregate(total=Sum('Loan_Amount'))['total'] or 0
    remaining_loan_balance = Loan.objects.filter(Status='Approved').aggregate(total_balance=Sum('Balance'))['total_balance'] or 0
    loan_difference = approved_loans_total - remaining_loan_balance
    total_transactions = TransactionHistory.objects.count()
    context = {
        'client': client,
        'client_count': client_count,
        'grand_total': grand_total,
        'approved_loans_total': approved_loans_total,  # Pass the total of all approved loans
        'remaining_loan_balance': remaining_loan_balance, 
        'loan_difference': loan_difference,
        'total_transactions': total_transactions, 
    }
    return render(request, 'adminpanel/adminhome.html', context)


@login_required
def accounts(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    accounts = Account.objects.all()
    totals_data = calculate_total_accounts() 
    context = {
        'client': client,
        'accounts': accounts,
        **totals_data 
    }    
    return render(request, 'adminpanel/accounts.html', context)

@login_required
def logs(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    logs = Logs.objects.all().order_by('-timestamp')  # Fetch all logs, ordered by most recent
    context = {
        'client': client,
        'logs': logs,
    }
    return render(request, 'adminpanel/logs.html', context)



@login_required
def admin_loans(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    if request.method == "POST":
        loan_id = request.POST.get("loan_id")
        action = request.POST.get("action")  
        loan = get_object_or_404(Loan, Loan_ID=loan_id)
        if action == "approve":
            loan.approve()  
        elif action == "reject":
            loan.reject()  
        else:
            return HttpResponse("Invalid action", status=400)

        return redirect(request.path) 
    loans = Loan.objects.select_related("Client").all()
    context = {
        'client': client,
        "loans": loans,
    } 
    return render(request, "adminpanel/loans.html", context)
    
@login_required    
def clients(request):
    client_id = request.session.get('client_id')
    if not client_id:
        return redirect('home:login')  # Redirect to login if client ID is not in session
    client = get_object_or_404(Client, Client_ID=client_id)
    
    clients = Client.objects.all()
    context = {
        'client': client,
        'clients': clients
    } 
    return render(request, 'adminpanel/clients.html', context) 

