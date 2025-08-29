# 🚀 Algorithm Visualizer - Deployment Guide

This guide covers deploying and running the Algorithm Visualizer from source code.

---

## 📋 Quick Start

### **Standard Installation**
```bash
# Clone the repository
git clone https://github.com/Rblea97/Algorithm-Visualizer.git
cd Algorithm-Visualizer

# Run the application (no installation required!)
python main.py
```

### **Development Installation**
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]

# Run application after installation
algorithm-visualizer  # Via entry point
# or
python -m main        # Direct module execution
```

---

## 📦 Package Distribution

### **Build Distribution Packages**
```bash
# Build Distribution Packages
python setup.py sdist bdist_wheel

# Note: This project is designed for direct execution or local builds
# PyPI publishing is not configured for this portfolio project
```

### **Development Package Installation**
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[dev]

# Run application after installation
algorithm-visualizer  # Via entry point
# or
python -m main        # Direct module execution
```

---

## 🖥️ Local Development

### **Testing the Installation**
```bash
# Verify the installation works correctly
python -c "from algorithms import ALGORITHMS; print(f'Loaded {len(ALGORITHMS)} algorithms')"
python -c "from ui import ControlPanel, VisualizationCanvas, LegendPanel; print('UI components loaded')"

# Run the application
python main.py
```

---

## 🧪 Development Tools

### **Code Quality**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Format code
black .

# Type checking
mypy .

# Linting
ruff check .

# Run tests
pytest --verbose
```

### **Testing Framework**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_input_validator.py -v
```

---

## 📋 System Requirements

### **Runtime Requirements**
- **Python**: 3.8 or higher
- **tkinter**: Included with Python standard library
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512 MB RAM minimum
- **Storage**: 50 MB available space
- **Display**: 1024x768 resolution minimum

### **Development Requirements**
- **Python**: 3.8 or higher
- **Development tools**: pytest, black, mypy, ruff (via requirements-dev.txt)
- **Git**: For version control and development workflow

---

## 🌐 Deployment Options

### **Quick Start Installation**
```bash
# Option 1: Direct Python Execution (Requires Python 3.8+)
git clone https://github.com/yourusername/Algorithm-Visualizer.git
cd Algorithm-Visualizer
python main.py

# Option 2: Local Installation
pip install -e .
algorithm-visualizer

# Option 3: Development Installation
pip install -r requirements-dev.txt
# Includes testing and development tools
```

### **System Requirements Documentation**
```markdown
## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher (for source installation)
- **Memory**: 512 MB RAM
- **Storage**: 100 MB available space
- **Display**: 1024x768 resolution minimum

### Recommended Requirements
- **Operating System**: Latest stable versions
- **Python**: 3.11+ for optimal performance
- **Memory**: 1 GB RAM or higher
- **Storage**: 500 MB available space
- **Display**: 1920x1080 or higher resolution
```

---

## 🔧 Configuration

### **Environment Variables**
No special environment variables are required. The application uses Python standard library only.

### **Configuration Files**
The application requires no external configuration files. All settings are managed within the application interface.

---

## 🚀 Performance Optimization

### **Application Performance**
- **Startup Time**: ~2-3 seconds on modern systems
- **Memory Usage**: ~50-100 MB during operation
- **Animation Performance**: Optimized for 60fps on educational datasets (10-50 elements)
- **Cross-Platform**: Consistent performance across Windows, macOS, and Linux

### **Development Performance**
- **Code Quality**: Automated formatting, linting, and type checking
- **Testing**: Comprehensive test suite for reliability
- **CI/CD**: Automated quality assurance via GitHub Actions

---

## 📚 Educational Deployment

Perfect for:
- **Computer Science Courses**: Algorithm visualization and education
- **Coding Bootcamps**: Interactive learning tool for sorting concepts  
- **Self-Study**: Personal learning and algorithm exploration
- **Technical Interviews**: Demonstration of algorithm understanding

---

## 🤝 Contributing

For development workflow and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.