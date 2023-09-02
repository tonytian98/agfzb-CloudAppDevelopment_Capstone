import  requests
import json
def test(request, dealer_id):

    if request == "POST":
      
        review = {
            "name": "eee",
            "dealership": dealer_id,
            "review":"content",
            "purchase": "purchasecheck",
            }
            
        json_payload = {"review": review}
        URL = "https://us-south.functions.appdomain.cloud/api/v1/web/9935a40a-054a-4ce3-a68c-bda69f819662/dealership-package/review"
        posttt_request(URL, json_payload, dealerId=dealer_id)
    

def posttt_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")
test("POST",1)