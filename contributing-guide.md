# Contributing to SportAI Suite

First off, thank you for considering contributing to SportAI Suite! 🎉

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Show empathy towards other community members

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**To submit a bug report:**
1. Use the issue template
2. Include detailed steps to reproduce
3. Include system information
4. Add screenshots if applicable
5. Describe expected vs actual behavior

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**To suggest an enhancement:**
1. Use a clear and descriptive title
2. Provide a detailed description of the proposed functionality
3. Explain why this enhancement would be useful
4. List any alternative solutions you've considered

### 🔧 Pull Requests

1. **Fork the repository** and create your branch from `develop`
2. **Write clear commit messages** following conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions or changes
   - `chore:` Build process or auxiliary tool changes

3. **Follow the coding standards:**
   ```python
   # Good
   def calculate_facility_usage(facility_id: str, date: datetime) -> float:
       """Calculate facility usage percentage for a given date."""
       pass
   
   # Bad
   def calc(f, d):
       pass
   ```

4. **Write tests** for your changes:
   ```python
   def test_calculate_facility_usage():
       result = calculate_facility_usage("facility-1", datetime.now())
       assert 0 <= result <= 100
   ```

5. **Update documentation** if needed

6. **Run the test suite:**
   ```bash
   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=.
   
   # Run specific test
   pytest tests/test_security.py
   ```

7. **Format your code:**
   ```bash
   # Format with Black
   black .
   
   # Check with Flake8
   flake8 .
   
   # Type checking
   mypy sportai_main_app_file.py
   ```

8. **Submit the pull request** with:
   - Clear description of changes
   - Link to related issue (if applicable)
   - Screenshots for UI changes
   - Confirmation that tests pass

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Docker (optional)

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/sportai-suite.git
cd sportai-suite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
streamlit run sportai_main_app_file.py

# Run tests
pytest

# Commit changes
git add .
git commit -m "feat: add awesome feature"

# Push to your fork
git push origin feature/your-feature-name
```

## Project Structure

```
sportai-suite/
├── sportai_main_app_file.py    # Main application (be careful!)
├── ai_modules/                  # AI components
│   └── *.py                    # Add new AI modules here
├── modules/                     # Feature modules
│   ├── facility_management/    # Facility-related features
│   ├── membership_management/  # Member features
│   └── ...                     # Other feature categories
├── tests/                       # Test files
│   └── test_*.py               # Test files must start with test_
└── docs/                        # Documentation
```

## Adding New Modules

To add a new module:

1. Create module file in appropriate directory:
```python
# modules/facility_management/my_new_feature.py

def run():
    """Entry point for the module."""
    import streamlit as st
    st.header("My New Feature")
    # Your implementation here
```

2. Add to module loader in main file (carefully!)

3. Write tests:
```python
# tests/test_my_new_feature.py

def test_my_new_feature():
    from modules.facility_management import my_new_feature
    assert hasattr(my_new_feature, 'run')
```

## Git Workflow

We use Git Flow:
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - Feature branches
- `hotfix/*` - Urgent fixes
- `release/*` - Release preparation

## Review Process

All submissions require review:
1. Automated tests must pass
2. Code review by maintainer
3. Documentation updated
4. No merge conflicts

## Community

- **Discord**: [Join our community](https://discord.gg/sportai)
- **Forum**: [GitHub Discussions](https://github.com/yourusername/sportai-suite/discussions)
- **Twitter**: [@SportAISuite](https://twitter.com/SportAISuite)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Annual contributor spotlight

## Questions?

Feel free to:
- Open an issue for questions
- Join our Discord server
- Email: contributors@sportai.com

Thank you for making SportAI Suite better! 🏆