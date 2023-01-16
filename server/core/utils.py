import pickle
import pandas as pd
from datetime import datetime
import time

from bs4 import BeautifulSoup

from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

APP_ID = "DivineIk-s-PRD-59c7a1d25-67a7167e"
DEV_ID = "f3547dca-f775-4599-bb9f-671721a836a9"
CERT_ID = "PRD-9c7a1d252d9c-ce6c-47c1-b962-69f7"
TOKEN = "v^1.1#i^1#I^3#p^3#r^1#f^0#t^Ul4xMF8wOjRBOEIzQUVDNkFDOTkxMUE1QzQ4MDgzMjEzREFBOUQ3XzNfMSNFXjI2MA=="


def to_seconds(date):
    return time.mktime(date.timetuple())


def login_to_ebay_and_get_browser(username_or_email, password):
    import mechanize
    import http.cookiejar as cookielib  # http.cookiejar in python3

    user_agent = [('user-agent',
                   'Mozilla/5.0 (X11;U;Linux 2.4.2.-2 i586; en-us;m18) Gecko/200010131 Netscape6/6.01'
                   ), ('authority', 'www.ebay.com'), ('method', 'GET'), ('cookie', '__ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=561e4010-3dbe-4fc8-999b-7b1ce9ac6763; __uzmbj2=1669897626; QuantumMetricUserID=6893aa251c4c58a55120e90fda5e9bb6; __uzma=bd2e057e-72f1-4d36-b69d-ab9ede3971aa; __uzmb=1670786918; __uzme=1713; cid=d3FvRhtIOLwhCOcS%23315244244; 5c477a5d-8795-43e4-9f5c-ef67ae7501a5=CgAPmACxjwoItMTk3LjIxMC43MC4yNDksMTk3LjIxMC43MC4yNDksMTA0Ljg2LjExMC4xODkD5wAKY8KCLTE2NzM2OTE2OTMXr8aK; _tk=AQAGAAAAYMxbptVTUlHzoL+Hmb67wBgqp4EfliTUXf2CVe3/WhSrvXpogs+dQDQXv+W8gXIeZHO5weHz1uiBaKOBCPbsw5cUxiOsS4A3uJtekt6fLTReSMdGS/uTVAyt18YnOMmlXQ; __gsas=ID; bm_sv=0F1F98F61FE2BAB93A474F65443613AD~TpWE6i09mxqR69ZPke/TvvvU83RC0AqOPgrr7sB2uY0BkY5r9Nj19kZ2jH3PdgcYx9f0wzytWcqBWwxtTYpQeXyJK5sHJspyCLgXbMGDilgynsngVRmtvWXfOw13K2EFW1R9204qVFavPJdxUuF/rQ; __gads=ID=d88462fd5ff1d567:T=1673691610:S=ALNI_Mbp99P0mLejgJA30yzpp5fJq_jcCQ; QuantumMetricSessionID=63278a7f18d30ffec12a2c34565bb20b; __gpi=UID=00000bc20cf0a42d:T=1673691610:RT=1673792999:S=ALNI_MZiF8CUFhrMjaIOvJMFRydJF0View; cpt=%5Ecpt_guid%3Dfbc7be38-4a67-453a-913f-391ed50fa63a%5Ecpt_prvd%3Dhcaptcha%5E; ds1=ats/1673799025360; shs=BAQAAAYWobRBvAAaAAVUAD2WlWPEyMTUxOTQ0NjI0MDAxLDJAu3dRWuv3r0MW0QezcVXuU9xhcQ**; JSESSIONID=C7F237549D8B7E561B601212D145C9D1; __uzmc=1614523513460; __uzmd=1673802204; __uzmf=7f6000480e484e-f5c0-47e8-8513-404fb16cb28e16707869186503015285471-b08f5a2fbb1e375a235; __uzmcj2=3648211594843; __uzmdj2=1673802208; ak_bmsc=922E36447CB508F5B2F38CFDD7EF85E1~000000000000000000000000000000~YAAQbMYcuABGnEOFAQAAWvaFthIEWY6NHbn2v1tw7B2sL21+4Q5qMGYchm+bmVlzab7EuBxxBWKj/y8UIKlIVhXWlFZXxyimLc/ZnpEtDp3TZvXQnjgoAwKyvxoDvVHPDGYN0e9LvoaA5bW7Vw/8Sl2xAwlYz86WP3SdjoV7Cdy/HQD198s7rdhYy5il2Rc7xbyEI7DbHKjMcB1fvpoNf6IEWyxHBOz+Woi49nL56xARXzoZAOI3TLUgIsJj9/6wcC+ARzPtxen6kD4Cun72QENYx093tYu0jnak/FrKkucyhSpoT1WL03c3YdGa3oa8Sl1Fzsus/AU8CWlrjkHVwTMJjrKfCpe3kpViIolm+zd0upjSm3QsPJSE0l2Iq4cOH3BcxrZW9w==; __deba=i0wpKtFLtHqWtBE8X4PvvZlcmdbDtz1erktPN6_7igHz2kABNe25cbhoF9VdKfFALmnhyK4Qhzcfnncv-bAflTTd0YxGxDIBmEUNbcCk8hv4ooZk5mqE8uSJouG0g5GtTxbSOh-mw8CW_oQN1hkecg==; ebay=%5Ejs%3D1%5EsfLMD%3D0%5Esin%3Din%5Esbf%3D%2360000000000010000000004%5Epsi%3DAiSoN6eM*%5E; ns1=BAQAAAYQ/7+h2AAaAAKUADWWlcJ4yNDg4NTQxMTkyLzA7ANgASmWlcJ5jNjl8NjAxXjE2NzM3OTk0NzAwMDleXjFeM3wyfDV8NHw3fDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NcCs0538RznjrXG4+LxaUvTLZOho; s=BAQAAAYQ/7+h2AAWAAAEACWPFdvFkaXZpa2h1LTAAAwABY8V4uDAADAAKY8V4uDI0ODg1NDExOTIAPQAJY8V4uGRpdmlraHUtMACoAAFjxXbxMQDuAGVjxXi4MwZodHRwczovL3d3dy5lYmF5LmNvbS9zY2gvaS5odG1sP19mcm9tPVI0MCZfc2FjYXQ9NjAwMCZfbmt3PXRlc2xhJnJ0PW5jJkxIX0F1Y3Rpb249MSNpdGVtNTRjNmIxNmIxMAcA+AAgY8V4uGFmYmM2MDQxMTg1MGE2ZTVjNmJjMzQ2M2ZmZmQ1NWI2AUUACGWlcJ42M2M0MWUzMgFlAANjxXi4IzAykeqOzB55p5tZyFzgwKTCl52IKp4*; dp1=bu1p/ZGl2aWtodS0w6786a41e^kms/in6786a41e^pbf/%23200008000e0000001808200000065a5709e^u1f/Divine6786a41e^expt/000167369083353764b31891^mpc/0%7C065a5709e^bl/NGen-US6786a41e^; nonsession=BAQAAAYQ/7+h2AAaAAAQACWWlWPFkaXZpa2h1LTAACAAcY+vKHjE2NzM3OTk0ODB4MzY0MTEwNzY4OTEyeDB4MlkAEAAJZaVwnmRpdmlraHUtMAAzAAplpXCeMzAwMTAyLE5HQQBAAAllpXCeZGl2aWtodS0wAJoACmPGyHFkaXZpa2h1LTBnAJwAOGWlcJ5uWStzSFoyUHJCbWRqNndWblkrc0VaMlByQTJkajZNQW1JcWtESkdEcUE2ZGo2eDluWStzZVE9PQCdAAhlpXCeMDAwMDAwMDEAygAgZ4akHmFmYmM2MDQxMTg1MGE2ZTVjNmJjMzQ2M2ZmZmQ1NWI2AMsAAmPERCYxMwFkAAdnhqQeIzAwMDA4YezfCQPcAMLSFQ2cPhhclM7MKQFo; ds2=asotr/bCQtUzzzzzzz^sotr/bCQtUzzzzzzz^; totp=1673806857689.B/QlnqMvEwgky/XLfatY4BxNypQ2Se/3sYLYHE/8eGTZckuKwjXfoN5j96bcJfa90u1XXZCbSqnDr0UBBCFMMfwVE4sq92uHPyG9tW9zu9hCcvKsxg4BbKVY4PN4UNHF'),
                  ('sec-ch-ua-platform', 'Windows'), ('sec-fetch-site', 'same-origin')]
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = user_agent
    br.set_cookiejar(cj)
    br.open("https://www.ebay.com/signin/")

    br.select_form(nr=0)
    br.form['userid'] = username_or_email
    br.form['pass'] = password
    br.submit()
    print(br.response().read())
    return br


