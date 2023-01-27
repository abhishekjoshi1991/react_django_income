from . models import Income, IncomeCategory, ExpenseCategory, Expense
from rest_framework import serializers
from django.contrib.auth.models import User

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # def create_user(self, validated_data):
    #     import pdb; pdb.set_trace()
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #
    #     user.set_password(validated_data['password'])
    #     user.save()
    #
    #     return user