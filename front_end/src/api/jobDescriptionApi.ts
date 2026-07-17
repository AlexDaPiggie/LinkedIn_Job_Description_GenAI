import { apiFetch } from "./client";
import type {
  GenerateRequest,
  GenerateResponse,
  QuestionResponse,
  RefineRequest,
} from "../types/api";

export function getQuestions(): Promise<QuestionResponse[]> {
  return apiFetch<QuestionResponse[]>("/questions");
}

export function generateJobDescription(request: GenerateRequest): Promise<GenerateResponse> {
  return apiFetch<GenerateResponse>("/generate", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export function refineJobDescription(request: RefineRequest): Promise<GenerateResponse> {
  return apiFetch<GenerateResponse>("/refine", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
