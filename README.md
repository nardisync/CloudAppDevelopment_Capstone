# Dealerships Cloud Web App

## A fully functional Full-Stack Cloud Web App created with Django that use REST API for fetching datas from various Databases in the Cloud   

This project it for the Final Course of the <a href="https://www.coursera.org/learn/ibm-cloud-native-full-stack-development-capstone">"Full Stack Cloud Development Capstone Project"</a> Professional Certificate. You can find the full functional Website at the following link: 
<a href="https://nardisync.eu-gb.cf.appdomain.cloud/djangoapp/index">Website App</a>




## How to use the Website App
The app is hosted at the following link: <a href="https://nardisync.eu-gb.cf.appdomain.cloud/djangoapp/index">Website App</a><br>
You will be welcomed by a list of dealerships fetched from a cloud databases. For each of them, you can click on it and see all the reviews lefted from other users.<br>
If you wan, you also can leave a review, but you need to be logged in. This site also give the possibility for an user to registers on this platform. <br>
All the reviews wil lbe analized by an NLU Service offered by IBM and a "positive", negative" or "neutral" tag will be gived to them.

In summary, in this Webapp you can:
* See all the dealerships hosted in a databases
* Add or remove Cars and Cars Maker (need to be an admin)
* See all the reviews of others users 
* Leave your personal review
* Sign in and Login


## How to get started with this project
The easiest way to see how this app works by going to the actual website. But here is an alternative solution but it requires >Python3.6 and an IBM Cloud account.
1. Clone this project
2. Create an NLU Service in the IBM Cloud Service
3. Create an instance of Cloudant from the IBM Cloud Service with two databases : "dealerships" and "reviews"
4. Get the API of the Cloudant and NLU Service
6. In the root repository of this project launch <code> python3 pip install -r requirements.txt</code>
7. Launch <code>cd ./server</code>
8. Launch <code>python3 manage.py runserver</code>
9. Go to <a href="localhost:8000/djangoapp/index">localhost:8000/djangoapp/index</a>

You will still need to create the REST API endpoints in the Function catalog of IBM Cloud, I will leave an example inside the project.