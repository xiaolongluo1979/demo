import streamlit as st
import pandas as pd
from datetime import date
import os

st.title("DMD Disease Progression Model")
### st.write("Welcome to your first Streamlit app.")

# Initialize a session state to store data
if 'data' not in st.session_state:
    st.session_state.data = []

# Create a form
with st.form("Patient History"):
    st.write("Enter the baseline data:")

    # Add input widgets
    USUBJID = st.text_input("Patient id")
    Start_date = st.date_input("Date Starting Follow Up at Day 1", value=date(2020, 1, 1))  # Default date
    AGE = st.number_input('Age at Baseline', min_value=0)
    NSAA_TS = st.number_input('NSAA Total Score at Baseline', min_value=0)
    A4STR = st.number_input('Acseding 4 Step Time in Second at Baseline', min_value=0)
    ## agree = st.checkbox("I confirm the details are correct")

    st.write("Enter any post baseline data:")
    col1, col2 = st.columns(2)
    Visit_date=[]
    y=[]
   
 # Loop to collect follow-up visit data
    for k in range(5):
        Visit_date.append(
            col1.date_input(
                f"Date of Follow Up Visit {k+1}",
                value=date(2020, 1, 1),
                key=f"visit_date_{k}",
            )
        )
        y.append(
            col2.text_input(  # Use text_input for flexibility
                f"NSAA Total Score at Visit {k+1} (Leave blank for NA)",
                value="",
                key=f"nsaa_score_{k}",
            )
        )

    # Submit button
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    st.write(f"Patient ID: {USUBJID}")
    st.write(f"Date Starting Follow-Up: {Start_date.strftime('%B %d, %Y')}")
    st.write(f"Age at Baseline: {AGE}")
    st.write(f"NSAA Total Score at Baseline: {NSAA_TS}")
    st.write(f"Ascending 4 Step Time at Baseline: {A4STR}")

    st.session_state['data'].append({'USUBJID': USUBJID, 'Start_date': Start_date, 'AGE': AGE,
				'NSAA_TS':NSAA_TS,'A4STR':A4STR,'Visit_date':Visit_date,
				'y':y})

    st.write("Follow-Up Visits:")

    for idx, (visit_date, score) in enumerate(zip(Visit_date, y), start=1):
        try:
            # Convert score to float, or treat as "NA" if blank
            score_display = float(score) if score.strip() else "NA"
        except ValueError:
            score_display = "NA"
        st.write(f"Visit {idx}: {visit_date.strftime('%B %d, %Y')} - NSAA Score: {score_display}")
        


# Display the DataFrame
if st.session_state['data']:
    df = pd.DataFrame(st.session_state['data'])


    st.write("Current DataFrame:")
    st.dataframe(df)

    # Save as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )
else:
    st.info("No data added yet.")
