import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

# Your existing imports
from utils.pdf_reader import read_pdf
from utils.rag import create_vectorstore
from utils.ai_helper import ask_ai
from utils.validator import is_medical_document
from utils.report_classifier import detect_report_type

# ====================== SESSION STATE ======================
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "processed_text" not in st.session_state:
    st.session_state.processed_text = None

if "processed_df" not in st.session_state:      # ← New for Excel
    st.session_state.processed_df = None

if "file_type" not in st.session_state:         # ← New
    st.session_state.file_type = None

st.set_page_config(page_title="MediGuide AI", page_icon="🏥", layout="wide")

# ====================== WELCOME PAGE ======================
if st.session_state.page == "welcome":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>🏥 MediGuide AI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Professional AI Medical Document Assistant</p>", unsafe_allow_html=True)
        if st.button("🚀 ENTER MEDIGUIDE AI", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

# ====================== DASHBOARD ======================
else:
    with st.sidebar:
        st.markdown("### 🏥 MediGuide AI")
        st.caption("AI Medical Document Assistant")
        menu = st.radio("Navigation", 
                       ["🏠 Home", "📄 Summary Report", "📊 Report Analysis", "💬 AI Chat", "⚙ Settings"],
                       label_visibility="collapsed")

    st.title("🏥 MediGuide AI")
    st.caption("Professional AI Medical Document Assistant")

    # ==================== HOME PAGE ====================
    if menu == "🏠 Home":
        st.subheader("Upload Medical Document")
        uploaded_file = st.file_uploader(
            "Drag and drop your report (PDF or Excel)", 
            type=["pdf", "xlsx", "xls"]
        )

        if uploaded_file:
            with st.spinner("Processing file..."):
                file_type = uploaded_file.name.split('.')[-1].lower()
                st.session_state.file_type = file_type

                if file_type == "pdf":
                    text = read_pdf(uploaded_file)
                    is_medical, _ = is_medical_document(text)
                    df = None
                else:  # Excel
                    df = pd.read_excel(uploaded_file)
                    text = df.to_string()   # Convert to text for RAG
                    is_medical = True  # You can add better validation later

                if is_medical:
                    st.session_state.processed_text = text
                    st.session_state.processed_df = df
                    st.session_state.vectorstore = create_vectorstore(text)
                    st.session_state.report_type = detect_report_type(text)
                    
                    st.success(f"✅ {file_type.upper()} Report processed successfully!")
                    st.info(f"Report Type: **{st.session_state.report_type}**")
                else:
                    st.error("Not a valid medical document.")

    # ==================== SUMMARY REPORT ====================
    elif menu == "📄 Summary Report":
        # (Same as before - I kept it unchanged for now)
        st.subheader("📄 Patient Summary Report")
        if st.session_state.processed_text:
            text_preview = st.session_state.processed_text[:2000]
            summary_text = f"""MEDIGUIDE AI - PATIENT SUMMARY REPORT
Generated on: {datetime.now().strftime('%d %B %Y at %H:%M')}

File Type: {st.session_state.file_type.upper() if st.session_state.file_type else 'PDF'}
Report Type: {st.session_state.report_type or 'Medical Report'}

KEY FINDINGS:
• Document successfully analyzed
• AI-powered insights generated

PREVIEW:
{text_preview[:1000]}...
"""
            st.text_area("Summary", summary_text, height=400)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button("⬇ Download Summary PDF", data=summary_text, 
                                 file_name="Medical_Summary_Report.pdf", mime="application/pdf")
            with col2:
                st.download_button("⬇ Download TXT", data=summary_text, 
                                 file_name="Medical_Summary_Report.txt", mime="text/plain")
            with col3:
                st.download_button("⬇ Download Raw Data", 
                                 data=st.session_state.processed_text, 
                                 file_name=f"Full_Report.{st.session_state.file_type or 'txt'}", 
                                 mime="text/plain")
        else:
            st.warning("Please upload a report first.")

    # ==================== REPORT ANALYSIS ====================
    elif menu == "📊 Report Analysis":
        st.subheader("📊 Medical Data Visualization")
        
        if st.session_state.processed_df is not None:          # Excel data available
            df = st.session_state.processed_df
            st.dataframe(df, use_container_width=True)
            
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Line Chart"])
                
                fig, ax = plt.subplots(figsize=(10, 6))
                if chart_type == "Bar Chart":
                    df.plot(kind='bar', x=df.columns[0], y=numeric_cols[0], ax=ax)
                elif chart_type == "Pie Chart":
                    df[numeric_cols[0]].plot(kind='pie', ax=ax, autopct='%1.1f%%')
                else:
                    df.plot(kind='line', ax=ax)
                
                st.pyplot(fig)
                
                # Download Chart
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
                buf.seek(0)
                st.download_button("⬇ Download Chart PNG", buf, "Medical_Chart.png", mime="image/png")
            else:
                st.info("No numeric columns found for visualization.")
                
        elif st.session_state.processed_text:
            st.info("Using sample data (PDF mode)")
            # Keep your previous sample chart logic here...
        else:
            st.warning("Please upload a report first.")

    # ==================== AI CHAT (unchanged) ====================
    elif menu == "💬 AI Chat":
        # ... your existing chat code ...
        st.subheader("💬 AI Medical Assistant")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask anything about your report..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                if st.session_state.vectorstore:
                    response = ask_ai(st.session_state.vectorstore, prompt)
                else:
                    response = "Please upload a report first."
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    else:
        st.subheader("⚙ Settings")
        st.write("Settings page")

    st.caption("MediGuide AI v2.1")