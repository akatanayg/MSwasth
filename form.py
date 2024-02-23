import streamlit as st
import pandas as pd
import pymongo
import datetime
import urllib.parse

# Escape username and password
username = urllib.parse.quote_plus("khushi")
password = urllib.parse.quote_plus("Khushi@2109")

# Construct the MongoDB connection string
connection_string = f"mongodb+srv://{username}:{password}@cluster1.kajywqv.mongodb.net/"

def main():
    st.title("Expense Reimbursement Form")

    # Input fields
    name = st.text_input("Name")
    reimbursement_item = st.text_input("Reimbursement (for which item)")
    status = st.radio("Status", ("Yes", "No"))
    date_issued = st.date_input("Date issued")
    date_payment_done = st.date_input("Date payment done")

    # Submit button
    if st.button("Submit"):
        # Connect to the MongoDB server
        client = pymongo.MongoClient(connection_string)
        
        # Select a database
        db = client["Sample_DB"]
        
        # Select a collection within the database
        collection = db["Sample_Coll"]

        # Convert date objects to datetime
        date_issued = datetime.datetime.combine(date_issued, datetime.time.min)
        date_payment_done = datetime.datetime.combine(date_payment_done, datetime.time.min)

        # Generate timestamp for submission
        timestamp = datetime.datetime.now()

        # Create dictionary to store data
        data = {
            "Name": name,
            "Reimbursement (for which item)": reimbursement_item,
            "Status": status,
            "Date issued": date_issued,
            "Date payment done": date_payment_done,
            "Timestamp": timestamp
        }

        # Insert the data into the collection
        collection.insert_one(data)

        # Display a success message
        st.success("Data submitted successfully!")

if _name_ == "_main_":
    main()
