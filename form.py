import streamlit as st
import pandas as pd
import pymongo
import datetime
import urllib.parse

# Escape username and password
username = urllib.parse.quote_plus("tanay")
password = urllib.parse.quote_plus("tanay123")

# Construct the MongoDB connection string
connection_string = "mongodb+srv://tanay:tanay123@tanay.drqdft7.mongodb.net/"

def main():
    st.title("Expense Reimbursement Form")

    # Input fields
    name = st.text_input("Name")
    reimbursement_item = st.text_input("Reimbursement (for which item)")
    amount = st.number_input("Amount", step=1.0)
    status = st.radio("Status", ("Yes", "No"))
    date_issued = st.date_input("Date issued")
    date_payment_done = st.date_input("Date payment done")

    # Submit button
    if st.button("Submit"):
        # Connect to the MongoDB server
        client = pymongo.MongoClient(connection_string)

        client.server_selection_timeout = None

        # Select a database
        db = client["Sample_DB"]

        # Select a collection within the database
        collection = db["Sample_Col"]

        # Convert date objects to datetime
        date_issued = datetime.datetime.combine(date_issued, datetime.time.min)
        date_payment_done = datetime.datetime.combine(date_payment_done, datetime.time.min)

        # Generate timestamp for submission
        timestamp = datetime.datetime.now()

        # Create dictionary to store data
        data = {
            "Name": name,
            "Reimbursement (for which item)": reimbursement_item,
            "Amount": amount,
            "Status": status,
            "Date issued": date_issued,
            "Date payment done": date_payment_done,
            "Timestamp": timestamp
        }

        # Insert the data into the collection
        collection.insert_one(data)

        # Display a success message
        st.success("Data submitted successfully!")

if __name__ == "__main__":
    main()