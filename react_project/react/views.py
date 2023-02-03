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
class StatusMessage:
    @staticmethod
    def get_status(status_type, message=None):
        res = {}
        if status_type == 'failed':
            res['status'] = 'failed'
            res['status_code'] = 400
            if message:
                res['message'] = message
        else:
            res['status'] = 'success'
            res['status_code'] = 200
            if message:
                res['message'] = message
        return res

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


# View get called while registering new user
class RegisterView(APIView):
    def post(self, request, pk=None):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            res = StatusMessage.get_status('failed', 'Password did not match!')
            return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.set_password(user_obj.password)
            user_obj.save()
            token = user_obj.auth_token
            res = StatusMessage.get_status('success')
            res['user_data'] = {}
            res['user_data']['name'] = user_obj.username
            res['user_data']['token'] = token.key
            return Response({'data': res}, status=status.HTTP_200_OK)
        res = StatusMessage.get_status('failed')
        res['message'] = []
        for error, description in serializer.errors.items():
            res['message'].append({error: description[0].title()})
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


# View get called when logging in
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj:
            password_check = user_obj.check_password(password)
            if password_check:
                token = user_obj.auth_token
                res = StatusMessage.get_status('success')
                res['user_data'] = {}
                res['user_data']['name'] = user_obj.username
                res['user_data']['token'] = token.key
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Password does not match!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = StatusMessage.get_status('failed', 'User does not exists!')
            return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


# view get called while adding new expense by logged in user
class ExpenseAdd(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data['user_id'] = user.id
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = StatusMessage.get_status('success', 'Entry added successfully!')
            return Response({'data': res}, status=status.HTTP_200_OK)

        res = StatusMessage.get_status('failed')
        res['message'] = []
        for error, description in serializer.errors.items():
            res['message'].append({error: description[0].title()})
        return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class IncomeAdd(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data['user_id'] = user.id
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = StatusMessage.get_status('success', 'Entry added successfully!')
            return Response({'data': res}, status=status.HTTP_200_OK)

        res = StatusMessage.get_status('failed')
        res['message'] = []
        for error, description in serializer.errors.items():
            res['message'].append({error: description[0].title()})
        return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                res = StatusMessage.get_status('success')
                res['user_id'] = user.id
                res['username'] = user.username
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

