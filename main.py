import streamlit as st
import pandas as pd
from agent import create_agent, AgentState
from io import BytesIO

# ------------------- Utility Functions -------------------

def validate_data(df):
    """Check dataset for missing values, mixed types, and outliers."""
    report = []
    issues_found = False

    # Missing values
    missing = df.isnull().sum()
    if missing.any():
        issues_found = True
        report.append(f"Missing values detected: {missing[missing > 0].to_dict()}")

    # Mixed types in numeric-like columns
    for col in df.columns:
        if df[col].dtype == 'object' and col.lower() not in ['customer', 'region', 'product', 'category']:
            issues_found = True
            report.append(f"Column '{col}' has non-numeric data that may affect calculations.")

    # Detect outliers (IQR method)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    outlier_cols = []
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
        if not outliers.empty:
            outlier_cols.append(col)
    if outlier_cols:
        issues_found = True
        report.append(f"Outliers detected in: {', '.join(outlier_cols)}")

    return issues_found, report


def auto_correct_data(df):
    """Automatically clean the dataset for better accuracy."""
    df = df.drop_duplicates()  # Remove duplicates

    # Convert numeric-like columns
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass

    # Fill missing values with median
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Remove outliers (IQR)
    for col in numeric_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    return df

# ------------------- Streamlit App -------------------

st.set_page_config(page_title="AI Data Analyst (LangGraph)", layout="wide")

# Custom CSS for modern look
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff4b2b, #ff416c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .tagline {
        font-size: 18px;
        text-align: center;
        color: #dddddd;
        margin-bottom: 30px;
    }
    .feature-box {
        background: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        margin: 0 auto;
        width: 60%;
        margin-bottom: 20px;
    }
    .feature-box h3 {
        color: #ff4b2b;
        margin-bottom: 10px;
        text-align: center;
    }
    .feature-box ul {
        color: #cccccc;
        font-size: 16px;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Session State -------------------
if "df" not in st.session_state:
    st.session_state.df = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "visualization_history" not in st.session_state:
    st.session_state.visualization_history = []
if "summary_history" not in st.session_state:
    st.session_state.summary_history = []

agent = create_agent()

# ------------------- Landing Page -------------------
if st.session_state.df is None:
    st.markdown('<div class="main-title">🧠 AI Data Analyst</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Turn your raw data into actionable insights within seconds ⚡</div>', unsafe_allow_html=True)

    # Intro section
    st.markdown("""
    <div class="feature-box">
        <h3>What is this?</h3>
        <p>An AI-powered data analyst that converts your CSV files into instant insights, stunning visualizations, and concise summaries.</p>
    </div>

    <div class="feature-box">
        <h3>Why use it?</h3>
        <ul>
            <li>✅ Ask questions in plain English, get expert-level answers</li>
            <li>✅ Create interactive visualizations in one click</li>
            <li>✅ Extract patterns and actionable insights effortlessly</li>
            <li>✅ No coding skills required — just upload your data</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("### 📂 Upload your CSV file to get started")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file.getvalue()
else:
    # Back button
    if st.button("⬅ Back to Upload"):
        st.session_state.df = None
        st.session_state.uploaded_file = None
        st.session_state.analysis_history.clear()
        st.session_state.visualization_history.clear()
        st.session_state.summary_history.clear()
        st.rerun()

# ------------------- Main Logic -------------------
if st.session_state.uploaded_file:
    st.session_state.df = pd.read_csv(BytesIO(st.session_state.uploaded_file))
    df = st.session_state.df

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Validate data
    issues_found, report = validate_data(df)
    if issues_found:
        st.warning("⚠ Data Issues Detected:")
        for issue in report:
            st.write(f"- {issue}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Auto-Correct Data"):
                df = auto_correct_data(df)
                st.success("✅ Data cleaned successfully! Analysis will be more accurate now.")
                st.session_state.df = df
        with col2:
            if st.button("❌ Keep Original Data"):
                st.info("Using original dataset without corrections.")
                st.session_state.df = df
    else:
        st.success("✅ No major issues found in your data.")

    # ------------------- Tabs -------------------
    if st.session_state.df is not None:
        st.write("---")
        tab1, tab2, tab3 = st.tabs(["🔍 Analysis", "📊 Visualization", "📑 Summary"])

        # -------------------- ANALYSIS TAB --------------------
        with tab1:
            st.subheader("Ask analysis questions")
            for q, ans, code in st.session_state.analysis_history:
                with st.chat_message("user"):
                    st.write(q)
                with st.chat_message("assistant"):
                    if ans is not None:
                        if isinstance(ans, pd.DataFrame):
                            st.dataframe(ans)
                        elif isinstance(ans, pd.Series):
                            st.dataframe(ans.reset_index().rename(columns={ans.name or "": "Value"}))
                        else:
                            st.markdown(f"**Result:** {ans}")
                    if code:
                        st.code(code, language="python")

            user_query = st.chat_input("Ask an analysis question...")
            if user_query:
                try:
                    df_csv = st.session_state.df.to_csv(index=False)
                    state = AgentState(user_query=user_query, intent="analysis", df=df_csv)
                    result_state = agent.invoke(state, config={"configurable": {"thread_id": "session-1"}})

                    answer = result_state.get("raw_result", result_state.get("result", "No result returned"))
                    code = result_state.get("generated_code", None)
                    st.session_state.analysis_history.append((user_query, answer, code))
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

        # -------------------- VISUALIZATION TAB --------------------
        with tab2:
            st.subheader("Ask visualization questions")
            for q, fig, code in st.session_state.visualization_history:
                with st.chat_message("user"):
                    st.write(q)
                with st.chat_message("assistant"):
                    if fig is not None:
                        st.plotly_chart(fig, use_container_width=True)
                    if code:
                        st.code(code, language="python")

            viz_query = st.chat_input("Ask for a visualization...")
            if viz_query:
                try:
                    df_csv = st.session_state.df.to_csv(index=False)
                    state = AgentState(user_query=viz_query, intent="visualization", df=df_csv)
                    result_state = agent.invoke(state, config={"configurable": {"thread_id": "session-1"}})

                    fig = result_state.get("result", None)
                    code = result_state.get("generated_code", None)
                    st.session_state.visualization_history.append((viz_query, fig, code))
                    st.rerun()
                except Exception as e:
                    st.error(f"Visualization failed: {e}")

        # -------------------- SUMMARY TAB --------------------
        with tab3:
            st.subheader("Ask summarization questions")
            for i, (q, ans) in enumerate(st.session_state.summary_history):
                with st.chat_message("user"):
                    st.write(q)
                with st.chat_message("assistant"):
                    st.write(ans)
                    text_bytes = ans.encode('utf-8')
                    st.download_button(
                        "⬇ Download Summary",
                        text_bytes,
                        file_name=f"summary_{i+1}.txt",
                        key=f"download_summary_{i}"
                    )

            summary_query = st.chat_input("Ask about summary or insights...")
            if summary_query:
                try:
                    df_csv = st.session_state.df.to_csv(index=False)
                    state = AgentState(user_query=summary_query, intent="summary", df=df_csv)
                    result_state = agent.invoke(state, config={"configurable": {"thread_id": "session-1"}})

                    answer = result_state.get("result", "No summary returned")
                    st.session_state.summary_history.append((summary_query, answer))
                    st.rerun()
                except Exception as e:
                    st.error(f"Summary failed: {e}")
