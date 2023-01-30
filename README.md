# DRF_REST_PHOTO_MANAGER

#### API photo manager, with the ability to add, delete and edit data.
___
## API Overview

| Description                | Url                                    |
| ---------------------------|----------------------------------------|
| Display and upload images  | display-and-upload/?geolocation=&date= |
| Select and delete image    | select-and-delete/\<str:pk\>           |
| Update image and metadata  | update-image/\<str:pk\>                |
| Basic registration         | registr/                               |
| Get authorization token    | auth/token/login/                      |

You must be logged in to make any changes.
___
## Installation

#### Fill in the .env file:

```bash
photo_manager_project/photo_manager_project/.env
```

#### Run the following command:

```bash
docker-compose up 
```

#### Enter the application container:

```bash
docker-compose exec web sh
```

#### Create and run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Start using!