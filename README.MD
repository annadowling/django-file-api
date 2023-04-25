Inscribe File API Technical Exercise
==============================

Overview
-------------

This is a simple Python3 / Django application intended to provide a working example of a range of file storage API's.

### Pre-requisites
* Docker cli

Below pre-reqs are handled via docker / bootstrapped via sqllite:
* Django 4.2
* Python >= 3.9
* basic auth user (pre-loaded)

#### Run via docker
From the inscribe_file_api/ directory run the following:
```console
cd inscribe_file_api/
docker-compose up
```

##### Troubleshooting
*If you encounter a permission denied error during execution of entrypoint.sh by docker container you may just need to make the file executable again.
This is handled in the DockerFile but does not work for some reason. 
Seems to be a known issue which more time may resolve: 
https://stackoverflow.com/questions/70928077/permission-denied-while-executing-script-entrypoint-sh-from-dockerfile-in-kubern*
```console
cd inscribe_file_api/
chmod +x entrypoint.sh
docker-compose up
```


### Basic Auth
Bootstrapped sqlite db
```console
username: admin
password: adminpassword
```

#### Run Unit Tests
```console
cd inscribe_file_api/
python manage.py test
```

### Requests
#### Create a file
```console
curl --location 'http://127.0.0.1:8000/upload_file?category=personal&subject=python' \
--header 'Authorization: Basic YWRtaW46YWRtaW5wYXNzd29yZA==' \
--form 'file=@"/path/To/File/test.png"' \
--form 'category="test"' \
--form 'subject="python"'
```

#### Delete a file
```console
curl --location --request DELETE 'http://127.0.0.1:8000/delete_file?id=1' \
--header 'Authorization: Basic YWRtaW46YWRtaW5wYXNzd29yZA=='
```

#### Retrieve a file by id
```console
curl --location 'http://127.0.0.1:8000/get_file?id=2' \
--header 'Authorization: Basic YWRtaW46YWRtaW5wYXNzd29yZA=='
```

#### Retrieve a file by tag
```console
curl --location --globoff 'http://127.0.0.1:8000/get_file?tags={category%3Atest2}' \
--header 'Authorization: Basic YWRtaW46YWRtaW5wYXNzd29yZA=='
```