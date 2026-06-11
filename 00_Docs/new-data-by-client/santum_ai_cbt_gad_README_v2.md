# Santum AI CBT Generalised Anxiety RAG Pack

Generated: 2026-05-31

This is a second-stage RAG conversion of the uploaded CCI generalised anxiety workbook series. It is not a raw PDF extraction. It converts workbook content into retrieval-oriented CBT chunks and separates safety/routing content from normal vector retrieval.

## Files

- `santum_ai_cbt_gad_vector_index_v2.json`: use this for embeddings.
- `santum_ai_cbt_gad_complete_pack_v2.json`: master pack with vector chunks and rule-engine items.
- `santum_ai_cbt_gad_exercise_library_v2.json`: exercise-only subset.
- `santum_ai_cbt_gad_worksheet_library_v2.json`: worksheet instruction subset.
- `santum_ai_cbt_gad_socratic_prompts_v2.json`: dialogue strategy subset.
- `santum_ai_cbt_gad_safety_rules_v2.json`: do not embed; use before retrieval as routing rules.
- `santum_ai_cbt_gad_coverage_matrix_v2.json`: module coverage and chunk IDs.
- `santum_ai_cbt_gad_schema_v2.json`: schema notes.

## Counts

- Vector chunks: 120
- Psychoeducation chunks: 100
- Exercise chunks: 10
- Worksheet chunks: 5
- Socratic prompt chunks: 5
- Safety/rule items: 5

## Implementation

Embed `embedding_text`, store `id` and metadata, and retrieve only chunks where `safety.embed_allowed = true`.
Run crisis/safety rules before normal vector retrieval.
Clinical review is recommended before public release.
