# Contributing to Tanzanian Rent Invoice Processor

Thank you for your interest in contributing! This project helps Tanzanian businesses comply with tax regulations, so contributions must be accurate and well-tested.

## How to Contribute

### Reporting Bugs

If you find a bug:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version)

### Suggesting Enhancements

For feature requests:

1. **Check existing issues** for similar requests
2. **Create an issue** describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Why this would benefit users
   - Any implementation ideas

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following our guidelines below
4. **Test thoroughly** (see Testing section)
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request** with:
   - Description of changes
   - Issue number (if applicable)
   - Test results
   - Screenshots (if UI changes)

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small

Example:
```python
def calculate_wht(gross_rent: Decimal) -> Decimal:
    """
    Calculate 10% withholding tax on gross rent.
    
    Args:
        gross_rent: Base rent amount before VAT
        
    Returns:
        Withholding tax amount (10% of gross_rent)
    """
    return (gross_rent * TaxCalculator.WHT_RATE).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
```

### Testing Requirements

**All tax calculation changes MUST be tested!**

1. **Run existing tests**: `python test_calculations.py`
2. **Add new tests** for your changes
3. **Verify edge cases**:
   - Zero amounts
   - Very large amounts
   - Decimal precision
   - Invalid inputs

Example test:
```python
def test_new_feature():
    """Test description"""
    # Arrange
    input_value = Decimal("1000000.00")
    
    # Act
    result = your_function(input_value)
    
    # Assert
    assert result == expected_value, "Error message"
    print("✅ PASS: Test name")
```

### Tax Compliance

**CRITICAL**: Tax calculations must be accurate!

Before submitting tax-related changes:

1. ✅ Verify against TRA official guidelines
2. ✅ Include references to TRA documentation
3. ✅ Add tests proving correctness
4. ✅ Update documentation with sources
5. ✅ Note the effective date of tax changes

Example:
```python
# As per TRA Finance Act 2026, Section X
# Commercial rent WHT rate: 10%
# Reference: https://www.tra.go.tz/...
WHT_RATE = Decimal("0.10")
```

### Documentation

Update documentation when:

- Adding new features
- Changing tax rates
- Modifying calculations
- Adding dependencies
- Changing UI/UX

Files to update:
- `README.md` - Main documentation
- `QUICKSTART.md` - If setup changes
- `config.ini` - Add new settings
- Docstrings in code

## Types of Contributions Needed

### High Priority

- 🐛 Bug fixes (especially calculation errors)
- 📚 TRA guideline updates
- 🧪 Additional test cases
- 🌍 Swahili language support
- ♿ Accessibility improvements

### Medium Priority

- 🎨 UI/UX enhancements
- 📊 Export features (PDF, Excel)
- 🔍 Better OCR accuracy
- 📱 Mobile responsiveness
- 🗄️ Invoice history/database

### Nice to Have

- 🎯 Batch processing
- 🔌 API integration
- 📈 Analytics dashboard
- 🎓 Tutorial videos
- 🌐 Multi-currency support

## Tax Rate Changes

If TRA changes tax rates:

1. **Create an issue** with:
   - Official TRA announcement link
   - Effective date
   - Old vs new rates

2. **Update code**:
   - `config.ini` - Default rates
   - `app.py` - TaxCalculator class
   - `test_calculations.py` - Test cases
   - Documentation files

3. **Add migration guide** for existing users

## Review Process

Pull requests are reviewed for:

1. **Correctness** - Does it work as intended?
2. **Testing** - Are there adequate tests?
3. **Documentation** - Is it documented?
4. **Code quality** - Is it readable and maintainable?
5. **Tax accuracy** - For tax changes, is it TRA-compliant?

We aim to review PRs within 1 week.

## Getting Help

- 💬 Open a discussion for questions
- 📧 Contact maintainers for private matters
- 📖 Check existing issues and PRs
- 🔍 Search documentation

## Code of Conduct

- Be respectful and professional
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Keep discussions on-topic

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation (if desired)

## Legal

By contributing, you agree that:
- Your contributions will be licensed under MIT License
- You have the right to submit the contribution
- You've tested your changes thoroughly

## Questions?

Not sure about something? Ask! We're here to help.

---

**Thank you for helping Tanzanian businesses stay compliant!** 🇹🇿
