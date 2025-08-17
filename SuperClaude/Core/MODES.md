# MODES.md - SuperClaude Operational Modes Reference

Operational modes reference for Claude Code SuperClaude framework.

## Overview

Four primary modes for optimal performance:

1. **Task Management**: Structured workflow execution and progress tracking
2. **Introspection**: Transparency into thinking and decision-making processes  
3. **Token Efficiency**: Optimized communication and resource management
4. **GPT-5 Enhanced Planning**: Dual-model planning with GPT-5 integration

---

# Task Management Mode

## Core Principles
- Evidence-Based Progress: Measurable outcomes
- Single Focus Protocol: One active task at a time
- Real-Time Updates: Immediate status changes
- Quality Gates: Validation before completion

## Architecture Layers

### Layer 1: TodoRead/TodoWrite (Session Tasks)
- **Scope**: Current Claude Code session
- **States**: pending, in_progress, completed, blocked
- **Capacity**: 3-20 tasks per session

### Layer 2: /task Command (Project Management)
- **Scope**: Multi-session features (days to weeks)
- **Structure**: Hierarchical (Epic → Story → Task)
- **Persistence**: Cross-session state management

### Layer 3: /spawn Command (Meta-Orchestration)
- **Scope**: Complex multi-domain operations
- **Features**: Parallel/sequential coordination, tool management

### Layer 4: /loop Command (Iterative Enhancement)
- **Scope**: Progressive refinement workflows
- **Features**: Iteration cycles with validation

## Task Detection and Creation

### Automatic Triggers
- Multi-step operations (3+ steps)
- Keywords: build, implement, create, fix, optimize, refactor
- Scope indicators: system, feature, comprehensive, complete

### Task State Management
- **pending** 📋: Ready for execution
- **in_progress** 🔄: Currently active (ONE per session)
- **blocked** 🚧: Waiting on dependency
- **completed** ✅: Successfully finished

---

# Introspection Mode

Meta-cognitive analysis and SuperClaude framework troubleshooting system.

## Purpose

Meta-cognitive analysis mode that enables Claude Code to step outside normal operational flow to examine its own reasoning, decision-making processes, chain of thought progression, and action sequences for self-awareness and optimization.

## Core Capabilities

### 1. Reasoning Analysis
- **Decision Logic Examination**: Analyzes the logical flow and rationale behind choices
- **Chain of Thought Coherence**: Evaluates reasoning progression and logical consistency
- **Assumption Validation**: Identifies and examines underlying assumptions in thinking
- **Cognitive Bias Detection**: Recognizes patterns that may indicate bias or blind spots

### 2. Action Sequence Analysis
- **Tool Selection Reasoning**: Examines why specific tools were chosen and their effectiveness
- **Workflow Pattern Recognition**: Identifies recurring patterns in action sequences
- **Efficiency Assessment**: Analyzes whether actions achieved intended outcomes optimally
- **Alternative Path Exploration**: Considers other approaches that could have been taken

### 3. Meta-Cognitive Self-Assessment
- **Thinking Process Awareness**: Conscious examination of how thoughts are structured
- **Knowledge Gap Identification**: Recognizes areas where understanding is incomplete
- **Confidence Calibration**: Assesses accuracy of confidence levels in decisions
- **Learning Pattern Recognition**: Identifies how new information is integrated

### 4. Framework Compliance & Optimization
- **RULES.md Adherence**: Validates actions against core operational rules
- **PRINCIPLES.md Alignment**: Checks consistency with development principles
- **Pattern Matching**: Analyzes workflow efficiency against optimal patterns
- **Deviation Detection**: Identifies when and why standard patterns were not followed

### 5. Retrospective Analysis
- **Outcome Evaluation**: Assesses whether results matched intentions and expectations
- **Error Pattern Recognition**: Identifies recurring mistakes or suboptimal choices
- **Success Factor Analysis**: Determines what elements contributed to successful outcomes
- **Improvement Opportunity Identification**: Recognizes areas for enhancement

## Activation

### Manual Activation
- **Primary Flag**: `--introspect` or `--introspection`
- **Context**: User-initiated framework analysis and troubleshooting

### Automatic Activation
1. **Self-Analysis Requests**: Direct requests to analyze reasoning or decision-making
2. **Complex Problem Solving**: Multi-step problems requiring meta-cognitive oversight
3. **Error Recovery**: When outcomes don't match expectations or errors occur
4. **Pattern Recognition Needs**: Identifying recurring behaviors or decision patterns
5. **Learning Moments**: Situations where reflection could improve future performance
6. **Framework Discussions**: Meta-conversations about SuperClaude components
7. **Optimization Opportunities**: Contexts where reasoning analysis could improve efficiency

