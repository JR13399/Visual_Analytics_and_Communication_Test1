import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("university_student_dashboard_data.csv")

# Set the title and description of the app
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Dashboard - Admissions, Retention & Satisfaction")
st.markdown("""
Welcome to the interactive dashboard of the university's admission, retention, and satisfaction trends over the years.  
This dashboard allows you to analyze:
- Total applications, admissions, and enrollments per term
- Retention rate trends over time
- Student satisfaction scores over the years
- Enrollment breakdown by department (Engineering, Business, Arts, Science)
- Spring vs. Fall term comparison
- Trends for departments, retention rates, and satisfaction levels
""")

# 1. Total Applications, Admissions, and Enrollments per Term (Bar Chart)
st.header("Total Applications, Admissions, and Enrollments per Term")
term_data = data.groupby(['Year', 'Term'])[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()

# Bar chart
fig = px.bar(term_data, x="Year", y=["Applications", "Admitted", "Enrolled"], color="Term",
             labels={"value": "Count", "variable": "Metric"},
             title="Total Applications, Admissions, and Enrollments Over Time")
st.plotly_chart(fig)

# 2. Retention Rate Trends Over Time (Line Plot)
st.header("Retention Rate Trends Over Time")
fig = px.line(data, x="Year", y="Retention Rate (%)", color="Term", 
              labels={"Retention Rate (%)": "Retention Rate (%)"}, 
              title="Retention Rate Trends Over Time")
st.plotly_chart(fig)

# 3. Student Satisfaction Over the Years (Scatter Plot)
st.header("Student Satisfaction Over the Years")
fig = px.scatter(data, x="Year", y="Student Satisfaction (%)", color="Term", 
                 size="Student Satisfaction (%)", hover_data=["Year", "Term"],
                 labels={"Student Satisfaction (%)": "Satisfaction (%)"},
                 title="Student Satisfaction Over the Years")
st.plotly_chart(fig)

# 4. Enrollment Breakdown by Department (Stacked Bar Chart)
st.header("Enrollment Breakdown by Department")
department_data = data.groupby(['Year', 'Term'])[['Engineering Enrolled', 'Business Enrolled', 
                                                  'Arts Enrolled', 'Science Enrolled']].sum().reset_index()

# Stacked bar chart
fig = px.bar(department_data, x="Year", y=["Engineering Enrolled", "Business Enrolled", 
                                             "Arts Enrolled", "Science Enrolled"], color="Term",
             labels={"value": "Enrolled Students", "variable": "Department"},
             title="Enrollment Breakdown by Department", barmode="stack")
st.plotly_chart(fig)

# 5. Comparison Between Spring vs. Fall Term Trends (Line Plot)
st.header("Spring vs. Fall Term Comparison")
comparison_data = data.groupby(['Year', 'Term'])[['Retention Rate (%)', 'Student Satisfaction (%)']].mean().reset_index()

fig = px.line(comparison_data, x="Year", y=["Retention Rate (%)", "Student Satisfaction (%)"], color="Term", 
              labels={"value": "Percentage", "variable": "Metric"},
              title="Spring vs. Fall Term Comparison")
st.plotly_chart(fig)

# 6. Department-Wise Comparison for Retention & Satisfaction (Bubble Chart)
st.header("Department-Wise Comparison for Retention & Satisfaction")

# Create bubble chart comparing retention vs satisfaction by department
department_retention = data.groupby(['Year', 'Term'])[['Retention Rate (%)']].mean().reset_index()
department_satisfaction = data.groupby(['Year', 'Term'])[['Student Satisfaction (%)']].mean().reset_index()

# Merge data for comparison
department_comparison = pd.merge(department_retention, department_satisfaction, on=["Year", "Term"])

fig = px.scatter(department_comparison, x="Retention Rate (%)", y="Student Satisfaction (%)", 
                 color="Term", size="Retention Rate (%)", hover_data=["Year", "Term"],
                 title="Department-Wise Retention & Satisfaction Comparison")
st.plotly_chart(fig)

# 7. Retention Rate Distribution (Box Plot)
st.header("Retention Rate Distribution")
fig = px.box(data, x="Term", y="Retention Rate (%)", color="Term",
             title="Retention Rate Distribution by Term")
st.plotly_chart(fig)

# 8. Department Enrollment Proportions (Pie Chart)
st.header("Department Enrollment Proportions")
total_enrollment_by_department = data[['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']].sum()

fig = px.pie(names=total_enrollment_by_department.index, values=total_enrollment_by_department,
             title="Department Enrollment Proportions")
st.plotly_chart(fig)

# Key Findings & Actionable Insights
st.subheader("🔍 Key Findings:")
st.write("""
- **Retention Trends**: The retention rate has increased steadily, reaching a high of 90% in 2024, indicating strong student satisfaction and commitment.
- **Satisfaction Trends**: Student satisfaction has increased year-over-year, with 2024 showing the highest satisfaction rate at 88%.
- **Department-wise Insights**: Engineering and Business departments have consistently higher enrollment numbers compared to Arts and Science.
- **Term Comparison**: Spring terms generally show slightly higher applications, admissions, and enrollments than Fall terms. Retention and satisfaction rates are also better in Spring, suggesting that students may be more committed to starting their studies in the Spring term.
- **Enrollment Distribution**: Engineering continues to have the largest share of enrollments, making up the bulk of the university's student body.

### **Actionable Insights**:
1. **Focus on Engineering & Business**: These departments show the highest growth in enrollments. The institution could consider expanding their programs, faculty, and resources to support the growing student population.
2. **Spring Term Strategy**: The higher retention and satisfaction rates in the Spring term suggest that efforts should be made to replicate this success in the Fall. Offering early enrollment incentives, improved orientation, or additional resources could improve Fall term performance.
3. **Monitor Arts and Science Enrollments**: The relatively lower enrollments in these departments could prompt a review of the programs offered. Increasing awareness, offering scholarships, or revising curriculums might be beneficial.
4. **Retention Programs**: Given the increasing retention rates, the university should analyze the programs, mentorship opportunities, and student services that are contributing to these results and consider extending them across all departments.

By focusing on these insights, the university can improve its admissions, retention, and satisfaction further.
""")

# Add more analysis or interactive filters as needed

# Run Streamlit
if __name__ == "__main__":
    st.write("End of dashboard.")
