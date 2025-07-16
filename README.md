# Enhanced PRS System

## Overview
The Personal Reasoning System (PRS) now supports file-based task input for structured, reusable task definitions. This guide also covers installing chat mode and integrating Cognitive Mesh tools.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/prs-cognitive-system.git
cd prs-cognitive-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Enable Chat Mode
To use the interactive chat mode:
```bash
pip install streamlit
streamlit run chat_mode.py
```
*This launches a web-based chat interface for PRS.*

### 4. Add Cognitive Mesh Tools
To enable Cognitive Mesh features:
- Ensure `cognitive_mesh/` is present in your repo (or copy from `tools/cognitive_mesh/`).
- Install any extra dependencies:
    ```bash
    pip install -r cognitive_mesh/requirements.txt
    ```
- Enable mesh tools in your config (see `config.yaml`):
    ```yaml
    mesh_tools_enabled: true
    mesh_tools_path: cognitive_mesh/
    ```

---

## Usage Modes

### 1. Interactive Mode (Original)
```bash
python3 .github/prompts/generate_prs_log.py
```
Prompts for task input via CLI.

### 2. Direct CLI Task
```bash
python3 .github/prompts/generate_prs_log.py --task "Your task description"
```

### 3. File-Based Input (New)
```bash
python3 .github/prompts/generate_prs_log.py --file task.yaml
```

### 4. Template Creation (New)
```bash
python3 .github/prompts/generate_prs_log.py --template my_template.yaml
```

---

## Task File Formats

### YAML Format (Recommended)
```yaml
task: "Primary task description"
context: |
  Additional background information
  Multi-line context supported
constraints: |
  - Constraint 1
  - Constraint 2
priority: "high|medium|low"
expected_outcome: "Success criteria"
```

### JSON Format
```json
{
  "task": "Primary task description",
  "context": "Additional context",
  "constraints": "Specific requirements",
  "priority": "high",
  "expected_outcome": "Success criteria"
}
```

### Plain Text Format
Simple text files are treated as task descriptions:
```
Implement new feature X with consideration for Y and Z constraints.
```

---

## Benefits

1. **Reusability**: Save and reuse task templates
2. **Version Control**: Track task evolution in git
3. **Collaboration**: Share structured task definitions
4. **Batch Processing**: Process multiple predefined tasks
5. **Structured Context**: Include detailed background and constraints

---

## Memory Integration

File-based tasks integrate with the existing PRS memory system:
- All reasoning phases are preserved
- Memory hooks are maintained
- Builder/Visionary/Skeptic perspectives are applied
- Confidence tracking continues

---

## Examples

See the provided template files:
- `task_template.yaml` - Full structured template
- `example_task.yaml` - Simple example
- `test_template.yaml` - Generated template

---

## Cognitive Mesh Integration

This enhancement supports the Cognitive Mesh approach by:
- Enabling persistent task definition
- Supporting structured reasoning workflows
- Facilitating memory-driven decision making
- Maintaining BDI + OODA framework integration

For advanced mesh tools, see `cognitive_mesh/README.md` for usage and