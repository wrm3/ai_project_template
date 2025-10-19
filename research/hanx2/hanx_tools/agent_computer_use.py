#!/usr/bin/env python3
"""
Computer Use Agent Module

This module provides an agent that can control the computer using OpenAI's computer-use-preview model.
It captures screenshots and executes actions like clicking and typing based on AI recommendations.
"""

import argparse
import base64
import io
import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Union, Tuple

# Add the parent directory to the path so we can import from hanx_tools and hanx_apis
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import pyautogui
from PIL import Image
from openai import OpenAI

# Import base agent
try:
    from hanx.hanx_tools.base_agent import BaseAgent
except ImportError:
    try:
        from base_agent import BaseAgent
    except ImportError:
        print("Error: Could not import BaseAgent. Using dummy implementation.")
        
        class BaseAgent:
            def __init__(self, name="BaseAgent", log_level=logging.INFO):
                self.name = name
                self.logger = logging.getLogger(name)
                
            def read_file(self, file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"Error reading file: {e}")
                    return ""
                
            def query_llm(self, prompt, provider="openai", model=None, temperature=0.7, max_tokens=None):
                print(f"Querying LLM with prompt: {prompt[:100]}...")
                return "Dummy LLM response"

class ComputerUseAgent(BaseAgent):
    """Agent that can control the computer using OpenAI's computer-use-preview model"""
    
    def __init__(self, name: str = "ComputerUseAgent"):
        """Initialize the computer use agent"""
        super().__init__(name)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Configure PyAutoGUI safety features
        pyautogui.PAUSE = 0.5  # Add a 0.5 second pause after each PyAutoGUI call
        pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
        
        self.log("Initialized Computer Use Agent")
    
    def take_screenshot(self) -> Tuple[str, str]:
        """Take a screenshot and return the path and base64 encoded image"""
        # Take a screenshot using PyAutoGUI
        screenshot = pyautogui.screenshot()
        
        # Save the screenshot to a file
        timestamp = int(time.time())
        screenshot_path = self.screenshot_dir / f"screenshot_{timestamp}.png"
        screenshot.save(screenshot_path)
        
        # Convert the screenshot to base64
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return str(screenshot_path), img_str
    
    def execute_action(self, action_type: str, params: Dict[str, Any]) -> bool:
        """Execute a computer action based on the action type and parameters"""
        try:
            if action_type == "click":
                x, y = params.get("x"), params.get("y")
                if x is not None and y is not None:
                    pyautogui.click(x=x, y=y)
                    self.log(f"Clicked at position ({x}, {y})")
                    return True
            
            elif action_type == "type":
                text = params.get("text")
                if text:
                    pyautogui.typewrite(text)
                    self.log(f"Typed text: {text}")
                    return True
            
            elif action_type == "press":
                key = params.get("key")
                if key:
                    pyautogui.press(key)
                    self.log(f"Pressed key: {key}")
                    return True
            
            elif action_type == "scroll":
                clicks = params.get("clicks", 0)
                pyautogui.scroll(clicks)
                self.log(f"Scrolled {clicks} clicks")
                return True
            
            elif action_type == "moveTo":
                x, y = params.get("x"), params.get("y")
                if x is not None and y is not None:
                    pyautogui.moveTo(x=x, y=y)
                    self.log(f"Moved to position ({x}, {y})")
                    return True
            
            self.log(f"Unknown or invalid action: {action_type} with params {params}")
            return False
        
        except Exception as e:
            self.log(f"Error executing action {action_type}: {e}")
            return False
    
    def get_computer_action(self, screenshot_b64: str, task: str) -> List[Dict[str, Any]]:
        """Get computer actions from OpenAI's computer-use-preview model"""
        try:
            response = self.client.chat.completions.create(
                model="computer-use-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that can control a computer."},
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": f"Task: {task}. What should I do next?"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}
                            }
                        ]
                    }
                ],
                tools=[{
                    "type": "computer",
                    "computer": {
                        "description": "Control the user's computer to complete tasks.",
                        "actions": [
                            {
                                "name": "click",
                                "description": "Click at a specific position on the screen",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "x": {"type": "number", "description": "X coordinate"},
                                        "y": {"type": "number", "description": "Y coordinate"}
                                    },
                                    "required": ["x", "y"]
                                }
                            },
                            {
                                "name": "type",
                                "description": "Type text",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string", "description": "Text to type"}
                                    },
                                    "required": ["text"]
                                }
                            },
                            {
                                "name": "press",
                                "description": "Press a key",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "key": {"type": "string", "description": "Key to press (e.g., 'enter', 'tab', 'esc')"}
                                    },
                                    "required": ["key"]
                                }
                            },
                            {
                                "name": "scroll",
                                "description": "Scroll the page",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "clicks": {"type": "number", "description": "Number of clicks to scroll (positive for down, negative for up)"}
                                    },
                                    "required": ["clicks"]
                                }
                            },
                            {
                                "name": "moveTo",
                                "description": "Move the cursor to a position",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "x": {"type": "number", "description": "X coordinate"},
                                        "y": {"type": "number", "description": "Y coordinate"}
                                    },
                                    "required": ["x", "y"]
                                }
                            }
                        ]
                    }
                }],
                tool_choice={"type": "computer"}
            )
            
            # Extract computer actions from the response
            actions = []
            for choice in response.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls'):
                    for tool_call in choice.message.tool_calls:
                        if tool_call.type == "computer":
                            for action in tool_call.computer.actions:
                                actions.append({
                                    "type": action.name,
                                    "params": action.parameters
                                })
            
            return actions
        
        except Exception as e:
            self.log(f"Error getting computer actions: {e}")
            return []
    
    def run(self, args: Optional[Dict[str, Any]] = None) -> str:
        """Run the computer use agent with the given arguments"""
        if args is None:
            args = {}
        
        task = args.get("task", "Help me navigate this screen")
        max_steps = args.get("max_steps", 10)
        
        self.log(f"Starting computer use agent with task: {task}")
        self.log(f"Will execute up to {max_steps} steps")
        
        results = []
        for step in range(max_steps):
            self.log(f"Step {step + 1}/{max_steps}")
            
            # Take a screenshot
            screenshot_path, screenshot_b64 = self.take_screenshot()
            self.log(f"Took screenshot: {screenshot_path}")
            
            # Get actions from OpenAI
            actions = self.get_computer_action(screenshot_b64, task)
            
            if not actions:
                self.log("No actions received, stopping")
                break
            
            # Execute each action
            for action in actions:
                action_type = action.get("type")
                params = action.get("params", {})
                
                self.log(f"Executing action: {action_type} with params {params}")
                success = self.execute_action(action_type, params)
                
                results.append({
                    "step": step + 1,
                    "action": action_type,
                    "params": params,
                    "success": success
                })
                
                # Small delay between actions
                time.sleep(1)
        
        self.log("Computer use agent completed")
        return str(results)

def main():
    """Main function to run the computer use agent from the command line"""
    parser = argparse.ArgumentParser(description="Computer Use Agent")
    parser.add_argument("--task", type=str, default="Help me navigate this screen",
                        help="Task to perform on the computer")
    parser.add_argument("--max-steps", type=int, default=10,
                        help="Maximum number of steps to execute")
    
    args = parser.parse_args()
    
    agent = ComputerUseAgent()
    result = agent.run({
        "task": args.task,
        "max_steps": args.max_steps
    })
    
    print(result)

if __name__ == "__main__":
    main() 