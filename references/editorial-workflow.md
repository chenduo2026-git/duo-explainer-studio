# Editorial workflow

## 1. Framework discussion

Start with a compact structure, not a finished script. A useful default for a 1-2 minute knowledge or finance video is:

1. Counterintuitive question or familiar misunderstanding.
2. Concrete analogy that makes the mistake visible.
3. What the idea is not.
4. What the idea is: 3-5 decisive questions or steps.
5. One limitation or error-cost reminder.
6. A closing sentence that reframes the opening.

Keep the framework to the minimum needed for a decision. When several hooks are plausible, show 2-3 alternatives and explain the tradeoff in one line each.

## 2. Spoken-script pass

- Write for the ear: short clauses, explicit subjects, and natural transitions.
- Use one analogy, not a chain of analogies.
- Convert abstract nouns into questions or actions.
- Keep humor observational and restrained. A useful rhythm is `serious premise -> familiar example -> slight twist -> clear conclusion`.
- Preserve factual qualifiers. Do not improve cadence by changing a number, causal claim, or degree of certainty.
- Read the script aloud or estimate at the intended voice speed. For Mandarin, a rough first estimate is 3.5-4.5 Chinese characters per second, but real generated duration is authoritative.

## 3. Storyboard contract

Create a table with these columns:

| ID | Narration | On-screen text | Visual anchor | Emphasis words | Estimated seconds | Status |
|---|---|---|---|---|---:|---|

Rules:

- One row normally becomes one slide and one TTS asset.
- On-screen text is a compression of the narration, not a transcript dump.
- Every row must name a visible anchor that can be verified in a frame.
- The opening and closing may echo conceptually, but title reuse is never automatic.
- Mark rows `locked` only after the user approves both narration and on-screen content.

## 4. Content lock

Before production, present the final script and storyboard together and ask for one explicit lock. The lock covers:

- narration wording and order;
- slide count and on-screen text;
- cover title and closing title independently;
- factual numbers and claims;
- approximate duration and aspect ratio.

After lock, treat changes as revisions:

- Narration wording change -> regenerate that voice segment, captions, duration, and downstream starts.
- Slide-only layout change -> re-record visuals and recheck anchors; keep audio only if timing is unchanged.
- Slide order change -> rebuild the complete timing manifest.
