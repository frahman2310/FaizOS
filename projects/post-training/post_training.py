"""Post-training — distillation vs RL, DPO, and tool calling (FaizOS build) — Module 16.

Three ways a raw pretrained model becomes useful:
  1. DISTILLATION - copy a strong teacher's reasoning traces (supervised, cheap, CAPPED by the teacher)
     vs RL          - discover your own solutions from reward (expensive, but no ceiling)
  2. DPO           - skip RLHF's separate reward model and optimise the preference pair directly
  3. TOOL CALLING  - the model only EMITS a call as text; your code decides whether to run it

Fill the THREE blanks, then run:  python3 post_training.py
"""

# --- 1. distillation vs RL -------------------------------------------------

def distilled_ceiling(teacher_score):
    """A student trained by copying a teacher approaches the teacher but cannot pass it."""
    # The student's best possible score is whatever the teacher itself scores.
    return teacher_score                # the student cannot pass the thing it copies


def rl_ceiling(teacher_score):
    """RL is not copying anyone, so the teacher's score is irrelevant to it."""
    return None                         # None means "no ceiling"


# --- 2. RLHF vs DPO --------------------------------------------------------

PIPELINE = {
    "RLHF": {"stages": 2, "models": ("policy", "reward model", "frozen reference")},
    "DPO":  {"stages": 1, "models": ("policy", "frozen reference")},
}


def training_stages(method):
    return PIPELINE[method]["stages"]


def models_needed(method):
    return len(PIPELINE[method]["models"])


# --- 3. tool calling -------------------------------------------------------

def calculator(args):
    return eval(args["expr"], {"__builtins__": {}})      # tiny sandbox: no builtins available


def clock(args):
    return "2026-08-12"


TOOLS = {"calculator": calculator, "clock": clock}       # the ONLY tools this agent may use


def run_tool_call(call, tools=TOOLS):
    """The model asked for a tool. THIS code decides whether it actually runs."""
    name, args = call["tool"], call["args"]
    if name not in tools:
        return f"refused: {name!r} is not an approved tool"
    # `tools[name]` looks up the approved function; calling it with `args` runs it.
    return tools[name](args)            # look the function up, then run it


if __name__ == "__main__":
    print("1. DISTILLATION vs RL (teacher scores 70%)")
    print(f"   distilled student ceiling : {distilled_ceiling(70)}%")
    print(f"   RL ceiling                : {rl_ceiling(70)}   (no ceiling — it copies nobody)")

    print("\n2. RLHF vs DPO")
    for m in ("RLHF", "DPO"):
        print(f"   {m:<5} {training_stages(m)} training stage(s), {models_needed(m)} models")

    print("\n3. TOOL CALLING — the model only asks; this code runs it")
    for call in ({"tool": "calculator", "args": {"expr": "17*23"}},
                 {"tool": "clock", "args": {}},
                 {"tool": "delete_file", "args": {"path": "/"}}):
        print(f"   model asked {call['tool']:<12} -> {run_tool_call(call)}")

    assert distilled_ceiling(70) == 70, "a copier cannot beat the thing it copies"
    assert rl_ceiling(70) is None, "RL has no teacher, so no ceiling"
    assert training_stages("RLHF") == 2 and training_stages("DPO") == 1
    assert models_needed("RLHF") == 3 and models_needed("DPO") == 2
    assert run_tool_call({"tool": "calculator", "args": {"expr": "17*23"}}) == 391
    assert "refused" in run_tool_call({"tool": "delete_file", "args": {"path": "/"}})
    print("\nPASS ✅  copying has a ceiling; DPO drops a stage; the model asks, your code decides.")
