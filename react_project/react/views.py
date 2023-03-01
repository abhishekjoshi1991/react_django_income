import calendar
import random
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Income, IncomeCategory, ExpenseCategory, Expense
from .serializers import IncomeCategorySerializer, ExpenseCategorySerializer, UserSerializer, \
    ExpenseSerializer, IncomeSerializer

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

    def put(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data.update({'user_id': user.id})
                expense_id = request.data.get('id')
                expense_obj = Expense.objects.get(id=expense_id)
                serializer = ExpenseSerializer(expense_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = StatusMessage.get_status('success', 'Entry Updated Successfully!')
                    return Response({'data': res})
                return Response(serializer.errors)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data.update({'user_id': user.id})
                expense_id = request.data.get('id')
                expense_obj = Expense.objects.get(id=expense_id)
                expense_obj.delete()
                res = StatusMessage.get_status('success', 'Entry Deleted Successfully!')
                return Response({'data': res})
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
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

    def put(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data.update({'user_id': user.id})
                income_id = request.data.get('id')
                income_obj = Income.objects.get(id=income_id)
                serializer = IncomeSerializer(income_obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    res = StatusMessage.get_status('success', 'Entry Updated Successfully!')
                    return Response({'data': res})
                return Response(serializer.errors)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                request.data.update({'user_id': user.id})
                income_id = request.data.get('id')
                income_obj = Income.objects.get(id=income_id)
                income_obj.delete()
                res = StatusMessage.get_status('success', 'Entry Deleted Successfully!')
                return Response({'data': res})
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    def get(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                res = StatusMessage.get_status('success')
                res['user_data'] = []
                res['user_data'].append({'user_id': user.id, 'username': user.username})

                # get all income of user
                all_income = Income.objects.filter(user_id=user.id).order_by('-transaction_date')
                if all_income:
                    res['income'] = []
                    for income in all_income:
                        income_dict = dict()
                        income_dict['id'] = income.id
                        income_dict['amount'] = income.amount
                        income_dict['description'] = income.description
                        income_dict['transaction_date'] = income.transaction_date.strftime("%b %d, %Y")
                        income_dict['income_categ_id'] = income.income_categ_id.name
                        res['income'].append(income_dict)
                else:
                    res['income'] = []

                # get all expense of user
                all_expense = Expense.objects.filter(user_id=user.id).order_by('-transaction_date')
                if all_expense:
                    res['expense'] = []
                    for expense in all_expense:
                        expense_dict = dict()
                        expense_dict['id'] = expense.id
                        expense_dict['amount'] = expense.amount
                        expense_dict['description'] = expense.description
                        expense_dict['transaction_date'] = expense.transaction_date.strftime("%b %d, %Y")
                        expense_dict['expense_categ_id'] = expense.expense_categ_id.name
                        res['expense'].append(expense_dict)
                else:
                    res['expense'] = []

                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)


class IncomeExpenseChart(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                current_month = request.data.get('month') or datetime.today().month
                current_month_income = Income.objects.filter(user_id=user.id).filter(transaction_date__month=current_month)
                current_month_expense = Expense.objects.filter(user_id=user.id).filter(transaction_date__month=current_month)

                res = StatusMessage.get_status('success')
                res['income'] = []
                res['expense'] = []
                for income in current_month_income.values('income_categ_id').annotate(Sum('amount')):
                    income_categ_name = IncomeCategory.objects.get(id=income['income_categ_id']).name
                    individual_income_dict = {'month': current_month,
                                              "income_category": income_categ_name,
                                              "amount": income['amount__sum']
                                              }
                    res['income'].append(individual_income_dict)

                for expense in current_month_expense.values('expense_categ_id').annotate(Sum('amount')):
                    expense_categ_name = ExpenseCategory.objects.get(id=expense['expense_categ_id']).name
                    individual_expense_dict = {'month': current_month,
                                              "expense_category": expense_categ_name,
                                              "amount": expense['amount__sum']
                                              }
                    res['expense'].append(individual_expense_dict)
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

class IncomeExpenseAllYear(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                current_year = request.data.get('year') or datetime.today().year
                current_year_income = Income.objects.filter(user_id=user.id).filter(
                    transaction_date__year=current_year)
                current_year_expense = Expense.objects.filter(user_id=user.id).filter(
                    transaction_date__year=current_year)

                month_wise_income = current_year_income.annotate(month=ExtractMonth('transaction_date')).values('month').annotate(total=Sum('amount')).values('month','total')
                month_wise_expense = current_year_expense.annotate(month=ExtractMonth('transaction_date')).values('month').annotate(total=Sum('amount')).values('month','total')

                months_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                vals_income = ['' for i in range(12)]
                for record in month_wise_income:
                    if record['month'] in months_list:
                        index = months_list.index(record['month'])
                        vals_income[index] = record['total']

                vals_expense = ['' for j in range(12)]
                for record_e in month_wise_expense:
                    if record_e['month'] in months_list:
                        index_e = months_list.index(record_e['month'])
                        vals_expense[index_e] = record_e['total']

                dataset = [{
                    'label': 'Income',
                    'data': vals_income,
                    'backgroundColor': 'rgb(102, 179, 255)'
                    },
                    {
                        'label': 'Expense',
                        'data': vals_expense,
                        'backgroundColor': 'rgb(255, 166, 77)'
                    }
                ]
                return Response(dataset, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetail(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                expense_id = request.data.get('id')
                expense_obj = Expense.objects.filter(id=expense_id).first()
                res = StatusMessage.get_status('success')
                vals = {
                    'id': expense_id,
                    'amount': expense_obj.amount,
                    'description': expense_obj.description,
                    'transaction_date': expense_obj.transaction_date.strftime("%Y-%m-%d"),
                    'expense_categ_id': expense_obj.expense_categ_id.id
                }
                res['expense'] = [vals]
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)

class IncomeDetail(APIView):
    def post(self, request):
        access_token = request.headers.get('Access-Token')
        if access_token:
            user = User.objects.filter(auth_token=access_token).first()
            if user:
                income_id = request.data.get('id')
                income_obj = Income.objects.filter(id=income_id).first()
                res = StatusMessage.get_status('success')
                vals = {
                    'id': income_id,
                    'amount': income_obj.amount,
                    'description': income_obj.description,
                    'transaction_date': income_obj.transaction_date.strftime("%Y-%m-%d"),
                    'income_categ_id': income_obj.income_categ_id.id
                }
                res['income'] = [vals]
                return Response({'data': res}, status=status.HTTP_200_OK)
            else:
                res = StatusMessage.get_status('failed', 'Provide Valid Token!')
                return Response({'data': res}, status=status.HTTP_400_BAD_REQUEST)