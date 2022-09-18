import requests
import json
from random import randrange
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from configparser import ConfigParser, RawConfigParser

constants = RawConfigParser()
constants.read("./constant.ini")


# A function to make HTTP GET requests.
# Return a JSON String
def get_request(url, dealerId=None, stateId=None, apiKey=None, **kwargs):
    print("GET from {} ".format(url))
    try:
        if apiKey:
            # Basic authentication GET with API_KEY
            
            authenticator = IAMAuthenticator(apiKey)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
                version='2022-04-07',
                authenticator=authenticator
            )
            natural_language_understanding.set_service_url(url)
            print(f"Text to be analyze: {kwargs['kwargs']['text']}")
            print("Preparing the response...")
            try:

                response = natural_language_understanding.analyze(
                    text=kwargs["kwargs"]["text"],
                    features=Features(
                        sentiment=SentimentOptions())).get_result()

                print(f"All good! The response is: {json.dumps(response, indent=2)}")
                return response['sentiment']['document']['label']

            except Exception as e:
                print(e.code)
                if e.code == 422:
                    print(f"Network exception occurred for NLU: {e}")
                    print("Returning neutral")
                    return "neutral"
        
        else:
            # Call with GET with no authentication 
            if dealerId != None:
                print("Call Selector with Dealer ID")
                url += f"?dealership={dealerId}"
                print(f"URL: {url}")
        
            elif stateId != None:
                print("Call Selector with Dealer State")
                url += f"?st={stateId}"
                print(f"URL: {url}")

            else:
                # Call get method of requests library with URL and parameters
                print("Classic Call, no Selector")
                
            response = requests.get(url, 
                                headers={'Content-Type': 'application/json'},
                                params=kwargs)

    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")
    status_code = response.status_code

    print(f"With status {status_code}.")
    print(response.text)
    
    json_data = json.loads(response.text)
    return json_data



# Post Request for adding a Review in the cloudand app
def post_request(url, jsonPayload, **kwargs):
    json_payload = {}
    json_payload['review'] = jsonPayload
    json_object = json.dumps(json_payload, indent = 4) 
    print(f"Payload: {json_object}")
    response = requests.post(url, 
                            params=kwargs, 
                            json=json_payload)
    return response


# A Function to get dealers from a cloud function
#   - Call get_request() with specified arguments
#   - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url)
    return car_dealer_from_json(json_result)


def get_dealer_by_id_from_cf(url, dealerId, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    

    return car_dealer_from_json(json_result)

def get_dealers_by_state(url, stateId, **kwargs):

    # Call get_request with a URL parameter
    json_result = get_request(url, stateId=stateId)

    return car_dealer_from_json(json_result)


# Method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId, **kwargs):
    
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    

    #return car_dealer_from_json(json_result)
    return dealer_review_from_json(json_result)

# Method for call Watson NLU and analyze a review
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    params = dict()
    params["text"] = dealerreview
    params["version"] = "1.0.0"
    params["features"] = "false"
    params["return_analyzed_text"] = "true"
    
    url = constants.get("CONSTANTS", "NATURAL_LANGUAGE_UNDERSTANDING_URL")
    api_key = constants.get("CONSTANTS", "NATURAL_LANGUAGE_UNDERSTANDING_API_KEY")
    
    sentiment_result = get_request(url, apiKey=api_key, kwargs=params)

    return sentiment_result

# A function that process a JSON String into a CarDealer Object.
# Return a JSON String with all the CarDealer created
def car_dealer_from_json(json_result):
    results = []
    if json_result:
        # Get the row list in JSON as dealers
        if json_result.get("rows"):
            print("Received a dictionary with various rows")
            dealers = json_result["rows"]
        else:
            print("Received a dictionary with a single document")
            dealers = [ { 'doc' : json_result['docs'][0] } ]
            
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# A function that process a JSON String into a CarDealer Object.
# Return a JSON String with all the CarDealer created
def dealer_review_from_json(json_result):
    results = []
    if json_result:
        # Get the doc list in JSON as dealers
        reviews = json_result["docs"]
        # For each review object
        for review_doc in reviews:
            review_doc["sentiment"] = "HARDCODED"
            if review_doc["purchase"] == "true":
                # Create a CarDealer object with values in `doc` object
                review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                        review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"], 
                                        car_model=review_doc["car_model"], car_year=review_doc["car_year"], sentiment=review_doc["sentiment"], 
                                        id=review_doc["id"])
            
            else:
                # Create a CarDealer object with values in `doc` object
                review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                        review=review_doc["review"], sentiment=review_doc["sentiment"], 
                                        id=review_doc["id"])
            
            review_obj.sentiment = str(analyze_review_sentiments(review_obj.review))
            print(f"Sentiment for the text: {review_obj.sentiment}")
            results.append(review_obj)

    return results




if __name__ == '__main__':
    #print(f"get_dealers_from_cf: {get_dealers_from_cf(url)}")
    print("---------------------------")
    #print(f"get_dealers_from_cf: {get_dealer_by_id_from_cf(url, dealerId=15)}")
    print("---------------------------")
    #print(f"get_dealers_from_cf: {get_dealers_by_state(url, stateId='TX')}")
    print("---------------------------")
    #print(f"get_dealers_from_cf: {get_dealer_by_id_from_cf(url, dealerId=15)}")
    print("---------------------------")
    #print(f"get_dealers_from_cf: {get_dealer_reviews_from_cf(url, dealerId=15)}")
    print("---------------------------")
    print(constants.get("CONSTANTS", "API"))
    