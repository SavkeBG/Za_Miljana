from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
import os
import datetime
from tezina.models import Data, MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from tezina.forms import UserForm, Post




def post_list(request):
    if request.method == 'POST':
        try:
            form = Post(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                print(request.user)
                data.save()
                print(data.save)

                return JsonResponse({

                    'date': data.date,
                    'weight': data.weight

                    })

            else:
                return JsonResponse({
                    'Message': 'Something went wrong',
                    'Error': dict(form.errors.items())

                    })
        except IntegrityError:

            return JsonResponse({
                'message': 'Date already exist',
                'date': data.date

            })
            

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
        print(data)
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


        return JsonResponse({
            'date':get_data.date,
            'weight':get_data.weight
        })




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

    else:
        return HttpResponse(status=400)

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
           

            return JsonResponse({
                'message': "user created",
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            })

        else:
            return JsonResponse({

                'message': 'something went wrong',
                'Error': dict(form.errors.items())


            },)

 



    
     

        

            
          
            
            


        



        
       

            
            
            

            
        


