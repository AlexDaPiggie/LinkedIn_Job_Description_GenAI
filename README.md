# [Linked In GenAI(Click to see the Website)](https://linked-in-gen-ai.vercel.app/)

End-to-end GenAI application that turns structured intake answers into polished, LinkedIn-ready job descriptions with real-time prompt refinement, multi-provider LLM benchmarking, credit billing, and user authentication.

On a Thursday's evening, Huy and I was fiddling around on LinkedIn, realizing that most Job Description follows a specific structure. We tried generating that on some free subscription AI models and the result was not so good. So that day, `LinkedIn Job Description GenAI` was born, simply because we feel like we could do better.

Special thanks to my friend [Huy Phan, a.k.a. Hertzy](https://hertzy-da-poet.github.io/Hugo-Portfolio), for bringing the web interface into life. Hertzy implemented the entire front end and crafted the visual effects that shape the user experience.

---

## Authors & Acknowledgements

| **Phong Nguyen (Alex)** | **Huy Phan (Hertzy)** |
|:---|:---|
| **AI Engineering & Database** | **Web Developing & Database** |
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

## Model Evaluation & Benchmarking

The project features an automated benchmarking suite (`src/evaluation/runner.py`) and evaluation analysis notebook ([Model_Comparison_Analysis.ipynb](file:///C:/Users/alexh/Coding/LinkedIn_Job_Description_GenAI/src/evaluation/Model_Comparison_Analysis.ipynb)) testing models across structured scenarios.

```bash
# Run benchmark across models and scenarios
python -m src.evaluation.runner
```

### 1. Token Usage & Cost Efficiency

Measures the trade-off between input/output token consumption and cost per generation.

<p align="center">
  <img src="front_end/images/eval_cost_and_tokens.png" alt="Estimated Cost vs Token Usage" width="85%"/>
</p>

* **Most Cost-Effective**: `llama-3.3-70b`, `mistral-small`, and `gpt-4o-mini` achieved the lowest cost profile while maintaining concise output length.
* **Token Efficiency**: Models like `gpt-4o-mini` generated structured drafts without token inflation, keeping API latency and expenses minimal.

### 2. Generation Latency

Measures end-to-end response time (seconds) across all test scenarios.

<p align="center">
  <img src="front_end/images/eval_latency_comparison.png" alt="Average Generation Latency per Model" width="85%"/>
</p>

* Fast, lightweight models like `gemini-2.5-flash-lite` and `gpt-4o-mini` delivered sub-2s generation times suitable for interactive applications.
* Larger open-weights models exhibited higher inference latency depending on endpoint hosting infrastructure.

## Model Sequencing & Fallback Architecture

Based on benchmark results, the application implements an automated model sequencing and fallback options:

* **Primary Model (`google/gemini-2.5-flash-lite`)**:
  * Chosen for its top overall performance: sub-2s generation latency, 100% schema and constraint pass rate, and high LinkedIn readiness scores at low token costs.
* **Fallback Options**:
  1. `openai/gpt-4o`: SOTA reasoning backup if the primary model encounters rate limits or provider downtime.
  2. `openai/gpt-4o-mini`: Cost-efficient structured output backup.
  3. `mistralai/mistral-small-24b-instruct-2501`: High-speed open-weights alternative.
  
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
