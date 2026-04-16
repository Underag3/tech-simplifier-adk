# Tech Jargon Simplifier

An intelligent multi-agent system built with the **Google Agent Development Kit (ADK)** and powered by **Gemini 2.5 Flash**. 

This project acts as a "Senior Technical Consultant". It automatically routes tasks, searches for complex IT terms on Wikipedia in real-time, and synthesizes the technical data into concise, high-level executive summaries suitable for business stakeholders.

## Technologies Used
* Google Agent Development Kit (ADK) v1.14.0
* Gemini 2.5 Flash (You can change it to gemini 3.1 flash preview for newer model)
* Langchain Wikipedia Tool
* Google Cloud Run (Serverless Deployment)

## How to Run
1. Rename `.env.example` to `.env` and fill in your GCP details.
2. Install dependencies: `uv pip install -r requirements.txt`
3. Run or deploy using ADK CLI.
