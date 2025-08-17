# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SuperClaude Framework is a Python-based enhancement system for Claude Code that adds specialized commands, personas, and MCP server integration. Version 3.1.0-gpt5 includes GPT-5 dual-model planning capabilities.

## Installation & Development Commands

### Package Installation
```bash
# Install from PyPI
pip install SuperClaude

# Install from source
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude_Framework
pip install -e .

# Using uv (faster)
uv sync
uv pip install SuperClaude
```

### Framework Installation to Claude Code
```bash
# Standard installation
python3 -m SuperClaude install

# Alternative entry points (all equivalent)
SuperClaude install
python3 SuperClaude install

# Installation profiles
SuperClaude install --minimal      # Core only
SuperClaude install --interactive  # Choose components
SuperClaude install --profile developer  # Everything
```

### Testing GPT-5 Integration
```bash
# Test GPT-5 logging system
python3 test_gpt5_logging.py

# View GPT-5 logs interactively
python3 view_gpt5_logs.py

# Check log files directly
ls ~/.claude/logs/gpt5/
```

## Architecture

### Core Framework Structure
The framework operates by installing documentation files to `~/.claude/` that guide Claude's behavior:

1. **Behavior Documentation** (`SuperClaude/Core/`)
   - `COMMANDS.md` - 16 slash command definitions with MCP integration
   - `FLAGS.md` - Command flags including GPT-5 controls
   - `PERSONAS.md` - 11 domain-specific AI personalities
   - `ORCHESTRATOR.md` - Intelligent routing and tool selection
   - `MCP.md` - External server integration (Deepwiki, Sequential, Magic, Browserbase)
   - `MODES.md` - Operational modes including GPT-5 enhanced planning

2. **GPT-5 Integration** (NEW)
   - `plan_mode_hook.py` - Intercepts Claude's plan mode
   - `openai_integration.py` - GPT-5 API wrapper with model variants
   - `dual_planner.py` - Orchestrates 5 planning strategies
   - `gpt5_logger.py` - Visual logging with color-coded output
   - `config/openai_settings.json` - Model configuration and pricing

3. **Installation System** (`setup/`)
   - Component-based architecture with registry pattern
   - Managers for config, files, and settings
   - Operations: install, update, uninstall, backup

### Command System
Commands follow `/sc:command` pattern with these categories:
- **Development**: implement, build, design
- **Analysis**: analyze, troubleshoot, explain
- **Quality**: improve, test, cleanup
- **Management**: document, git, task, estimate

### MCP Server Integration
External services provide additional capabilities:
- **Deepwiki**: Library documentation and patterns
- **Sequential**: Complex multi-step analysis (--think flags)
- **Magic**: UI component generation
- **Browserbase**: Cloud browser automation

### GPT-5 Planning Strategies
When `ENABLE_DUAL_PLANNING=true`:
1. **claude_only**: Traditional single-model
2. **gpt5_only**: Pure GPT-5 planning
3. **dual_model**: Parallel analysis with merging
4. **consensus**: Emphasizes model agreement
5. **complementary**: Leverages unique strengths

## Environment Configuration

### Required for GPT-5
```bash
export OPENAI_API_KEY=sk-your-key
export ENABLE_DUAL_PLANNING=true
export GPT5_MODEL=gpt-5  # or gpt-5-mini, gpt-5-nano
export GPT5_LOGGING=true
export GPT5_VERBOSITY=medium
```

### Installation Paths
- Framework files: `~/.claude/`
- Logs: `~/.claude/logs/gpt5/`
- Settings: `~/.claude/settings.json`
- MCP config: `~/.config/mcp/mcp-config.json`

## Key Implementation Details

### GPT-5 Integration Flow
1. Plan mode detection via hook system
2. Parallel API calls to Claude and GPT-5
3. Intelligent plan merging with consensus detection
4. Visual logging with cost tracking
5. Graceful fallback on API failures

### Logging System
- Color-coded console output (🎯 Plan, 🤖 API, ✅ Success, ⚠️ Warning)
- File logging to `~/.claude/logs/gpt5/`
- Real-time cost tracking ($1.25/M input, $10/M output)
- Session statistics and metrics

### Framework File Updates
When modifying core behavior:
1. Edit relevant `.md` files in `SuperClaude/Core/`
2. Update `FLAGS.md` for new command flags
3. Modify `MODES.md` for operational changes
4. Ensure `ORCHESTRATOR.md` routing rules align

## Development Guidelines

### Adding New Commands
1. Create command definition in `SuperClaude/Commands/`
2. Update `COMMANDS.md` with command metadata
3. Add routing rules to `ORCHESTRATOR.md`
4. Configure MCP server preferences if needed

### Extending GPT-5 Integration
1. Modify `openai_integration.py` for new API features
2. Update `dual_planner.py` for planning strategies
3. Enhance `gpt5_logger.py` for additional metrics
4. Adjust `plan_mode_hook.py` for detection logic

### Testing Changes
```bash
# Test GPT-5 integration
python3 test_gpt5_logging.py

# Verify installation
SuperClaude install --dry-run

# Check logs
python3 view_gpt5_logs.py --latest
```

## Version Information
- Current: 3.1.0-gpt5
- Python: >=3.8
- Dependencies: setuptools>=45.0.0
- Optional: OpenAI SDK for GPT-5 features