def scrape_and_get_item_bidders(item_id):
    br = login_to_ebay_and_get_browser("divuzki@gmail.com", "@divineQ1")
    br.open(f"https://www.ebay.com/bfl/viewbids/{item_id}?item={item_id}")
    soup = BeautifulSoup(br.response().read(), 'html.parser')
    bidders = soup.find_all("a")
    bidders_list = []
    bidder_id = 0
    for bidder in bidders:
        if bidder.has_attr('href'):
            if 'ViewBidderProfile' in bidder['href'] and 'item={}'.format(item_id) in bidder['href']:
                new_br = br
                new_br.open(bidder['href'])
                new_soup = BeautifulSoup(
                    new_br.response().read(), 'html.parser')
                possible_feedback = new_soup.find_all("span")
                # check if the span text is equal to Feedback Score
                for span in possible_feedback:
                    if span.text == "Feedback":
                        bidder_id += 1
                        feedback_score = span.parent.find_all("span")[1].text
                        bidders_list.append({'bidder_id': bidder_id, 'feedback_score': 1 if (
                            'positive' in feedback_score) else 0, 'feedback': feedback_score.replace('positive', '').replace('negative', '')})
    print(bidders_list)
    return bidders


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
    # print(item)
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
        # 'Auction_ID': item['sellerInfo']['sellerUserName'],
    })
    return data


