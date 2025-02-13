from django import forms
from .models import Client, PasswordImage, Account

class ClientForm(forms.ModelForm):
  class Meta:
    model = Client
    fields = [
      'Username', 'Name', 'Account_Number', 'ID_Number',
      'Email', 'Phone_Number', 'Address', 'Image_Upload', 'Password_Image',
    ]
    widgets = {
      'Username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Johnny'}),
      'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Kimani'}),
      'Account_Number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly','placeholder': 'click generate to create account number'}),
      'ID_Number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12345678'}),
      'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. jonney@gmail'}),
      'Phone_Number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0712345678'}),
      'Address': forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. 1234, Nairobi'}),
      'Image_Upload': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Add file input for image upload
      'Password_Image': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
    }


class LoginForm(forms.Form):
    Username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
    )
    password_images = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Dynamically set choices for password_images
        self.fields['password_images'].choices = [(image.id, image.name) for image in PasswordImage.objects.all()]


class DepositForm(forms.Form):
    ACCOUNT_TYPE_CHOICES = [
        ('Fixed_Account', 'Fixed Account'),
        ('Salary_Account', 'Salary Account'),
        ('Savings_Account', 'Savings Account'),
    ]

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        label="Account Type",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    deposit_amount = forms.DecimalField(        
        max_digits=10,
        decimal_places=2,
        label="Deposit Amount",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter deposit amount'}),
    )


class LoanApplicationForm(forms.Form):
    loan_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Loan Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'loanAmount',
            'step': '0.01',
            'placeholder': 'Enter loan amount'
        })
    )
    loan_reason = forms.CharField(
        required=True,
        label="Reason",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'loanReason',
            'rows': 4,
            'placeholder': 'Enter the reason for the loan'
        })
    )


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['Username', 'Name', 'Email', 'Phone_Number', 'Address', 'Image_Upload', 'Password_Image']
    
