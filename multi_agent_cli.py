#%%
from dotenv import load_dotenv
import os
from agents import Runner, set_tracing_disabled
from openai import AsyncOpenAI
from databricks.sdk import WorkspaceClient
import asyncio
from src.agents.shared_context import SharedAgentContext
from src.agents.agent_factory import create_agent_system
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich import print as rprint
from tqdm.asyncio import tqdm
import time
import argparse

# Initialize Rich console
console = Console()

load_dotenv(".env")

MODEL_NAME = os.getenv("DATABRICKS_MODEL") or ""
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "dummy_key_for_databricks_usage"
BASE_URL = os.getenv("DATABRICKS_BASE_URL") or ""
API_KEY = os.getenv("DATABRICKS_TOKEN") or ""
set_tracing_disabled(True)
# Initialize clients
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
w = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"), token=os.getenv("DATABRICKS_TOKEN")
)

# Create agent system
agent_system = create_agent_system(client, MODEL_NAME)
triage_agent = agent_system['triage_agent']

#%%

# Create lifecycle hooks to track agent execution
class AgentExecutionHooks:
    def __init__(self, console):
        self.console = console
        self.start_time = None
        
    async def on_agent_start(self, context, agent):
        self.start_time = time.time()
        agent_name = agent.name
        context.context.current_agent = agent_name
        # Log conversation history entries
        history_count = len(context.context.conversation_history) if context.context.conversation_history else 0
        self.console.print(f"[bold blue]🚀 Starting {agent_name} with {history_count} history entries")
    
    async def on_agent_end(self, context, agent, output):
        agent_name = agent.name
        duration = time.time() - self.start_time
        self.console.print(Panel(f"[bold green]✅ {agent_name} completed in {duration:.2f}s", expand=False))
        # Record agent response in conversation history
        context.context.add_message(f"{agent_name}", output)
        # Log the updated number of history entries
        history_count = len(context.context.conversation_history)
        self.console.print(f"[dim]Conversation history now has {history_count} entries[/dim]")
        
    async def on_tool_start(self, context, agent, tool):
        tool_name = tool.name
        context.context.current_tool = tool_name
        self.console.print(f"[yellow]🔧 Using tool: {tool_name}")
        
    async def on_tool_end(self, context, agent, tool, result):
        tool_name = tool.name
        self.console.print(f"[green]✓ Tool {tool_name} completed")
        # Record tool usage in conversation history
        context.context.add_message(f"Tool ({tool_name})", str(result))
        # Log the updated number of history entries
        history_count = len(context.context.conversation_history)
        self.console.print(f"[dim]Conversation history now has {history_count} entries[/dim]")
    
    async def on_handoff(self, context, from_agent, to_agent):
        from_name = from_agent.name
        to_name = to_agent.name
        self.console.print(Panel(f"[bold magenta]↪️ Handoff: {from_name} → {to_name}", expand=False))
        # Record handoff in conversation history
        context.context.add_message("System", f"Handoff from {from_name} to {to_name}")
        # Log the updated number of history entries
        history_count = len(context.context.conversation_history)
        self.console.print(f"[dim]Conversation history now has {history_count} entries[/dim]")


#%%
async def process_query(query, shared_context=None):
    """Process a single query through the multi-agent system"""
    # Create a shared context object if not provided
    if shared_context is None:
        shared_context = SharedAgentContext()
    
    # Record user query in conversation history
    shared_context.add_message("User", query)
    
    # Create hooks for visualization
    hooks = AgentExecutionHooks(console)
    
    console.print(f"[bold white on blue]User Query:[/] {query}")
    
    # Check if this is a summarization request
    if any(phrase in query.lower() for phrase in ["summarize", "summary", "what have we discussed", "our conversation"]):
        # Add the conversation history to the query for context
        conversation_history = shared_context.get_formatted_history()
        enhanced_query = f"{query}\n\nHere is the conversation history to summarize:\n{conversation_history}"
        console.print("[yellow]Detected summarization request. Including conversation history.[/]")
    else:
        enhanced_query = query
    
    # Run the agent with a progress bar wrapper
    with console.status("[bold yellow]Processing query...", spinner="dots") as status:
        result = await Runner.run(
            triage_agent, 
            enhanced_query,
            context=shared_context,
            hooks=hooks,
        )
    
    # Print the final output with nice formatting
    console.print(Panel(f"[bold green]🎯 Final Output:[/]\n\n{result.final_output}", 
                      expand=False, border_style="green"))
    
    # Record the final output in the conversation history
    shared_context.add_message("System", result.final_output)
    
    return result, shared_context

async def interactive_session():
    """Run an interactive session with the multi-agent system"""
    console.print(Panel.fit("[bold]🤖 Starting Multi-Agent System with Tools-for-Agents Pattern", 
                          style="blue", border_style="blue"))
    
    console.print("[bold]Type your queries and press Enter. Type 'exit' or 'quit' to end the session.[/]")
    console.print("[bold]Type 'debug' to see the raw conversation history (for troubleshooting).[/]")
    
    # Example queries for user reference
    console.print(Panel("[dim]Example queries:\n" + 
                       "- Based on where store 110 is located, what are the demographics of the area?\n" +
                       "- Is Florida a good place to open a new store compared to Virginia?\n" +
                       "- What is the policy for returns at our stores?\n" +
                       "- Can you summarize our conversation so far?[/dim]", 
                       title="Examples", expand=False))
    
    # Keep track of the shared context across queries
    shared_context = SharedAgentContext()
    
    # Continue processing queries until user exits
    while True:
        try:
            # Get query from user
            query = console.input("\n[bold cyan]Enter your query:[/] ")
            
            # Check if user wants to exit
            if query.lower() in ('exit', 'quit'):
                console.print("[bold]Exiting session. Goodbye![/]")
                break
                
            # Debug command to check conversation history
            if query.lower() == 'debug':
                console.print("[bold yellow]DEBUG: Conversation History[/]")
                for i, entry in enumerate(shared_context.conversation_history):
                    console.print(f"[dim]{i}.[/dim] {entry['role']}: {entry['content'][:100]}..." if len(entry['content']) > 100 else f"[dim]{i}.[/dim] {entry['role']}: {entry['content']}")
                continue
                
            # Skip empty queries
            if not query.strip():
                continue
            
            # Process the query with the shared context
            result, shared_context = await process_query(query, shared_context)
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Session interrupted. Exiting...[/]")
            break
        except Exception as e:
            console.print(f"[bold red]Error processing query: {str(e)}[/]")
            import traceback
            console.print(traceback.format_exc())
            
async def run_single_query(query):
    """Run a single query through the multi-agent system"""
    console.print(Panel.fit("[bold]🤖 Starting Multi-Agent System with Tools-for-Agents Pattern", 
                          style="blue", border_style="blue"))
    
    result, context = await process_query(query)

# Run the async function
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the multi-agent system with Tools-for-Agents pattern')
    parser.add_argument('-q', '--query', type=str, help='A single query to process (runs in non-interactive mode)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode (default if no query provided)')
    args = parser.parse_args()
    
    if args.query:
        # Run a single query
        asyncio.run(run_single_query(args.query))
    else:
        # Run in interactive mode
        asyncio.run(interactive_session())

# %% 