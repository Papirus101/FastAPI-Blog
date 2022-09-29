# User microservice

# How to start with docker compose:
1. clone this project `git clone https://github.com/Papirus101/fastapi_templpate.git `
2. copy .env_dist to .env `cp .env_dist .env`
3. change `.env` file
4. change `init.sql` in db folder
5. run `docker compose up `
6. open `127.0.0.1:8000/api/docs` on your browser

# How to start without docker:
1. clone this project `git clone https://github.com/Papirus101/fastapi_templpate.git`
2. create virtual venv `python -m venv venv` and activate `source venv/bin/activate`
3. install requirements `pip install -r requirements.txt`
4. copy .env_dist to .env `cp .env_dist .env`
5. change `init.sql` in db folder
6. start local redis or start redis in docker 
`
sudo docker run --restart=always -d --name redis_1 -p 6379:6379 redis redis-server
`
7. change `.env` file
8. run `uvicorn app:app`
9. open `127.0.0.1:8000/api/docs` on your browser
