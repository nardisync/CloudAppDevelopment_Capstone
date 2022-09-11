from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

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
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/syncogame%40gmail.com_djangoserver-space/CloudApp_FinalCapstone/getAllDealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealers_name = []
        for dealer in dealerships:
            dealers_name.append(dealer.short_name)
        context["dealers_short_name"] = dealers_name
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Creating a view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/syncogame%40gmail.com_djangoserver-space/CloudApp_FinalCapstone/getAllReviewsWithSelector"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        reviews_list = []
        for review in reviews:
            reviews_list.append(review)
        context["reviews"] = reviews_list
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)



# View for submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}

            #review["time"] = str(datetime.utcnow().isoformat())
            review["dealership"] = int(request.POST["DealerID"])
            review["review"] = str(request.POST["Review"])
            review["name"] = str(request.POST["Name"])
            review["purchase"] = str(request.POST["Purchase"])
            review["car_make"] = str(request.POST["CarMake"])
            review["car_model"] = str(request.POST["CarModel"])
            review["car_year"] = int(request.POST["CarYear"])
    "review": {
        "id": 1114,
        "name": "Upkar Lidder",
        "dealership": 15,
        "review": "Great service!",
        "purchase": "false",
        "another": "field",
        "purchase_date": "02/16/2021",
        "car_make": "Audi",
        "car_model": "Car",
        "car_year": 2021
    }

            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/syncogame%40gmail.com_djangoserver-space/CloudApp_FinalCapstone/postReviewForDealership"
            
            response = post_request(url=url, jsonPayload=review)
            print(f"Response: {response.text}")

            return redirect('djangoapp:login')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)



