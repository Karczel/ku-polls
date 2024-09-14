# Running the Application Tutorial
## 1. After you've finished the [Installation Tutorial](Installation.md)
you can run the application; run this in your terminal
```
python manage.py runserver
```
## 2. Use your web browser of choice
type this in your web browser's URL bar
```commandline
localhost:8000
```
And you should be redirected to the polls index page

**!Caution** Some web browser may block the application due to security concerns (like Safari)
Try Google Chrome or Brave

## 3. Saving data
To save your questions and choices:
```commandline
python manage.py dumpdata --indent=2 -o data/polls-file-name.json polls.question polls.choice
```
To save your votes:
```commandline
python manage.py dumpdata --indent=2 -o data/vote-file-name.json polls.vote
```
To save your users:
```commandline
python manage.py dumpdata --indent=2 -o data/users-file-name.json auth.user
```

## 4. Terminate the running application
`Ctrl+C` to stop the running web application.
If you've accidentally pressed `Ctrl+Z` and can't run the application again,
follow these instructions:
1. Type this in your terminal
```commandline
lsof -i :8000
//out put is the <PID>
```
Then,
```commandline
kill <PID>
//or
kill -9 <PID>
```
or Searching the PID in your Activity Moniter, right click, and press Quit.

## 5. Exit virtual environment
run this in your virtual environment:
```commandline
deactivate
```

Existing demo users and passwords: <br>

|    Username     |    password     |
|:---------------:|:---------------:|
|      harry      |    hackme22     |
|       Kar       |    password     |
|       abc       |    abckuwow     |