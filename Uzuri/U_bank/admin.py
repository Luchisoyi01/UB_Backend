from django.contrib import admin
from .models import Client, Loan, TransactionHistory, Account, PasswordImage, DepositHistory, Logs



admin.site.register(Client)
admin.site.register(Loan)
admin.site.register(TransactionHistory)
admin.site.register(Account)
admin.site.register(DepositHistory)
admin.site.register(Logs)

@admin.register(PasswordImage)
class PasswordImageAdmin(admin.ModelAdmin):
  list_display = ('name', 'image')
