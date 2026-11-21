# CheckYourServ
A web app that lets you check the status of Minecraft servers: your own, your favorites, and other


# Launch App for development

```bash
#Terminal 1 in frontend files
npm turbo dev
```

```bash
#Terminal 2 in backend files
uvicorn main:app #NEED TO BE IN VENV!
```

# Linters 

## Backend

- ruff
- mypy

```bash
ruff check --fix .   # lint + auto correct
ruff format .        # formate
mypy *.py            #check static types
```


## Frontend

- eslint
- prettier

```bash
vite lint   # check errors
vite lint:fix #correct
vite format # format with prettier
```


## General

- cspell

```bash
npm i -D cspell #at root
```