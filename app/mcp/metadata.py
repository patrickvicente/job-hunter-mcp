"""
MCP Tools Metadata Manager

This module provides utilities for managing and documenting MCP tools metadata.
It automatically collects metadata from all tool classes and provides
a unified interface for tool discovery and documentation.
"""

from typing import Dict, Any, List

from app.mcp.tools.fit_scoring import FitScoringTool
from .tools.enrich_job import EnrichJobTool

class MCPMetadata:
    """
    Centralized metadata manager for MCP tools.
    
    This class provides:
    - Automatic tool discovery
    - Consistent metadata format
    - Documentation generation
    - Tool validation
    """
    
    # Registry of all available tool classes
    TOOL_CLASSES = {
        "enrich_job": EnrichJobTool,
        "fit_scoring": FitScoringTool,
    }
    
    @classmethod
    def get_all_tools_metadata(cls) -> Dict[str, Any]:
        """Get metadata for all registered tools"""
        metadata = {}
        for tool_name, tool_class in cls.TOOL_CLASSES.items():
            if hasattr(tool_class, 'metadata'):
                metadata[tool_name] = tool_class.metadata()
        return metadata
    
    @classmethod
    def get_tool_metadata(cls, tool_name: str) -> Dict[str, Any]:
        """Get metadata for a specific tool"""
        tool_class = cls.TOOL_CLASSES.get(tool_name)
        if tool_class and hasattr(tool_class, 'metadata'):
            return tool_class.metadata()
        return {}
    
    @classmethod
    def get_tools_list(cls) -> List[str]:
        """Get list of all available tool names"""
        return list(cls.TOOL_CLASSES.keys())
    
    @classmethod
    def validate_tool(cls, tool_name: str) -> bool:
        """Validate that a tool exists and has proper metadata"""
        tool_class = cls.TOOL_CLASSES.get(tool_name)
        if not tool_class:
            return False
        
        # Check if tool has required methods
        required_methods = ['metadata', 'execute']
        return all(hasattr(tool_class, method) for method in required_methods)
    
    @classmethod
    def generate_documentation(cls) -> str:
        """Generate documentation for all tools"""
        doc = "# MCP Tools Documentation\n\n"
        
        for tool_name, tool_class in cls.TOOL_CLASSES.items():
            if hasattr(tool_class, 'metadata'):
                metadata = tool_class.metadata()
                doc += f"## {metadata.get('name', tool_name)}\n\n"
                doc += f"**Description:** {metadata.get('description', 'No description available')}\n\n"
                
                # Add input schema info
                input_schema = metadata.get('inputSchema', {})
                if input_schema.get('properties'):
                    doc += "**Input Fields:**\n"
                    for field, details in input_schema['properties'].items():
                        field_type = details.get('type', 'unknown')
                        description = details.get('description', '')
                        doc += f"- `{field}` ({field_type}): {description}\n"
                    doc += "\n"
                
                doc += "---\n\n"
        
        return doc

# Convenience functions
def get_tools_metadata() -> Dict[str, Any]:
    """Get metadata for all tools"""
    return MCPMetadata.get_all_tools_metadata()

def get_tool_metadata(tool_name: str) -> Dict[str, Any]:
    """Get metadata for a specific tool"""
    return MCPMetadata.get_tool_metadata(tool_name)
