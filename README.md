# table-converter

## Installation Steps

### 1. Installing Python (One-Time Setup)

#### Using Homebrew (Recommended)
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

#### Using Python Installer
1. Visit https://www.python.org/downloads/
2. Download the latest Python 3.11 installer
3. Open the downloaded .pkg file
4. Follow the installation wizard

To verify Python installation, open Terminal and run:
```bash
python3 --version
```

### 2. Get the Run Script

```bash
curl -O https://raw.githubusercontent.com/kkruglik/table-converter/refs/heads/main/run.sh
chmod +x run.sh
```

### 3. Run the Tool
```bash
./run.sh
```