import os
import requests
from dotenv import load_dotenv
# Your helper function to get Mongo client
from helpers.client.get_mongo_client import get_mongo_client

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# Step 1: Get data from MongoDB (including enterpriseId, teamId, and location)


def get_all_dealer_config_data():
    # Connect to MongoDB
    client, db = get_mongo_client(MONGO_URI, MONGO_DB)

    # Fetch all documents from the `dealerConfig` collection
    dealer_config_collection = db['dealerConfig']
    documents = dealer_config_collection.find({})  # Fetch all documents

    for document in documents:
        # Extract the relevant data from each document
        enterprise_id = document.get('enterprise_id')
        # Assuming teamId is stored like this
        team_id = document.get('team_id')

        location_1_data = document.get('dealerships', {}).get(
            'data', {}).get('location_1', {})

        # Pass the data to the post function
        if enterprise_id and team_id and location_1_data:
            post_dealer_details(enterprise_id, team_id, location_1_data)
        else:
            print(f"Missing data in document with enterprise_id: {
                  enterprise_id}")

    client.close()  # Close the connection to MongoDB

# Step 2: Send a POST request to the API


def post_dealer_details(enterprise_id, team_id, location_data):
    enterprise_id = str(enterprise_id) if enterprise_id else 'N/A'
    team_id = str(team_id) if team_id else 'N/A'

    payload = {
         "enterpriseId": enterprise_id,
          "teamId": team_id,
         "name": location_data.get('name', 'N/A'),
            "address": {
                "street": location_data.get('address', 'N/A'),
                "city": location_data.get('city', 'N/A'),
                "state": location_data.get('state', 'N/A'),
                "country": location_data.get('country', 'N/A'),
                "zip": location_data.get('zipcode', 'N/A')
            }
         }

    print("Payload to be sent:", payload)

    # URL for the API
    url = 'http://localhost:1337/dealers/v1/dealer/details'

    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes

        # Print response for debugging
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")


if __name__ == "__main__":
    # Fetch and process all dealer config documents
    get_all_dealer_config_data()
