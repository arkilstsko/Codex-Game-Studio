# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Model Tier Assignment

Skills and role references are assigned to reasoning tiers based on task
complexity:

| Tier | Codex setting | When to use |
|------|---------------|-------------|
| **Fast** | lower-cost model or low reasoning | Read-only status checks, formatting, simple lookups with no creative judgment |
| **Standard** | default model with medium reasoning | Implementation, design authoring, and analysis of individual systems |
| **Deep** | strongest available model with high reasoning | Multi-document synthesis, high-stakes phase gate verdicts, and cross-system review |

Skills with `reasoning-tier: Fast`: `/help`, `/sprint-status`, `/story-readiness`, `/scope-check`,
`/project-stage-detect`, `/changelog`, `/patch-notes`, `/onboard`

Skills with `reasoning-tier: Deep`: `/review-all-gdds`, `/architecture-review`, `/gate-check`

All other skills default to Standard. When creating new skills, assign Fast if
the skill only reads and formats; assign Deep if it must synthesize 5+ documents
with high-stakes output; otherwise use the default Standard tier.

## Subagents vs Agent Teams

This project uses two distinct multi-agent patterns:

### Subagents (current, always active)
Spawned via `Task` within a single Codex session. Used by all `team-*` skills
and orchestration skills. Subagents share the session's permission context, run
sequentially or in parallel within the session, and return results to the parent.

**When to spawn in parallel**: If two role passes' inputs are independent (neither
needs the other's output to begin), spawn both role-reference passes simultaneously rather
than waiting. Example: `/review-all-gdds` Phase 1 (consistency) and Phase 2
(design theory) are independent — spawn both at the same time.

### Agent Teams
Multiple independent Codex sessions running simultaneously, coordinated via a
shared task list. Each session has its own context window and token budget.

**Use agent teams when**:
- Work spans multiple subsystems that will not touch the same files
- Each workstream would take >30 minutes and benefits from true parallelism
- A senior agent (technical-director, producer) needs to coordinate 3+ specialist
  sessions working on different epics simultaneously

**Do not use agent teams when**:
- One session's output is required as input for another (use sequential role passes)
- The task fits in a single session's context (use role passes instead)
- Cost is a concern — each team member burns tokens independently

**Current status**: Use only when the user explicitly asks for parallel agent
work or when the active Codex environment exposes role pass tools.

## Parallel Task Protocol

When an orchestration skill spawns multiple independent agents:

1. Issue all independent role-reference passes before waiting for any result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately — do not silently skip
4. Always produce a partial report if some agents complete and others block