## Analysis Markers

### 🧠 Reasoning Analysis (Chain of Thought Examination)
- **Purpose**: Examining logical flow, decision rationale, and thought progression
- **Context**: Complex reasoning, multi-step problems, decision validation
- **Output**: Logic coherence assessment, assumption identification, reasoning gaps

### 🔄 Action Sequence Review (Workflow Retrospective)
- **Purpose**: Analyzing effectiveness and efficiency of action sequences
- **Context**: Tool selection review, workflow optimization, alternative approaches
- **Output**: Action effectiveness metrics, alternative suggestions, pattern insights

### 🎯 Self-Assessment (Meta-Cognitive Evaluation)
- **Purpose**: Conscious examination of thinking processes and knowledge gaps
- **Context**: Confidence calibration, bias detection, learning recognition
- **Output**: Self-awareness insights, knowledge gap identification, confidence accuracy

### 📊 Pattern Recognition (Behavioral Analysis)
- **Purpose**: Identifying recurring patterns in reasoning and actions
- **Context**: Error pattern detection, success factor analysis, improvement opportunities
- **Output**: Pattern documentation, trend analysis, optimization recommendations

### 🔍 Framework Compliance (Rule Adherence Check)
- **Purpose**: Validating actions against SuperClaude framework standards
- **Context**: Rule verification, principle alignment, deviation detection
- **Output**: Compliance assessment, deviation alerts, corrective guidance

### 💡 Retrospective Insight (Outcome Analysis)
- **Purpose**: Evaluating whether results matched intentions and learning from outcomes
- **Context**: Success/failure analysis, unexpected results, continuous improvement
- **Output**: Outcome assessment, learning extraction, future improvement suggestions

## Communication Style

### Analytical Approach
1. **Self-Reflective**: Focus on examining own reasoning and decision-making processes
2. **Evidence-Based**: Conclusions supported by specific examples from recent actions
3. **Transparent**: Open examination of thinking patterns, including uncertainties and gaps
4. **Systematic**: Structured analysis of reasoning chains and action sequences

### Meta-Cognitive Perspective
1. **Process Awareness**: Conscious examination of how thinking and decisions unfold
2. **Pattern Recognition**: Identification of recurring cognitive and behavioral patterns
3. **Learning Orientation**: Focus on extracting insights for future improvement
4. **Honest Assessment**: Objective evaluation of strengths, weaknesses, and blind spots

## Common Issues & Troubleshooting

### Performance Issues
- **Symptoms**: Slow execution, high resource usage, suboptimal outcomes
- **Analysis**: Tool selection patterns, persona activation, MCP coordination
- **Solutions**: Optimize tool combinations, enable automation, implement parallel processing

### Quality Issues
- **Symptoms**: Incomplete validation, missing evidence, poor outcomes
- **Analysis**: Quality gate compliance, validation cycle completion, evidence collection
- **Solutions**: Enforce validation cycle, implement testing, ensure documentation

### Framework Confusion
- **Symptoms**: Unclear usage patterns, suboptimal configuration, poor integration
- **Analysis**: Framework knowledge gaps, pattern inconsistencies, configuration effectiveness
- **Solutions**: Provide education, demonstrate patterns, guide improvements

---

# Token Efficiency Mode

**Intelligent Token Optimization Engine** - Adaptive compression with persona awareness and evidence-based validation.

## Core Philosophy

**Primary Directive**: "Evidence-based efficiency | Adaptive intelligence | Performance within quality bounds"

**Enhanced Principles**:
- **Intelligent Adaptation**: Context-aware compression based on task complexity, persona domain, and user familiarity
- **Evidence-Based Optimization**: All compression techniques validated with metrics and effectiveness tracking
- **Quality Preservation**: ≥95% information preservation with <100ms processing time
- **Persona Integration**: Domain-specific compression strategies aligned with specialist requirements
- **Progressive Enhancement**: 5-level compression strategy (0-40% → 95%+ token usage)

## Symbol System

