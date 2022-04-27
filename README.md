# SocialPython
### Author: Alex Skakun

This app is the first attempt to create an analogue of social network
for people who are interested in programming and want to provide their 
free time in social networks more efficient. To achieve this, the app
provides you an opportunity to look memes, chat with friends, 
show photos and videos of your work (common social networks features)
AND at the same time solve problems, tasks, exercises and tests suggested
or created by other users. You can create some exercises and share this with friends,
so they will be able to check their skills by solving your task!
Then you can compete with them via the rating system!

For now only Python is considering as applicable programming language, but it can be
reconsider soon.


## Implemented functionality/code parts:
* Registering/authentication
* Changing user data
* Looking user's pages
* Rating system
* Looking exercises
* (API) Creating exercises
* Checking(Testing correctness) exercises
* (API) Commenting exercises
* Looking comments
* Exercise rating system
* Rating lists
* Frontend design
* Backend

## TO TRY THE APP:

1. Create virtual environment (python 3.x)
2. Go to the folder "apicompropy" and install requirements:

        cd apicompropy
        pip install -r requirements.txt
3. Create database migrations and migrate them:
         
         python manage.py makemigrations
         python manage.py migrate

4. Run backend server:
      
         python manage.py runserver

5. Open new terminal and go to the folder "frontend" and install needed packages:
      
         cd ../frontend
         npm install package.json --save

6. Now just run frontend client:

         npm run serve

7. Now you can use the app (link: http://localhost:8080/)
