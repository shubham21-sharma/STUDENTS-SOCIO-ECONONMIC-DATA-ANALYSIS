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

def dashboard_page():
    st.title("Dashboard Page")
    st.markdown('---')
    program_options = ['Any'] + list(data_cleaned['Program'].unique())
    income_options = ['Any'] + list(data_cleaned['Family Annual Income(in lakhs)'].dropna().unique())
    hometown_options = ['Any'] + list(data_cleaned['Native'].unique())
    fathers_occupation_options = ['Any'] + list(data_cleaned["Father's Occupation"].unique())
    laptop_options = ['Any'] + list(data_cleaned['laptop'].unique())
    transportation_options = ['Any'] + list(data_cleaned['Mode of Transportation'].unique())
    medium_education_options = ['Any'] + list(data_cleaned['Medium of Education'].unique())
    board_options = ['Any'] + list(data_cleaned['Board'].unique())
    interest_options = ['Any'] + list(data_cleaned['Intrested in higher studies in India'].unique())
    education_loan_options = ['Any'] + list(data_cleaned['Education Loan Taken'].unique())

    # Sidebar filters
    selected_programs = st.sidebar.multiselect('Select Program(s)', options=program_options, default='Any')
    selected_income_range = st.sidebar.multiselect('Select Income Range', options=income_options, default='Any')
    selected_hometowns = st.sidebar.multiselect('Select Hometown(s)', options=hometown_options, default='Any')
    selected_fathers_occupation = st.sidebar.multiselect("Select Father's Occupation", options=fathers_occupation_options, default='Any')
    selected_laptop_ownership = st.sidebar.multiselect('Select Laptop Ownership', options=laptop_options, default='Any')
    selected_transportation_modes = st.sidebar.multiselect('Select Mode of Transportation', options=transportation_options, default='Any')
    selected_mediums_of_education = st.sidebar.multiselect('Select Medium of Education', options=medium_education_options, default='Any')
    selected_boards_of_education = st.sidebar.multiselect('Select Board of Education', options=board_options, default='Any')
    selected_interest_in_higher_studies = st.sidebar.multiselect('Select Interest in Higher Education', options=interest_options, default='Any')
    selected_education_loan = st.sidebar.multiselect('Select Education Loan Taken', options=education_loan_options, default='Any')

    # Apply filters, use all unique values when 'Any' is selected
    filtered_data = data_cleaned[
        (data_cleaned['Program'].isin(data_cleaned['Program'].unique() if 'Any' in selected_programs else selected_programs)) &
        (data_cleaned['Family Annual Income(in lakhs)'].isin(data_cleaned['Family Annual Income(in lakhs)'].dropna().unique() if 'Any' in selected_income_range else selected_income_range)) &
        (data_cleaned['Native'].isin(data_cleaned['Native'].unique() if 'Any' in selected_hometowns else selected_hometowns)) &
        (data_cleaned["Father's Occupation"].isin(data_cleaned["Father's Occupation"].unique() if 'Any' in selected_fathers_occupation else selected_fathers_occupation)) &
        (data_cleaned['laptop'].isin(data_cleaned['laptop'].unique() if 'Any' in selected_laptop_ownership else selected_laptop_ownership)) &
        (data_cleaned['Mode of Transportation'].isin(data_cleaned['Mode of Transportation'].unique() if 'Any' in selected_transportation_modes else selected_transportation_modes)) &
        (data_cleaned['Medium of Education'].isin(data_cleaned['Medium of Education'].unique() if 'Any' in selected_mediums_of_education else selected_mediums_of_education)) &
        (data_cleaned['Board'].isin(data_cleaned['Board'].unique() if 'Any' in selected_boards_of_education else selected_boards_of_education)) &
        (data_cleaned['Intrested in higher studies in India'].isin(data_cleaned['Intrested in higher studies in India'].unique() if 'Any' in selected_interest_in_higher_studies else selected_interest_in_higher_studies)) &
        (data_cleaned['Education Loan Taken'].isin(data_cleaned['Education Loan Taken'].unique() if 'Any' in selected_education_loan else selected_education_loan))
    ]

    st.markdown(" Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Total Students", value=len(filtered_data))
    col2.metric(label="Average 12th Percentage", value=round(data['12th Percentage'].mean(), 2))
    col3.metric(label="Average Family Income", value=f"{round(filtered_data['Family Annual Income(in lakhs)'].mean(), 2)} L")
    col4.metric(label="Laptop Owners", value=filtered_data['laptop'].value_counts().get('Yes', 0))

    st.markdown("---")
    def add_counts(ax):
        for bar in ax.patches:
            bar_height = bar.get_height()
            ax.annotate(f'{int(bar_height)}', (bar.get_x() + bar.get_width() / 2, bar_height), ha='center', va='bottom', fontsize=10, color='black')


    # 12th Percentage Distribution and Family Income Distribution
    st.markdown("12th Percentage Distribution")
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 5))
        ax=sns.histplot(data['12th Percentage'], kde=True, color='blue', bins=10)
        add_counts(ax)
        plt.legend(title='12th Percentage', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart shows the distribution of students' 12th-grade percentage scores. The curve represents the density of students across different percentages, helping identify the most common performance levels.")

    with col2:
        st.markdown(" Family Annual Income Distribution")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Family Annual Income(in lakhs)', hue='Family Annual Income(in lakhs)', data=filtered_data, palette='Set2')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Income Range', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart illustrates the distribution of family annual income ranges. The x-axis represents the income brackets, while the height of each bar indicates the number of students in that income range.")

    st.markdown("---")

    # Program Enrollment Breakdown and Mode of Transportation by Program
    st.markdown("Program Enrollment Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Program', hue='Program', data=filtered_data, palette='Set1')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Program', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This bar chart presents the number of students enrolled in each program, giving an overview of program popularity.")

    with col2:
        st.markdown(" Mode of Transportation by Program")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Mode of Transportation', hue='Program', data=filtered_data, palette='Set3')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Program', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart compares the modes of transportation students use to reach their program of study, broken down by the program they are enrolled in.")

    st.markdown("---")

    # Hometown Distribution and Family Income by Hometown
    st.markdown("Hometown Distribution of Students")
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Native', hue='Native', data=filtered_data, palette='Set3')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Hometown', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart displays the number of students from various hometowns, providing insights into the geographical diversity of the student body.")

    with col2:
        st.markdown(" Family Annual Income by Hometown")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Native', y='Family Annual Income(in lakhs)', data=filtered_data, palette='Set2')
        plt.xticks(rotation=45)
        plt.legend(title='Income vs Hometown')
        st.pyplot(plt)
        st.write("This boxplot illustrates the variation in family annual income across different hometowns, with each box representing the income range for students from a specific location.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(" Family Income vs Higher Studies Interest")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Family Annual Income(in lakhs)', y='Intrested in higher studies in India', data=filtered_data, palette='Set3')
        plt.xticks(rotation=45)
        plt.legend(title='Higher Studies vs Income')
        st.pyplot(plt)
        st.write("This plot examines the relationship between family income and students' interest in pursuing higher education in India.")

    with col2:
        st.markdown(" Board vs Native Location")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax=sns.countplot(x='Board', hue='Native', data=filtered_data, palette='Set1')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Board vs Hometown',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
        st.write("This chart shows the distribution of students' educational boards across different hometowns, highlighting regional trends in education.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Education Loan vs Family Income")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Education Loan Taken', y='Family Annual Income(in lakhs)', data=filtered_data, palette='Set2')
        plt.xticks(rotation=45)
        plt.legend(title='Loan vs Income',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This boxplot compares family income levels with whether students have taken an education loan, showing income trends among loan takers.")

    st.markdown("---")

    # Additional breakdowns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(" Board vs Program")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Board', hue='Program', data=filtered_data, palette='Set2')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Board vs Program',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart breaks down the distribution of educational boards within different academic programs.")

    with col2:
        st.markdown(" Medium of Education vs Program")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Medium of Education', hue='Program', data=filtered_data, palette='Set3')
        add_counts(ax)
        plt.xticks(rotation=45)
        plt.legend(title='Medium vs Program',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart compares the medium of education (English, local languages, etc.) across different academic programs.")

    # Additional comparisons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Laptop Ownership by Program")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='laptop', hue='Program', data=filtered_data, palette='Set2')
        add_counts(ax)
        plt.legend(title='Laptop Ownership vs Program',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart highlights the laptop ownership status of students across different academic programs.")
        
    with col2:
        st.markdown("Interest in Higher Studies by Program")
        plt.figure(figsize=(8, 5))
        ax=sns.countplot(x='Intrested in higher studies in India', hue='Program', data=filtered_data, palette='Set2')
        add_counts(ax)
        plt.legend(title='Higher Studies Interest vs Program',bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)
        st.write("This chart shows the interest of students in pursuing higher studies in India, broken down by their program.")

    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Education Loan Taken', y='Family Annual Income(in lakhs)', data=filtered_data, palette='Set2')
        plt.title("Family Annual Income vs Education Loan Taken")
        plt.ylabel("Family Annual Income (in lakhs)")
        plt.xlabel("Education Loan Taken")
        plt.show()

    st.markdown("### CGPA Analysis")

    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 5))
        ax=sns.histplot(filtered_data['CGPA'], kde=True, color='blue', bins=10)
        add_counts(ax)
        plt.title("CGPA Distribution")
        st.pyplot(plt)
        st.write("This chart shows the distribution of CGPA scores among the students.")

    with col2:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Program', y='CGPA', data=filtered_data, palette='Set2')
        plt.xticks(rotation=45)
        plt.title("CGPA by Program")
        st.pyplot(plt)
        st.write("This boxplot compares the distribution of CGPA scores across different academic programs.")

    # Correlation between CGPA and Higher Studies
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### CGPA vs Higher Studies Interest")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Intrested in higher studies in India', y='CGPA', data=filtered_data, palette='Set3')
        plt.title("CGPA vs Interest in Higher Studies")
        st.pyplot(plt)
        st.write("This boxplot shows the relationship between CGPA and students' interest in higher studies in India.")

    # Correlation between CGPA and Family Income

    with col2:
        st.markdown("### CGPA vs Family Income")
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x='Family Annual Income(in lakhs)', y='CGPA', data=filtered_data, hue='Program', palette='Set2')
        plt.title("CGPA vs Family Income")
        st.pyplot(plt)
        st.write("This scatterplot visualizes the relationship between family annual income and CGPA.")

    # Correlation between CGPA and Laptop Ownership
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### CGPA vs Laptop Ownership")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='laptop', y='CGPA', data=filtered_data, palette='Set3')
        plt.title("CGPA vs Laptop Ownership")
        st.pyplot(plt)
        st.write("This boxplot shows how CGPA varies with laptop ownership among students.")

    # Correlation between CGPA and Native Location
    with col2:
        st.markdown("### CGPA vs Native Location")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Native', y='CGPA', data=filtered_data, palette='Set1')
        plt.xticks(rotation=45)
        plt.title("CGPA vs Native Location")
        st.pyplot(plt)
        st.write("This boxplot compares the CGPA of students across different native locations.")

    # Correlation between CGPA and Medium of Education
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### CGPA vs Medium of Education")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Medium of Education', y='CGPA', data=filtered_data, palette='Set2')
        plt.xticks(rotation=45)
        plt.title("CGPA vs Medium of Education")
        st.pyplot(plt)
        st.write("This chart shows how CGPA is influenced by the medium of education (English, local languages, etc.).")

    # Correlation between CGPA and Board of Education
    with col2:
        st.markdown("### CGPA vs Board of Education")
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Board', y='CGPA', data=filtered_data, palette='Set3')
        plt.xticks(rotation=45)
        plt.title("CGPA vs Board of Education")
        st.pyplot(plt)
        st.write("This boxplot compares CGPA across students from different educational boards (CBSE, State Boards, etc.).")

    st.markdown("### Correlation Matrix: CGPA vs 12th Percentage")
    cgpa_vs_12th_percentage = data_cleaned[['CGPA', '12th Percentage']].corr()
    st.write(cgpa_vs_12th_percentage)

    # Visualize the CGPA vs 12th Percentage correlation matrix
    plt.figure(figsize=(4, 3))
    sns.heatmap(cgpa_vs_12th_percentage, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("CGPA vs 12th Percentage Correlation")
    st.pyplot(plt)

    st.markdown("---")

    # 2. Correlation Matrix: CGPA vs Family Annual Income
    st.markdown("### Correlation Matrix: CGPA vs Family Annual Income")
    cgpa_vs_family_income = data_cleaned[['CGPA', 'Family Annual Income(in lakhs)']].corr()
    st.write(cgpa_vs_family_income)

    # Visualize the CGPA vs Family Annual Income correlation matrix
    plt.figure(figsize=(4, 3))
    sns.heatmap(cgpa_vs_family_income, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("CGPA vs Family Annual Income Correlation")
    st.pyplot(plt)    
    # Display filtered data
    if st.checkbox('Show filtered data'):
        st.dataframe(filtered_data)

if __name__ == "__main__":
    dashboard_page()
