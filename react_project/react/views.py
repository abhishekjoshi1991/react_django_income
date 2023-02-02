from django.shortcuts import render
import json
from rest_framework.views import APIView
from .models import Income, IncomeCategory, ExpenseCategory, Expense
from .serializers import IncomeCategorySerializer, ExpenseCategorySerializer, UserSerializer, \
    ExpenseSerializer, IncomeSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


# Create your views here.
class IncomeCategoryView(APIView):
    def get(self, request, pk=None):
        income_category = IncomeCategory.objects.all()
        serializer = IncomeCategorySerializer(income_category, many=True)
        return Response(serializer.data)


class ExpenseCategoryView(APIView):
    def get(self, request, pk=None):
        expense_category = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(expense_category, many=True)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request, pk=None):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        res = {}
        res['message'] = []
        if password != confirm_password:
            res['status'] = 'failed'
            res['status_code'] = 400
            res['message'].append({'password' : 'Password did not match'})
            return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.set_password(user_obj.password)
            user_obj.save()
            token = user_obj.auth_token
            res.pop('message')
            res['status'] = 'success'
            res['status_code'] = 200
            res['user_data'] = {}
            res['user_data']['name'] = user_obj.username
            res['user_data']['token'] = token.key
            return Response({'data': res}, status=status.HTTP_200_OK)
        res['status'] = 'failed'
        res['status_code'] = 400
        for error, description in serializer.errors.items():
            res['message'].append({error: description[0].title()})
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        res = {}
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            password_check = user_obj.check_password(password)
            if password_check:
                token = user_obj.auth_token
                res['status'] = 'success'
                res['status_code'] = 200
                res['user_data'] = {}
                res['user_data']['name'] = user_obj.username
                res['user_data']['token'] = token.key
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res['status'] = 'failed'
                res['status_code'] = 400
                res['message'] = 'Password does not match!'
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        else:
            res['status'] = 'failed'
            res['status_code'] = 400
            res['message'] = 'User does not exists!'
            return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class ExpenseAdd(APIView):
    def post(self, request):
        res = {}
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res['status'] = 'success'
            res['status_code'] = 200
            res['message'] = 'Entry added successfully!'
            return Response({'data': res}, status=status.HTTP_200_OK)
        res['status'] = 'failed'
        res['status_code'] = 400
        res['message'] = serializer.errors
        return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class IncomeAdd(APIView):
    def post(self, request):
        res = {}
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res['status'] = 'success'
            res['status_code'] = 200
            res['message'] = 'Entry added successfully!'
            return Response({'data': res}, status=status.HTTP_200_OK)
        res['status'] = 'failed'
        res['status_code'] = 400
        res['message'] = serializer.errors
        return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)



