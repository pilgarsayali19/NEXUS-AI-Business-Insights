# ✦ NEXUS AI – Business Insights Assistant

NEXUS AI is an interactive Business Intelligence and Analytics web application built using Python and Streamlit. It helps users explore business sales data, analyze performance, visualize insights, and ask questions about uploaded PDF reports using AI.

## 🚀 Features

- **Business Overview:** View key business performance metrics such as revenue, profit, and total orders.
- **Sales Analytics:** Explore sales performance using interactive charts and filters.
- **Product Insights:** Analyze product and category performance.
- **AI Insights:** Get useful business insights from sales data.
- **Data Explorer:** Explore and filter business datasets.
- **Document Chat:** Upload PDF reports and ask questions about their content using Gemini AI.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- Google Gemini API
- PyPDF

## 📊 Project Highlights

- Interactive business intelligence dashboard.
- Data visualization using Plotly.
- Sales data analysis and filtering.
- AI-powered PDF question-answering.
- SQLite database integration.

## ⚙️ Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/pilgarsayali19/NEXUS-AI-Business-Insights.git
   ```

2. Open the project folder:

   ```bash
   cd NEXUS-AI-Business-Insights
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Gemini API key in `.streamlit/secrets.toml`:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

## 🔐 API Configuration

The Document Chat feature uses the Google Gemini API. Add your API key through Streamlit secrets. Never upload your API key or `secrets.toml` file to GitHub.

## 👩‍💻 Developed With

**NEXUS AI – Business Insights Assistant**

Built as a hands-on project to explore Python, business analytics, data visualization, and AI integration.

