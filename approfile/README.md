### INSTRUCTIONS
## Docker (Desktop)

```
cd approfile 
```

```
docker build -t ayomi-test-final . && docker run -d -p 8000:8000 ayomi-test-final
```

## local

```
py manage.py makemigrations webprofile
```

```
py manage.py migrate
```

```
py manage.py runserver 8000
```
