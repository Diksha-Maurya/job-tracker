// src/api.ts
export async function getJobs() {
  const response = await fetch("http://localhost:8000/jobs/");
  return response.json();
}
