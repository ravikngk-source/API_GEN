SYSTEM ROLE: You are an API test generator. You will receive an API schema in JSON format and connect to a database.

INPUT: ../api_GPT/Get_Prompt/generated_schema/extracted_schema.json
DB: Connect to PostgreSQL table `api_fields` and extract all mandatory fields (is_mandatory = TRUE).

TASK: Generate API endpoints for testing.

1- Positive Cases
    Valid endpoints using mandatory fields from DB.
2- Negative Cases
    Endpoints with invalid/missing mandatory field values.
3- Edge Cases
    Boundary values for mandatory fields.

RULES:
1- Extract mandatory fields from DB before generation.
2- Do not introduce parameters not defined in schema or DB.
3- Maintain correct base URL.
4- Generate at least: 5 positive, 3 negative, 5 edge case endpoints.
5- Save results into:
   ../api_GPT/Get_Prompt/generated_output/positive_requests.txt
   ../api_GPT/Get_Prompt/generated_output/negative_requests.txt
   ../api_GPT/Get_Prompt/generated_output/edge_case_requests.txt


======================================================================================================================

Add DB Connection Layer

Specify the database type (PostgreSQL, MySQL, MongoDB, etc.).

Include connection details (host, port, credentials, schema/table).

Example snippet:

python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="api_metadata",
    user="tester",
    password="secret"
)
cursor = conn.cursor()
cursor.execute("SELECT field_name FROM api_fields WHERE is_mandatory = TRUE;")
mandatory_fields = [row[0] for row in cursor.fetchall()]
Modify Prompt Rules

Instead of “Follow the schema exactly,” update to:

“Extract mandatory fields from DB table api_fields.”

“Use these fields to generate positive, negative, and edge case endpoints.”

This ensures the generator dynamically adapts to DB changes.

Dynamic Endpoint Construction

Use the mandatory fields list from DB to build URLs.

Example:

python
base_url = "https://api.restful-api.dev/collections"
for field in mandatory_fields:
    endpoints.append(f"{base_url}/objects?{field}=validValue")
Update Output Rules

Keep the same file outputs (positive_requests.txt, etc.).

But clarify: “Mandatory fields must be fetched from DB before endpoint generation.”
