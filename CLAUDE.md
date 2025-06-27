# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-Agent Business Intelligence System with collaborative AI agents for enterprise analytics and market research. The system uses OpenAI Agents framework with tools-for-agents pattern where agents can call each other as tools.

## Architecture

### Core Components
- **Triage Agent**: Routes queries to appropriate specialist agents based on content analysis
- **Enterprise Intelligence Agent**: Handles store performance, inventory, policies using Databricks Genie
- **Market Intelligence Agent**: Handles demographics, market research using Census API and Perplexity AI
- **SharedAgentContext**: Maintains conversation history and shared state across agent interactions

### Agent Communication Pattern
Agents use a "tools-for-agents" pattern where:
- Enterprise Agent can call Market Agent as `get_market_intelligence` tool
- Market Agent can call Enterprise Agent as `get_enterprise_data` tool
- This enables compound queries requiring data from multiple domains

### Data Sources
- **Databricks Genie**: Store performance and inventory data via REST API
- **Unity Catalog Functions**: Business policy lookup (`juan_dev.genai.retail_club_conduct`)
- **Census API**: Demographic data by state
- **Perplexity API**: Web research and reasoning (`sonar-reasoning-pro` model)

## Development Commands

### Environment Setup
```bash
# Virtual environment (uses uv)
uv venv --python 3.12 && source .venv/bin/activate
uv pip install -r requirements.txt
```

### Running the Application
```bash
# Web interface
streamlit run app.py

# CLI - single query
python multi_agent_cli.py --query "Your question here"

# CLI - interactive mode
python multi_agent_cli.py --interactive
```

### Environment Variables Required
See `app.yaml` for complete list. Key variables:
- `DATABRICKS_HOST`, `DATABRICKS_TOKEN`, `DATABRICKS_BASE_URL`, `DATABRICKS_MODEL`
- `GENIE_SPACE_ID`, `GENIE_SPACE_PRODUCT_INV_ID` 
- `CENSUS_API_KEY`, `PERPLEXITY_API_KEY`
- `MLFLOW_EXPERIMENT_ID` (optional, for tracing)

## File Structure

### Core Application Files
- `app.py`: Streamlit web interface with real-time agent execution tracking
- `multi_agent_cli.py`: Command-line interface with Rich console output
- `toolkit.py`: Custom function tools for external API integrations
- `app.yaml`: Deployment configuration with environment variables

### Agent Configuration
- `prompts/triage_agent.txt`: Routing logic and decision criteria
- `prompts/enterprise_intelligence_agent.txt`: Store/business data specialist
- `prompts/market_intelligence_agent.txt`: Demographics/market research specialist

### Key Implementation Details

#### Agent Lifecycle Hooks
Both interfaces implement lifecycle hooks for tracking:
- `on_agent_start/end`: Agent execution timing
- `on_tool_start/end`: Tool usage tracking  
- `on_handoff`: Inter-agent communication
- All events are logged to `SharedAgentContext.conversation_history`

#### Async Processing
- Uses `asyncio` for concurrent operations
- `Runner.run()` orchestrates agent execution
- Streamlit uses `asyncio.run_until_complete()` for async integration

#### Error Handling
- Timeout handling for external API calls (60s default)
- Graceful fallbacks for missing data
- Debug mode available in both interfaces

## Testing & Debugging

The application includes built-in debugging features:
- Streamlit: Debug mode toggle in sidebar showing context state and conversation history
- CLI: `debug` command to inspect conversation history
- Both interfaces track agent handoffs and tool usage

No formal test suite is present - testing is done through example queries and manual verification.