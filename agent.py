import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Point to your local python environment and server script
server_params = StdioServerParameters(
    command="python",  # or path to your venv python executable
    args=["weather_mcp.py"],
    env=None
)

async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize connection
            await session.initialize()
            print("Agent connected to MCP server successfully!")

            # Discover available tools
            tools_response = await session.list_tools()
            print("Discovered tools:", [t.name for t in tools_response.tools])

            # Call the tool from the agent logic
            result = await session.call_tool("fetch_weather", {"city": "tokyo"})
            print("Tool execution result:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())