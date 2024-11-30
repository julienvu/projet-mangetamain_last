# Mangetamain Project (Julien VU)

The **Mangetamain** application is an interactive data visualization tool built with **Streamlit**. It permits users to explore and analyze datasets in real-time using interactive visualizations. The project is managed with **Poetry** for dependency management, ensuring a smooth setup and environment management process.

## Features
- **Interactive Data Visualizations**: Create and explore interactive plots using **Plotly**.
- **Data Exploration**: The app provides functionality to filter and analyze datasets in various formats.
- **Streamlit Interface**: Intuitive user interface built using **Streamlit**, making it easy to visualize and interact with data.

## Requirements

### System Requirements
- **Python 3.11+**: Ensure you have Python 3.11 or later installed.

### Install Dependencies

#### Using Poetry (Recommended)
Poetry is used to manage project dependencies and virtual environments.

1. **Install Poetry** globally:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. **Install project dependencies**:
    ```bash
    poetry install
    ```

#### Using pip (if not using Poetry)
Alternatively, you can install dependencies manually using `pip`:

1. **Install dependencies** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### Python Dependencies/librairies 
The project uses the following libraries:

- **`requests` (version ^2.32.3)**: To send HTTP requests.
- **`streamlit` (version ^1.39.0)**: For creating the web app interface.
- **`plotly` (version ^5.24.1)**: For interactive data visualizations.
- **`scikit-learn` (version ^1.5.2)**: For machine learning functionality.
- **`numpy` (version ^2.1.2)**: For numerical operations.

### Development Dependencies/framework
- **`pytest` (version ^8.3.3)**: For running unit tests.
- **`pytest-cov` (version ^5.0.0)**: For measuring test coverage.
- **`sphinx` (version ^8.0.2)**: For generating documentation.
- **`flake8` (version ^7.1.1)**: For Python code linting.
- **`black` (version ^24.8.0)**: For automatic code formatting.

These dependencies are listed in the `pyproject.toml` file for **Poetry** and the `requirements.txt` file.

## File Structure

### `pyproject.toml` and `poetry.lock`
- **`pyproject.toml`**: Defines the project’s metadata, dependencies, and configuration for **Poetry**.
- **`poetry.lock`**: Ensures that the same versions of dependencies are installed across different environments.

### `requirements.txt`
Contains the list of Python dependencies for those who prefer using `pip` over **Poetry**.

### `.gitignore`
Lists files and directories to be ignored by Git (e.g., compiled Python files, virtual environments, etc.).

### `.yaml` Configuration Files
Configuration files in YAML format are used for deployment and CI/CD workflows.

### `src/`
Contains the main source code, including the Streamlit app.

### `tests/`
Includes unit tests for the application code.

### `dataset/`
Contains raw and processed datasets used for analysis.

### `docs/`
Documentation and guides for setting up and using the project.

## Platform-Specific Installation Instructions

### Windows
1. Install **Poetry** by running:
    ```bash
    curl -sSL https://install.python-poetry.org | python
    ```

2. Install dependencies using **Poetry**:
    ```bash
    poetry install
    ```

3. Run the app:
    ```bash
    poetry run streamlit run src/app.py
    ```

### macOS and Linux
Follow the same steps as for **Windows** to install Poetry and run the application.


