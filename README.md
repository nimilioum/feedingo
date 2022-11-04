# Feedingo app
a simple rss aggregator api, designed with drf,
postgresql and celery

### How to use
first copy .env.example to .env.docker and 
change the variables as you like, then run
this command in your terminal:

```
docker-compose up -d
```

you can access the api on
[this](http://localhost:8000/swagger) address.

Note that manually create/update/delete feeds 
can only be done as admin, as a simple user 
you can only add feeds by the rss url.
