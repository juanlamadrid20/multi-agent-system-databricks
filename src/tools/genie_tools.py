import os
import requests
import time
from agents import function_tool
import streamlit as st


@function_tool
def get_store_performance_info(user_query: str):
    """
    For us, we use this to get information about the store location, store performance, returns, BOPIS(buy online pick up in store) etc.
    """
    st.write(
        "<span style='color:green;'>[🛠️TOOL-CALL]: the <a href='https://e2-demo-field-eng.cloud.databricks.com/genie/rooms/01f03a38fa6b1b9cbfb7027d932045e4' target='_blank'>get_store_performance_info</a> tool was called</span>",
        unsafe_allow_html=True,
    )
    print("INFO: `get_store_performance_info` tool called")
    databricks_instance = os.getenv("DATABRICKS_HOST")
    space_id = os.getenv("GENIE_SPACE_ID")
    access_token = os.getenv("DATABRICKS_TOKEN")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    poll_interval = 2.0
    timeout = 60.0

    # Step 1: Start a new conversation
    start_url = (
        f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/start-conversation"
    )
    payload = {"content": user_query}
    resp = requests.post(start_url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print(data)
    conversation_id = data["conversation_id"]
    message_id = data["message_id"]

    # Step 2: Poll for completion
    poll_url = f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}"
    start_time = time.time()
    while True:
        poll_resp = requests.get(poll_url, headers=headers)
        poll_resp.raise_for_status()
        poll_data = poll_resp.json()
        status = poll_data.get("status")
        if status == "COMPLETED":
            attachment_id = poll_data["attachments"][0]["attachment_id"]
            url = f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/attachments/{attachment_id}/query-result"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["statement_response"]
        if time.time() - start_time > timeout:
            raise TimeoutError("Genie API query timed out.")
        time.sleep(poll_interval)


@function_tool
def get_product_inventory_info(user_query: str):
    """
    For us, we use this to get information about products and the current inventory snapshot across stores
    """
    st.write(
        "<span style='color:green;'>[🛠️TOOL-CALL]: the <a href='https://e2-demo-field-eng.cloud.databricks.com/genie/rooms/01f03a384f82135fbf006fdbe7810caa' target='_blank'>get_product_inventory_info</a> tool was called</span>",
        unsafe_allow_html=True,
    )
    print("INFO: `get_product_inventory_info` tool called")
    databricks_instance = os.getenv("DATABRICKS_HOST")
    space_id = os.getenv("GENIE_SPACE_PRODUCT_INV_ID")
    access_token = os.getenv("DATABRICKS_TOKEN")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    poll_interval = 2.0
    timeout = 60.0

    # Step 1: Start a new conversation
    start_url = (
        f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/start-conversation"
    )
    payload = {"content": user_query}
    resp = requests.post(start_url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print(data)
    conversation_id = data["conversation_id"]
    message_id = data["message_id"]

    # Step 2: Poll for completion
    poll_url = f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}"
    start_time = time.time()
    while True:
        poll_resp = requests.get(poll_url, headers=headers)
        poll_resp.raise_for_status()
        poll_data = poll_resp.json()
        status = poll_data.get("status")
        if status == "COMPLETED":
            attachment_id = poll_data["attachments"][0]["attachment_id"]
            url = f"{databricks_instance}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/attachments/{attachment_id}/query-result"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["statement_response"]
        if time.time() - start_time > timeout:
            raise TimeoutError("Genie API query timed out.")
        time.sleep(poll_interval)