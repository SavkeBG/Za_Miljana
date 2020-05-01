from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import os
import datetime
from tezina.models import Data, MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from tezina.forms import UserForm
from django.contrib import messages






def post_list(request):
    if request.method == 'POST':     
        post_data = json.loads(request.body)
        date = post_data.get('date')
        weight = post_data.get('weight')

        if 'date' not in post_data:
            return HttpResponse(status=400)
        if 'weight' not in post_data:
            return HttpResponse(status=400)


        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')

        except ValueError:
            return JsonResponse({

                'error': 'Incorect data format, should be YYYY-MM-DD',
                'date': date

            }, status=400)   
   
        try:
            create_data = Data.objects.create(weight=weight, date=date)
            create_data.save()

            return JsonResponse({
                'date': date,
                'weight': weight
            }, status = 201)

        except IntegrityError:
            return JsonResponse({

                'message': 'Date already exists',
                'date': date

            },status=400)

    if request.method == 'GET':
        all_data = Data.objects.values('date', 'weight')

        return JsonResponse({

            'All data': list(all_data)

            }, status=200)

    else:
        return HttpResponse(status=400)


def get_delete_patch(request,date):
    try:
        data = Data.objects.get(date=date)

    except ObjectDoesNotExist:
        return JsonResponse({

            'message': "The fallowing date has not been found",
            'date': date
          
        })
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')

    except ValueError:
        return JsonResponse({

            'error': 'Incorect data format, should be YYYY-MM-DD',
            'date': date

            }, status=400)


    if request.method == 'GET':

        get_data = Data.objects.get(date=date)

        response = {

        'date': get_data.date,
        'weight': get_data.weight

        }

        return JsonResponse(response, status=200)


    if request.method == 'DELETE':
            delete_data = Data.objects.get(date=date).delete()

            return JsonResponse({

                'message': 'The date has been deleted',
                'date': date
            },status=200)



    if request.method == "PATCH":
        post_data = json.loads(request.body)
        email = post_data.get('email')
        password = post_data.get('password')
        weight = post_data.get('weight')

        if 'email' not in post_data:
            return HttpResponse(status=400)
        if 'password' not in post_data:
            return HttpResponse(status=400) 

        user = authenticate(email=email,password=password)

        if user is None:
            return JsonResponse({
                
                "error": "user or password incorrect",
                "message": "please enter valid credentials"

            }, status=404)

        if user.is_authenticated:
            if user.is_active:
                data = Data.objects.get(date=date)
                data.weight = weight
                data.save()
                           
                return JsonResponse({

                "message": "weight has been change",
                "user": email

                })

            else:
                return JsonResponse({
                    'message': "The user is not active",
                    "user": email
                })

    if request.method not in ['PATCH','DELETE','GET']:

        return HttpResponse(status = 400)





def log_in(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        email = post_data.get('email')
        password = post_data.get('password')

        if 'email' not in post_data:
            return HttpResponse(status=400)
        if 'password' not in post_data:
            return HttpResponse(status=400) 

        user = authenticate(email=email,password=password)

        if user is None:
            return JsonResponse({
                
                "error": "user or password incorrect",
                "message": "please enter valid credentials"

            }, status=404)

        if user.is_authenticated:
            if user.is_active:
                login(request, user)

            
                return JsonResponse({

                "message": "logged in",
                "user": email

                })

            else:
                return JsonResponse({
                    'message': "The user is not active",
                    "user": email
                })
                
    else:
        return HttpResponse(status=400)



def change_pass(request, email):
    try:
        check_user = MyUser.objects.get(email=email)

    except ObjectDoesNotExist:
        return JsonResponse({

        'message': "User doesn't exist",
        'user': email
          
        },status=404)

    if request.method == "PATCH":
        post_data = json.loads(request.body)
        password = post_data.get('password')
      
        user = MyUser.objects.get(email=email)

        if user.is_authenticated:
            user.set_password(password)
            user.save()
 

            return JsonResponse({
                "message": "Password has been changed",
                "username": user.email
            },status=200)

        else:
                return JsonResponse({
                    'message': "The user is not active",
                    "user": email
                })

    if request.method not in ["PATCH"]:
        return HttpResponse(status=400)

def create_user(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            
          
            
            


        



        
       

            
            
            

            
        


