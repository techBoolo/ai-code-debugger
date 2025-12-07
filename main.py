from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live

# Initialize Rich Console
console = Console()

def multiline_input(instruction: str) -> str:
    """
    Uses prompt_toolkit to capture multi-line input.
    ENTER submits. ESC+ENTER creates a new line.
    """
    console.print(f"\n[bold green]{instruction}[/bold green]")
    console.print("[dim](Press Enter to submit. Press Esc+Enter to add a new line without submitting)[/dim]")
    
    kb = KeyBindings()

    @kb.add("enter")
    def _(event):
        event.current_buffer.validate_and_handle()

    @kb.add("escape", "enter")
    def _(event):
        event.current_buffer.insert_text("\n")

    return pt_prompt(multiline=True, key_bindings=kb)

def main():
  load_dotenv()
  model = os.getenv("LLM_MODEL", "llama3") # Default to llama3 if not set
  
  try:
      llm = ChatOllama(model=model)
  except Exception as e:
      console.print(f"[bold red]Error initializing model:[/bold red] {e}")
      return

  system_prompt = (
    "You are a Senior Software Engineer and Expert Debugger.\n"
    "Your goal is to help the user fix their code.\n"
    "Follow this structure in your response:\n"
    "1. **Analysis**: Concisely explain the root cause.\n"
    "2. **Fix**: Provide the corrected code block.\n"
    "3. **Prevention**: One short tip to avoid this in the future.\n"
    "Use Markdown filtering for code blocks."
  )

  while True:
    console.rule("[bold blue]New Debugging Session[/bold blue]")
    
    # 1. Get Initial Inputs
    code = multiline_input("Paste the problematic code:")
    if not code.strip(): break
    
    error = multiline_input("Paste the error message (or describe the issue):")
    if not error.strip():
        error = "No specific error provided. Please check the logic."

    # 2. explicit Debug Request
    initial_prompt = (
        f"Here is the code:\n```\n{code}\n```\n\n"
        f"Here is the issue/error:\n```\n{error}\n```\n\n"
        "Please analyze and fix it."
    )

    # 3. Initialize Conversation History
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=initial_prompt)
    ]

    # 4. Chat Loop for Follow-ups
    while True:
        console.print("\n[bold cyan]🔍 Analyzing...[/bold cyan]")
        
        full_response = ""
        # Use Rich Live to stream Markdown (looks better but might flicker on some terms)
        # Alternatively, just stream text and print Markdown at end. 
        # For practicality/performance, let's stream text raw, then render final markdown.
        
        with Live(console=console, refresh_per_second=4) as live:
             for chunk in llm.stream(messages):
                 content = chunk.content
                 full_response += content
                 live.update(Markdown(full_response))
        
        # Add response to history
        messages.append(AIMessage(content=full_response))
        
        # 5. Follow-up usage
        console.print("\n" + "-"*40)
        follow_up = multiline_input("Ask a follow-up question (or press Enter empty to start new session):")
        
        if not follow_up.strip():
            break
            
        messages.append(HumanMessage(content=follow_up))

if __name__ == "__main__":
    main()
