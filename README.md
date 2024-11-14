# CentralizedRateLimiter

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/waddafunk/CentralizedRateLimiter)
[![PyPI version](https://badge.fury.io/py/centralized-rate-limiter.svg)](https://badge.fury.io/py/centralized-rate-limiter)

A robust, centralized rate limiting utility for Python applications that need precise control over API request rates with built-in retry mechanisms and a single rate limit for all request methods.

## 🔧 Installation

```bash
pip install centralized-rate-limiter
```

## 🌟 Features

- **Centralized Configuration**: Set rate limiting parameters once and reuse across your application for all request methods
- **Comprehensive Retry Logic**: Built-in exponential backoff and configurable retry attempts
- **Thread-Safe**: Reliable rate limiting in multi-threaded environments
- **Flexible HTTP Support**: Works with all standard HTTP methods
- **Session Management**: Extends `requests.Session` for seamless integration
- **Type Hints**: Full type annotation support for better IDE integration


## 🎯 Quick Start

```python
from centralized_rate_limiter import get_rate_limiter

# Create a rate limiter with custom parameters
rate_limiter = get_rate_limiter(
    requests_per_second=10,
    total_retries=5,
    backoff_factor=0.25
)

# Use it for your API calls
response = rate_limiter.get('https://api.example.com/data')

# Works with all HTTP methods
post_response = rate_limiter.post(
    'https://api.example.com/create',
    json={'key': 'value'}
)
```

## 🔧 Advanced Usage

### Custom Configuration

```python
from centralized_rate_limiter import RateLimitedSession

# Create a session with specific parameters
session = RateLimitedSession(
    requests_per_second=5,
    total_retries=3,
    backoff_factor=0.5
)

# Use session in your application
responses = []
for endpoint in endpoints:
    response = session.get(endpoint)
    responses.append(response)
```

### Error Handling

```python
from requests.exceptions import RetryError

try:
    response = rate_limiter.get('https://api.example.com/data')
    data = response.json()
except RetryError:
    print("Max retries exceeded")
except Exception as e:
    print(f"An error occurred: {e}")
```

## 📊 Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `requests_per_second` | int | 10 | Maximum number of requests allowed per second |
| `total_retries` | int | 5 | Maximum number of retry attempts for failed requests |
| `backoff_factor` | float | 0.25 | Multiplier for exponential backoff between retries |

## 🤔 When to Use This vs. Other Solutions

### Use CentralizedRateLimiter When You Need:

1. **Centralized Rate Limiting and Retry Logic**
   - You want a single solution that handles both rate limiting and retries
   - You want a single rate limit for all your requests methods 
   - You need fine-grained control over retry behavior

2. **Thread-Safe Operation**
   - Your application makes API calls from multiple threads
   - You need reliable rate limiting in concurrent scenarios

3. **Session Management**
   - You want to maintain session state across requests
   - You need to reuse connections for better performance

4. **Custom Configuration**
   - You require specific combinations of rate limiting and retry parameters
   - You need to adjust settings per-instance

### Consider Alternatives When:

1. **Distributed Rate Limiting Required**
   - Consider `python-redis-rate-limit` for distributed systems
   - Use `Flask-Limiter` for API endpoint protection

2. **Simpler Requirements**
   - Use `requests-ratelimiter` for basic rate limiting
   - Use `backoff` package for simple retry logic

3. **Async Operation**
   - Consider `aiohttp` with `aiohttp-client-manager`
   - Use `asyncio` based solutions for async workflows

4. **Minimal Dependencies**
   - Use built-in `time.sleep()` for simple delays
   - Implement basic rate limiting without external packages

## 🔍 How It Works

The library uses a combination of:
- Decorator-based rate limiting using the `ratelimit` package
- `urllib3.util.Retry` for configurable retry behavior
- Custom session management extending `requests.Session`

Example retry sequence:
```
Request 1 (fails) → Wait 0.25s → Retry 1 (fails) → Wait 0.5s → Retry 2 (succeeds)
```

## 🛠️ Development

### Prerequisites

- Python 3.7+
- Make (optional, but recommended)
- Git

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/waddafunk/CentralizedRateLimiter.git
cd CentralizedRateLimiter
```

2. Install development dependencies:
```bash
make dev-install
```

Or without make:

```bash
python -m pip install -e ".[dev]"
```

### Development Tools

The project uses several development tools, all configured in `pyproject.toml`:

#### Code Formatting
- **Black**: Code formatter with a line length of 88 characters
- **isort**: Import statement organizer, configured to work with Black
- **pyupgrade**: Automatically upgrades Python syntax for newer versions

```bash
# Format all code
make format
```

or without make

```bash
# Individual tools
python -m black .
python -m isort .
python -m pyupgrade --py37-plus **/*.py
```

#### Code Quality
- **pylint**: Static code analysis
- **flake8**: Style guide enforcement

```bash
# Run all linters
make lint
```

or without make

```bash
python -m pylint centralized_rate_limiter tests
python -m flake8 centralized_rate_limiter tests
```

#### Testing
- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **responses**: HTTP request mocking

```bash
# Run tests with coverage
make test
```

or without make

```bash
make coverage
```

### Development Workflow

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and ensure quality:
```bash
make format  # Format code
make lint    # Check code quality
make test    # Run tests
# Or run all checks at once:
make all
```

3. Build and check the package:
```bash
make build
```

4. Submit a pull request

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make install` | Install package for production |
| `make dev-install` | Install package with development dependencies |
| `make format` | Format code using black and isort |
| `make lint` | Run code quality checks |
| `make test` | Run tests with pytest |
| `make coverage` | Generate test coverage report |
| `make clean` | Remove build artifacts and cache files |
| `make build` | Build distribution packages |
| `make publish` | Prepare package for PyPI publishing |
| `make all` | Run all quality checks and tests |
| `make help` | Show available commands |

### Project Structure

```
centralized_rate_limiter/
├── .git/
├── .gitignore
├── centralized_rate_limiter/
│   ├── __init__.py
│   └── rate_limiting.py
├── tests/
│   └── test_rate_limiting.py
├── Makefile
├── pyproject.toml
├── README.md
└── LICENSE
```

### Configuration Files

#### pyproject.toml
The `pyproject.toml` file contains all project configurations:

- Build system configuration
- Package metadata
- Dependencies (both runtime and development)
- Tool configurations:
  - pytest settings
  - coverage settings
  - black configuration
  - isort configuration

#### Makefile
The Makefile provides convenient commands for common development tasks. See the commands table above for available operations.

### Continuous Integration

The project uses GitHub Actions for CI/CD, running the following checks on each pull request:
- Code formatting (black, isort)
- Linting (pylint, flake8)
- Tests with coverage reporting
- Package building

## 🤝 Contributing

Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.


## 📜 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 📚 API Reference

### RateLimitedSession

```python
class RateLimitedSession(requests.Session):
    """A rate-limited HTTP session with built-in retry logic."""
    
    def __init__(
        self,
        requests_per_second: int = 10,
        total_retries: int = 5,
        backoff_factor: float = 0.25
    ) -> None:
        """Initialize a new rate-limited session."""
```

### get_rate_limiter

```python
def get_rate_limiter(
    requests_per_second: int = 10,
    total_retries: int = 5,
    backoff_factor: float = 0.25,
) -> RateLimitedSession:
    """Create a new rate-limited session with specified parameters."""
```

## 🙏 Acknowledgments

- [Requests](https://requests.readthedocs.io/) library
- [ratelimit](https://pypi.org/project/ratelimit/) package
- [urllib3](https://urllib3.readthedocs.io/) library

## 📧 Contact

For questions and support, please open an issue in the GitHub repository.

---
Made with ❤️ for the Python community
