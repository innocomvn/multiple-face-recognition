# Contributing to FRAMS

Thank you for your interest in contributing to the Face Recognition Attendance & Customer Management System (FRAMS)! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git
- Basic understanding of:
  - Flask web framework
  - Face recognition concepts
  - RESTful APIs
  - SQLite databases

### Areas to Contribute

We welcome contributions in these areas:

1. **Bug Fixes** - Fix existing issues
2. **New Features** - Add new functionality
3. **Documentation** - Improve guides and API docs
4. **Tests** - Add or improve test coverage
5. **Performance** - Optimize code and algorithms
6. **UI/UX** - Improve frontend design
7. **Translations** - Add i18n support
8. **Security** - Identify and fix vulnerabilities

---

## Development Setup

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/multiple-face-recognition.git
cd multiple-face-recognition
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/innocomvn/multiple-face-recognition.git
```

### 4. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 6. Create Development Branch

```bash
git checkout -b feature/your-feature-name
```

---

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check the issue tracker to avoid duplicates
- Collect relevant information (error messages, screenshots, logs)
- Try to reproduce the issue on the latest version

**When submitting a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces
- Screenshots (if applicable)

**Bug Report Template:**

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Ubuntu 20.04]
 - Python Version: [e.g., 3.8.5]
 - FRAMS Version: [e.g., 2.0.0]

**Additional Context**
Any other relevant information.
```

### Suggesting Features

**Before submitting a feature request:**
- Check if the feature already exists
- Check if someone else has requested it
- Consider if it aligns with the project's goals

**When submitting a feature request, include:**
- Clear, descriptive title
- Problem the feature would solve
- Proposed solution
- Alternative solutions considered
- Impact on existing functionality

**Feature Request Template:**

```markdown
**Feature Description**
A clear description of the feature.

**Problem It Solves**
Explain the problem this feature would address.

**Proposed Solution**
How you envision this feature working.

**Alternatives Considered**
Other solutions you've thought about.

**Additional Context**
Any other relevant information, mockups, examples.
```

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

**Line Length:**
- Maximum 100 characters (not 79)
- Break long lines logically

**Imports:**
```python
# Standard library
import os
import sys

# Third-party
import flask
import numpy as np

# Local
from frams_client import FRAMSClient
```

**Naming Conventions:**
```python
# Classes: PascalCase
class FaceRecognizer:
    pass

# Functions/variables: snake_case
def recognize_face(image_path):
    employee_name = "John_Doe"
    return employee_name

# Constants: UPPERCASE
MAX_FILE_SIZE = 10485760
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Private: prefix with underscore
def _internal_helper():
    pass
```

**Docstrings:**
```python
def register_employee(name: str, image_path: str) -> dict:
    """
    Register a new employee in the system.

    Args:
        name (str): Employee name (use UPPERCASE with underscores)
        image_path (str): Path to employee face image

    Returns:
        dict: Result dictionary with 'success' and 'message' keys

    Raises:
        ValueError: If name is invalid or image not found
        IOError: If image cannot be processed

    Example:
        >>> result = register_employee("JOHN_DOE", "/path/to/photo.jpg")
        >>> print(result['success'])
        True
    """
    pass
```

**Type Hints:**
```python
from typing import Dict, List, Optional, Union

def get_attendance(
    date: Optional[str] = None,
    employee_name: Optional[str] = None
) -> Dict[str, Union[bool, List[Dict]]]:
    """Type hints improve code clarity"""
    pass
```

### JavaScript Style Guide

**For frontend code:**
- Use ES6+ features
- Use `const` and `let` (no `var`)
- 2 spaces for indentation
- Semicolons required
- Single quotes for strings

```javascript
// Good
const apiUrl = '/api/attendance/recognize';
const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData
    });
    return await response.json();
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

### HTML/CSS

- Use Bootstrap 4 classes when possible
- Indent with 2 spaces
- Use semantic HTML5 elements
- Add ARIA labels for accessibility

---

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::TestHealthEndpoints::test_health_check
```

### Writing Tests

**Test Structure:**
```python
import unittest
from app_improved import app

class TestAttendanceAPI(unittest.TestCase):
    """Test attendance endpoints"""

    def setUp(self):
        """Setup test client before each test"""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_recognize_endpoint(self):
        """Test /api/attendance/recognize endpoint"""
        # Arrange
        with open('tests/fixtures/test_face.jpg', 'rb') as f:
            data = {'image': f}

            # Act
            response = self.client.post('/api/attendance/recognize', data=data)

            # Assert
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertTrue(result['success'])
            self.assertIn('faces_found', result)

    def tearDown(self):
        """Cleanup after each test"""
        pass
```

**Test Coverage Requirements:**
- New features must include tests
- Aim for 80%+ code coverage
- Test happy paths and error cases
- Include edge cases

**Test Fixtures:**
- Place test images in `tests/fixtures/`
- Use small file sizes
- Include valid and invalid test cases

---

## Pull Request Process

### 1. Update Your Fork

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch Naming:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent fixes
- `docs/` - Documentation only
- `refactor/` - Code refactoring
- `test/` - Adding tests

Examples:
- `feature/websocket-support`
- `bugfix/fix-customer-recognition`
- `docs/update-api-guide`

### 3. Make Your Changes

```bash
# Edit files
git add .
git commit -m "Clear, descriptive commit message"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding/updating tests
- `chore:` - Maintenance tasks

**Examples:**
```
feat: Add WebSocket support for real-time updates