### Application Directory Structure (with the tree view)
Our application is structured with the following organization below:
```bash
    projet-mangetamain_last/
    │
    ├── .github/                # GitHub Actions configuration files
    │   └── workflows/          # CI/CD pipeline YAML files
    │
    ├── docs/                    # Project documentation (user guides, setup instructions)
    │
    ├── dataset/                 # Datasets used for analysis
    │   ├── raw/                 # Raw data files
    │   └── processed/           # Processed data for the app
    │
    ├── preprocessed_data/       # Preprocessed data used for analysis
    │
    ├── src/                     # Source code for the application
    │   ├── app.py               # Main entry point for the Streamlit app
    │   └── utils.py             # Helper functions used by the app
    │
    ├── tests/                   # Unit tests for the application
    │   ├── test_app.py          # Tests for Streamlit app logic
    │   └── test_utils.py        # Tests for utility functions
    │
    ├── .gitignore               # Specifies files to ignore in Git (e.g., virtual envs)
    ├── LICENSE                  # Project license
    ├── pyproject.toml           # Poetry configuration for the project
    ├── poetry.lock              # Locked dependency versions for reproducibility
    ├── requirements.txt         # Dependencies for pip (alternative to Poetry)
    ├── .vscode/                 # VS Code workspace configuration
    │   └── settings.json        # VS Code settings (optional)
    ├── .devcontainer/           # Dev container configuration for consistent development environments
    │   └── devcontainer.json    # Configuration file for the dev container
    └── README.md                # Project documentation (this file)
  ```
## Running the Application Locally

1. **Clone the repository** to your local machine:
    ```bash 
    git clone git@github.com:julienvu/projet-mangetamain_last.git ssh mode
    cd projet-mangetamain_last
    ```

2. **Install dependencies** with Poetry:
    ```bash
    poetry install
    ```

3. **Run the Streamlit app**:
    ```bash
    poetry run streamlit run src/app.py
    ```

This will launch the app in your default web browser.

## Development Workflow

1. **Clone the repository**:
    ```bash
    git clone git@github.com:julienvu/projet-mangetamain_last.git ssh mode
    cd projet-mangetamain_last
    ```

2. **Install dependencies** using Poetry:
    ```bash
    poetry install
    ```

3. **Run the application** locally:
    ```bash
    poetry run streamlit run src/app.py
    ```

4. **Run tests**:
    If unit tests are included, run them using `pytest`:
    ```bash
    poetry run pytest
    ```

5. **Commit changes** to Git:
    After making changes, commit and push them to your local branch (not the main branch):
    ```bash
    git add .
    git commit -m "Description of changes"
    git push origin <your-local-branch>
    ```

Replace `<your-local-branch>` with the name of your local branch (for example, `feature-branch` or `bugfix-branch`).

## Poetry Configuration

**Poetry** is used for dependency management and environment setup. The configuration is stored in the `pyproject.toml` file. 

### Poetry Commands
- **Install dependencies**:
    ```bash
    poetry install
    ```

- **Run the application**:
    ```bash
    poetry run streamlit run src/app.py
    ```

- **Update dependencies**:
    ```bash
    poetry update
    ```

## GitHub Actions (CI/CD)

The project uses **GitHub Actions** to automate continuous integration and deployment (CI/CD). The CI pipeline runs tests and guarantees that code quality checks are met before merging any changes into the main branch.

The configuration for these workflows can be found in the `.github/workflows` directory. 
'''bash
    name: Python CI

    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - name: Set up Python 3.11
            uses: actions/setup-python@v4
            with:
              python-version: "3.11"
          - name: Install Poetry
            run: |
              python -m pip install --upgrade pip
              pip install poetry
          - name: Install dependencies
            run: |
              poetry install
          - name: Set PYTHONPATH
            run: |
              echo "PYTHONPATH=$PYTHONPATH:$(pwd)/src" >> $GITHUB_ENV
          - name: Run Flake8
            run: |
              poetry run flake8 --max-line-length 88 --ignore=E402,E262,E265 src/
          - name: Run Black
            run: |
              poetry run black --check src/
          - name: Run tests with coverage
            run: |
              poetry run pytest --cov=src --cov-fail-under=90
    '''

### Automated Tasks:
- **Test Automation**: Every push to the distant repository triggers a set of **tests** to ensure code correctness.
- **Deployment**: Once tests pass, the application can be automatically deployed to production or staging environments (depending on your configuration).

## Testing

Testing is done using **pytest** to ensure the reliability and stability of the application.

### Running Tests
To run tests with a coverage superior to 90%:
  ```bash
    poetry run pytest --cov=src --cov-fail-under=90
  '''
