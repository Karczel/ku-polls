# Installation Tutorial
## 1. Clone the repository
Run this in your terminal:
```
https://github.com/Karczel/ku-polls.git
```
## 2. Navigate to the project directory
```commandline
cd ku-polls
```
## 3. Create a virtual environment
```commandline
python -m venv myenv
```
## 4. Activate the Virtual environment
For Mac/Linux:
```commandline
source myenv/bin/activate
```
For Windows:
```commandline
.\myenv\Scripts\activate
```
## 5. Install requirements
```
pip install -r requirements.txt
```
## 6. Create your own .env file
In the sample.env file, we have provided everything necessary to run the file,
So you can copy that right into your .env file
However, if you want to generate your own SECRET_KEY, here is how you could do it:
```commandline
import secrets
print(secrets.token_urlsafe(50))
//use the output result as your SECRET_KEY 
```

## 7. Migrate
```commandline
python manage.py migrate
```

## 8. Load data
```commandline
python3 manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

## 9. [Run](Running.md)