- Implemented Flask-SocketIO integration
- Added real-time attendance notifications
- Updated frontend to connect to WebSocket
- Added documentation for WebSocket usage

Closes #123
```

```
fix: Correct face encoding threshold calculation

The threshold was too strict causing false negatives.
Changed from 0.4 to 0.5 based on testing.

Fixes #456
```

### 4. Run Tests and Linting

```bash
# Run tests
pytest tests/

# Check code style
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Format code
black . --check

# Security scan
bandit -r . -ll
```

### 5. Push Changes

```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request

**Go to GitHub and create a PR with:**

**Title:** Clear, descriptive summary

**Description:**
```markdown
## Description
Brief description of changes.

## Motivation
Why is this change needed?

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions found

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
- [ ] No new warnings

## Related Issues
Closes #123
Fixes #456
```

### 7. Code Review Process

**What to Expect:**
- Maintainers will review within 3-5 days
- Be open to feedback and suggestions
- Make requested changes promptly
- Keep discussions professional and constructive

**Addressing Feedback:**
```bash
# Make changes
git add .
git commit -m "Address review feedback"
git push origin feature/your-feature-name
```

### 8. Merging

Once approved:
- Maintainer will merge your PR
- Your branch will be deleted
- Update your fork's main branch

---

## Issue Guidelines

### Good Issue Titles

**Bad:**
- "Bug"
- "Feature request"
- "Help needed"

**Good:**
- "Face recognition fails with PNG images"
- "Add support for PostgreSQL database"
- "API returns 500 error when uploading large images"

### Labeling

We use these labels:

- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested
- `wontfix` - This will not be worked on
- `duplicate` - Duplicate issue
- `invalid` - Invalid issue

---

## Documentation

### What Needs Documentation

- **Code changes** - Update relevant markdown files
- **New features** - Add to API_DOCUMENTATION.md
- **API changes** - Update openapi.yaml
- **Configuration** - Update .env.example
- **Breaking changes** - Add to CHANGELOG.md

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep README.md up to date
- Use proper markdown formatting

### Example Documentation

```markdown
## New Feature: Customer Loyalty Program

### Overview
Track customer visits and assign loyalty points.

### Usage

**API Endpoint:**
\`\`\`
POST /api/customers/{customer_id}/add-points
\`\`\`

**Request:**
\`\`\`json
{
  "points": 10,
  "reason": "Purchase"
}
\`\`\`

**Response:**
\`\`\`json
{
  "success": true,
  "total_points": 150,
  "tier": "Gold"
}
\`\`\`

**Python Example:**
\`\`\`python
client = FRAMSClient()
result = client.add_loyalty_points(customer_id=1, points=10)
print(result['total_points'])
\`\`\`

### Configuration

Add to `.env`:
\`\`\`
LOYALTY_ENABLED=true
POINTS_PER_VISIT=10
\`\`\`
```

---

## Community

### Communication Channels

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and community support
- **Pull Requests** - Code contributions and reviews

### Getting Help

**Before asking for help:**
1. Read the documentation (README.md, SETUP_GUIDE.md)
2. Search existing issues
3. Try the troubleshooting guide
4. Review the FAQ

**When asking for help:**
- Be specific about your problem
- Include error messages
- Show what you've tried
- Provide relevant context

### Recognition

Contributors will be:
- Added to CONTRIBUTORS.md (coming soon)
- Mentioned in release notes
- Recognized in the community

---

## Development Tips

### Useful Commands

```bash
# Install in development mode
pip install -e .

# Run app in debug mode
export FLASK_ENV=development
python app_improved.py

# Generate requirements.txt
pip freeze > requirements.txt

# Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Run security scan
bandit -r . -ll -f json -o security-report.json
```

### Debugging

**Enable debug logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Use Flask debug mode:**
```python
app.run(debug=True)
```

**Print debugging:**
```python
print(f"DEBUG: Variable value = {variable}")
app.logger.debug(f"Processing image: {filename}")
```

### Common Pitfalls

1. **Forgetting to activate venv**
   ```bash
   source venv/bin/activate  # Always activate first
   ```

2. **Not updating requirements.txt**
   ```bash
   pip freeze > requirements.txt  # After installing packages
   ```

3. **Hardcoded paths**
   ```python
   # Bad
   path = 'C:\\Users\\john\\images'

   # Good
   path = os.path.join(os.getcwd(), 'images')
   ```

4. **Not handling errors**
   ```python
   # Bad
   image = face_recognition.load_image_file(path)

   # Good
   try:
       image = face_recognition.load_image_file(path)
   except Exception as e:
       app.logger.error(f"Failed to load image: {e}")
       return None
   ```

---

## Release Process

(For maintainers)

### Version Numbering

We use Semantic Versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 2.0.0)
- MAJOR - Breaking changes
- MINOR - New features (backward compatible)
- PATCH - Bug fixes

### Creating a Release

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create git tag
4. Push tag to GitHub
5. Create GitHub release
6. Build and push Docker image

---

## License

By contributing to FRAMS, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

- Check the [FAQ](README.md#faq)
- Open a [GitHub Discussion](https://github.com/innocomvn/multiple-face-recognition/discussions)
- Review existing [Issues](https://github.com/innocomvn/multiple-face-recognition/issues)

---

**Thank you for contributing to FRAMS!**

Your contributions make this project better for everyone.
