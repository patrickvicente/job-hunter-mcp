"""
MCP Server Configuration

This module sets up and configures the FastMCP server with all available tools.
It provides both class-based and function-based approaches for registering tools.
"""

from mcp.server.fastmcp import FastMCP

from app.mcp.tools.fit_scoring import FitScoringTool, fit_scoring, fit_scoring_prompt
from .tools.enrich_job import EnrichJobTool, enrich_job, enrich_job_prompt

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
        self.mcp.tool()(fit_scoring)
        self.mcp.prompt()(fit_scoring_prompt)
    
    def get_tools_metadata(self):
        """Get metadata for all registered tools"""
        return {
            "enrich_job": EnrichJobTool.metadata(),
            "fit_scoring": FitScoringTool.metadata(),
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
