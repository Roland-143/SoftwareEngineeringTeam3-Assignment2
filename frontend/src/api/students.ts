import type {
  CourseAveragesResponse,
  CreateStudentPayload,
  DeleteEnrollmentResponse,
  Student,
} from "../types/Student";

const DEFAULT_API_BASE_URL = "http://localhost:5000";
const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim() ||
  DEFAULT_API_BASE_URL;

type ApiErrorPayload = {
  error?: string;
  details?: string[];
};

function buildApiUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}

function getApiErrorMessage(payload: unknown, fallback: string): string {
  if (!payload || typeof payload !== "object") {
    return fallback;
  }

  const maybeError = payload as ApiErrorPayload;
  const details = Array.isArray(maybeError.details)
    ? maybeError.details.filter(
        (detail): detail is string =>
          typeof detail === "string" && detail.trim().length > 0,
      )
    : [];

  if (details.length > 0) {
    if (typeof maybeError.error === "string" && maybeError.error.trim().length > 0) {
      return `${maybeError.error} ${details.join(" ")}`;
    }
    return details.join(" ");
  }

  if (typeof maybeError.error === "string" && maybeError.error.trim().length > 0) {
    return maybeError.error;
  }

  return fallback;
}

async function parseJsonResponse(response: Response): Promise<unknown | null> {
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return null;
  }

  try {
    return await response.json();
  } catch {
    return null;
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(buildApiUrl(path), init);
  } catch {
    throw new Error(`Could not connect to backend API at ${API_BASE_URL}.`);
  }

  const payload = await parseJsonResponse(response);

  if (!response.ok) {
    throw new Error(
      getApiErrorMessage(
        payload,
        `Request failed with status ${response.status}.`,
      ),
    );
  }

  return payload as T;
}

export function fetchStudents(): Promise<Student[]> {
  return requestJson<Student[]>("/api/students");
}

export function fetchCourseAverages(): Promise<CourseAveragesResponse> {
  return requestJson<CourseAveragesResponse>("/api/students/average");
}

export function createStudent(payload: CreateStudentPayload): Promise<Student> {
  return requestJson<Student>("/api/students", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function deleteStudentEnrollment(
  studentId: number,
  courseId: number,
): Promise<DeleteEnrollmentResponse> {
  return requestJson<DeleteEnrollmentResponse>(
    `/api/students/${studentId}/enrollments/${courseId}`,
    {
      method: "DELETE",
    },
  );
}
