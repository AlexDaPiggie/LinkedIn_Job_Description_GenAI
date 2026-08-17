# LinkedIn Job Description GenAI

End-to-end GenAI application that turns structured intake answers into polished, LinkedIn-ready job descriptions with real-time prompt refinement, multi-provider LLM benchmarking, credit billing, and user authentication.

On a Thursday's evening, Huy and I was fiddling around on LinkedIn, realizing that most Job Description follows a specific structure. We tried generating that on some free subscription AI models and the result was not so good. So that day, `LinkedIn Job Description GenAI` was born, simply because we feel like we could do better.

Special thanks to my friend [Huy Phan, a.k.a. Hertzy](https://hertzy-da-poet.github.io/Hugo-Portfolio), for bringing the web interface into life. Hertzy implemented the entire front end and crafted the visual effects that shape the user experience.

---

## Authors & Acknowledgements

| **Phong Nguyen (Alex)** | **Huy Phan (Hertzy)** |
|:---|:---|
| **AI / LLM Engineering & Full-Stack Architecture** | **Frontend Engineering & Database Architecture** |
| Built backend, state machine, multi-provider LLM client (OpenAI, Hugging Face, OpenRouter), prompt engineering pipeline, evaluation harness, FastAPI backend, Supabase auth/DB, Stripe credit billing, and AI evaluation. | Built responsive SPA frontend using HTML5, CSS3, and Vanilla JavaScript (ES6+), integrated client-side document export (docx.js), and designed core relational database schemas in Supabase. |
| GitHub: [@AlexDaPiggie](https://github.com/AlexDaPiggie)<br>LinkedIn: [Hoai Phong Nguyen](https://www.linkedin.com/in/hoai-phong-nguyen-9367a4384/) | GitHub: [@hertzy-da-poet](https://github.com/hertzy-da-poet)<br>Portfolio: [Huy Phan Portfolio](https://hertzy-da-poet.github.io/Hugo-Portfolio/) |

---

## Key Features

- **Step-by-step questionaires**: User answers questions one by one. Required questions can't be skipped, optional ones can. These answers are then used to generate the draft.
- **Strict JSON format**: Model outputs clean JSON matching Pydantic schema `JobDescriptionDraft`. This is to guarantee the output always follow LinkedIn structures, minimize problems caused by hallucination (broken text, missing section, ...).
- **Markdown Converter**: Turns JSON draft into Markdown with headres and bullet points/paragrah (depending on the question)
- **Interactive edit (Refine feature)**: user can type custom feedback (e.g. "make it sound start-up like, add Docker into requirments, remove the last bulletpoints,..."). Model edits draft without losing existing facts.
- **Preventing Confusion between versions (`draft_outdated`)**: If user changes erlier answers after making a draft, app blocks `refine` feature until user clicks `generate` again. Stop model from mixing old and new info  
- **Production Backend**: FastAPI backend with Supabase login, SlowAPI limit, and Stripe credits system.

---

## Architecture Pipeline
<p align="center">
  <img src="front_end\images\Workflow.drawio.png" alt="LinkedIn Job Description GenAI Architecture Workflow" width="100%"/>
</p>

1. **Intake (JobAgent + SessionState)**: Collets required & optional info.
2. **Draft Generation (build_generation_prompt)**: Prompts LLM to turn short notes into an actual job description.
3. **Parsing & Validation (parse_job_description)**: Cleans markdown, parses JSON, validates against JobDescriptionDraft.
4. **Markdown Rendering (MarkdownRenderer)**: Formats sections into # Title, ## About the Role, ## Responsibilities, ## Requirements, ## Benefits.
5. **Refinement (`build_refinement_prompt`)**: Takes existing JSON draft + user edit request -> Returns updated full JSON draft.
6. **Billing & Auth Check**: Deducts 1 credit in Supabse before running LLM. `Generate` and `Refine` wil be blocked when running out of credits.

---

## Tech Stack

| Layer | Technologies |
|:---|:---|
| **LLM & Prompt Engineering** | OpenAI API (`gpt-4o`, `gpt-4o-mini`), Hugging Face Inference API / Serverless (`Qwen2.5`, `Mistral-7B`, `Phi-3.5`), OpenRouter, Pydantic Schema Validation, Few-Shot Anti-Hallucination Prompting |
| **Backend & APIs** | FastAPI, Uvicorn, Python 3.11, SlowAPI (Rate Limiting) |
| **Database & Auth** | Supabase (PostgreSQL, Row-Level Security, Auth, Google OAuth) |
| **Payments & Credits** | Stripe API, Webhook Verification |
| **Evaluation Suite** | Automated Benchmark Harness (`runner.py`), LLM-as-a-Judge (`metrics.py`), Matplotlib / Jupyter Notebooks |
| **Frontend** | Vanilla JavaScript (SPA), HTML5, CSS3 |

---

## Quickstart (Run Locally)

### Prerequisites
- Python 3.11+
- API Keys: `OPENAI_API_KEY`, `HUGGINGFACE_API_KEY` (optional), `SUPABASE_URL`, `SUPABASE_KEY`, `STRIPE_SECRET_KEY`

### 1. Backend Setup

```bash
# Clone repository
git clone https://github.com/AlexDaPiggie/LinkedIn_Job_Description_GenAI.git
cd LinkedIn_Job_Description_GenAI

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment variables (.env)
# OPENAI_API_KEY=your_openai_key
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_key

# Run FastAPI backend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

- API Base URL: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

Open `front_end/index.html` directly in a browser or serve using Live Server / HTTP server:

```bash
cd front_end
python -m http.server 3000
```

---

## API Reference

### `POST /generate`
Generate a fresh job description draft from `JobInfo`.

**Request Body:**
```json
{
  "company_name": "Xavier AI",
  "role_title": "Senior ML Engineer",
  "location": "San Francisco, CA",
  "work_arrangement": "Hybrid",
  "role_summary": "Lead computer vision and foundation model deployment.",
  "responsibilities": ["Train vision models", "Optimize inference on GPU"],
  "requirements": ["5+ years PyTorch", "Experience with TensorRT"],
  "tone": "technical",
  "target_length": "medium"
}
```

**Response:**
```json
{
  "draft": {
    "title": "Senior ML Engineer - Xavier AI",
    "about_company": "Xavier AI is building cutting-edge agentic workflows...",
    "about_role": "We are seeking a Senior ML Engineer to lead vision model deployment...",
    "responsibilities": [
      "Train vision models and foundation architectures",
      "Optimize low-latency inference on serverless GPUs"
    ],
    "requirements": [
      "5+ years of production experience with PyTorch",
      "Hands-on expertise with TensorRT and ONNX Runtime"
    ],
    "nice_to_have": [],
    "benefits": [],
    "location": "San Francisco, CA (Hybrid)",
    "equal_opportunity": "Xavier AI is an Equal Opportunity Employer."
  },
  "markdown": "# Senior ML Engineer - Xavier AI\n\n## About the Role...",
  "llm_result": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "latency_seconds": 1.28,
    "input_tokens": 620,
    "output_tokens": 480,
    "estimated_cost": 0.00038
  }
}
```

### `POST /refine`
Submit natural language refinement requests on an active draft.

---

## Model Evaluation & Benchmarking

The project features an automated benchmarking suite (`src/evaluation/runner.py`) and evaluation analysis notebook ([Model_Comparison_Analysis.ipynb](file:///C:/Users/alexh/Coding/LinkedIn_Job_Description_GenAI/src/evaluation/Model_Comparison_Analysis.ipynb)) testing models across structured scenarios.

```bash
# Run benchmark across models and scenarios
python -m src.evaluation.runner
```

### 1. Schema Pass Rate & Constraint Adherence

Evaluates whether models strictly adhere to JSON schema, required keywords (`must_include`), and avoid prohibited keywords (`must_not_include`).

<p align="center">
  <img src="front_end/images/eval_failures_pass_rates.png" alt="Failure Types Count by Model and Scenario" width="95%"/>
</p>

* **Top Performers**: `gpt-4o` and `gemini-2.5-flash-lite` passed all test cases with 0 schema or constraint violations.
* **Minor Constraint Violations**: `mistral-small`, `qwen-2.5-72b`, `mixtral-8x22b`, and `command-r` had only 1 `must_not_include` failure.
* **Scenario Difficulty**: Scenarios with minimal inputs (Required Fields only) produced higher failure rates across weaker models compared to rich, complex prompts, showing the importance of input density for maintaining JSON structure.

### 2. Token Usage & Cost Efficiency

Measures the trade-off between input/output token consumption and cost per generation.

<p align="center">
  <img src="front_end/images/eval_cost_and_tokens.png" alt="Estimated Cost vs Token Usage" width="85%"/>
</p>

* **Most Cost-Effective**: `llama-3.3-70b`, `mistral-small`, and `gpt-4o-mini` achieved the lowest cost profile while maintaining concise output length.
* **Token Efficiency**: Models like `gpt-4o-mini` generated structured drafts without token inflation, keeping API latency and expenses minimal.

### 3. Generation Latency

Measures end-to-end response time (seconds) across all test scenarios.

<p align="center">
  <img src="front_end/images/eval_latency_comparison.png" alt="Average Generation Latency per Model" width="85%"/>
</p>

* Fast, lightweight models like `gemini-2.5-flash-lite` and `gpt-4o-mini` delivered sub-2s generation times suitable for interactive applications.
* Larger open-weights models exhibited higher inference latency depending on endpoint hosting infrastructure.

### 4. LLM-as-a-Judge Quality Scores

Scores generated job descriptions on a 1–5 scale across 6 core criteria: **Specificity**, **Tone**, **Faithfulness**, **LinkedIn Readiness**, **Refinement Quality**, and **Overall Quality**.

<p align="center">
  <img src="front_end/images/eval_quality_scores.png" alt="LLM Judge Quality Scores by Dimension" width="95%"/>
</p>

* **Overall Quality**: `gpt-4o` and `gemini-2.5-flash-lite` scored highest across LinkedIn readiness and tone fidelity.
* **Faithfulness & Specificity**: Larger models showed lower hallucination rates, preserving exact intake parameters without inventing false company perks or responsibilities.

## Model Sequencing & Fallback Architecture

Based on benchmark results, the application implements an automated model sequencing and fallback strategy defined in [`src/llm/models.py`](src/llm/models.py) and executed via [`src/llm/client.py`](src/llm/client.py):

* **Primary Model (`google/gemini-2.5-flash-lite`)**:
  * Chosen for its top overall performance: sub-2s generation latency, 100% schema and constraint pass rate, and high LinkedIn readiness scores at low token costs.
* **Fallback Options**:
  1. `openai/gpt-4o`: SOTA reasoning backup if the primary model encounters rate limits or provider downtime.
  2. `openai/gpt-4o-mini`: Cost-efficient structured output backup.
  3. `mistralai/mistral-small-24b-instruct-2501`: High-speed open-weights alternative.
* **When It Is Used**:
  * Executed inside `JobAgent.generate_draft()` and `JobAgent.refine_draft()` in [`src/agent/job_agent.py`](src/agent/job_agent.py).
  * Automatically catches API exceptions, connection timeouts, or provider 5xx errors and seamlessly retries with the next model in the fallback list without user-facing disruption.

---

## Repository Structure

```
LinkedIn_Job_Description_GenAI/
├── docs/                       # Architecture diagrams & documentation
├── eval_results/               # Automated benchmark CSVs & analysis notebooks
├── front_end/                  # Frontend UI (HTML, CSS, JS)
├── src/
│   ├── agent/
│   │   ├── job_agent.py        # Orchestration for generation & refinement
│   │   ├── parser.py           # JSON parsing & validation helpers
│   │   ├── prompts.py          # System & user prompt templates
│   │   ├── questions.py        # Intake questions definition & skip logic
│   │   └── state.py            # SessionState & QuestionAnswer data classes
│   ├── api/
│   │   ├── main.py             # FastAPI entrypoint, auth, stripe & endpoints
│   │   ├── schemas.py          # Request / Response Pydantic models
│   │   └── services.py         # Business logic connectors
│   ├── auth/                   # Supabase authentication & Google OAuth verifier
│   ├── database/               # Supabase PostgreSQL client & credit queries
│   ├── evaluation/
│   │   ├── metrics.py          # Schema validation, cost calculation & judge
│   │   ├── runner.py           # Benchmark test harness
│   │   └── scenarios.py        # Test cases across diverse industry roles
│   ├── llm/
│   │   ├── client.py           # Unified client interface
│   │   ├── models.py           # Supported models configuration
│   │   └── providers.py        # Provider adapters (OpenAI, HF, OpenRouter)
│   ├── rendering/
│   │   └── markdown_renderer.py # JSON-to-Markdown renderer
│   └── schema/
│       ├── job_description.py  # JobDescriptionDraft Pydantic model
│       └── job_info.py         # JobInfo input schema
├── pyproject.toml              # Project metadata
├── requirements.txt            # Python dependencies
└── README.md                   # Project overview
```
