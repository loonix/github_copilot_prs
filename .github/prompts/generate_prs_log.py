from crimson.copilot_init_client.client import CopilotClient
from datetime import datetime
import os
import json
import yaml
import argparse
import sys

# Connect to the Copilot API server at the correct port
client = CopilotClient(base_url="http://localhost:3000")

def load_task_from_file(filepath):
    """Load task configuration from a YAML or JSON file."""
    try:
        with open(filepath, 'r') as f:
            if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                return yaml.safe_load(f)
            elif filepath.endswith('.json'):
                return json.load(f)
            else:
                # Treat as plain text task description
                return {"task": f.read().strip()}
    except Exception as e:
        print(f"Error loading task file: {e}")
        sys.exit(1)

def validate_task_data(task_data):
    """Validate and normalize task data structure."""
    if isinstance(task_data, str):
        return {"task": task_data}
    elif isinstance(task_data, dict):
        if "task" not in task_data:
            raise ValueError("Task file must contain a 'task' field")
        return task_data
    else:
        raise ValueError("Invalid task file format")

def detect_project_context():
    context_parts = []

    if os.path.exists("package.json"):
        with open("package.json") as f:
            package = json.load(f)
            context_parts.append("Detected Node.js project (package.json):")
            context_parts.append(f"  name: {package.get('name')}")
            context_parts.append(f"  dependencies: {', '.join(package.get('dependencies', {}).keys())}")

    if os.path.exists("pubspec.yaml"):
        with open("pubspec.yaml") as f:
            pubspec = yaml.safe_load(f)
            context_parts.append("Detected Flutter project (pubspec.yaml):")
            context_parts.append(f"  name: {pubspec.get('name')}")
            deps = pubspec.get("dependencies", {})
            context_parts.append(f"  dependencies: {', '.join(deps.keys())}")

    if os.path.exists("requirements.txt"):
        with open("requirements.txt") as f:
            reqs = [line.strip() for line in f if line.strip()]
            context_parts.append("Detected Python project (requirements.txt):")
            context_parts.append(f"  dependencies: {', '.join(reqs)}")

    return "\n".join(context_parts) if context_parts else "No known project structure detected."

def ask_copilot(prompt):
    return client.chat(prompt)

def save_prs(task, reasoning, evaluation, adaptation, result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f".github/prompts/prs_{timestamp}.prompt.md"
    content = f"""# PRS Prompt - {task}

## Task
{task}

## Reasoning
{reasoning}

## Evaluation
{evaluation}

## Adaptation
{adaptation}

## Final Output Summary
{result}

# [GOD MODE: ON]
"""
    with open(filename, "w") as f:
        f.write(content)
    print(f"Saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate PRS log entries from tasks')
    parser.add_argument('--file', '-f', help='Load task from file (YAML, JSON, or plain text)')
    parser.add_argument('--task', '-t', help='Specify task directly via command line')
    parser.add_argument('--template', help='Create a template task file')
    
    args = parser.parse_args()
    
    if args.template:
        create_template(args.template)
        return
    
    # Determine task source
    if args.file:
        task_data = load_task_from_file(args.file)
        task_data = validate_task_data(task_data)
        task = task_data["task"]
        additional_context = task_data.get("context", "")
        constraints = task_data.get("constraints", "")
    elif args.task:
        task = args.task
        additional_context = ""
        constraints = ""
    else:
        # Fall back to interactive mode
        task = input("Task: ")
        additional_context = ""
        constraints = ""
    
    # Build context
    project_context = detect_project_context()
    full_context = f"Given the following project context:\n{project_context}"
    
    if additional_context:
        full_context += f"\n\nAdditional context:\n{additional_context}"
    
    if constraints:
        full_context += f"\n\nConstraints:\n{constraints}"
    
    context_prompt = f"{full_context}\n\nTask: {task}"

    print(f"\n🧠 Processing task: {task}")
    print("📊 Reasoning phase...")
    reasoning = ask_copilot(context_prompt)
    
    print("🔍 Evaluation phase...")
    evaluation = ask_copilot(f"Evaluate the reasoning: {reasoning}")
    
    print("🔄 Adaptation phase...")
    adaptation = ask_copilot(f"Refactor the approach based on: {evaluation}")
    
    print("✅ Final synthesis...")
    final = ask_copilot(f"{task}\n\nImproved strategy:\n{adaptation}")

    save_prs(task, reasoning, evaluation, adaptation, final)

def create_template(template_path):
    """Create a template task file."""
    template_content = {
        "task": "Describe your task here",
        "context": "Additional context or background information",
        "constraints": "Any specific constraints or requirements",
        "priority": "high|medium|low",
        "expected_outcome": "What success looks like"
    }
    
    try:
        with open(template_path, 'w') as f:
            if template_path.endswith('.json'):
                json.dump(template_content, f, indent=2)
            else:
                yaml.dump(template_content, f, default_flow_style=False)
        print(f"✅ Template created: {template_path}")
        print("Edit the file and run with --file flag to process it.")
    except Exception as e:
        print(f"❌ Error creating template: {e}")

if __name__ == "__main__":
    main()
