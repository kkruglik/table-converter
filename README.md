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

Run next command in terminal:

```bash
curl -O https://raw.githubusercontent.com/kkruglik/table-converter/refs/heads/main/run.sh
chmod +x run.sh
```

or [download](https://github.com/kkruglik/table-converter/blob/main/run.sh) from repository

### 3. Create a working directory in Mac
* put downloaded script into created folder
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

After the script finished, the result will be in the folder `data/output/date_and_time` the script was run.


## Установка

### 1. Установить Python

#### Через Homebrew
```bash
/bin/bash -c «$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)»
brew install python@3.11
```

#### Использование программы установки Python
1. Перейдите на сайт https://www.python.org/downloads/.
2. Загрузите последнюю версию программы установки Python
3. Откройте загруженный файл .pkg
4. Следуйте указаниям мастера установки

Чтобы проверить установку Python, откройте терминал и запустите комманду:
```bash
python3 --version
```

### 2. Скачайте скрипт для запуска конвертера

Выполните следующую команду в терминале:

```bash
curl -O https://raw.githubusercontent.com/kkruglik/table-converter/refs/heads/main/run.sh
chmod +x run.sh
```

или [скачайте скрипт](https://github.com/kkruglik/table-converter/blob/main/run.sh) из репозитория.

### 3. Создайте рабочую директорию в Mac
* создайте рабочую папку где угодно в документах
* поместите скачанный скрипт в созданную папку
* запустите скрипт двойным щелчком мыши

При первом запуске скрипт создаст рабочую директорию следующим образом:
```
.
└── data
    ├──── input
    └── output
```

### 4. Скопируйте документы, которые вы хотите обработать, в папку `data/input`.
и запустите скрипт снова.

После завершения работы скрипта результат будет находиться в папке `data/output/date_and_time`, в которой был запущен скрипт.