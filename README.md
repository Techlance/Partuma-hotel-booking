# Partuma-hotel-booking

## STEP-1 : Install PostgreSQl with pgAdmin
### How to install PostgreSQL?
##### Download postgreSQL from following link and install 
##### https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

## STEP-2 : Set Up Database 
##### Open PgAdmin and Create a database with name Partuma in PgAdmin.

## STEP-3 : Clone this repository

## STEP-4 : Creating Virtual environment
##### Use following command to set up virtual environment
```py -m venv <env-name>```
##### Activate environment
```<env-name>\Scripts\activate.bat```

## STEP-5 Install requirements.txt
```pip install -r requirements.txt```

## STEP-6 : Go to partuma/settings.py
##### Replace database_name, database_user and database_password in following code

```DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'your-user-name',
        'PASSWORD': 'your-password',
        'HOST': 'localhost'
    }
} 
```

## STEP-7 : Go to partuma/settings.py
#### Enter your email_id and password in following code

```EMAIL_HOST_USER = "your-email"```

```EMAIL_HOST_PASSWORD = "your-password"```


## STEP-8 : Go to rooms/views.py
#### Enter your account_sid and auth_token for twilio in following code
``` account_sid = "your-account-sid"
 auth_token  = "your-auth-token"
 ```
 #### [Note: There are multiple variables in views.py so you have to replace all]

#### Also change from_ = "number" with your twilio number in views.py under function send_sms, partuma_confirmation, client_confirmation
#### For example :
```from_="your-twilio-number"```

## STEP-9 : Go to rooms/views.py
#### Under partuma_confirmation function enter manager/owner number so confirmation message will be sent to manager/owner.
```to="+<country_code>" + str(manager_number)```

## STEP-10 : Run following commands
```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py runserver```

#### Hurrah your website is running


## Set up superuser
#### Use following command
```python manage.py createsuperuser```

## Thank you


