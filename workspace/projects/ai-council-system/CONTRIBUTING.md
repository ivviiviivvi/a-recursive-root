# Contributing to AI Council System

First off, thank you for considering contributing to AI Council System! It's people like you that make this project such a great tool for exploring multi-AI coordination and debate.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## How Can I Contribute?

### Reporting Bugs

**Before Submitting a Bug Report**:
- Check the [existing issues](https://github.com/your-org/ai-council-system/issues) to see if it's already reported
- Collect information about the bug (OS, Python version, error messages, etc.)

**How to Submit a Bug Report**:
1. Use the GitHub issue tracker
2. Use a clear, descriptive title
3. Describe the exact steps to reproduce
4. Provide specific examples
5. Include any error messages/logs
6. Mention your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/your-org/ai-council-system/issues).

**How to Submit an Enhancement**:
1. Use a clear, descriptive title
2. Provide a detailed description of the proposed feature
3. Explain why this enhancement would be useful
4. List any alternative solutions you've considered

### Contributing Code

#### Good First Issues

Look for issues labeled [`good first issue`](https://github.com/your-org/ai-council-system/labels/good%20first%20issue) - these are great for newcomers!

#### Areas We Need Help

- **New AI Personalities**: Add unique debate personalities
- **New Streaming Platforms**: Integrate additional platforms
- **Enhanced Visual Effects**: Create new transition/visualization effects
- **Multi-Language Support**: Help implement Phase 4.4
- **Documentation**: Improve guides, add examples
- **Testing**: Write unit/integration tests
- **Performance**: Optimize bottlenecks
- **Bug Fixes**: Fix reported issues

---

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- (Optional) Docker for deployment testing

### Quick Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-council-system.git
cd ai-council-system

# 3. Add upstream remote
git remote add upstream https://github.com/your-org/ai-council-system.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# 6. Set up environment
cp .env.example .env
# Edit .env with your API keys

# 7. Run tests
./scripts/test.sh all

# 8. Try a demo
./quick-start.sh
```

### GitHub Codespaces (Recommended!)

Click the "Open in GitHub Codespaces" button in the README for instant setup!

---

## Pull Request Process

### Before You Start

1. **Check existing PRs**: Make sure someone isn't already working on it
2. **Open an issue**: Discuss major changes before implementing
3. **Create a branch**: Use descriptive names like `feature/new-personality` or `fix/avatar-cache-bug`

### Development Workflow

```bash
# 1. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make your changes
# ... edit files ...

# 4. Run tests
./scripts/test.sh all

# 5. Commit your changes
git add .
git commit -m "Add descriptive commit message"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Open Pull Request on GitHub
```

### Pull Request Guidelines

**Your PR should**:
- ✅ Have a clear, descriptive title
- ✅ Reference any related issues
- ✅ Include tests for new features
- ✅ Update documentation if needed
- ✅ Follow the code style guidelines
- ✅ Pass all CI checks

**PR Template**:
```markdown
## Description
[Brief description of changes]

## Related Issues
Fixes #[issue number]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No new warnings
```

### Review Process

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge

**Typical Timeline**:
- Initial review: Within 48 hours
- Follow-up: Within 24 hours
- Merge: Once approved and CI passes

---

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some additions:

```python
# Use type hints
def create_debate(topic: str, agents: List[Agent]) -> Debate:
    """
    Create a new debate.

    Args:
        topic: The debate topic
        agents: List of participating agents

    Returns:
        Configured Debate instance
    """
    pass

# Use dataclasses for configuration
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration for debate system"""
    topic: str
    rounds: int = 3
    timeout: float = 30.0

# Use async/await for I/O
async def generate_response(prompt: str) -> str:
    """Generate AI response"""
    response = await llm_client.generate(prompt)
    return response
```

**Tools**:
- **Black**: Code formatting (`black .`)
- **pylint**: Linting (`pylint core/ automation/`)
- **mypy**: Type checking (`mypy .`)

### Commit Messages

Follow the **Conventional Commits** format:

```
type(scope): brief description

Longer description if needed.

- Detail 1
- Detail 2

Fixes #123
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance tasks

**Examples**:
```
feat(avatars): add expression interpolation
fix(streaming): resolve bitrate calculation bug
docs(readme): update installation instructions
test(agents): add personality tests
```

### Documentation

- **Docstrings**: Google style for all public functions/classes
- **README**: Update if adding major features
- **Examples**: Provide runnable examples for new features
- **API Docs**: Update `api/openapi.yaml` if changing endpoints

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Discord**: Real-time chat (link in README)
- **Twitter**: Updates and announcements (@AICouncilSystem)

### Getting Help

**Stuck?** Don't hesitate to ask!

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/your-org/ai-council-system/issues)
3. Ask in [GitHub Discussions](https://github.com/your-org/ai-council-system/discussions)
4. Join our [Discord server](DISCORD_LINK)

### Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Project website (if/when established)
- Annual contributor spotlight

**Top Contributors** may receive:
- Exclusive swag
- Early access to new features
- Invitation to planning discussions
- Letter of recommendation (if desired)

---

## Development Resources

### Useful Documentation

- [META_REPORT.md](META_REPORT.md): Development methodology
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md): Complete development guide
- [ROADMAP.md](ROADMAP.md): Future plans
- [COMPILATION.md](COMPILATION.md): Project overview

### Examples

All examples are in the `examples/` directory:
- `demo_debate.py`: Quick debate demo
- `end_to_end_integration.py`: Complete workflow
- `phase5_complete_demo.py`: Automation demo

### Testing

```bash
# Run all tests
./scripts/test.sh all

# Run specific suite
./scripts/test.sh unit
./scripts/test.sh integration
./scripts/test.sh performance

# Run with coverage
./scripts/test.sh coverage
```

---

## Questions?

If you have questions about contributing, please:

1. Check this guide thoroughly
2. Search existing issues and discussions
3. Ask in GitHub Discussions
4. Contact maintainers directly (for sensitive issues)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Council System!** 🎉🤖

Every contribution, no matter how small, helps make this project better for everyone.
