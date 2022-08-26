# disease-severity-api
 
  > Use **python3** for MacOs or Unix and **python** for Windows
  
  #### MacOS or Unix
    python3 -m venv venv
    source venv/bin/activate
  
  #### Windows
    python -m venv venv
  ###### *PowerShell*
    venv\Scripts\activate.ps1
  ###### *CMD*
    venv\Scripts\activate     
  
  ## Install dependencies
    (env) pip install -r requirements.txt 
    
  ##### Example directory
  ```
   disease-severity-api
   |───disease_severity
   |───model
   |      model.h5
   |──severity
   |──manage.py
   ```  
  ## Migrations
  #### MacOS or Unix
    python3 manage.py makemigrations
    python3 manage.py migrate
    
   #### Windows
    python manage.py makemigrations
    python manage.py migrate
  
  ## Run
  ##### MacOS or Unix
    python3 manage.py runserver
  #### Windows  
    python manage.py runserver
    
