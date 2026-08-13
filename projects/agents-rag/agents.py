"""Agents & retrieval (FaizOS build) — Module 17.

  1. RAG       - vector search finds MEANING, keyword search finds EXACT strings. Run both (hybrid),
                 retrieve many cheap candidates, then RERANK to a few good ones. Recall, then precision.
  2. MEMORY    - the context window is big but finite and it resets. Keep facts in a persistent store
                 outside it and retrieve only what is relevant this turn.
  3. AGENTIC RL- an agent takes many steps and gets ONE reward at the end. Credit the whole trajectory.
  4. EVALS     - agents are stochastic. pass@1 measures RELIABILITY, pass@k measures CAPABILITY.

Fill the THREE blanks, then run:  python3 agents.py
"""

# --- 1. retrieval: does the right chunk actually reach the model? ----------

def survives_to_context(chunk_rank, n_kept):
    """The model only sees the top `n_kept` chunks. Did the right one make the cut?"""
    # It survives when its rank is within the number kept (rank 1 is the best).
    return chunk_rank <= n_kept             # rank 1 is best; it survives if within what is kept


def hybrid_hits(vector_hits, keyword_hits):
    """Hybrid retrieval keeps everything either search found — meaning OR exact match."""
    return sorted(set(vector_hits) | set(keyword_hits))   # `|` merges two sets, dropping duplicates


# --- 2. memory: retrieve, do not load ------------------------------------

def fits_in_context(store_tokens, context_tokens):
    return store_tokens <= context_tokens


def retrieved_tokens(n_items, tokens_each):
    return n_items * tokens_each


# --- 3. agentic RL: one reward, many steps -------------------------------

def trajectory_advantage(reward, group_mean):
    """The whole trajectory is judged against how the group of attempts did (same rule as GRPO)."""
    # Above the group average must come out positive.
    return reward - group_mean              # how much better than the group (a size, not a yes/no)


def credit_per_step(advantage, n_steps):
    """Blunt but effective: every step in the trajectory receives the same advantage."""
    return [advantage] * n_steps


# --- 4. evals: capability vs reliability ---------------------------------

def reliability_gap(pass_at_1, pass_at_k):
    """How much better the model does when allowed several attempts."""
    # A big gap means it CAN do the task but does not do it consistently.
    return pass_at_k - pass_at_1            # bigger minus smaller, so the gap is positive


def diagnosis(pass_at_1, pass_at_k):
    return "reliability" if reliability_gap(pass_at_1, pass_at_k) > 0.2 else "capability"


if __name__ == "__main__":
    print("1. RETRIEVAL")
    print(f"   right chunk at rank 37, top-5 kept  -> reaches model? {survives_to_context(37, 5)}")
    print(f"   after reranking it sits at rank 2   -> reaches model? {survives_to_context(2, 5)}")
    print(f"   hybrid of vector {['a','b']} + keyword {['b','XR-4471B']} -> "
          f"{hybrid_hits(['a','b'], ['b','XR-4471B'])}")

    print("\n2. MEMORY")
    print(f"   10M-token history in a 200k window? {fits_in_context(10_000_000, 200_000)}")
    print(f"   retrieve 20 items x 500 tokens     = {retrieved_tokens(20, 500):,} tokens (fits)")

    print("\n3. AGENTIC RL")
    adv = trajectory_advantage(reward=1.0, group_mean=0.4)
    print(f"   trajectory scored 1.0, group mean 0.4 -> advantage {adv:+.1f}")
    print(f"   applied to all 10 steps: {credit_per_step(adv, 10)}")

    print("\n4. EVALS")
    for p1, pk in ((0.40, 0.75), (0.35, 0.38)):
        print(f"   pass@1 {p1:.0%}, pass@8 {pk:.0%} -> gap {reliability_gap(p1, pk):.0%} "
              f"-> a {diagnosis(p1, pk)} problem")

    assert survives_to_context(37, 5) is False, "rank 37 never reaches a top-5 context"
    assert survives_to_context(2, 5) is True, "reranking is what saves it"
    assert hybrid_hits(['a','b'], ['b','XR-4471B']) == ['XR-4471B', 'a', 'b'], "union, no duplicates"
    assert fits_in_context(10_000_000, 200_000) is False
    assert abs(trajectory_advantage(1.0, 0.4) - 0.6) < 1e-9, "1.0 - 0.4 = +0.6"
    assert credit_per_step(0.6, 10) == [0.6] * 10, "every step gets the same credit"
    assert abs(reliability_gap(0.40, 0.75) - 0.35) < 1e-9
    assert diagnosis(0.40, 0.75) == "reliability" and diagnosis(0.35, 0.38) == "capability"
    print("\nPASS ✅  retrieve then rerank; store then retrieve; credit the trajectory; measure twice.")
