import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import SearchFlightsTool, SearchTrainsTool

# 1. Setup Brain (Using Gemini 2.5 Flash for 2026)
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5,
    verbose=True
)

# 2. Define Agent
atlas = Agent(
    role='Travel Logistics Manager',
    goal='Plan optimal trips comparing Flights and Trains',
    backstory="You are ATLAS. You expertly combine flight data and train data.",
    tools=[SearchFlightsTool(), SearchTrainsTool()],
    llm=gemini_llm,
    verbose=True,
    memory=True
)

# 3. Define Mission
# FIX: Updated date to 17 Feb 2026 (YYYY-MM-DD format)
task = Task(
    description=(
        "Plan a trip from Delhi to Mumbai for 2026-02-17. "
        "1. Check flights from DEL to BOM. "
        "2. Check trains from NDLS to MMCT. "
        "Compare them and recommend one."
    ),
    expected_output='A comparison table and final recommendation.',
    agent=atlas
)

# 4. Launch
crew = Crew(
    agents=[atlas],
    tasks=[task],
    process=Process.sequential
)

if __name__ == "__main__":
    print("### ATLAS (Google Edition) STARTING... ###")
    result = crew.kickoff()
    print("\n\n########################")
    print(result)
