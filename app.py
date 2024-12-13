import streamlit as st
from pages.dashboard import dashboard_page
from pages.policy import policies_page
import pandas as pd
import re

data = pd.read_csv('pages/dummy_3.csv')

# Clean up the data
data_cleaned = data.drop(columns=[col for col in data.columns if 'Unnamed' in col])
data_cleaned.columns = data_cleaned.columns.str.strip()

def clean_income(income):
    income = re.sub(r'\b(above|below)\b', '', income, flags=re.IGNORECASE).strip()
    income = re.sub(r'(\d+)\s*[<>]=?\s*(\d+)', lambda x: str((int(x.group(1)) + int(x.group(2))) / 2), income)
    income = re.sub(r'(\d+)-(\d+)', lambda x: str((int(x.group(1)) + int(x.group(2))) / 2), income)
    income = re.sub(r'[<>]', '', income)
    try:
        return float(income)
    except ValueError:
        return None

# Clean income column
data_cleaned['Family Annual Income(in lakhs)'] = data_cleaned['Family Annual Income(in lakhs)'].apply(clean_income)

st.title("Student Socio-Economic Data Analysis Dashboard")


st.write("""
    Welcome to the Student Socio-Economic Data Analysis Dashboard.
    
    We offer valuable insights into the socio-economic factors that influence student success, well-being, and opportunities. By analyzing data related to income levels, family background, access to resources, and more, we aim to provide actionable information that can help educators, policymakers, and communities make informed decisions.
""")

st.subheader("Key Features:")

st.write("""
- **Data-Driven Insights:** Explore comprehensive reports on the socio-economic conditions affecting student performance, access to education, and future opportunities.
  
- **Interactive Dashboards:** Visualize trends and key metrics related to income, family structures, academic achievement, and other socio-economic indicators.


- **Policy Recommendations:** Based on the data analysis, receive recommendations that can shape policies to support students from various socio-economic backgrounds, ensuring equitable educational opportunities for all.
""")

st.subheader("Why It Matters:")

st.write("""
    Understanding the socio-economic factors that impact students is crucial for fostering an inclusive educational environment. With our platform, we strive to raise awareness, identify key challenges, and promote interventions that can improve educational outcomes for students from all walks of life.
""")

st.subheader("""
    Created by
""")
st.write("Kishan Rupavatiya")
st.write('Jay Senjaliya')
st.write('Shubham Sharma')
st.write("Hardikkumar Patel")