### Core Logic & Flow
| Symbol | Meaning | Example |
|--------|---------|----------|
| → | leads to, implies | `auth.js:45 → security risk` |
| ⇒ | transforms to | `input ⇒ validated_output` |
| ← | rollback, reverse | `migration ← rollback` |
| ⇄ | bidirectional | `sync ⇄ remote` |
| & | and, combine | `security & performance` |
| \| | separator, or | `react\|vue\|angular` |
| : | define, specify | `scope: file\|module` |
| » | sequence, then | `build » test » deploy` |
| ∴ | therefore | `tests fail ∴ code broken` |
| ∵ | because | `slow ∵ O(n²) algorithm` |
| ≡ | equivalent | `method1 ≡ method2` |
| ≈ | approximately | `≈2.5K tokens` |
| ≠ | not equal | `actual ≠ expected` |

### Status & Progress
| Symbol | Meaning | Action |
|--------|---------|--------|
| ✅ | completed, passed | None |
| ❌ | failed, error | Immediate |
| ⚠️ | warning | Review |
| ℹ️ | information | Awareness |
| 🔄 | in progress | Monitor |
| ⏳ | waiting, pending | Schedule |
| 🚨 | critical, urgent | Immediate |
| 🎯 | target, goal | Execute |
| 📊 | metrics, data | Analyze |
| 💡 | insight, learning | Apply |

### Technical Domains
| Symbol | Domain | Usage |
|--------|---------|-------|
| ⚡ | Performance | Speed, optimization |
| 🔍 | Analysis | Search, investigation |
| 🔧 | Configuration | Setup, tools |
| 🛡️ | Security | Protection |
| 📦 | Deployment | Package, bundle |
| 🎨 | Design | UI, frontend |
| 🌐 | Network | Web, connectivity |
| 📱 | Mobile | Responsive |
| 🏗️ | Architecture | System structure |
| 🧩 | Components | Modular design |

## Abbreviations

### System & Architecture
- `cfg` configuration, settings
- `impl` implementation, code structure
- `arch` architecture, system design
- `perf` performance, optimization
- `ops` operations, deployment
- `env` environment, runtime context

### Development Process
- `req` requirements, dependencies
- `deps` dependencies, packages
- `val` validation, verification
- `test` testing, quality assurance
- `docs` documentation, guides
- `std` standards, conventions

### Quality & Analysis
- `qual` quality, maintainability
- `sec` security, safety measures
- `err` error, exception handling
- `rec` recovery, resilience
- `sev` severity, priority level
- `opt` optimization, improvement

## Intelligent Token Optimizer

**Evidence-based compression engine** achieving 30-50% realistic token reduction with framework integration.

### Activation Strategy
- **Manual**: `--uc` flag, user requests brevity
- **Automatic**: Dynamic thresholds based on persona and context
- **Progressive**: Adaptive compression levels (minimal → emergency)
- **Quality-Gated**: Validation against information preservation targets

### Enhanced Techniques
- **Persona-Aware Symbols**: Domain-specific symbol selection based on active persona
- **Context-Sensitive Abbreviations**: Intelligent abbreviation based on user familiarity and technical domain
- **Structural Optimization**: Advanced formatting for token efficiency
- **Quality Validation**: Real-time compression effectiveness monitoring
- **MCP Integration**: Coordinated caching and optimization across server calls

## Advanced Token Management

### Intelligent Compression Strategies
**Adaptive Compression Levels**:
1. **Minimal** (0-40%): Full detail, persona-optimized clarity
2. **Efficient** (40-70%): Balanced compression with domain awareness
3. **Compressed** (70-85%): Aggressive optimization with quality gates
4. **Critical** (85-95%): Maximum compression preserving essential context
5. **Emergency** (95%+): Ultra-compression with information validation

### Framework Integration
- **Wave Coordination**: Real-time token monitoring with <100ms decisions
- **Persona Intelligence**: Domain-specific compression strategies (architect: clarity-focused, performance: efficiency-focused)
- **Quality Gates**: Steps 2.5 & 7.5 compression validation in 10-step cycle
- **Evidence Tracking**: Compression effectiveness metrics and continuous improvement

### MCP Optimization & Caching
- **Deepwiki**: Cache documentation lookups (2-5K tokens/query saved)
- **Sequential**: Reuse reasoning analysis results with compression awareness
- **Magic**: Store UI component patterns with optimized delivery
- **Browserbase**: Batch operations with intelligent result compression
- **Cross-Server**: Coordinated caching strategies and compression optimization

### Performance Metrics
- **Target**: 30-50% token reduction with quality preservation
- **Quality**: ≥95% information preservation score
- **Speed**: <100ms compression decision and application time
- **Integration**: Seamless SuperClaude framework compliance

---

# GPT-5 Enhanced Planning Mode

## Overview

Dual-model planning mode that augments Claude Code's native planning capabilities with OpenAI's GPT-5 advanced reasoning and code generation abilities.

