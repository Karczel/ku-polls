# Installation Tutorial
## 1. Clone the repository
Run this in your terminal
```
git clone https://github.com/Karczel/ku-polls.git
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
For Mac/Linux
```commandline
source myenv/bin/activate
```
For Windows
```commandline
.\myenv\Scripts\activate
```
## 5. Install requirements
```
pip install -r requirements.txt
```
## 6. Create your own .env file
In the `sample.env` file, we have provided everything necessary to run the file,
So you can duplicate and rename it to `.env`
### To create a .env file in terminal
For Mac/Linux
```commandline
cp sample.env .env
```
For windows
```commandline
copy sample.env .env
```
However, if you want to generate your own SECRET_KEY, here is how you can do it
```commandline
import secrets
print(secrets.token_urlsafe(50))
//use the output result as your SECRET_KEY by replacing it in .env
```

## 7. Migrate
```commandline
python manage.py migrate
```

## 8. Run tests
```commandline
python manage.py test
```

## 9. Load data
```commandline
python3 manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

## 10. [Run the web application](Running.md)
