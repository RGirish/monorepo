from setuptools import setup, find_packages

setup(
    name="mcp-server",
    version="0.1.0",
    description="An MCP server built with FastMCP",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastmcp>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-server=server.server:main",
        ],
    },
)
