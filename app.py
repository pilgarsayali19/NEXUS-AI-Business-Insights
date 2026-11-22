import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import hashlib

from pypdf import PdfReader
from google import genai
from io import BytesIO

# PAGE CONFIG
st.set_page_config(
    page_title="NEXUS AI | Business Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CHAT HISTORY INITIALIZATION
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "current_pdf_id" not in st.session_state:
    st.session_state["current_pdf_id"] = None

# PREMIUM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

.stApp {
    background: #F4EBDD;
    font-family: 'DM Sans', sans-serif;
    color: #3D2528;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #641E2B;
    border-right: 1px solid #8D4652;
}

[data-testid="stSidebar"] * {
    color: #FFF8EF !important;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 700;
    color: #641E2B;
    margin-bottom: 0px;
}

.subtitle {
    color: #8D6B66;
    font-size: 14px;
    margin-bottom: 25px;
}

.kpi-card {
    background: linear-gradient(135deg, #FFFCF6, #EADCCB);
    border: 1px solid #DDC8B6;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(100,30,43,0.07);
    transition: all 0.3s ease;
    min-height: 125px;
}

.kpi-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 25px rgba(100,30,43,0.15);
}

.kpi-label {
    color: #8D6B66;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: #641E2B;
    font-size: 27px;
    font-weight: 800;
    margin-top: 10px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    color: #641E2B;
    font-size: 23px;
    font-weight: 700;
}

.insight-card {
    background: #641E2B;
    color: #FFF8EF;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 12px;
    box-shadow: 0 5px 15px rgba(100,30,43,0.12);
}

div.stButton > button {
    background: #641E2B;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

div.stButton > button:hover {
    background: #8D4652;
    color: white;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #DDC8B6;
    border-radius: 12px;
}

hr {
    border-color: #DDC8B6;
}
</style>
""", unsafe_allow_html=True)

# LOAD DATABASE
@st.cache_data
def load_data():
    conn = sqlite3.connect("data/sales.db")
    data = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    data["Order_Date"] = pd.to_datetime(data["Order_Date"])
    return data

try:
    df = load_data()
except Exception as e:
    st.error(f"Database loading error: {e}")
    st.stop()

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 5px;'>
        <div style='font-size:38px;'>✦</div>
        <h2 style='font-family:Playfair Display;font-size:28px;'>
        NEXUS AI
        </h2>
        <p style='font-size:12px;letter-spacing:2px;'>
        BUSINESS INTELLIGENCE
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Sales Analytics",
            "Product Insights",
            "AI Insights",
            "Data Explorer",
            "Document Chat"
        ]
    )

    st.markdown("---")
    st.caption("✦ Powered by Python + SQL + Streamlit")

# HEADER
st.markdown(
    '<div class="main-title">Business Overview ✦</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Your business performance, beautifully simplified.</div>',
    unsafe_allow_html=True
)

# FILTERS
with st.expander("⚙️ Customize Dashboard Filters", expanded=False):
    regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
    categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

    c1, c2 = st.columns(2)
    selected_region = c1.selectbox("Select Region", regions)
    selected_category = c2.selectbox("Select Category", categories)

filtered = df.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

if filtered.empty:
    st.warning("No data found for selected filters.")
    st.stop()

# KPI CALCULATIONS
revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
quantity = filtered["Quantity"].sum()

# KPI CARDS
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TOTAL REVENUE</div>
        <div class="kpi-value">₹{revenue:,.0f}</div>
        <div style="color:#8D6B66;font-size:12px;">Sales performance</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TOTAL PROFIT</div>
        <div class="kpi-value">₹{profit:,.0f}</div>
        <div style="color:#8D6B66;font-size:12px;">Business earnings</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">TOTAL ORDERS</div>
        <div class="kpi-value">{orders:,}</div>
        <div style="color:#8D6B66;font-size:12px;">Orders processed</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">UNITS SOLD</div>
        <div class="kpi-value">{quantity:,}</div>
        <div style="color:#8D6B66;font-size:12px;">Products sold</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# CHART THEME
chart_layout = dict(
    paper_bgcolor="#FFFCF6",
    plot_bgcolor="#FFFCF6",
    font=dict(color="#641E2B", family="DM Sans"),
    margin=dict(l=25, r=25, t=45, b=25),
    hoverlabel=dict(bgcolor="#641E2B", font_color="white")
)

# OVERVIEW PAGE
if page == "Overview":
    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">Revenue by Category</div>',
            unsafe_allow_html=True
        )
        cat = filtered.groupby("Category", as_index=False)["Revenue"].sum()
        fig = px.pie(
            cat,
            names="Category",
            values="Revenue",
            hole=0.58,
            color_discrete_sequence=[
                "#641E2B", "#8D4652", "#B77A7D", "#D8B9A7"
            ]
        )
        fig.update_layout(**chart_layout)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown(
            '<div class="section-title">Regional Performance</div>',
            unsafe_allow_html=True
        )
        reg = filtered.groupby(
            "Region", as_index=False
        )["Revenue"].sum().sort_values("Revenue")
        fig = px.bar(
            reg,
            x="Revenue",
            y="Region",
            orientation="h",
            color="Revenue",
            color_continuous_scale=["#D8B9A7", "#641E2B"]
        )
        fig.update_layout(**chart_layout, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Monthly Revenue Trend</div>',
        unsafe_allow_html=True
    )
    monthly = filtered.copy()
    monthly["Month"] = monthly["Order_Date"].dt.to_period("M").astype(str)
    monthly = monthly.groupby("Month", as_index=False)["Revenue"].sum()

    fig = px.area(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        color_discrete_sequence=["#8D4652"]
    )
    fig.update_traces(
        fillcolor="rgba(141,70,82,0.15)",
        line=dict(width=3)
    )
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

# SALES ANALYTICS
elif page == "Sales Analytics":
    st.markdown(
        '<div class="section-title">Sales Analytics</div>',
        unsafe_allow_html=True
    )

    monthly = filtered.copy()
    monthly["Month"] = monthly["Order_Date"].dt.to_period("M").astype(str)
    monthly = monthly.groupby(
        "Month", as_index=False
    )[["Revenue", "Profit"]].sum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Revenue"],
        name="Revenue",
        mode="lines+markers",
        line=dict(color="#641E2B", width=4)
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Month"],
        y=monthly["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color="#B77A7D", width=3)
    ))
    fig.update_layout(**chart_layout, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Region-wise Profit</div>',
        unsafe_allow_html=True
    )
    region_profit = filtered.groupby(
        "Region", as_index=False
    )["Profit"].sum()
    fig = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color_discrete_sequence=["#641E2B"]
    )
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

# PRODUCT INSIGHTS
elif page == "Product Insights":
    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True
    )

    products = filtered.groupby(
        "Product", as_index=False
    )["Quantity"].sum()
    products = products.sort_values("Quantity", ascending=False)

    fig = px.bar(
        products,
        x="Product",
        y="Quantity",
        color="Quantity",
        color_continuous_scale=["#D8B9A7", "#641E2B"]
    )
    fig.update_layout(**chart_layout, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(products, use_container_width=True)

# AI INSIGHTS
elif page == "AI Insights":
    st.markdown(
        '<div class="section-title">Business Intelligence ✦</div>',
        unsafe_allow_html=True
    )

    top_region = filtered.groupby("Region")["Revenue"].sum().idxmax()
    top_product = filtered.groupby("Product")["Quantity"].sum().idxmax()
    top_category = filtered.groupby("Category")["Revenue"].sum().idxmax()
    margin = (profit / revenue * 100) if revenue else 0

    insights = [
        (
            "🏆 Top Performing Region",
            f"{top_region} is generating the highest revenue in the selected data."
        ),
        (
            "✦ Best Selling Product",
            f"{top_product} has the highest total quantity sold."
        ),
        (
            "📦 Leading Category",
            f"{top_category} is contributing the highest category revenue."
        ),
        (
            "📈 Profit Margin",
            f"Overall profit margin for the selected data is {margin:.2f}%."
        )
    ]

    for heading, description in insights:
        st.markdown(f"""
        <div class="insight-card">
            <h4>{heading}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "These are automatically generated rule-based insights from your sales data, "
        "not an external AI model."
    )

# DATA EXPLORER
elif page == "Data Explorer":
    st.markdown(
        '<div class="section-title">Explore Your Sales Data</div>',
        unsafe_allow_html=True
    )
    st.dataframe(filtered, use_container_width=True)

    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=csv,
        file_name="nexus_sales_report.csv",
        mime="text/csv"
    )

