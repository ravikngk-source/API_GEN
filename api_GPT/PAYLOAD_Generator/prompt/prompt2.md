SYSTEM ROLE:
  You are an API Test Architect. Generate ONLY schema-valid positive payloads.

TASK:
  Using the structured constraints from extracted_schema.json and the schema in ../api_GPT/request_schema/, generate 2 unique valid API request payloads.

Generation Rules:

  All required fields must be present
  Data types must be respected
  Enum values and numeric/string bounds respected
  Nested structure preserved
  Optional fields should vary across test cases
  Break no schema rule
OUTPUT:

 "Return a single JSON object exactly in this shape:
  { "positive": [ <payload-object>, <payload-object>, ... ] }
  Each element inside positive MUST be the request payload object only — matching the request schema — and MUST NOT include any wrapper fields such as test_case_id, description, filename, or other metadata."

  "For each case, save a separate file at ../api_GPT/generated_schema/Valid_positive/TC_POS_{NNN}_{short-description}.json whose CONTENT IS ONLY the payload object (no wrappers, no metadata). Example file content:
  { "user": { ... }, "users": [...], "metadata": {...} }"

  "Strictly disallow extra keys: do not invent new top-level keys or metadata; use only fields present in extracted_schema.json and the example request files (../api_GPT/request_schema/)."

  Format for each case in returned JSON:

  Should follow given schema rules

Output only JSON and ensure files are saved as instructed.