def train_shill_detector(data_path):
    # Load the data into a pandas DataFrame
    df = pd.read_csv(data_path)

    # Extract the features you want to use
    X = df[['Bidder_Tendency', 'Bidding_Ratio', 'Successive_Outbidding', 'Last_Bidding',
            'Auction_Bids', 'Starting_Price_Average', 'Early_Bidding', 'Winning_Ratio', 'Auction_Duration']]
    y = df['Class']

    # Split the data into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Train the model
    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)

    # Evaluate the model on the testing data
    y_pred = logistic_regression.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    # Save the model to a file
    with open('shill_detector.pkl', 'wb') as handle:
        pickle.dump(logistic_regression, handle,
                    protocol=pickle.HIGHEST_PROTOCOL)

    return logistic_regression

# train_shill_detector("shill_bidding_dataset.csv")


# Load the model from a file
with open('shill_detector.pkl', 'rb') as handle:
    loaded_model = pickle.load(handle)

# # create a dataframe for the new item
# item_data = pd.DataFrame({
#     'Bidder_Tendency': [0.5],
#     'Bidding_Ratio': [0.2],
#     'Successive_Outbidding': [5],
#     'Last_Bidding': [100],
#     'Auction_Bids': [50],
#     'Starting_Price_Average': [20],
#     'Early_Bidding': [10],
#     'Winning_Ratio': [0.4],
#     'Auction_Duration': [7]
# })


def check_item_is_shill(item_data, model, threshold=0.5) -> bool:
    # Extract the features from the item data
    print(item_data)
    item_features = pd.DataFrame(item_data)
    # item_features = extract_data(item_data)

    # Use the model to make a prediction
    prediction = model.predict(item_features)
    probability = model.predict_proba(item_features)
    print(prediction, probability)
    if probability[0][prediction[0]] <= threshold:
        return True
    else:
        return False

    return prediction, probability


# check the item using the loaded model
# item_data = extract_data(get_item_info("185737032386"))
# print(get_bid_history("185737032386"))
# scrape_and_get_item_bidders("185737032386")
# print(check_item(item_data, loaded_model))
