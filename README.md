# LinkedIn Job Description Generator 
See the detailed idea for the architecture of the project in structure/architecture.md

Purpose of folders:

agent: implement agent behaviors, fix intake question list and skip rules, build prompts for generating & refining output, parse JSON text, orchestrate generation and refinement

schema: Init data model and answer parsing helpers functions.

rendering: render model into .md structure

llm: call provider models, extract the model's performance for evaluation

evaluation: test model's performance on different scenarios, comparing latency - cost - specificity - completeness

NOTE:
switch to a faster model for refining
backend response is not matching with front-end

experiment on more models - priotize speed for refinement tasks
