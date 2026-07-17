import {
  generateJobDescription,
  getQuestions,
  refineJobDescription,
} from "./jobDescriptionApi";
import { apiFetch } from "./client";
import type { GenerateRequest, GenerateResponse, RefineRequest } from "../types/api";

const response: GenerateResponse = {
  draft: {
    title: "AI Engineer",
    about_company: "About the company.",
    about_role: "About the role.",
    responsibilities: ["Build reliable systems."],
    requirements: ["Python experience."],
    nice_to_haves: [],
    benefits: [],
    why_join_us: "Meaningful work.",
    equal_opportunity: "We are an equal opportunity employer.",
  },
  markdown: "# AI Engineer",
};

beforeEach(() => {
  vi.restoreAllMocks();
});

it("loads questions with GET", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(
      JSON.stringify([
        {
          question_name: "company_name",
          question_text: "What is your company name?",
          required: true,
          answer_type: "text",
        },
      ]),
      { status: 200, headers: { "Content-Type": "application/json" } },
    ),
  );

  await expect(getQuestions()).resolves.toHaveLength(1);
  expect(fetchMock).toHaveBeenCalledWith(expect.stringMatching(/\/questions$/), expect.any(Object));
  const headers = new Headers(fetchMock.mock.calls[0][1]?.headers);
  expect(headers.get("Accept")).toBe("application/json");
  expect(headers.has("Content-Type")).toBe(false);
});

it("preserves custom values supplied through a Headers instance", async () => {
  const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    }),
  );
  const headers = new Headers({
    Accept: "application/vnd.linkedin-job+json",
    "Content-Type": "application/merge-patch+json",
    "X-Request-Id": "request-123",
  });

  await apiFetch<{ ok: boolean }>("/custom", {
    method: "POST",
    body: JSON.stringify({ title: "Engineer" }),
    headers,
  });

  const sentHeaders = new Headers(fetchMock.mock.calls[0][1]?.headers);
  expect(sentHeaders.get("Accept")).toBe("application/vnd.linkedin-job+json");
  expect(sentHeaders.get("Content-Type")).toBe("application/merge-patch+json");
  expect(sentHeaders.get("X-Request-Id")).toBe("request-123");
});

it("posts generation and refinement requests", async () => {
  const fetchMock = vi
    .spyOn(globalThis, "fetch")
    .mockImplementation(() => Promise.resolve(
      new Response(JSON.stringify(response), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    ));
  const generateRequest: GenerateRequest = {
    job_info: {
      company_name: "Alex AI",
      role_title: "AI Engineer",
      role_summary: "Build hiring tools.",
      responsibilities: ["Build reliable systems."],
      requirements: ["Python experience."],
      company_description: null,
      nice_to_haves: [],
      benefits: [],
      why_join_us: "",
      equal_opportunity: "",
      tone: "professional",
      target_length: "medium",
    },
    skipped_fields: ["company_description"],
  };
  const refineRequest: RefineRequest = {
    ...generateRequest,
    current_draft: response.draft,
    user_request: "Make the tone warmer.",
  };

  await generateJobDescription(generateRequest);
  await refineJobDescription(refineRequest);

  expect(fetchMock).toHaveBeenNthCalledWith(
    1,
    expect.stringMatching(/\/generate$/),
    expect.objectContaining({ method: "POST", body: JSON.stringify(generateRequest) }),
  );
  expect(fetchMock).toHaveBeenNthCalledWith(
    2,
    expect.stringMatching(/\/refine$/),
    expect.objectContaining({ method: "POST", body: JSON.stringify(refineRequest) }),
  );
  for (const [, init] of fetchMock.mock.calls) {
    const headers = new Headers(init?.headers);
    expect(headers.get("Accept")).toBe("application/json");
    expect(headers.get("Content-Type")).toBe("application/json");
  }
});

it("surfaces the FastAPI detail message", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify({ detail: "Required answers are missing" }), {
      status: 422,
      headers: { "Content-Type": "application/json" },
    }),
  );

  await expect(getQuestions()).rejects.toThrow("Required answers are missing");
});
