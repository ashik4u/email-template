# Instructions for Email Template Project

## Project Overview
This is a Flask-based web application for generating and managing business email templates (cab requests, hotel reservations, air ticket requests, etc.). The app is designed for rapid, form-driven email creation with copy-to-clipboard functionality and a dashboard for navigation.

## Architecture & Data Flow
- **app.py**: Main Flask backend. Handles all routes, form processing, and template rendering. Reads dynamic data (names, guests) from text files.
- **templates/**: Contains all Jinja2 HTML templates for forms and email outputs. Each template is self-contained and styled for professional output.
- **employee.txt, guests.txt**: Source files for dynamic dropdowns (names, guest details). `guests.txt` uses a pipe-delimited format: `id|Name|Email|Mobile|ProjectCode|Instructions`.

## Key Workflows
- **Start the app**: `python app.py` (ensure Flask is installed)
- **Access dashboard**: Homepage `/` lists all available templates and forms
- **Add new guest**: Edit `guests.txt` (no code change needed)
- **Generate email**: Fill out a form, submit, and use the copy-to-clipboard button

## Patterns & Conventions
- **Forms**: Each form template (e.g., `hotel_form.html`, `form.html`) includes a "Back to Dashboard" button and is styled for compact, two-column layout.
- **Email Templates**: All email templates include a copy-to-clipboard button and notification bar. Output is formatted for easy pasting into Outlook/OWA.
- **Dynamic Data**: Dropdowns for names/guests are populated from text files, not hardcoded.
- **Guest-Specific Logic**: For air ticket requests, the output email adapts based on guest selection using data from `guests.txt`.
- **Navigation**: All forms and templates link back to the dashboard (homepage `/`).

## Extending the Project
- **Add new template**: Create a new HTML file in `templates/`, add a route in `app.py`, and link it from `dashboard.html`.
- **Add new guest**: Append to `guests.txt` using the established format.
- **Add new name**: Edit `employee.txt`.

## Example: Adding a Guest
```
olivia|Olivia Carter|olivia.carter@example.com|+919830014397|4980104|front-aisle seats (free options only), 6E Curated Snacks Bag
```

## External Dependencies
- **Flask**: Only external Python dependency required. Install with `pip install flask`.
- **No database**: All data is file-based for simplicity and portability.

## Testing & Debugging
- No automated tests; validate by running `python app.py` and using the forms in the browser.
- If dropdowns do not update, check the format of `employee.txt` and `guests.txt`.

## Key Files
- `app.py`: Main backend logic and routing
- `templates/dashboard.html`: Navigation hub
- `templates/*_form.html`: Form templates
- `templates/*_email_template.html`: Email output templates
- `employee.txt`, `guests.txt`: Data sources for dropdowns

---

For questions or unclear conventions, review `app.py` and the relevant template. Ask the user for clarification if a workflow or pattern is ambiguous.
