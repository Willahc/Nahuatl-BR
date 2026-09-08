"""Gate 5 canonical ingestion pipeline (read-only by default).

The pipeline resolves Sources, enforces the Rights and Variety gates, captures
SOURCE_FORM immutably, derives controlled orthographic layers under an approved
policy, builds DRAFT Claim/Evidence/Attestation candidates with origin PIPELINE,
and is deterministic over (input, policy versions, source registry). It never
writes to data/pilot/ or to any canonical store; every run is a dry run unless
a future writer is explicitly added and approved.
"""