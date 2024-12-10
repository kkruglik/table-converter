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
2. Download the latest Python installer
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

or [download](https://github.com/kkruglik/table-converter/blob/main/run.sh) from repository

### 3. Create a working directory in Mac
* put the sctipt in it
* run script with double click

With first run script will create a working directory like this:
```
.
└── data
    ├── input
    └── output
```

### 4. Copy the documents you want to process to the `data/input` folder
and run the script again.

After the script finishes, the result will be in the folder `data/output/date_and_time` the script was run.