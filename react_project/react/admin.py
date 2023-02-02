from django.contrib import admin
from . models import *

# Register your models here.
# myModels = [Income, IncomeCategory, Expense, ExpenseCategory]
#
# admin.site.register(myModels)

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'description', 'transaction_date', 'user_id', 'income_categ_id']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'description', 'transaction_date', 'user_id', 'expense_categ_id']

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
