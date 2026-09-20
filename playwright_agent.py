import asyncio
import os
import logging
from dotenv import load_dotenv
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# 1. TURN ON LOGGING: This forces the agent to print what the LLM is thinking 
# and what browser actions it is choosing in real-time in the terminal.
logging.basicConfig(level=logging.INFO)

async def main():
    llm = ChatOpenAI(model="gpt-4o")
    browser = Browser(headless=False)

    task = (
        "Go to reddit.com, search for 'Python programming', "
        "and find the title of the top trending post today."
    )
    
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser
    )

    # Run the agent
    history = await agent.run()
    
    print("\n==========================================")
    print("      🔍 INSPECTING LLM PROVIDE DATA      ")
    print("==========================================\n")
    
    # 2. GET THE FINAL CONTEXT: This is the definitive final text the LLM produced
    final_result = history.final_result()
    print(f"🎯 1. Final Answer Provided by LLM:\n{final_result}\n")
    
    # 3. GET STEP-BY-STEP LLM ACTIONS: See every single tool the LLM decided to use
    print("🛠️ 2. Steps and Tool Calls the LLM decided to execute:")
    for i, action in enumerate(history.model_actions(), 1):
        print(f"  Step {i}: {action}")
        
    # 4. GET EXTRACTED PAGE TEXT: See what raw page text the LLM read from the site
    print("\n📄 3. Content Extracted by the LLM during the last step:")
    extracted = history.extracted_content()
    if extracted:
        print(extracted[-1]) # Prints the text from the final browser state
    else:
        print("No text was explicitly extracted into the history array.")

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
