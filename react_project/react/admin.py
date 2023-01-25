from django.contrib import admin
from . models import *

# Register your models here.
myModels = [Income, IncomeCategory, Expense, ExpenseCategory]

admin.site.register(myModels)
