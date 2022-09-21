from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from configparser import ConfigParser, RawConfigParser
from django.contrib import messages
from datetime import datetime

import logging
import json
import time


constants = RawConfigParser()
constants.read("./constant.ini")

# Get an instance of a logger
logger = logging.getLogger(__name__)


# An `about` view to render a static about page
def get_about_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# An `contact` view to return a static contact page
def get_contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# An `my links` view to return a static my links page
def get_my_links(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/my_links.html', context)

# An `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# An `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)

    elif request.method == 'POST':

        # Checking if the user already Exists
        if request.method == "POST":
            username    = request.POST['Username']
            first_name  = request.POST['First Name']
            last_name   = request.POST['Last Name']
            password    = request.POST['Password']
            user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, 
                                            last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)



# Creating a view for render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = constants.get("CONSTANTS", "REST_API_GET_ALL_DEALERSHIPS")
        
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships

        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Creating a view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = constants.get("CONSTANTS", "REST_API_GET_ALL_REVIEWS_WITH_SELECTOR")
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)



# View for submit a review
def add_review(request, dealer_id):
    context = {}
    
    if request.method == 'GET':
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"]         = cars
        context["dealer_id"]    = dealer_id

        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        if request.user.is_authenticated:
            print(f"POST Received: {request.POST}")
            review = {}

            if request.POST.get("car"):

                car_objects = CarModel.objects.filter(car_id=int(request.POST["car"]))

                # Da migliorare direi
                dt = datetime(2022, 9, 22, 0, 0)
                review["id"] = int(dt.timestamp())
                
                review["name"]          = str(request.POST["name"])
                review["dealership"]    = int(dealer_id)
                review["review"]        = str(request.POST["review"])
                
                if request.POST.get("purchasecheck"):
                    try:
                        review["purchase"]      = "true"
                        review["purchase_date"] = str(request.POST["purchasedate"])
                        review["car_make"]      = str(car_objects.values_list('car_maker', flat=True)[0])
                        review["car_model"]     = str(car_objects.values_list('car_name', flat=True)[0])
                        review["car_year"]      = int(car_objects.values_list('car_year', flat=True)[0].strftime("%Y"))
                        
                    except Exception as e:
                        print(f"Error received: {e}\nRedirection...")
                        return redirect("djangoapp:add_review", dealer_id=dealer_id)
                else:
                    review["purchase"]      = "false"

            else:
                # Da migliorare direi
                dt = datetime(2022, 9, 22, 0, 0)
                review["id"] = int(dt.timestamp())
                
                review["name"]          = str(request.POST["name"])
                review["dealership"]    = int(dealer_id)
                review["review"]        = str(request.POST["review"])
                review["purchase"]      = "false"


            url = constants.get("CONSTANTS", "REST_API_POST_REVIEW_FOR_DEALERSHIP")
            
            response = post_request(url=url, jsonPayload=review)
            print(f"Response: {response.text}")
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            #return redirect('djangoapp:login')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)



