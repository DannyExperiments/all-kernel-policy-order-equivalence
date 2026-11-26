# Scope and limitations

The theorem compares all stationary randomized policies, including ties, at a fixed discount 0 < γ < 1 with a full-support start distribution. Each transition row can be any point of its closed simplex. The input has finite nonempty state and common action sets.

The main test uses polynomial identities, real factors and relative-interior sign measurements on finitely many faces. It is effective in exact arithmetic for rational or real algebraic inputs. The proof gives no general runtime guarantee, canonical transformation formula for successor-dependent rewards, or claim about a varying discount. Allowing arbitrary trajectory distributions gives a stronger equivalence, discussed in earlier work.

The positive affine companion assumes successor-independent rewards and at least two actions. Its deterministic tests apply under that restriction. A single action gives a single policy, so every reward pair induces the same order. The main counterexamples illustrate why arbitrary successor-dependent rewards need interior kernels and boundary ties.
