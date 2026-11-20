---
wordpress_id: 386
title: "AI-Powered Network Assistant"
date: "2026-02-24T14:54:04"
url: "https://networkpuzzles.com/2026/02/24/ai-powered-read-only-network-assistant/"
---

In this lab project, I built an AI-powered network assistant that:

* Receives questions via Telegram
* Decides which Cisco IOS commands are needed
* Connects to the router via SSH
* Executes read-only commands
* Analyzes the output using GPT-4o-mini
* Returns structured findings and recommendations

###### The Idea

Instead of manually running commands like:

```
show ip interface brief  
show interface Gi0/1  
show logging | include BGP
```

We can simply ask:

* “Why is Gi0/1 down?”
* “Is BGP healthy?”
* “Is TACACS configured?”
* “Can the router reach 8.8.8.8?”

The AI determines the required CLI commands, executes them safely, analyzes the results, and provides structured conclusions.

The workflow looks like this:

User (Telegram)  
↓  
GPT-4o-mini (decides which command is needed)  
↓  
Tool Call  
↓  
SSH to Router (Netmiko)  
↓  
CLI Output  
↓  
GPT Analysis  
↓  
Telegram Response

Set environment variables:

export TELEGRAM\_BOT\_TOKEN=”your\_telegram\_token”  
export OPENAI\_API\_KEY=”your\_openai\_api\_key”

```
import os
import json
import re
from netmiko import ConnectHandler

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# Read API keys and define router connection settings


# Read Telegram and OpenAI API keys from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Define router name (used only for display)
ROUTER_NAME = os.environ.get("ROUTER_NAME", "R1")

# Define router SSH connection details
ROUTER = {
    "device_type": "cisco_ios",
    "host": "192.168.199.30",
    "username": "admin",
    "password": "cisco"
}



# Define allowed command types using regex


# Allow only commands starting with "show"
SHOW_ONLY = re.compile(r"^\s*show\s+", re.IGNORECASE)

# Allow only commands starting with "ping"
PING_OK   = re.compile(r"^\s*ping(\s+|$)", re.IGNORECASE)

# Allow only commands starting with "traceroute"
TRACE_OK  = re.compile(r"^\s*traceroute(\s+|$)", re.IGNORECASE)



# This function safely executes CLI commands on the router


def run_cli(command: str) -> str:
    cmd = command.strip()

    # Block dangerous configuration or disruptive commands
    FORBIDDEN = ["conf", "configure", "reload", "write", "copy", "clear", "debug"]
    if any(word in cmd.lower() for word in FORBIDDEN):
        return "ERROR: Configuration or disruptive commands are forbidden."

    # Allow only show, ping, or traceroute commands
    if not (SHOW_ONLY.match(cmd) or PING_OK.match(cmd) or TRACE_OK.match(cmd)):
        return "ERROR: Only 'show', 'ping', and 'traceroute' are allowed."

    # Prevent full running-config dump for security/performance reasons
    if cmd.lower() == "show running-config":
        return "ERROR: Full running-config is not allowed."

    try:
        # Connect to router via SSH
        conn = ConnectHandler(**ROUTER)

        # Execute the command
        output = conn.send_command(cmd, read_timeout=30)

        # Close the SSH session
        conn.disconnect()

    except Exception as e:
        return f"ERROR: CLI execution failed: {e}"

    # If IOS reports invalid syntax, return a clean error
    if "% Invalid input" in output or "% Incomplete command" in output:
        return "ERROR: Invalid Cisco IOS command."

    return output



# Limit how many times the AI can run commands


# Maximum number of CLI commands per user question
MAX_TOOL_CALLS_PER_QUESTION = 3

# Maximum number of back-and-forth loops with AI
MAX_ROUNDS = 4



# Initialize OpenAI client


# Create OpenAI client using API key
client = OpenAI(api_key=OPENAI_API_KEY)



# Define tools that the AI is allowed to use


# These are the only actions the AI can request
FUNCTIONS = [
    {
        "name": "run_show",
        "description": f"Run a read-only Cisco IOS SHOW command on device {ROUTER_NAME}",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    },
    {
        "name": "run_ping",
        "description": f"Run a ping command on device {ROUTER_NAME}",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    },
    {
        "name": "run_traceroute",
        "description": f"Run a traceroute command on device {ROUTER_NAME}",
        "parameters": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"]
        }
    }
]



# System instructions that control AI behavior


# This prompt defines how the AI should behave
SYSTEM_INSTRUCTIONS = """
You are a Cisco IOS troubleshooting assistant.
You must decide which commands to run.
You must not ask the user for commands.
You may only use tool calls.
Never enter configuration mode.
Stop once enough data is collected.
"""



# Main AI decision loop


def agent_answer(question: str) -> str:

    # Start conversation with system rules and user question
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": question},
    ]

    tool_calls_used = 0

    # Allow limited AI diagnostic iterations
    for _ in range(MAX_ROUNDS):

        # Ask GPT what to do next
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            functions=FUNCTIONS,
            function_call="auto",
        )

        msg = response.choices[0].message

        # If AI requests to run a tool (CLI command)
        if msg.function_call:
            tool_calls_used += 1

            if tool_calls_used > MAX_TOOL_CALLS_PER_QUESTION:
                return "Too many diagnostic steps."

            # Extract command from AI tool call
            args = json.loads(msg.function_call.arguments or "{}")
            cmd = (args.get("command") or "").strip()

            # Execute command safely
            result = run_cli(cmd)

            # Add tool call and result back to conversation
            messages.append(msg)
            messages.append({
                "role": "function",
                "name": msg.function_call.name,
                "content": f"COMMAND: {cmd}\n\nOUTPUT:\n{result}"
            })

            continue

        # If no tool call → AI provides final answer
        return (msg.content or "").strip()

    return "Could not complete within allowed steps."


# Telegram bot handlers


# Runs when user types /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"AI Router Assistant Ready\nDevice: {ROUTER_NAME}"
    )


# Runs when user sends any message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = (update.message.text or "").strip()

    if not question:
        return

    await update.message.reply_text("Checking the router and analyzing...")

    try:
        answer = agent_answer(question)
    except Exception as e:
        answer = f"Error: {e}"

    # Trim long messages to avoid Telegram limits
    if len(answer) > 3800:
        answer = answer[:3800] + "\n\n(Trimmed)"

    await update.message.reply_text(answer)



# Start Telegram bot


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN env var.")
    if not OPENAI_API_KEY:
        raise SystemExit("Set OPENAI_API_KEY env var.")

    # Create Telegram bot application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram Router Agent running...")
    app.run_polling()


# Entry point of the script
if __name__ == "__main__":
    main()
```
![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/t1t.jpg?resize=1124%2C2048&ssl=1)
![](https://i0.wp.com/networkpuzzles.com/wp-content/uploads/2026/02/t2t.jpg?resize=1170%2C2029&ssl=1)
