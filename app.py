from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file
import streamlit as st
import sqlite3
import pandas as pd

import google.genai as genai

#function to load gemini model and provide sql queries as response
def get_gemini_response(prompt, question):
    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=[prompt, question]
    )
    return response.text

#define prompt
# define prompt as STRING (not list)
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, ROLL

For context:
- CLASS values include: 7th, 8th, 9th, 10th, 11th, 12th
- SECTION values include: A, B, C, D, E
- ROLL is a unique integer identifier

Example 1 - How many entries of records are present?
SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in 10th class?
SELECT * FROM STUDENT WHERE CLASS="10th";

Example 3 - Show me students in section A
SELECT * FROM STUDENT WHERE SECTION="A";

Example 4 - How many students are in 12th class?
SELECT COUNT(*) FROM STUDENT WHERE CLASS="12th";

Example 5 - List all students with their names and classes
SELECT NAME, CLASS FROM STUDENT;

Example 6 - Find students from 7th to 9th grade
SELECT * FROM STUDENT WHERE CLASS IN ("7th", "8th", "9th");

Example 7 - Show me the names and rolls of students in section B
SELECT NAME, ROLL FROM STUDENT WHERE SECTION="B";

Example 8 - How many students are in each class?
SELECT CLASS, COUNT(*) FROM STUDENT GROUP BY CLASS;

Example 9 - List all sections available
SELECT DISTINCT SECTION FROM STUDENT;

Example 10 - Find students with roll numbers between 10 and 20
SELECT * FROM STUDENT WHERE ROLL BETWEEN 10 AND 20;

