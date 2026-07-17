export interface QuestionResponse {
  question_name: string;
  question_text: string;
  required: boolean;
  answer_type: string;
}

export interface JobInfo {
  company_name: string;
  role_title: string;
  role_summary: string;
  responsibilities: string[];
  requirements: string[];
  company_description: string | null;
  nice_to_haves: string[];
  benefits: string[];
  why_join_us: string;
  equal_opportunity: string;
  tone: string;
  target_length: string;
}

export interface JobDescriptionDraft {
  title: string;
  about_company: string;
  about_role: string;
  responsibilities: string[];
  requirements: string[];
  nice_to_haves: string[];
  benefits: string[];
  why_join_us: string;
  equal_opportunity: string;
}

export interface GenerateRequest {
  job_info: JobInfo;
  skipped_fields: string[];
  provider?: string;
  model?: string;
}

export interface GenerateResponse {
  draft: JobDescriptionDraft;
  markdown: string;
}

export interface RefineRequest extends GenerateRequest {
  current_draft: JobDescriptionDraft;
  user_request: string;
}
