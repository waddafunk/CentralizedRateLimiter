# Contributing to CentralizedRateLimiter

First off, thank you for considering contributing to CentralizedRateLimiter! It's people like you that make CentralizedRateLimiter such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [jacopo.piccirillo@gmail.com](mailto:jacopo.piccirillo@gmail.com).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the [issues](https://github.com/waddafunk/CentralizedRateLimiter/issues) for a list of current known issues.
- Perform a cursory search to see if the problem has already been reported.

**How Do I Submit A (Good) Bug Report?**

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include code samples and stack traces if relevant**
- **Include your environment details** (OS, Python version, package version)

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

**Before Submitting An Enhancement Suggestion:**
- Check if there's already a package which provides that enhancement.
- Check the [issues list](https://github.com/waddafunk/CentralizedRateLimiter/issues) for existing suggestions.

**How Do I Submit A (Good) Enhancement Suggestion?**

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the behavior you expected to see instead**
- **Explain why this enhancement would be useful**
- **List some other packages where this enhancement exists, if applicable**

### Pull Requests

#### Getting Started

1. Fork the repo and create your branch from `main`:
   ```bash
   git clone https://github.com/your-username/CentralizedRateLimiter.git
   cd CentralizedRateLimiter
   git checkout -b feature/your-feature-name
   ```

2. Set up your development environment:
   ```bash
   make dev-install
   ```

#### Making Changes

1. Make your changes in your fork
2. Follow our coding conventions:
   - Use [Black](https://black.readthedocs.io/) for code formatting
   - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
   - Write [good commit messages](https://chris.beams.io/posts/git-commit/)

3. Add tests for any new functionality

4. Ensure your changes pass all checks:
   ```bash
   make all  # Runs formatting, linting, and tests
   ```

#### Submitting Changes

1. Push to your fork
2. Submit a pull request to the main repository

**Pull Request Process**

1. Update the README.md with details of changes if needed
2. Update the documentation with details of any new functionality
3. The PR will be merged once you have the sign-off of at least one maintainer

**Pull Request Guidelines**

- Keep each PR focused on one specific change
- Include tests for any new functionality
- Update documentation as needed
- Follow the existing code style
- Write descriptive commit messages
- Link to relevant issues

## Development Process

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting:
  ```bash
  make format
  ```

- **isort** for import sorting:
  ```bash
  # Included in make format
  python -m isort .
  ```

- **pylint** and **flake8** for code quality:
  ```bash
  make lint
  ```

### Testing

- Write tests for all new functionality
- Maintain or improve code coverage
- Run tests locally before submitting:
  ```bash
  make test
  ```

### Documentation

- Keep docstrings up to date
- Follow Google-style docstring format
- Update README.md if adding new features
- Add typing hints to all new code

### Version Control

- Create feature branches from `main`
- Use meaningful commit messages
- Keep commits focused and atomic
- Rebase your branch before submitting PR

## Additional Notes

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `invalid`: Not a valid issue
- `question`: Further information needed
- `wontfix`: This will not be worked on

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests after the first line

## Recognition

Contributors will be recognized in our README.md and release notes. Thank you for your contributions!

## Questions?

Feel free to [open an issue](https://github.com/waddafunk/CentralizedRateLimiter/issues) with your question. We're here to help!