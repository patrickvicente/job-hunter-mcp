"""
MCP Server Configuration

This module sets up and configures the FastMCP server with all available tools.
It provides both class-based and function-based approaches for registering tools.
"""

from mcp.server.fastmcp import FastMCP
from .tools.enrich_job import EnrichJobTool, enrich_job, enrich_job_prompt
from .schemas.enrich_job import EnrichJobInput

class MCPServer:
    """
    Class-based MCP server configuration.
    
    This approach provides better organization and makes it easier to:
    - Manage multiple tools
    - Handle server lifecycle
    - Add middleware or configuration
    - Test server components
    """
    
    def __init__(self, name: str = "job-hunter"):
        self.mcp = FastMCP(name)
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools"""
        # Register function-based tools (FastMCP style)
        self.mcp.tool()(enrich_job)
        self.mcp.prompt()(enrich_job_prompt)
    
    def get_tools_metadata(self):
        """Get metadata for all registered tools"""
        return {
            "enrich_job": EnrichJobTool.metadata(),
            # Add other tools here as you create them
        }
    
    def run(self, transport: str = 'stdio'):
        """Run the MCP server"""
        self.mcp.run(transport=transport)
    
    def get_server(self):
        """Get the underlying FastMCP server instance"""
        return self.mcp

# Initialize global server instance
mcp_server = MCPServer()

# Export for direct use
mcp = mcp_server.get_server()

if __name__ == "__main__":
    # Run server directly
    mcp_server.run()
