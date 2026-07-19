# Contributing to Glasgow Roofmasters Website

## Development Setup

```bash
# Clone the repo
git clone https://github.com/your-org/glasgow-roofmasters.git
cd glasgow-roofmasters

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env .env.local
# Edit .env.local with your settings

# Run development server
python run.py
```

## Branch Strategy

- `main` — Production branch, auto-deploys to Render
- `develop` — Integration branch
- `feature/*` — Feature branches
- `hotfix/*` — Emergency fixes

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes with clear commit messages
3. Ensure tests pass: `pytest`
4. Update documentation if needed
5. Open PR to `develop` (or `main` for hotfixes)
6. Require 1 review before merge

## Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example: `feat(contact): add honeypot field to reduce spam`
