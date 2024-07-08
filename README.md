## Setup Instructions

### Step 1: Install Python and pip
- Install <b><a href="https://www.python.org/downloads/">Python</a></b> (v3.8+) and <b><a href="https://pip.pypa.io/en/stable/installation/">PIP</a></b> and add to your System PATH

### Step 2: Clone the project
```
https://github.com/JohnRitchie/forcepoint.git
cd forcepoint
```

### Step 3: Create and activate a virtual environment
#### For Windows:
```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```
#### For Mac:
```
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
```
### Step 4: Install requirements
```
pip install -r requirements.txt
```
### Step 5: Install playwright
```
playwright install
```
## Work with tasks
### Task 1
```
cd task_1
```
#### Running the main code
```
python main.py
```
#### Running tests and view Allure test results (default report)

Running tests
```
pytest
```
View Allure test results
```
allure serve
```
or (opens only from IDE)
```
allure generate
```
open `allure-report\index.html` in Browser

#### Running tests and view simple test results
```
pytest --html=report.html
```
open `report.html` in Browser

### Task 2
```
cd ..
cd task_2
```
#### Running tests and view Allure test results (default report)
Running tests
> [!NOTE]
> (headless by default. If you want to see the work in the browser, you need to change the headless mode in the file task_2/tests/conftest.py on line 10: headless=False)
```
pytest
```
View Allure test results
```
allure serve
```
or (opens only from IDE)
```
allure generate
```
open `allure-report\index.html` in Browser

#### Running tests and view simple test results
```
pytest --html=report.html
```
open `report.html` in Browser
