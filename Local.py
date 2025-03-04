import requests
import json
import csv

# Marketo API credentials
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://your-marketo-instance.mktorest.com"  # Replace with your instance URL


# Function to get access token
def get_access_token():
    auth_url = f"{BASE_URL}/identity/oauth/token?grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    response = requests.get(auth_url)
    data = response.json()
    return data.get("access_token")


# Function to get Marketo assets
def get_marketo_assets(asset_type, access_token):
    url = f"{BASE_URL}/rest/asset/v1/{asset_type}.json?maxReturn=200"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


# Function to save assets to CSV
def save_to_csv(asset_type, data):
    filename = f"{asset_type}.csv"

    if "result" in data and data["result"]:
        # Collect all unique field names from the records
        fieldnames = set()
        for record in data["result"]:
            fieldnames.update(record.keys())

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=list(fieldnames))
            writer.writeheader()
            writer.writerows(data["result"])

        print(f"Saved {asset_type} data to {filename}")
    else:
        print(f"No data found for {asset_type}")


# Main function
def main():
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token")
        return

    asset_types = ["forms", "emails", "programs", "smartCampaigns", "lists", "smartLists"]

    for asset_type in asset_types:
        print(f"Fetching {asset_type}...")
        data = get_marketo_assets(asset_type, access_token)
        save_to_csv(asset_type, data)
        print(f"Saved {asset_type} data to {asset_type}.csv")


if __name__ == "__main__":
    main()