# DOCUMENT CHAT
elif page == "Document Chat":
    st.markdown(
        '<div class="section-title">AI Document Chat ✦</div>',
        unsafe_allow_html=True
    )

    st.write("Upload a business PDF and ask questions about its content.")

    uploaded_pdf = st.file_uploader(
        "Upload PDF Report",
        type=["pdf"]
    )

    if uploaded_pdf is not None:
        # Create a unique ID for the uploaded PDF.
        # If a different PDF is uploaded, clear the previous PDF's chat.
        pdf_id = hashlib.md5(uploaded_pdf.getvalue()).hexdigest()

        if st.session_state.current_pdf_id != pdf_id:
            st.session_state.chat_history = []
            st.session_state.current_pdf_id = pdf_id

        try:
            pdf_reader = PdfReader(BytesIO(uploaded_pdf.getvalue()))

            pdf_text = "\n".join(
                page.extract_text() or ""
                for page in pdf_reader.pages
            )

            if not pdf_text.strip():
                st.warning("PDF madhye selectable text sapadla nahi.")
            else:
                st.success(
                    f"PDF loaded successfully! Pages: {len(pdf_reader.pages)}"
                )

                with st.expander("Preview Extracted Text"):
                    st.text(pdf_text[:5000])

                question = st.text_input(
                    "Ask a question about this PDF"
                )

                # Clear History button on the right side
                col1, col2 = st.columns([4, 1])

                with col2:
                    if st.button("🗑️ Clear History"):
                        st.session_state.chat_history = []
                        st.rerun()

                # Display Previous Chat History
                for chat in st.session_state.chat_history:
                    st.markdown(f"**You:** {chat['question']}")
                    st.markdown(f"**NEXUS AI:** {chat['answer']}")
                    st.divider()

                if st.button("Ask NEXUS AI"):
                    if not question.strip():
                        st.warning("Please enter a question.")
                    else:
                        with st.spinner("NEXUS AI is thinking..."):
                            try:
                                client = genai.Client(
                                    api_key=st.secrets["GEMINI_API_KEY"]
                                )

                                response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=f"""
                                    Answer using only the PDF content below.
                                    If the answer is not available,
                                    say so.

                                    Respond in the same language as the user's question.

                                    PDF CONTENT:
                                    {pdf_text[:30000]}

                                    QUESTION:
                                    {question}
                                    """
                                )

                                answer = response.text or "NEXUS AI could not generate an answer."

                                st.markdown("### NEXUS AI Answer")
                                st.write(answer)

                                st.session_state.chat_history.append({
                                    "question": question,
                                    "answer": answer
                                })

                            except Exception as e:
                                st.error(f"Gemini Error: {e}")

        except Exception as e:
            st.error(f"PDF processing error: {e}")

# FOOTER
st.markdown("---")
st.markdown(
    "<center style='color:#8D6B66;font-size:12px;'>"
    "✦ NEXUS AI · Business Intelligence Dashboard · 2026"
    "</center>",
    unsafe_allow_html=True
)
