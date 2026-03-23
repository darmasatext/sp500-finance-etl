# 🤝 Contributing to S&P 500 Finance ETL

## 🇬🇧 Welcome Contributors!

Thank you for your interest in contributing to the S&P 500 Finance ETL project! This document provides guidelines for contributing to the codebase.

---

## 🇪🇸 ¡Bienvenidos Contribuidores!

¡Gracias por tu interés en contribuir al proyecto S&P 500 Finance ETL! Este documento provee guías para contribuir al código.

---

## 🚀 Getting Started / Comenzando

### Fork & Clone

```bash
# Fork the repository on GitHub
# Then clone your fork locally

git clone https://github.com/YOUR_USERNAME/sp500-finance-etl.git
cd sp500-finance-etl

# Add upstream remote
git remote add upstream https://github.com/darmasatext/sp500-finance-etl.git
```

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest pytest-cov black flake8 mypy
```

---

## 🎯 Areas for Contribution / Áreas de Contribución

### 🇬🇧 We Welcome Contributions in:

1. **New Technical Indicators** (see [FUTURE.md](./FUTURE.md))
   - Implement additional indicators (Stochastic, ADX, etc.)
   - Optimize calculation performance
   - Add unit tests

2. **Documentation**
   - Improve existing documentation
   - Add translations (French, Portuguese, etc.)
   - Create tutorials and examples
   - Fix typos and clarify explanations

3. **Bug Fixes**
   - Fix reported issues
   - Handle edge cases
   - Improve error messages

4. **Code Quality**
   - Add type hints
   - Improve code organization
   - Optimize performance
   - Add logging

5. **Testing**
   - Write unit tests
   - Add integration tests
   - Improve test coverage

6. **Features**
   - Dashboard templates (Looker Studio, Tableau)
   - Additional data sources
   - API layer development
   - Alerting mechanisms

### 🇪🇸 Damos Bienvenida a Contribuciones en:

*(Ver lista arriba)*

---

## 📝 Contribution Process / Proceso de Contribución

### 1. Create an Issue / Crear Issue

Before starting work, create an issue to discuss:
- What you want to build/fix
- Why it's needed
- How you plan to implement it

### 2. Create a Branch / Crear Rama

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions

### 3. Make Changes / Hacer Cambios

**Code Style Guidelines**:

- **Python**: Follow PEP 8
- **Line length**: Max 100 characters
- **Docstrings**: Use Google style
- **Comments**: Write in English (bilingual OK for inline)

**Example**:
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        prices: Series of closing prices
        period: RSI period (default 14 days)
        
    Returns:
        Series containing RSI values (0-100)
        
    Example:
        >>> rsi = calculate_rsi(df['Close'], period=14)
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gains/losses
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi
```

### 4. Add Tests / Agregar Pruebas

All new features should include tests:

```python
# tests/test_indicators.py
import pytest
import pandas as pd
from indicators import calculate_rsi

def test_rsi_basic():
    """Test basic RSI calculation"""
    prices = pd.Series([100, 102, 101, 103, 105, 104, 106])
    rsi = calculate_rsi(prices, period=3)
    
    assert len(rsi) == len(prices)
    assert 0 <= rsi.iloc[-1] <= 100
    
def test_rsi_overbought():
    """Test RSI detects overbought conditions"""
    prices = pd.Series([100, 105, 110, 115, 120, 125, 130])
    rsi = calculate_rsi(prices, period=3)
    
    assert rsi.iloc[-1] > 70  # Should be overbought
```

Run tests:
```bash
pytest tests/
pytest --cov=. tests/  # With coverage report
```

### 5. Update Documentation / Actualizar Documentación

If your change affects user-facing behavior:
- Update relevant `.md` files
- Add inline code comments
- Update docstrings
- Include examples

### 6. Commit Changes / Hacer Commit