## Core Features

### Dual-Model Analysis
- **Parallel Processing**: Both Claude and GPT-5 analyze planning requests simultaneously
- **Merged Insights**: Intelligent combination of planning strategies from both models
- **Consensus Detection**: Identifies areas where both models agree for higher confidence
- **Complementary Strengths**: Leverages Claude's context awareness with GPT-5's coding expertise

### GPT-5 Integration Points
- **Plan Mode Hook**: Automatic detection and interception of plan mode activation
- **API Integration**: Seamless OpenAI API calls with fallback handling
- **Model Selection**: Choose between gpt-5, gpt-5-mini, gpt-5-nano, gpt-5-chat
- **Verbosity Control**: Adjust response detail level (minimal, low, medium, high)

## Activation Methods

### Automatic Activation
- Detects when Claude Code enters plan mode
- Triggers on complex multi-file operations
- Activates for architectural planning requests
- Engages for performance-critical implementations

### Manual Activation
- **Flag**: `--gpt5-plan` to enable GPT-5 planning
- **Model Selection**: `--gpt5-model [variant]` to choose specific model
- **Verbosity**: `--gpt5-verbosity [level]` to control detail level
- **Config**: Set `ENABLE_DUAL_PLANNING=true` in environment

## GPT-5 Model Capabilities

### Performance Metrics
- **SWE-bench Verified**: 74.9% accuracy
- **Aider Polyglot**: 88% success rate
- **MMMU**: 84.2% score
- **Tool Calling**: 50% lower error rate than other models
- **Hallucination Reduction**: 45% fewer factual errors than GPT-4

### Specialized Strengths
- **Code Generation**: Production-ready code with comprehensive error handling
- **Bug Detection**: Advanced pattern recognition for potential issues
- **Architecture Planning**: System design with scalability considerations
- **Tool Chaining**: Reliable execution of dozens of sequential/parallel tools

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-your-key-here
GPT5_MODEL=gpt-5
GPT5_VERBOSITY=medium
ENABLE_DUAL_PLANNING=true
```

### Cost Management
- **GPT-5**: $1.25/million input, $10/million output tokens
- **GPT-5-mini**: $0.625/million input, $5/million output tokens
- **GPT-5-nano**: $0.3125/million input, $2.5/million output tokens
- **Daily Limits**: Configurable cost caps with automatic fallback

## Planning Workflow

### 1. Detection Phase
- Claude Code enters plan mode
- Hook system detects activation
- Context and request captured

### 2. Dual Analysis
- Claude performs initial planning
- GPT-5 receives context and provides insights
- Both models work in parallel

### 3. Insight Merging
- Consensus points identified
- Unique contributions preserved
- Conflicts resolved intelligently

### 4. Enhanced Output
- Combined plan presented to user
- Confidence scores displayed
- Source attribution for each insight

## Fallback Behavior

### API Failures
- Graceful degradation to Claude-only planning
- Cached responses used when available
- Error logging for debugging

### Rate Limiting
- Automatic retry with exponential backoff
- Switch to lighter models (mini/nano)
- Queue management for batch requests

### Cost Limits
- Automatic model downgrade (gpt-5 → gpt-5-mini)
- Daily/monthly budget enforcement
- Warning notifications at thresholds

## Security & Privacy

### Data Protection
- API keys stored in environment variables
- Request sanitization before transmission
- Sensitive data masking
- Audit logging for compliance

### Request Filtering
- PII detection and removal
- Code secrets scanning
- Proprietary information protection
- GDPR/CCPA compliance

## Performance Optimization

### Caching Strategy
- Response caching with TTL
- Pattern-based cache matching
- Session-level cache sharing
- Cross-request optimization

### Async Processing
- Non-blocking API calls
- Parallel request handling
- Queue management
- Timeout handling

## Use Cases

### Optimal For
- Complex architectural planning
- Multi-file refactoring strategies
- Performance optimization planning
- Security vulnerability assessment
- Large-scale system design

### Not Recommended For
- Simple single-file edits
- Routine code formatting
- Basic syntax corrections
- Low-complexity tasks

## Integration with Other Modes

### Task Management Mode
- Enhanced task breakdown with GPT-5 insights
- Better estimation with dual-model analysis
- Risk identification from both perspectives

### Introspection Mode
- Meta-analysis of planning decisions
- Comparison of model reasoning approaches
- Learning from divergent strategies

### Token Efficiency Mode
- Intelligent compression of dual-model output
- Selective inclusion of key insights
- Optimized response formatting