# Vantage AI (Agentic Career Intelligence)

An advanced, multi-agent AI application designed to revolutionize the job discovery process. By simply uploading a resume, this system autonomously analyzes the user's skillset, searches the live web for the best-matching job opportunities in India, and provides a premium analytics dashboard with role breakdowns and skill gaps.

## Key Features

- **Automated Resume Parsing**: Uses GenAI to extract core technical skills and generate optimized search queries.
- **Agentic Web Search**: Leverages a multi-agent workflow to search live job boards (Naukri, Internshala, LinkedIn, etc.) using Tavily.
- **Deep ATS Analysis**: Compares your resume against real-world job requirements using specialized career architect agents.
- **Premium Dashboard**: Visualizes match percentages, skill gaps, and recommended certifications.
- **Strict Location Filtering**: Intelligent filtering focused specifically on the Indian job market.

## Technology Stack

- **Category**: Agentic AI
- **LLM**: Llama 3.3 70B (via Groq)
- **Framework**: LangGraph (for multi-agent orchestration)
- **Search Engine**: Tavily AI (Advanced Search Depth)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **PDF Processing**: PyPDF

## Project Structure

```text
├── agent/                  # Agentic AI Core
│   ├── job_graph.py        # LangGraph workflow definition
│   ├── job_nodes.py        # Independent AI agent nodes (Extraction, Search, Ranking)
│   ├── state.py            # Graph state management
│   └── state.py            # Graph state management
├── ui/                     # Frontend
│   └── app.py              # Streamlit Premium Dashboard
├── main.py                 # FastAPI Backend Entry Point
└── requirements.txt        # Project dependencies
```

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "GenAi Lab"
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

## Execution

The project requires running both the backend and the frontend simultaneously.

### 1. Start the Backend (FastAPI)
```bash
python main.py
```
*The API will be available at `http://127.0.0.1:8000`*

### 2. Start the Frontend (Streamlit)
```bash
streamlit run ui/app.py
```
*The dashboard will open in your browser.*

## How it Works (The Agentic Workflow)

1. **Resume Extraction Agent**: Parses the PDF and extracts key tech stacks.
2. **Search Agent**: Formulates diverse search queries and crawls top job boards in real-time.
3. **Filtering Agent**: Strictly filters results for Indian locations and excludes global noise.
4. **Ranking Agent**: Performs a final deep-match analysis and generates the analytics JSON.