**Commit message format**:
```
[type]: Short description (max 72 chars)

Longer explanation if needed:
- What changed
- Why it changed
- Any breaking changes

Closes #123
```

**Commit types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Test additions
- `chore:` - Maintenance tasks

**Examples**:
```bash
git commit -m "feat: Add RSI indicator calculation"
git commit -m "fix: Handle null values in Beta calculation"
git commit -m "docs: Update SETUP.md with Telegram bot instructions"
```

### 7. Push & Create Pull Request / Push y Crear PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

**Pull Request Template**:

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe how you tested your changes:
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] Integration tests passed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added in hard-to-understand areas
- [ ] Documentation updated (if applicable)
- [ ] No new warnings generated
- [ ] Tests added and passing

## Related Issues
Closes #issue_number
```

---

## 🧪 Testing Guidelines / Guías de Pruebas

### Unit Tests

Test individual functions in isolation:

```python
def test_fetch_yahoo_data():
    """Test Yahoo Finance data fetching"""
    ticker = "AAPL"
    data = fetch_yahoo_data(ticker, period="1d")
    
    assert not data.empty
    assert 'Close' in data.columns
    assert 'Volume' in data.columns
```

### Integration Tests

Test component interactions:

```python
def test_pipeline_execution():
    """Test full pipeline execution"""
    # Mock external dependencies
    with patch('maestro_tickers.update_bigquery_master'):
        result = ejecutar_pipeline()
        
    assert result['status'] == 'success'
```

### Mocking External Services

Always mock external API calls in tests:

```python
from unittest.mock import patch, MagicMock

@patch('yfinance.download')
def test_historico_with_mock(mock_download):
    """Test historical data processing with mocked Yahoo Finance"""
    # Setup mock data
    mock_data = pd.DataFrame({
        'Close': [100, 101, 102],
        'Volume': [1000, 1100, 1200]
    })
    mock_download.return_value = mock_data
    
    # Run test
    result = process_historical_data(['AAPL'])
    
    assert len(result) == 3
    mock_download.assert_called_once()
```

---

## 📋 Code Review Checklist / Lista de Revisión de Código

**For Reviewers**:

- [ ] Code is readable and well-commented
- [ ] Logic is correct and handles edge cases
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No hardcoded credentials or secrets
- [ ] Performance considerations addressed
- [ ] Backwards compatible (or breaking changes documented)
- [ ] Follows project conventions

**For Contributors**:

- [ ] PR description is clear and complete
- [ ] Related issue is linked
- [ ] All tests pass locally
- [ ] Code is self-reviewed
- [ ] No console.log / print debugging left in code
- [ ] Commit messages follow convention

---

## 🐛 Reporting Bugs / Reportar Bugs

### Bug Report Template

```markdown
**Describe the bug**
Clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With configuration '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened (include error messages).

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10.5]
- Package versions: [output of `pip freeze`]

**Additional context**
Add any other context about the problem here.
```

---

## 💡 Feature Requests / Solicitudes de Características

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
- Use cases
- Benefits
- Implementation ideas
```

---

## 📚 Resources / Recursos

### Technical Analysis References
- [Investopedia - Technical Indicators](https://www.investopedia.com/terms/t/technicalindicator.asp)
- [TA-Lib Documentation](https://mrjbq7.github.io/ta-lib/)

### Python Best Practices
- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### Testing
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Mocking Guide](https://realpython.com/python-mock-library/)

### BigQuery
- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)
- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)

---

## 🎉 Recognition / Reconocimiento

Contributors will be:
- Listed in CHANGELOG.md
- Mentioned in release notes
- Added to GitHub contributors list

Thank you for making this project better! 🙌

---

## ❓ Questions?

- **GitHub Discussions**: Ask questions in the Discussions tab
- **Issues**: Technical problems should be reported as issues
- **Twitter**: Reach out to [@darmasatext](https://twitter.com/darmasatext)

---

**Last Updated**: March 2026
