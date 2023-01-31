from django.shortcuts import render
import json
from rest_framework.views import APIView
from .models import Income, IncomeCategory, ExpenseCategory, Expense
from .serializers import IncomeCategorySerializer, ExpenseCategorySerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status


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
