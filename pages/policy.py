import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

# Load the data

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
def policies_page():
    st.title("Policies Page")
    st.write("Here are the details of our various policies.")
    merit_scholarship_students = data_cleaned.nlargest(15, 'CGPA')
    st.subheader("1. Merit Based Scholarship")
    st.write("Top 5 students with highest CGPA:")
    st.dataframe(merit_scholarship_students)

    # Need Based Scholarship - Top 5 students with high CGPA and income <= 5 lakhs
    average_cgpa = data_cleaned['CGPA'].mean()
    need_scholarship_students = data_cleaned[
    (data_cleaned['Family Annual Income(in lakhs)'] <= 5) & 
    (data_cleaned['CGPA'] < average_cgpa)
    ].nsmallest(15, 'CGPA')
    st.subheader("2. Need Based Scholarship")
    st.write("Top 5 students with low to medium CGPA and family annual income of 5 lakhs or below:")
    st.dataframe(need_scholarship_students)


    monetary_support_students = data_cleaned[
    (data_cleaned['Family Structure'].isin(['Single-Parent', 'Orphaned'])) &
    (data_cleaned['CGPA'] >= data_cleaned['CGPA'].mean()) &
    (data_cleaned['Family Annual Income(in lakhs)'] <= 5) &
    (data_cleaned['Number of Students in Family']>1)
    ].nsmallest(15, 'CGPA')

    st.subheader("3. Monetary Support for Students with Specific Family Structure")
    st.write("Students with high CGPA and a family structure as a single parent or orphaned:")
    st.dataframe(monetary_support_students)

    # Laptop Policy - Students who don't have a laptop and family income <= 5 lakhs
    laptop_policy_students = data_cleaned[
        (data_cleaned['laptop'] == 'No') & 
        (data_cleaned['Family Annual Income(in lakhs)'] <= 5) &
        (data_cleaned['CGPA']>=data_cleaned['CGPA'].mean())
    ].nlargest(15, 'CGPA')
    
    st.subheader("4. Laptop Policy")
    st.write("Students who do not have a laptop and family income of 5 lakhs or below:")
    st.dataframe(laptop_policy_students)

    st.subheader("5.Accessibility Accommodation Policy")
    st.write("Offers support and resources to students with disabilities, ensuring equitable access to education.")
    accessibility_acc=data_cleaned[
    (data_cleaned['Disability Status']=='Yes')&
    (data_cleaned['CGPA']>=data_cleaned['CGPA'].mean())   
    ].nlargest(15,'CGPA')
    st.dataframe(accessibility_acc)

    st.subheader("6. Language Mentorship")
    language_mentorship_students = data_cleaned[
    (data_cleaned['Medium of Education'].isin(['Gujarati', 'Hindi'])) &
    (data_cleaned['Board'] == 'State Board') &
    (data_cleaned['12th Percentage']>=data_cleaned['12th Percentage'].mean())]
    st.write("Students whose medium of education is Gujarati or Hindi, studied in State Board, and have a medium 12th percentage:")
    st.dataframe(language_mentorship_students)

    st.subheader("7.Academic Mentorship Policy")
    st.write("Students are paired with mentors based on their academic interests and goals. Mentors provide guidance on coursework, research opportunities, career paths, and more. Open to all students, with a special focus on freshmen and those in academic need.")
    
    st.subheader("8. Entrepreneurship and Innovation Support Policy")
    st.write("Offers startup incubation, seed funding, mentorship programs, and innovation labs.")

    
if __name__ == "__main__":
    policies_page()
