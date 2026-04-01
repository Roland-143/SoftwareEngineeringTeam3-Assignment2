# Project Scope

## Assignment-grounded Summary

Build a small website that allows users to enter student information and course scores, store that data in MySQL, and display the saved records in ascending order plus the average score for 20 students. Development should use Ubuntu, Docker, GitHub, and stable software versions. The deliverables also include collaboration evidence, a report, and a presentation.

## In Scope

- Basic frontend form for student data entry
- Backend endpoints or equivalent server-side logic
- MySQL schema and sample SQL
- Docker-based local development setup
- GitHub collaboration workflow
- QA test plan and validation checks
- Documentation, report support, and presentation support

## Out of Scope

- Authentication or account systems
- Role-based access control
- Full LMS features
- Course enrollment systems
- Messaging, grades history, analytics dashboards, or notifications
- Fancy UI work that slows the project down
- Any technology choice that creates extra setup burden without helping the assignment

## Core Data Model

Minimum data required:
- first_name
- middle_name
- last_name
- student_id
- course_score

## Core Outputs

- Display student records in ascending order
- Display average score for the input students

## Default Technical Assumptions

- Sort by `student_id ASC`
- Middle name optional
- Database is MySQL
- Docker is used for local setup and demonstration
- Ubuntu is the main development environment
- Stable versions only

## Epic-to-Scope Alignment

### DevOps / PM
Owns repo structure, Docker bootstrap, workflow docs, handoff process, and delivery tracking.

### Database team
Owns schema proposal, SQL examples, seed data examples, and data validation rules.

### Backend team
Owns server project structure, API contract, database integration plan, validation, and error handling.

### Frontend team
Owns UI structure, forms, results table, average display, and user-facing validation behavior.

### QA team
Owns test plan, acceptance criteria verification, integration checks, and bug reproduction notes.

## Scope Control Rules

1. Do not add features unless they directly support a Jira issue.
2. Do not change stack decisions without documenting them.
3. Do not rename core folders casually.
4. Do not implement "nice to have" work before the required flow is functional.
5. If a decision could affect another team, document it the same day.
6. Suggest UI fixes and optimization only after required features are implemented.
