from django.contrib import admin
from .models import Client, Loan, TransactionHistory, Account, PasswordImage



admin.site.register(Client)
admin.site.register(Loan)
admin.site.register(TransactionHistory)
admin.site.register(Account)

@admin.register(PasswordImage)
class PasswordImageAdmin(admin.ModelAdmin):
  list_display = ('name', 'image')
