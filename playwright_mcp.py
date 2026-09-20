import asyncio
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI

# Load keys
load_dotenv()

# Initialize FastMCP Server
mcp = FastMCP("Local Browser Agent Server")

@mcp.tool()
async def run_browser_task(instructions: str) -> str:
    """
    Executes a web automation task in a real-time local browser window 
    using natural language instructions.
    
    Args:
        instructions: The specific task description (e.g., 'Go to Reddit and find Python topics')
    """
    # 1. Initialize the LLM driver
    llm = ChatOpenAI(model="gpt-4o", timeout=60.0)
    
    # 2. Boot the visible local browser instance
    browser = Browser(headless=False)
    
    # 3. Instantiate the agent lifecycle
    agent = Agent(
        task=instructions,
        llm=llm,
        browser=browser
    )
    
    try:
        # Run the agent steps
        history = await agent.run()
        
        # Format a structural summary return for the MCP client
        result = history.final_result()
        if result:
            return f"Success: {result}"
        elif history.extracted_content():
            return f"Completed with logs: {history.extracted_content()[-1]}"
        else:
            return "Task finished but no descriptive result was returned by the model."
            
    except Exception as e:
        return f"Automation failed due to an error: {str(e)}"
        
    finally:
        # Ensure the browser process exits cleanly even if an extraction crash happens
        await browser.close()

if __name__ == "__main__":
    # Start the server using standard input/output transport streams
    mcp.run(transport="stdio")
