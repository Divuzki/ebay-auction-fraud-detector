import pickle
import pandas as pd
from datetime import datetime
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

APP_ID = "DivineIk-s-PRD-59c7a1d25-67a7167e"
DEV_ID = "f3547dca-f775-4599-bb9f-671721a836a9"
CERT_ID = "PRD-9c7a1d252d9c-ce6c-47c1-b962-69f7"
TOKEN = "v^1.1#i^1#I^3#p^3#r^1#f^0#t^Ul4xMF8wOjRBOEIzQUVDNkFDOTkxMUE1QzQ4MDgzMjEzREFBOUQ3XzNfMSNFXjI2MA=="

def to_seconds(date):
    return time.mktime(date.timetuple())

def get_item_info(item_id):
    try:
        # Use the Finding API to search for the item
        finding_api = Finding(appid=APP_ID, config_file=None)
        api_request = {'keywords': item_id, 'outputSelector': 'SellerInfo'}
        response = finding_api.execute('findItemsByKeywords', api_request)
        return response.dict()

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return None

# Function to extract relevant data from the eBay API response
def extract_data(response):
    data = []
    item = response['searchResult']['item'][0]
    bid = item['sellingStatus']
    start_time = datetime.strptime(
        item['listingInfo']['startTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = datetime.strptime(
        item['listingInfo']['endTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
    # Calculate time difference
    time_left = end_time - start_time
    time_left_in_seconds = time_left.total_seconds()
    try:
        item['listingInfo']['buyItNowPrice']['value']
    except KeyError:
        item['listingInfo']['buyItNowPrice'] = {
            'value': bid['currentPrice']['value']}
        
    # listingInfo
    data.append({
        'Bidder_Tendency': float(item['sellerInfo']['feedbackScore']) / float(item['sellerInfo']['positiveFeedbackPercent']),
        'Bidding_Ratio': int(bid['bidCount']) / time_left_in_seconds,
        'Successive_Outbidding': int(bid['bidCount']) / float(item['listingInfo']['buyItNowPrice']['value']),
        'Last_Bidding': int(bid['bidCount']) / int(to_seconds(start_time)),
        'Auction_Bids': int(bid['bidCount']),
        'Starting_Price_Average': float(bid['currentPrice']['value']) / float(item['listingInfo']['buyItNowPrice']['value']),
        'Early_Bidding': int(bid['bidCount']) / int(item['sellerInfo']['feedbackScore']),
        'Winning_Ratio': float(item['sellerInfo']['feedbackScore']) / float(item['sellerInfo']['positiveFeedbackPercent']),
        'Auction_Duration': time_left_in_seconds,
    })
    return data

# Load the model from a file
with open('shill_detector.pkl', 'rb') as handle:
    loaded_model = pickle.load(handle)


import matplotlib.pyplot as plt

def check_item_is_shill(item_data, model=loaded_model, threshold=0.5) -> bool:
    # Extract the features from the item data
    item_features = pd.DataFrame(item_data)

    # Use the model to make a prediction
    prediction = model.predict(item_features)
    probability = model.predict_proba(item_features)
    
    print("Prediction:", prediction)
    print("Probability:", probability)

    # Determine if the item is classified as a shill based on the probability threshold
    if probability[0][prediction[0]] <= threshold:
        is_shill = True
    else:
        is_shill = False

    # Plotting
    classes = model.classes_
    probabilities = probability[0]

    plt.bar(classes, probabilities)
    plt.xlabel('Classes')
    plt.ylabel('Probabilities')
    plt.title('Shill Detection Probabilities')
    plt.show()

    return is_shill


