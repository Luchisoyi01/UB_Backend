from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class PasswordImage(models.Model): 
  name = models.CharField(max_length=100, unique=True)
  image = models.ImageField(upload_to='password_images/')
  def __str__(self): 
    return f"Image {self.id}"



class Client(models.Model):
    Client_ID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Name = models.CharField(max_length=255)
    Account_Number = models.CharField(max_length=20, unique=True)
    ID_Number = models.CharField(max_length=20, unique=True)
    Email = models.EmailField(unique=True)
    Phone_Number = models.CharField(max_length=15)
    Address = models.TextField()
    Image_Upload = models.ImageField(upload_to='client_images/', null=True, blank=True)
    Password_Image = models.ManyToManyField('PasswordImage', blank=True)

    def __str__(self):
        return self.Name


class Loan(models.Model):
    Loan_ID = models.AutoField(primary_key=True)
    Client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="loans")
    Loan_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Reason = models.TextField()
    Status = models.CharField(
        max_length=20,
        choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def approve(self):
        """Approve the loan and set balance to loan amount."""
        self.Status = 'Approved'
        self.Balance = self.Loan_Amount
        self.save()

    def reject(self):
        """Reject the loan."""
        self.Status = 'Rejected'
        self.save()

    def make_payment(self, amount):
        """Reduce loan balance when payment is made."""
        if self.Status != 'Approved':
            raise ValueError("Cannot make a payment on a loan that is not approved.")
        
        if self.Balance < amount:
            raise ValueError("Payment amount exceeds remaining balance.")

        self.Balance -= amount
        self.save()

    def __str__(self):
        return f"Loan {self.Loan_ID} - {self.Status} (Balance: {self.Balance})"




class TransactionHistory(models.Model):
  Transaction_ID = models.AutoField(primary_key=True)
  Client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="transactions")
  Amount = models.DecimalField(max_digits=10, decimal_places=2)
  Time = models.DateTimeField(auto_now_add=True)
  Receipt_Accno = models.CharField(max_length=20)

  def __str__(self):
    return f"Transaction {self.Transaction_ID} - {self.Amount}"


class Account(models.Model):
  Account_ID = models.AutoField(primary_key=True)
  Client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="account")
  Fixed_Account = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  Salary_Account = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  Savings_Account = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

  def __str__(self):
    return f"Account {self.Account_ID} for {self.Client.Name}"
  
  

class ImageHash(models.Model):
  hash_value = models.CharField(max_length=64, unique=True)  # Store the image hash
  created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the hash was generated

  def __str__(self):
    return self.hash_value
  
  
class DepositHistory(models.Model):
    # Reference to the client making the deposit
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='deposits')    
    # The account where the deposit was made
    account_type_choices = [
        ('fixed', 'Fixed Account'),
        ('salary', 'Salary Account'),
        ('savings', 'Savings Account'),
    ]
    account_type = models.CharField(max_length=20, choices=account_type_choices)
    # The deposit amount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Timestamp when the deposit was made
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.Name} - {self.account_type.title()} - {self.amount} at {self.timestamp}"

    class Meta:
        # Orders by the most recent deposit first
        ordering = ['-timestamp']
        
        

class Logs(models.Model):
    # Define the types of actions that can be logged
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('DEPOSIT', 'Deposit'),
        ('TRANSACTION', 'Transaction'),
        ('LOAN_APPROVAL', 'Loan Approval'),
        ('LOAN_PAYMENT', 'Loan Payment'),
        ('PROFILE_UPDATE', 'Profile Update'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='logs')  # Link to the Client
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)  # Type of action
    details = models.TextField(blank=True, null=True)  # Additional details about the action
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the action

    def __str__(self):
        return f"{self.client.Username} - {self.action} at {self.timestamp}"

    class Meta:
        verbose_name_plural = "Logs"
        ordering = ['-timestamp']  # Order logs by most recent first