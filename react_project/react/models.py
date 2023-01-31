from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    transaction_date = models.DateField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    income_categ_id = models.ForeignKey('IncomeCategory', on_delete=models.CASCADE)

    def __str__(self):
        return 'Income amount {} with {}'.format(self.amount, self.description)


class Expense(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    transaction_date = models.DateField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    expense_categ_id = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE)

    def __str__(self):
        return 'Expense amount {} with {}'.format(self.amount, self.description[:10])


# To generate token using signals

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
