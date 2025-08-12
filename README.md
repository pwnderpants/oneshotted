# OneShotted - Utility Scripts Collection

A collection of useful Python scripts for various system administration and development tasks.

## Repository Structure

```
oneshotted/
├── LICENSE
├── README.md
└── python3/
    ├── delete_markers.py
    ├── file_normie.py
    ├── populate_files.py
    └── requirements.txt
```

## Contributing

We welcome contributions to this utility scripts collection! Here's how you can contribute:

### How to Contribute via Pull Request

1. **Fork the Repository**
   - Click the "Fork" button on the GitHub repository page
   - Clone your fork locally: `git clone https://github.com/YOUR_USERNAME/oneshotted.git`

2. **Create a Feature Branch**
   ```bash
   cd oneshotted
   git checkout -b feature/your-script-name
   ```

3. **Add Your Script**
   - Place your script in the appropriate language folder (e.g., `python3/`)
   - Follow the existing naming conventions and code style
   - Include some usage documentation and error handling

4. **Update Documentation**
   - Add your script description to this README.md
   - Update `requirements.txt` if your script has external dependencies
   - Include usage examples and feature descriptions

5. **Test Your Script**
   - Ensure your script runs without errors
   - Test edge cases and error conditions

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add [script-name]: brief description of functionality"
   git push origin feature/your-script-name
   ```

7. **Create Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Provide a clear description of what your script does and why it's useful
   - Reference any related issues

### Contribution Guidelines

- **Dependencies**: Minimize external dependencies when possible
- **Security**: Never include credentials or sensitive data in scripts
- **Licensing**: All contributions will be licensed under MIT License
- **Script Categories**: Organize scripts by language/technology (python3/, bash/, etc.)

### What Makes a Good Utility Script

- Solves a common, repetitive task
- Well-documented with clear usage instructions
- Robust error handling and user feedback
- Command-line interface with helpful options
- Can be used as a "one-shot" solution for specific problems
