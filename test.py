import streamlit as st
import requests
import csv
import json
from io import StringIO

# UI Title
st.title("Marketo Asset Downloader")

# User Inputs
base_url = st.text_input("Enter Marketo Instance URL", "https://your-marketo-instance.mktorest.com")
client_id = st.text_input("Enter Client ID", "", type="password")
client_secret = st.text_input("Enter Client Secret", "", type="password")
asset_types = ["forms", "emails", "programs", "smartCampaigns", "lists", "smartLists"]
selected_asset = st.selectbox("Select Asset Type", asset_types)


# Function to get access token
def get_access_token(base_url, client_id, client_secret):
    auth_url = f"{base_url}/identity/oauth/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    response = requests.get(auth_url)
    data = response.json()
    return data.get("access_token")


# Function to get Marketo assets
def get_marketo_assets(base_url, asset_type, access_token):
    url = f"{base_url}/rest/asset/v1/{asset_type}.json?maxReturn=200"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


# Function to generate CSV
# Function to generate CSV in byte format
def generate_csv(data):
    if "result" in data and data["result"]:
        fieldnames = set()
        for record in data["result"]:
            fieldnames.update(record.keys())

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(data["result"])

        return output.getvalue().encode("utf-8")  # Convert to bytes
    return None



# Execute Button
if st.button("Execute"):
    if not base_url or not client_id or not client_secret:
        st.error("Please enter all required fields.")
    else:
        st.info("Fetching data...")
        access_token = get_access_token(base_url, client_id, client_secret)
        if access_token:
            data = get_marketo_assets(base_url, selected_asset, access_token)
            csv_output = generate_csv(data)
            if csv_output:
                st.download_button(
                    label=f"Download {selected_asset}.csv",
                    data=csv_output,
                    file_name=f"{selected_asset}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for the selected asset.")
        else:
            st.error("Failed to get access token. Please check your credentials.")
