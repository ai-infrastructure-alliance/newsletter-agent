### Add repo in Heroku

```
heroku git:remote -a <heroku-project-name>
```

### Prepare Heroku for deployment

```
heroku buildpacks:clear
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

### Deploy on Heroku

```
git push heroku main
```