## To run the API please follow these steps:

### First make sure:
- you have docker installed
- you are in the src/ folder

### Create .env files with:

```
make env-files
```

This will create `.env` and `.env_test` files.

`.env` file contains the minimal set of environment variables for the API configuration. It has `DB_PASSWORD` (required) and `DB_PORT` (optional) variables. `DB_PORT` variable is set to `5233` in case you have the standard `5232` port in use (because it will be exposed from the docker container to make the database accessible to checks).
You can change it to whatever you want.

`.env_test` file contains only the `DB_PASSWORD` (required) variable. It's used by the tests. The test container doesn't expose the database port.

### Run the API locally on port 8000 using:

```
make
```

### Check that the API is running:

Go to http://localhost:8000 in your browser, you should see there the API name, version and status

### Use the swagger UI to explore the API:

Go to http://localhost:8000/swagger in your browser. There you can see the API in detail.

### Optionally you can run the tests and check the coverage with:

```
make test
```