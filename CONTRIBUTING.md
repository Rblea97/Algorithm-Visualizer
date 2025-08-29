# 🤝 Contributing to Algorithm Visualizer

Thank you for your interest in contributing to the Algorithm Visualizer! This document provides guidelines for contributing to this educational project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Adding New Algorithms](#adding-new-algorithms)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)

## 📜 Code of Conduct

This project is committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the educational community
- Show empathy towards other community members

## 🚀 How to Contribute

### Ways to Contribute
- 🐛 **Bug Reports**: Help identify and fix issues
- ✨ **Feature Requests**: Suggest educational enhancements
- 🔧 **Code Contributions**: Implement new features or fixes
- 📚 **Documentation**: Improve guides and documentation
- 🎨 **UI/UX Improvements**: Enhance user experience
- 🧪 **Testing**: Add tests and improve coverage
- 🎓 **Educational Content**: Improve learning materials

### Getting Started
1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Code editor (VSCode, PyCharm, etc.)

### Setup Instructions
```bash
# Clone your fork
git clone https://github.com/yourusername/Algorithm-Visualizer.git
cd Algorithm-Visualizer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Verify setup
python main.py
```

### Development Dependencies
```bash
# Optional but recommended
pip install pytest>=7.0.0     # Testing
pip install black>=22.0.0     # Code formatting  
pip install mypy>=1.0.0       # Type checking
pip install flake8>=5.0.0     # Linting
```

## 📝 Contribution Guidelines

### Educational Focus
This is an educational project. All contributions should:
- **Enhance Learning**: Improve understanding of sorting algorithms
- **Maintain Clarity**: Keep visualizations clear and intuitive
- **Support Teachers**: Consider classroom and self-learning use
- **Stay Accessible**: Ensure features are easy to understand and use

### Technical Standards
- **Clean Code**: Follow Python best practices and PEP 8
- **Type Hints**: Include type annotations for all functions
- **Documentation**: Add comprehensive docstrings
- **Performance**: Maintain 60fps animation target
- **Testing**: Include tests for new functionality

### Before Contributing
- 🔍 **Check existing issues** to avoid duplicate work
- 💬 **Discuss major changes** by opening an issue first
- 📖 **Read the documentation** to understand the architecture
- 🧪 **Test your changes** on different array sizes and algorithms

## 🔄 Pull Request Process

### 1. Preparation
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... implement your feature ...

# Test your changes
python main.py  # Manual testing
# Add unit tests if applicable
```

### 2. Code Quality
```bash
# Format code
black .

# Check types
mypy main.py algorithms/ ui/ utils/

# Lint code
flake8 --max-line-length=88 .
```

### 3. Commit Guidelines
```bash
# Use descriptive commit messages
git commit -m "feat(algorithms): add heap sort implementation

- Implement HeapSort class with get_steps() method
- Add heap visualization with parent-child highlighting  
- Include educational descriptions for heap operations
- Update algorithm registry and constants
- Add unit tests for correctness and step generation

Closes #123"
```

### 4. Pull Request Submission
- **Title**: Clear, descriptive title
- **Description**: Use the PR template
- **Testing**: Document test cases and results
- **Screenshots**: Include if UI changes made
- **Educational Impact**: Explain learning benefits

### 5. Review Process
- **Automated Checks**: Ensure all CI checks pass
- **Code Review**: Address reviewer feedback
- **Testing**: Verify functionality works as expected
- **Documentation**: Update relevant docs if needed

## 🧮 Adding New Algorithms

### Algorithm Implementation
```python
# Example: Adding a new sorting algorithm
from typing import List, Tuple
from algorithms.base_algorithm import SortingAlgorithm

class YourSort(SortingAlgorithm):
    """
    Your Sort algorithm implementation with educational focus.
    
    Brief description of how the algorithm works and its characteristics.
    Include time/space complexity and best use cases.
    """
    
    def get_name(self) -> str:
        return "Your Sort"
    
    def get_steps(self, arr: List[int]) -> List[Tuple[str, List[int], str]]:
        """
        Generate educational animation steps.
        
        Focus on:
        - Clear step descriptions
        - Logical progression
        - Educational value
        - Proper action types
        """
        steps = []
        # Implementation with educational descriptions
        return steps
    
    def get_complexity(self) -> Tuple[str, str]:
        return ("O(?)", "O(?)")  # Replace with actual complexity
    
    def get_description(self) -> str:
        return "Educational description of the algorithm's approach and characteristics."
```

### Registration
```python
# In algorithms/__init__.py
from algorithms.your_sort import YourSort

ALGORITHMS = {
    # ... existing algorithms ...
    'Your Sort': YourSort,
}
```

### Testing
```python
# Create test file: test_your_sort.py
def test_your_sort_correctness():
    """Test algorithm produces correct results."""
    algorithm = YourSort()
    test_cases = [
        ([3, 1, 4, 1, 5], [1, 1, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        # Add more test cases
    ]
    
    for input_array, expected in test_cases:
        result = algorithm.sort_array(input_array)
        assert result == expected

def test_your_sort_steps():
    """Test step generation for animation."""
    algorithm = YourSort()
    steps = algorithm.get_steps([3, 1, 2])
    
    # Verify step format and educational value
    assert len(steps) > 0
    for action, indices, description in steps:
        assert action in ['compare', 'swap', 'mark_sorted', 'your_custom_action']
        assert isinstance(indices, list)
        assert len(description) > 10  # Meaningful descriptions
```

## 🎨 Style Guidelines

### Python Code Style
- **PEP 8**: Follow Python style guide (88 character line limit)
- **Black**: Use Black formatter for consistent formatting
- **Type Hints**: Include type annotations for all public methods
- **Docstrings**: Google-style docstrings for all classes and methods

### Documentation Style
```python
def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of function purpose.
    
    Longer description if needed, explaining the educational context
    and how this function contributes to algorithm visualization.
    
    Args:
        param1: Description of parameter and its constraints
        param2: Description of parameter and its purpose
        
    Returns:
        Description of return value and its meaning in educational context
        
    Raises:
        ValueError: When and why this exception might be raised
        
    Example:
        >>> example_function(42, "test")
        True
    """
    # Implementation with clear, educational comments
    return True
```

### UI/UX Guidelines
- **Consistency**: Follow existing design patterns
- **Accessibility**: Ensure clear visual hierarchy and contrast
- **Educational Focus**: Prioritize learning over aesthetics
- **Performance**: Maintain smooth 60fps animations

## 🧪 Testing

### Test Requirements
- **Algorithm Correctness**: Verify sorting produces correct results
- **Step Generation**: Ensure animation steps are valid and educational
- **UI Functionality**: Test user interactions work as expected
- **Performance**: Verify animations maintain target framerate
- **Edge Cases**: Test with various array sizes and data patterns

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_algorithms.py

# Run with coverage
python -m pytest --cov=algorithms --cov=ui --cov=utils

# Manual testing
python main.py  # Test full application
```

### Test Coverage Goals
- **Algorithms**: 100% test coverage for correctness
- **UI Components**: Test all user interactions
- **Edge Cases**: Empty arrays, single elements, duplicate values
- **Performance**: Animation timing and memory usage

## 📚 Documentation Standards

### Required Documentation
- **Code Comments**: Explain complex logic and educational decisions
- **Docstrings**: All public methods and classes
- **README Updates**: For new features or significant changes
- **Architecture Docs**: For structural changes
- **User Guide**: For new user-facing features

### Documentation Style
- **Clear Language**: Write for students and educators
- **Examples**: Include concrete examples and use cases
- **Visual Aids**: Use diagrams and screenshots when helpful
- **Educational Context**: Explain why features are educationally valuable

## 🎯 Contribution Focus Areas

### High Priority
- 📊 **New Sorting Algorithms**: Heap sort, radix sort, counting sort
- 🎨 **Visualization Improvements**: Better animations, clearer indicators
- 📱 **Accessibility**: Keyboard navigation, screen reader support
- 🧪 **Testing**: Improve test coverage and add integration tests
- 📖 **Documentation**: Better guides and educational content

### Medium Priority  
- 🎵 **Audio Feedback**: Sound effects for operations
- 📊 **Algorithm Comparison**: Side-by-side visualization
- 🎮 **Interactive Features**: Step-through mode, manual sorting
- 🌐 **Web Version**: Browser-based implementation
- 📈 **Analytics**: Learning progress tracking

### Future Enhancements
- 🎯 **Guided Tutorials**: Interactive learning paths
- 🏆 **Gamification**: Challenges and achievements
- 📱 **Mobile Version**: Touch-friendly interface
- 🔌 **Plugin System**: External algorithm loading
- 🌍 **Internationalization**: Multi-language support

## 🐛 Bug Reports

### Before Reporting
- ✅ **Check existing issues** for duplicates
- ✅ **Test with latest version**
- ✅ **Try different algorithms and array sizes**
- ✅ **Note your system specifications**

### Bug Report Information
- **System**: OS, Python version, display resolution
- **Reproduction**: Step-by-step instructions
- **Expected vs Actual**: Clear description of the issue
- **Screenshots**: Visual evidence of the problem
- **Logs**: Any error messages or console output

## ✨ Feature Requests

### Good Feature Requests Include
- **Educational Value**: How it improves learning
- **Use Cases**: Specific scenarios where it's helpful
- **Implementation Ideas**: Technical approach if known
- **Alternatives Considered**: Other solutions you've thought about
- **Priority**: How important it is for educational goals

### Feature Categories
- **Algorithm Features**: New algorithms or algorithm improvements
- **UI/UX Features**: Interface and interaction improvements
- **Educational Features**: Learning aids and teaching tools
- **Technical Features**: Performance, compatibility, deployment
- **Accessibility Features**: Making the app more inclusive

## 📞 Getting Help

### Resources
- 📚 **Documentation**: Read architecture and development guides
- 🐛 **Issues**: Search existing issues for similar problems
- 💬 **Discussions**: Start a discussion for questions
- 📧 **Contact**: Reach out for major contributions

### Response Times
- **Bug Reports**: Typically reviewed within 48 hours
- **Feature Requests**: Reviewed within 1 week  
- **Pull Requests**: Initial review within 3-5 days
- **Questions**: Answered as time allows

---

## 🙏 Recognition

Contributors who make significant contributions will be:
- ✅ **Credited** in the project documentation
- ✅ **Listed** in the contributors section
- ✅ **Mentioned** in release notes for their contributions
- ✅ **Invited** to be project maintainers for substantial ongoing contributions

---

Thank you for contributing to Algorithm Visualizer! Your efforts help make computer science education more accessible and engaging for learners worldwide. 🚀