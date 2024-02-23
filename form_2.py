import streamlit as st
import pandas as pd
import pymongo
import urllib.parse
import datetime
import csv
import io
import base64 

# Escape username and password
username = urllib.parse.quote_plus("khushi")
password = urllib.parse.quote_plus("Khushi@2109")

# Construct the MongoDB connection string
connection_string = f"mongodb+srv://{username}:{password}@cluster1.kajywqv.mongodb.net/"

def main():
    st.title("Data Retrieval")

    # Input fields
    file_name = st.text_input("File name", "data.csv")
    from_date = st.date_input("From Date")
    to_date = st.date_input("To Date")

    # Submit button
    if st.button("Submit"):
        # Connect to the MongoDB server
        client = pymongo.MongoClient(connection_string)
        
        # Select a database
        db = client["Sample_DB"]
        
        # Select a collection within the database
        collection = db["Sample_Coll"]

        # Convert date objects to datetime
        from_date = datetime.datetime.combine(from_date, datetime.time.min)
        to_date = datetime.datetime.combine(to_date, datetime.time.max)

        # Retrieve data from MongoDB within the specified date range
        data = collection.find({
            "Timestamp": {
                "$gte": from_date,
                "$lte": to_date
            }
        })

        # Convert MongoDB cursor to DataFrame
        df = pd.DataFrame(list(data))

        # Download CSV file
        if not df.empty:
            csv_data = df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("No data found within the specified date range.")

if _name_ == "_main_":
    main()
