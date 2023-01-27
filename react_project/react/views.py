from django.shortcuts import render
import json
from rest_framework.views import APIView
from .models import Income, IncomeCategory, ExpenseCategory, Expense
from .serializers import IncomeCategorySerializer, ExpenseCategorySerializer, UserSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
class IncomeCategoryView(APIView):
    def get(self, request, pk=None):
        output = {}
        income_category = IncomeCategory.objects.all()
        serializer = IncomeCategorySerializer(income_category, many=True)
        # res = JsonResponse(serializer.data, safe=False)
        # output['data'] = json.loads(res.content)
        # headers = {'Access-Control-Allow-Origin': "*", 'Accept': '*/*'}
        return Response(serializer.data)
        # return Response(serializer.data)


class ExpenseCategoryView(APIView):
    def get(self, request, pk=None):
        expense_category = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(expense_category, many=True)
        return Response(serializer.data)

class UserView(APIView):
    # def get(self, request, pk=None):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)

    def post(self, request, pk=None):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({'error': 'Password did not match'})
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.set_password(user_obj.password)
            user_obj.save()
            return Response({'message': 'User Created Successfully'})
        return Response(serializer.errors)
