import os
from agents import function_tool
import streamlit as st
from src.utils.genie_client import GenieClient

# Initialize Genie client
genie_client = GenieClient()


@function_tool
def get_store_performance_info(user_query: str):
    """
    For us, we use this to get information about the store location, store performance, returns, BOPIS(buy online pick up in store) etc.
    """
    st.write(
        f"<span style='color:green;'>[🛠️TOOL-CALL]: the <a href='{os.getenv('DATABRICKS_HOST')}/genie/rooms/{os.getenv('GENIE_SPACE_STORE_PERFORMANCE_ID')}/monitoring' target='_blank'>get_store_performance_info</a> tool was called</span>",
        unsafe_allow_html=True,
    )
    
    return genie_client.query_store_performance(user_query)


@function_tool
def get_product_inventory_info(user_query: str):
    """
    For us, we use this to get information about products and the current inventory snapshot across stores
    """
    st.write(
        f"<span style='color:green;'>[🛠️TOOL-CALL]: the <a href='{os.getenv('DATABRICKS_HOST')}/genie/rooms/{os.getenv('GENIE_SPACE_PRODUCT_INV_ID')}/monitoring' target='_blank'>get_product_inventory_info</a> tool was called</span>",
        unsafe_allow_html=True,
    )
    
    return genie_client.query_product_inventory(user_query)