Important rules:
- Always use the table name "STUDENT" (all caps)
- Use double quotes for string values in WHERE clauses
- For aggregate queries, use appropriate GROUP BY
- For counting, use COUNT(*)
- For listing unique values, use DISTINCT
- Do not include ``` or the word SQL in output
- Output only the SQL query, nothing else
"""

##function to retrive query results from the database
def red_sql_query(sql,db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql)
    data = c.fetchall()
    conn.commit()
    conn.close()
    for row in data:
        print(row)
    return data

# Streamlit app
st.set_page_config(page_title="Text to SQL with Gemini", page_icon="🤖", layout="wide")

# Theme selector
theme = st.sidebar.selectbox("Choose Theme", ["Purple Gradient", "Blue Ocean", "Dark Mode", "Light Mode"])
themes = {
    "Purple Gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "Blue Ocean": "linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)",
    "Dark Mode": "#1e1e1e",
    "Light Mode": "#ffffff"
}

bg_color = themes[theme]

# Custom CSS for cool background
st.markdown(f"""
<style>
    .stApp {{
        background: {bg_color};
        color: {'white' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else 'black'};
    }}
    .stTextInput {{
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        border: 2px solid #ff6b6b;
        padding: 10px;
        backdrop-filter: blur(10px);
    }}
    .stTextInput input {{
        color: {'white' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else 'black'} !important;
        font-size: 16px;
        font-weight: 500;
        background: transparent !important;
        border: none !important;
        outline: none !important;
    }}
    .stTextInput input::placeholder {{
        color: {'rgba(255,255,255,0.7)' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else 'rgba(0,0,0,0.5)'} !important;
        font-style: italic;
    }}
    .stTextInput label {{
        color: {'#ffffff' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else '#000000'} !important;
        font-weight: bold;
        font-size: 18px;
    }}
    .stButton, .stSelectbox {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: {'white' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else 'black'};
    }}
    .stButton button {{
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        background-color: #ff5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }}
    .stSelectbox select {{
        color: {'white' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else 'black'};
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}
    h1, h2, h3 {{
        color: {'#ffffff' if theme in ['Purple Gradient', 'Blue Ocean', 'Dark Mode'] else '#000000'};
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    .stDataFrame {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }}
    .stTable {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}
    .stSuccess {{
        background-color: rgba(76, 175, 80, 0.2);
        border: 1px solid #4caf50;
        border-radius: 10px;
    }}
    .stError {{
        background-color: rgba(244, 67, 54, 0.2);
        border: 1px solid #f44336;
        border-radius: 10px;
    }}
    .stInfo {{
        background-color: rgba(33, 150, 243, 0.2);
        border: 1px solid #2196f3;
        border-radius: 10px;
    }}
    .stCode {{
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📋 Database Info")
st.sidebar.markdown("**Table: STUDENT**")
st.sidebar.markdown("- NAME (VARCHAR) - Student names")
st.sidebar.markdown("- CLASS (VARCHAR) - 7th to 12th grade")
st.sidebar.markdown("- SECTION (VARCHAR) - A to E")
st.sidebar.markdown("- ROLL (INTEGER) - Unique ID")

# Quick stats
conn = sqlite3.connect("student.db")
total_students = pd.read_sql_query("SELECT COUNT(*) as total FROM STUDENT", conn).iloc[0]['total']
classes_count = pd.read_sql_query("SELECT COUNT(DISTINCT CLASS) as classes FROM STUDENT", conn).iloc[0]['classes']
sections_count = pd.read_sql_query("SELECT COUNT(DISTINCT SECTION) as sections FROM STUDENT", conn).iloc[0]['sections']
conn.close()

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Quick Stats:**")
st.sidebar.markdown(f"• Total Students: **{total_students}**")
st.sidebar.markdown(f"• Classes: **{classes_count}**")
st.sidebar.markdown(f"• Sections: **{sections_count}**")

if st.sidebar.button("👀 View Full Table", type="primary", use_container_width=True):
    conn = sqlite3.connect("student.db")
    df_full = pd.read_sql_query("SELECT * FROM STUDENT ORDER BY ROLL", conn)
    conn.close()
    st.sidebar.markdown("### 📋 Complete Student Table (100 Students)")
    st.sidebar.dataframe(df_full, width='stretch', height=400)
    
    # Add download button for full table
    csv_full = df_full.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download Full Table",
        data=csv_full,
        file_name="full_student_table.csv",
        mime="text/csv",
        width='stretch'
    )

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.sidebar.success("History cleared!")

st.title("🤖 Text to SQL with Gemini")
st.markdown("Convert natural language questions to SQL queries and execute them on the STUDENT database!")

# Database preview - Always visible
st.subheader("📊 Database Preview (Sample of 10 Students)")
conn = sqlite3.connect("student.db")
df_preview = pd.read_sql_query("SELECT * FROM STUDENT ORDER BY ROLL LIMIT 10", conn)
conn.close()
st.dataframe(df_preview, width='stretch', height=300)
st.markdown("*💡 This shows a sample. Use sidebar to view the complete table.*")

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Example questions
example_questions = [
    "Select an example question...",
    # Basic counting
    "How many entries of records are present?",
    "What's the total number of students?",
    "Count all the records in the database",
    "How many rows are there in the student table?",
    
    # Simple filtering by class
    "Tell me all the students studying in 10th class?",
    "Show me everyone in 10th grade",
    "List students from 10th class",
    "Who are the 10th graders?",
    "Display all 10th class students",
    
    # Filtering by section
    "Show me students in section A",
    "List all students from section A",
    "Who is in section A?",
    "Display section A students",
    "Find students in section A",
    
    # Counting with conditions
    "How many students are in 12th class?",
    "Count the number of 12th graders",
    "What's the total count of 12th class students?",
    "How many people are in 12th grade?",
    
    # Column selection
    "List all students with their names and classes",
    "Show me names and classes of all students",
    "Display student names and their classes",
    "What are the names and classes of students?",
    
    # Multiple conditions
    "Find students from 7th to 9th grade",
    "Show me students in grades 7th, 8th, or 9th",
    "List students from 7th, 8th, and 9th classes",
    "Who are the students in lower grades (7th-9th)?",
    
    # Specific column selection with conditions
    "Show me the names and rolls of students in section B",
    "List names and roll numbers for section B students",
    "What are the names and rolls of students in section B?",
    "Display student names and their roll numbers from section B",
    
    # Aggregation - GROUP BY
    "How many students are in each class?",
    "Count students per class",
    "Show me the number of students in each grade",
    "What's the distribution of students across classes?",
    "Group students by class and count them",
    
    # DISTINCT operations
    "List all sections available",
    "What are the different sections?",
    "Show me all unique sections",
    "What sections exist in the school?",
    "Display distinct section values",
    
    # Range queries
    "Find students with roll numbers between 10 and 20",
    "Show students whose roll is from 10 to 20",
    "List students with rolls between 10 and 20",
    "Who has roll numbers ranging from 10 to 20?",
    
    # More complex queries
    "How many students are there in section C of 11th class?",
    "Count 11th graders in section C",
    "Show me all 9th class students in section A",
    "List students from 8th grade section B",
    
    # Different phrasings
    "Give me the total student count",
    "What's the size of our student database?",
    "How big is the student table?",
    "Total number of records please",
    
    "Can you show me 10th class students?",
    "I want to see all 10th graders",
    "Please list 10th class students",
    "Show 10th grade students",
    
    "Students in section D please",
    "List everyone from section D",
    "Who are the section D students?",
    "Show me section D members",
    
    "Count of 7th graders?",
    "How many 7th class students?",
    "Number of students in 7th grade",
    "Total 7th graders",
    
    "Names and classes only",
    "Just show names and classes",
    "Display student names with their classes",
    "List names along with classes",
    
    "Students from middle grades (7th-9th)",
    "List junior grade students",
    "Show students in lower classes",
    "Display 7th through 9th graders",
    
    "Names and rolls for section E",
    "Show me names and roll numbers of section E students",
    "List the names and rolls from section E",
    "What are the names and rolls in section E?",
    
    "Student count by grade",
    "Number of students per class level",
    "How many students in each grade level?",
    "Count students grouped by class",
    
    "What sections do we have?",
    "List all available sections",
    "Show me the sections",
    "What are the section options?",
    
    "Students with rolls 5 to 15",
    "Show rolls from 5 to 15",
    "List students whose roll numbers are between 5 and 15",
    "Find students in roll range 5-15"
]

col1, col2 = st.columns([3, 1])

with col1:
    question = st.text_input("Enter your question:", key="input", placeholder="e.g., How many students are in 10th class?")

with col2:
    selected_example = st.selectbox("Or choose an example:", example_questions)
    if selected_example != "Select an example question...":
        question = selected_example

submit_button = st.button("🚀 Submit", width='stretch')

# Chat History
if st.session_state.history:
    with st.expander("📜 Query History"):
        for i, entry in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**Q{i+1}:** {entry['question']}")
            st.code(entry['sql'], language="sql")
            if entry['results']:
                st.dataframe(entry['results'], width='stretch')
            st.markdown("---")

# if submit is clicked
if submit_button and question:
    with st.spinner("🤖 Generating SQL query..."):
        response = get_gemini_response(prompt, question)
    
    st.success("✅ SQL Query Generated Successfully!")
    st.markdown("### 🔍 Generated SQL Query:")
    st.code(response, language="sql")
    
    with st.spinner("⚡ Executing query on database..."):
        try:
            data = red_sql_query(response, "student.db")
            df = pd.DataFrame(data) if data else None
            
            # Add to history
            st.session_state.history.append({
                'question': question,
                'sql': response,
                'results': df
            })
            
            if data:
                st.markdown("### 📊 Query Results:")
                st.dataframe(df, width='stretch')
                
                # Show result count
                st.info(f"📈 Found {len(data)} result(s)")
                
                # Export to CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="query_results.csv",
                    mime="text/csv",
                    width='stretch',
                    type="primary"
                )
            else:
                st.info("🔍 No data found for this query.")
        except Exception as e:
            st.error(f"❌ Error executing query: {str(e)}. Please check the generated SQL.")
            # Add failed query to history
            st.session_state.history.append({
                'question': question,
                'sql': response,
                'results': None
            })
elif submit_button and not question:
    st.warning("⚠️ Please enter a question or select an example.")
