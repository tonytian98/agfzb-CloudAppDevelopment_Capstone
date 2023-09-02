from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_from_cf_by_id, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.urls import reverse
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)
context = {}

# Create your views here.
def about(request):
    return render(request, 'djangoapp/about.html')

# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to=reverse('admin:index'))
        else:
            return redirect('djangoapp:index')


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):

    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
      
        context = {
            "dealerships": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/index.html', context)
        
        #context["dealership_list"] = dealerships
        #return render(request, 'djangoapp/index.html', context)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url_r = f"https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/review?dealerId={dealer_id}"
        url_ds = f"https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "dealer": get_dealers_from_cf(url_ds)[0],
            "reviews": get_dealer_reviews_from_cf(url_r, url_ds),
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealers_from_cf(url)[0],
        }
        
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        form = request.POST
        review = {
            "id":100,
            "name": "admin",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": "true" if form.get("purchasecheck") == "on" else "false",
            }
        if form.get("purchasecheck"):
            review["purchase_date"] = form.get("purchasedate")
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"]= int(car.year.strftime("%Y"))
        json_payload = {"review": review}
        URL = "https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/review"
        post_request(URL, json_payload, dealerId=dealer_id)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

