EVALUATION_SCENARIOS = [
    {
        "id": "scenario_only_required_fields",
        "category": "required_only",
        "job_info": {
            "company_name": "TechStart Inc",
            "role_title": "Software Engineer",
            "role_summary": "Develop and maintain core application features.",
            "responsibilities": ["Write code", "Review pull requests", "Fix bugs"],
            "requirements": ["3+ years Python experience", "Bachelor's degree in CS"],
            "tone": "professional",
            "target_length": "medium"
        },
        "refinement_request": "Make it sound exciting for a startup environment.",
        "expected_checks": {
            "must_include": ["TechStart", "Python", "code"],
            "must_not_include": ["401k", "dental", "equal opportunity employer"]
        },
    },
    {
        "id": "scenario_all_fields",
        "category": "all_fields",
        "job_info": {
            "company_name": "GlobalFin",
            "role_title": "Senior Data Scientist",
            "company_description": "GlobalFin is a leading multinational financial services corporation dedicated to transforming banking through AI.",
            "role_summary": "Lead the development of predictive models for fraud detection.",
            "responsibilities": ["Design machine learning models", "Collaborate with data engineering", "Present findings to stakeholders"],
            "requirements": ["Ph.D. in Computer Science or related field", "5+ years applied ML experience", "Expertise in PyTorch"],
            "nice_to_haves": ["Experience in the financial sector", "Knowledge of graph neural networks"],
            "benefits": ["Comprehensive health coverage", "Unlimited PTO", "Annual bonus"],
            "why_join_us": "We offer a unique opportunity to work on massive datasets that impact millions of users globally.",
            "equal_opportunity": "GlobalFin is proud to be an Equal Employment Opportunity and Affirmative Action employer.",
            "tone": "corporate and authoritative",
            "target_length": "long"
        },
        "refinement_request": "Ensure the tone reflects a large, prestigious financial institution.",
        "expected_checks": {
            "must_include": ["GlobalFin", "fraud", "PyTorch", "health coverage", "Equal Employment Opportunity"],
            "must_not_include": ["startup", "scrappy"]
        },
    },
    {
        "id": "scenario_various_fields_sparse",
        "category": "various_fields",
        "job_info": {
            "role_title": "Content Marketing Specialist",
            "responsibilities": ["Write blog posts", "Manage social media calendar"],
            "benefits": ["Remote work stipend"],
            "why_join_us": "Join a creative team that values outside-the-box thinking.",
            "tone": "creative and quirky",
            "target_length": "short"
        },
        "refinement_request": "Keep it very brief but highly engaging.",
        "expected_checks": {
            "must_include": ["blog posts", "creative", "stipend"],
            "must_not_include": ["Python", "years of experience", "TechStart"]
        },
    },
    {
        "id": "scenario_complex_edge_case",
        "category": "complex_edge_case",
        "job_info": {
            "company_name": "HealthTech Solutions",
            "role_title": "DevOps Engineer",
            "role_summary": "Streamline our deployment pipelines for HIPAA-compliant infrastructure.",
            "requirements": ["AWS Certified Solutions Architect", "Kubernetes administration", "Terraform"],
            "nice_to_haves": ["Experience with healthcare data"],
            "tone": "direct and technical",
            "target_length": "medium"
        },
        "refinement_request": "Focus heavily on the infrastructure as code and security aspects without mentioning specific benefits.",
        "expected_checks": {
            "must_include": ["HIPAA", "Kubernetes", "Terraform"],
            "must_not_include": ["health insurance", "PTO", "vacation"]
        },
    }
]