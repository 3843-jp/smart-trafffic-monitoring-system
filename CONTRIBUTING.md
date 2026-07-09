# Contributing to Smart Traffic Monitoring System

First off, thank you for considering contributing to this project! It's people like you that make this system such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment** (OS, Python version, CUDA version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected enhancement**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguide
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add vehicle classification filtering
Fix speed calculation precision issue
Update calibration documentation
```

### Python Styleguide

* Follow PEP 8
* Use type hints where possible
* Add docstrings to functions and classes
* Keep lines under 100 characters
* Use meaningful variable names

Example:
```python
def calculate_speed(pixel_distance: float, time_delta: float) -> float:
    """
    Calculate vehicle speed in km/h.
    
    Args:
        pixel_distance: Distance traveled in pixels
        time_delta: Time elapsed in seconds
        
    Returns:
        Speed in kilometers per hour
    """
    from config import METERS_PER_PIXEL
    
    meters = pixel_distance * METERS_PER_PIXEL
    speed_ms = meters / time_delta
    return speed_ms * 3.6
```

## Project Structure

```
smart-trafffic-monitoring-system/
├── speed_detection.py       # Main script
├── config.py               # Configuration parameters
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── README.md              # Documentation
├── CONTRIBUTING.md        # This file
├── examples/              # Example scripts
│   ├── example_basic.py
│   ├── example_calibrate.py
│   └── README.md
└── tests/                 # Unit tests (if added)
```

## Testing

Before submitting a PR, please test your changes:

```bash
python speed_detection.py
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `performance` - Performance improvements
* `help wanted` - Extra attention is needed

## Recognition

Contributors will be listed in the README.md file. Thank you for your help!

---

Questions? Feel free to open an issue or contact the maintainers.
