# AI edit/refine actions: references (V = fetched this session, M = memory, unverified)

## 1. Per product
- Google Docs Refine (V, support.google.com/docs/answer/13447609): floating bar on selection. Visible: Rephrase, Shorten, "More" -> Elaborate, More formal, More casual, Bulletize, Summarize. 2 up front, 5 in overflow. Result inline as suggested change; checkmark accepts one, Accept all / Reject all. No credit shown (M: quota in plan).
- Notion AI (V, notion.com/help/guides/notion-ai-for-docs): select text -> "Edit with AI" prompt (fix grammar, shorter, tone). Result: accept / discard / try again. (M: menu has Improve writing, Make shorter/longer, Change tone submenu, Fix spelling; result in a floating card under selection.)
- Wordtune (V, third-party reviews only, e.g. contentellect.com/wordtune-review): highlight -> rewrite cards; tone (formal/casual) + length (shorten/expand) as one-click modes. Free-tier rewrite cap shown as counter (M).
- ChatGPT canvas (V attempt: openai.com/index/introducing-canvas 403; M): shortcuts menu bottom-right: Suggest edits, Add final polish, Adjust length (slider), Reading level (slider, kindergarten..graduate), Add emojis. Selection -> inline "Ask ChatGPT". Version arrows top right (< 3/4 >), restore. Sliders = ordered axes, not chips.
- Apple Writing Tools (M): selection popover. Proofread, Rewrite, then segmented tone row Friendly / Professional / Concise; Summary, Key points, List, Table below. Shows result in panel with Replace / Undo-style revert arrow. Free.
- Grammarly (M): right sidebar of suggestion cards, one issue each, Accept / dismiss; Goals (audience, formality, domain) as setup; score ring on top that expands to categories (Correctness, Clarity, Engagement, Delivery). Premium suggestions blurred/locked with small badge.
- Hemingway (V attempt: help page had no detail; M): right sidebar = grade level big number, then colored counts per issue type that match highlight colors in text. No AI cost.
- Word/Copilot (M): floating Copilot icon at selection -> Rewrite, Visualize; Rewrite shows 3 variants with arrows and Replace / Regenerate. Tone dropdown in Copilot Draft.
- Gmail Help me write (M): Refine menu pill under draft: Formalize, Elaborate, Shorten, Recreate. 4 items, in a dropdown. Inline, undo link.
- Canva Magic Write (M): selection toolbar button -> menu list (Rewrite, Shorten, Expand, Fix spelling, tone). Credit use shown in plan/tooltip, not per action.
- Jasper (M): "Command" bar + selection toolbar; actions in dropdown; credits/words hidden in account area.
- Lex (M): slash menu + "+" / Cmd+Enter prompt; suggestions inline with accept/reject.
- Superhuman AI (M): Cmd+J palette, one-line prompt; result inline in compose with Insert / discard.
- GitHub Copilot (M): ghost text inline; Tab accept, Esc reject; zero UI chrome.
- Cursor Cmd+K (M): inline prompt box at selection; result as red/green diff with Accept (Cmd+Enter) / Reject.
- Linear/Raycast (M): Cmd+K palette, fuzzy search, grouped sections with small group labels, shortcut hints right-aligned, ~6-8 rows visible.

## 2. Principles (sources: V = Google doc above; rest M)
- Show 2-3 primary actions, rest behind "More" (Google Docs Refine, V). Progressive disclosure (NN/g, nngroup.com/articles/progressive-disclosure, M).
- Pair opposites as one control: length = shorter/longer, tone = casual/formal -> slider or segmented (canvas, Wordtune, Apple). 7 chips -> 2 controls + 2-3 extras.
- Act on selection or section, not whole doc: preview in place (Cursor diff, Google suggestion marks).
- Preview then accept/reject, with undo as safety net (Google V, Notion V, Cursor M).
- Group labels beat count: Linear/Raycast groups (M).
- Hick's law: fewer simultaneous choices (lawsofux.com/hicks-law, M).
- Disabled before content: hide or replace with a one-line prompt, do not show faded controls (M, common empty-state guidance).
- Cost: show only the exception. Free actions carry no label; paid action carries a small "1 credit" tag on the button (M, Grammarly lock pattern).

## 3. Fit for job description (h2 sections, 7 actions)
Map the 7 actions to axes:
- Length: Shorter | Longer (Shorter, Cut to 6 bullets as extra)
- Tone: Casual | Neutral | Formal (+ More inclusive as its own toggle)
- Wording: Simplify wording
- Structure: Move extras to nice-to-have
Recommend:
- "Adjust" card: two segmented controls (Length 3 steps: Shorter / As is / Longer; Tone 3 steps: Casual / Neutral / Formal). Applies to whole doc. Free: heading says "Free", once.
- Row of 2 text buttons: "More inclusive", "Simplify wording". "More" menu: Cut to 6 bullets, Move extras to nice-to-have.
- Per-section hover toolbar on each h2 (Shorter, Rewrite, more...) for selection editing; 1 credit shown only on custom prompt.
- Result: inline apply + toast "Made shorter. Undo" (6 s), plus existing version bar becomes arrows "< v3 >" only. Diff highlight fades after 2 s.
- Custom prompt: single-line input "Ask for a change..." with send button labeled "1 credit" in small muted text. No explainer paragraph; put help in a tooltip.
- Quality: slim row "Quality 82 / 100 - 3 to fix  v". Expands to findings list, each with "Fix" button, Hemingway-style colored dots matching highlights.
- Before draft: show nothing but a muted line "Edit tools appear once you have a draft." No faded chips.

## 4. Looks generic/AI-made, and the authored alternative
- Wall of identical outlined pills, wrapped over rows -> two segmented controls with labeled axes.
- Explainer paragraph under controls -> tooltip or nothing; label the controls clearly instead.
- Repeated "free" and "1 credit" badges, equal weight -> one "free" note, credit only on the custom prompt button.
- Faded chips pre-draft -> single empty-state line.
- Card within card for custom prompt -> plain input row.
- Emoji / sparkle on every chip -> none; one small icon at most for the custom prompt.
- Authored touches: JD-specific wording ("Cut to 6 bullets", "nice-to-have"), numbers (82/100, 3 to fix), calm neutral palette, one accent color for the primary action.

## 5. Wireframe (320px column; element count = 14 interactive)
```
ADJUST  free
Length  [ Shorter | As is | Longer ]     (3)
Tone    [ Casual | Neutral | Formal ]    (3)
[More inclusive] [Simplify]  [More v]    (3)   More menu: 2 items
------------------------------------
[ Ask for a change...        ] [Send]    (2)
                         1 credit
------------------------------------
Quality 82/100 - 3 to fix            v   (1, expands to list + Fix buttons)
< v3 >  Undo                             (2-3)
```
Mobile full width: same order. Segmented controls full width (min 44px height). Adjust collapses into a bottom sheet opened by a sticky "Edit" button; custom prompt stays as a sticky input above keyboard. Quality row stays slim, expands inline.
Count: visible 11-14 vs current 7 chips + textarea + text (about 10 plus paragraph), but 3 rows -> about 5 rows, clear hierarchy.
