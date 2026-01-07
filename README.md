# ATLAS_TRAVEL_AGENT
# ATLAS: AI Travel Logistics Agent System

**Student Name:** Tushar Dhingra
**Date:** 7 January 2026

## Project Overview
**ATLAS** is an autonomous AI travel consultant built using **CrewAI**. It acts as a smart logistics manager that can plan multi-modal travel itineraries by connecting to real-world APIs. 

Unlike standard travel search engines, ATLAS intelligently searches for **Flights** (via Amadeus) and **Trains** (via RapidAPI/IRCTC) simultaneously, compares them based on price, duration, and convenience, and generates a final recommendation for the user.

## Key Features
* **Multi-Modal Search:** seamless integration of Flight and Train data in one query.
* **AI-Powered Decisions:** Uses **Google Gemini 2.5 Flash** to analyze data and make logical recommendations.
* **Live Data Connectivity:**
    * **Flights:** Professional-grade data via the **Amadeus API**.
    * **Trains:** Real-time Indian Railway schedules via **RapidAPI**.
* **Autonomous Agent:** Built on the **CrewAI** framework to handle tool delegation and task execution autonomously.

---

## Tech Stack
* **Language:** Python 3.12
* **AI Framework:** CrewAI & LangChain
* **LLM (Brain):** Google Gemini (gemini-2.5-flash)
* **APIs:**
    * Amadeus for Developers (Flights)
    * RapidAPI (Trainman/IRCTC)
* **Environment Management:** `python-dotenv` for secure key management.

---

## Project Structure

```text
atlas_travel_agent/
├── main.py            # The Agent's Brain: Configures the Crew, LLM, and Tasks
├── tools.py           # The Tool Belt: Connects to Amadeus and RapidAPI
├── .env               # Security: Stores API Keys (Not uploaded to GitHub)
├── requirements.txt   # Dependencies: List of libraries needed to run the app
└── README.md          # Documentation
