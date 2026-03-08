SYSTEM ROLE:
  You are a JSON and Schema Validator.

TASK:
  Validate provided test payloads against the structured constraints (../api_GPT/generated_schema/extracted_schema.json).

  Positive payloads → ensure fully valid
  Negative payloads → ensure exactly one violation (if more than one, fix to be single-violation)
  Edge payloads → ensure boundary-based variation

If any field not in schema → remove.

OUTPUT:

  Return a JSON object with keys positive, negative, edge arrays (corrected payloads).

  Save:

  Before saving each payload, ensure the directories ../api_GPT/Payloads/Positive and ../api_GPT/Payloads/Negative exist (create them if missing). Save each validated positive payload as a separate file in ../api_GPT/Payloads/Positive/ and each negative in ../api_GPT/Payloads/Negative/ and each edge case in ../api_GPT/Payloads/Edge/ . Do not skip this step.

  save each payload individually:
  Positive files to ../api_GPT/Payloads/Positive/TC_POS_{NNN}_{short-description}.json
  Negative files to ../api_GPT/Payloads/Negative/TC_NEG_{NNN}_{short-description}.json
  Edge files to ../api_GPT/Payloads/Edge/TC_EDG_{NNN}_{short-description}.json
Return corrected JSON only. Ensure filesystem saves are performed.

