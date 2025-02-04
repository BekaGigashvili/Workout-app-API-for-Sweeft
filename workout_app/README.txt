if you want to use this application follow this instructions: download this folder, create virtual environment inside it and activate, inside terminal run "pip install -r requirements.txt", this will install all the files required for this application.
I use postgresql. If you want to use postgresql as well, you need to set up the postgresql database and user for that database and change the "NAME", "USER", and "PASSWORD", "HOST", and "PORT" fields inside settings.py file accordingly, which is located inside the /workout_app directory.


to run migrations run this commands: python manage.py makemigrations python manage.py migrate
after that to run the application, simply write this command in the terminal: python manage.py runserver

go to swagger to check the endpoints "http://127.0.0.1:8000/swagger"

inside swagger you first need to register. provide name, email and password for /users/register endpoint and click execute.

after that you need to authenticate user. copy access token provided by that endpoint and paste it in the authenticate field like that:
Bearer <access token>
 after that you can log in. ptovide emai and password for users/login endpoint and click execute.

 after that you can create workout plans. for that provide name, goal, workout frequency, exercise_id, sets, repetitions,duration and distance, but some workout is not relatable for distance and some are not relatable to sets or repetitions, so I made validators for it.

 after that you can list all workout pans related to that user by exercises/workout_plans endpoint.

 after that you can crete weight logs and list all the weight logs by exercises/weight_logs post and get endpoints.

 after that you can set fitness goals and list them by exercises/fitness_goals post and get endpoints.

 after that you can create and list workout sessions with exercises/workout_sesions post and get endpoints.

 after that you can update workout session data by providing session id and data for related fields