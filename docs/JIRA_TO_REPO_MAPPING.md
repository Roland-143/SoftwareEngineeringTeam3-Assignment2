# Jira to Repository Mapping

Use this file to connect Jira work with repo areas.

## Team Ownership Map

### DevOps / PM
Likely files:
- `README.md`
- `docs/*`
- `.github/*`
- `docker-compose.yml`
- `Makefile`
- `scripts/*`

### Database Team
Likely files:
- `database/`
- schema notes
- seed data examples
- data validation notes
- docs touching data assumptions

### Backend Team
Likely files:
- `backend/`
- API notes
- server setup
- DB integration layer
- validation and error handling docs

### Frontend Team
Likely files:
- `frontend/`
- UI structure
- API integration points
- user input/output behavior docs

### QA Team
Likely files:
- test plans
- test cases
- bug logs
- verification notes
- docs that capture acceptance checks

## Current Epic Alignment

- PM / DevOps epic -> repo structure, docs, handoff, Docker placeholders
- Database epic -> schema, SQL, validation rules
- Backend epic -> API and business logic
- Frontend epic -> form, table, average display, UI polish
- QA epic -> test plan, validation testing, business output checks
- Documentation epic -> report and presentation support materials

## Rule

If a Jira task changes repo structure or team workflow, DevOps / PM must be informed and the docs must be updated in the same PR.
