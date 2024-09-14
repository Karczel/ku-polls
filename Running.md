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
### And you should be redirected to the polls index page
<img width="925" alt="Screenshot 2567-09-14 at 17 58 26" src="https://github.com/user-attachments/assets/0410416c-5cb7-450d-beed-65f1957d7dfb">

**!Caution** Some web browser may block the application due to security concerns (like Safari) <br>
Try Google Chrome or Brave.

## 3. Saving data
To save your questions and choices
```commandline
python manage.py dumpdata --indent=2 -o data/polls-file-name.json polls.question polls.choice
```
To save your votes
```commandline
python manage.py dumpdata --indent=2 -o data/vote-file-name.json polls.vote
```
To save your users
```commandline
python manage.py dumpdata --indent=2 -o data/users-file-name.json auth.user
```

## 4. Terminate the running application
`Ctrl+C` to stop the running web application.
If you've accidentally pressed `Ctrl+Z` and can't run the application again,
follow these instructions
1. Type this in your terminal
For Mac/Linux <br>
**sudo is added to execute the command with superuser(root) privileges**
```commandline
sudo lsof -i :8000
//The second column of the output is the <PID>
```
Then replace <PID> in this code below and run,
```commandline
sudo kill <PID>
//or
sudo kill -9 <PID>
```
or 
Mac
Searching the PID in your Activity Moniter, right click, and press Quit.

For Windows <br>
```commandline
netstat -ano | findstr :8000
//The last column is the <PID>
```
Then replace <PID> in this code below and run,
```commandline
taskkill /PID <PID> /F
```
## 5. Exit virtual environment
run this in your virtual environment
```commandline
deactivate
```

Existing demo users and passwords <br>

|    Username     |    password     |
|:---------------:|:---------------:|
|      harry      |    hackme22     |
|       Kar       |    password     |
|       abc       |    abckuwow     |
