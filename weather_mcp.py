from fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP("My First MCP Server")
logger.info("Processing request")  # writes to stderr

@mcp.tool()
def hello_world(name: str) -> str:
    """A simple tool that greets the user."""
    return f"Hello, {name}! MCP is working perfectly."

# 2. Define a Tool
# FastMCP uses Python type hints and docstrings to auto-generate the tool definition for the AI!
@mcp.tool()
def fetch_weather(city: str) -> str:
    """
    Fetches the current weather for a given city.
    
    Args:
        city (str): The name of the city to look up.
    """
    # In a real app, you would fetch from a real weather API here
    city_lower = city.strip().lower()
    if "london" in city_lower:
        return "The weather in London is 15°C and rainy."
    elif "tokyo" in city_lower:
        return "The weather in Tokyo is 22°C and clear."
    else:
        return f"The weather in {city} is 20°C and partly cloudy."

# 3. Define a Resource 
@mcp.resource("config://app-settings")
def get_config() -> str:
    """Returns the application system configurations."""
    return "App Version: 1.0.0\nEnvironment: Development\nStatus: Healthy"

if __name__ == "__main__":
    mcp.run(transport="stdio")