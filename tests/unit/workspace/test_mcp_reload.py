# -*- coding: utf-8 -*-
"""Tests for MCP hot-reload safety handling."""

from types import SimpleNamespace

from copaw.app.multi_agent_manager import MultiAgentManager
from copaw.config.config import MCPClientConfig, MCPConfig


def test_requires_serial_reload_when_any_client_is_unsafe():
    """Agents with unsafe MCP clients should avoid zero-downtime reload."""
    agent_config = SimpleNamespace(
        mcp=MCPConfig(
            clients={
                "chrome-mcp-stdio": MCPClientConfig(
                    name="chrome-mcp-stdio",
                    transport="stdio",
                    command="npx",
                    args=["node", "mcp-server-stdio.js"],
                    hot_reload_safe=False,
                ),
            },
        ),
    )

    assert MultiAgentManager._requires_serial_reload(agent_config) is True


def test_requires_serial_reload_ignores_disabled_or_safe_clients():
    """Disabled or default-safe MCP clients should not force serial reload."""
    agent_config = SimpleNamespace(
        mcp=MCPConfig(
            clients={
                "chrome-mcp-stdio": MCPClientConfig(
                    name="chrome-mcp-stdio",
                    enabled=False,
                    transport="stdio",
                    command="npx",
                    args=["node", "mcp-server-stdio.js"],
                    hot_reload_safe=False,
                ),
                "playwright": MCPClientConfig(
                    name="playwright",
                    transport="stdio",
                    command="npx",
                    args=["@playwright/mcp@latest"],
                ),
            },
        ),
    )

    assert MultiAgentManager._requires_serial_reload(agent_config) is False
