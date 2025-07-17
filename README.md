# 🧠 AI Data Analyst Agent (Streamlit + LangGraph)

![Home](assets/home.png)

## 🚀 Overview
**AI Data Analyst Agent** is an intelligent web app that transforms your CSV data into actionable insights using **Streamlit**, **LangGraph**, and **LLMs**.  
It can:
- Validate and clean datasets automatically.
- Answer natural language queries for analysis.
- Create interactive visualizations.
- Generate summaries and insights.

Unlike static dashboards, this is a **real AI Agent** powered by **hybrid LLM models** for reasoning and visualization.

---

## ✨ Features
✅ **Upload & Auto-Validate Data**
- Detects missing values, outliers, and mixed data types.
- Option to auto-correct data for accuracy.

✅ **Analysis Tab**
- Ask plain English queries like:  
  *"Find the top 5 customers by Revenue"*
- Returns:
  - ✅ Accurate table results.
  - ✅ Python code used for the calculation (transparency).

✅ **Visualization Tab**
- Generate **interactive charts** (bar, pie, line) from natural queries.

✅ **Summary Tab**
- Summarize trends and generate key insights.
- Download summaries as `.txt`.

✅ **Session History**
- Keeps previous questions and answers in all tabs.

✅ **Modern UI**
- Clean, responsive layout with custom CSS.

---

## 🧠 Agent Architecture

### **Hybrid Model Strategy**
- **Mistral** → For Analysis & Summarization (reasoning-focused).
- **LLaMA 3** → For Visualization (creative and structured output).

The agent dynamically:
- Interprets queries.
- Generates Python code.
- Executes code on the dataset.
- Returns **results + the code snippet** for transparency.

---

## 🖼 Screenshots

### Home
![Home](assets/home1.png)

### Data Upload & Auto-Correction
![Data Preview](assets/Data%20Preview.png)
![Auto Preprocessing](assets/auto%20data%20preprocessing%20if%20needed.png)

### Analysis
![Analysis](assets/AnalysisQuestionSample.png)
![Analysis](assets/AnalysisQuestionSample1.png)

### Visualization
![Visualization](assets/visualizationsample.png)
![Visualization](assets/visualizationsample1.png)

### Summary
![Summary](assets/summarizationsample.png)
![Summary](assets/summarizationsample1.png)

---

## 🛠 Tech Stack
- **Frontend:** Streamlit
- **Agent Framework:** LangGraph
- **Models:**  
  - Mistral → Analysis & Summary  
  - LLaMA 3 → Visualization  
- **Data Handling:** Pandas
- **Visualization:** Plotly
- **Language:** Python

---

## ⚠ Disclaimer
This public repository contains the **Streamlit app (`main.py`)** and assets for demo purposes.  
The **full working LangGraph agent code** (including nodes, execution logic, etc.) will be provided **on request** for educational or professional use.

📩 Contact: **syedsaadi427@gmail.com**

---

