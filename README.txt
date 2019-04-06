Python, Flask, Nginx, Postgres, Docker sample application.

How to use:

#Clone/download the github project
#export the working directory to an env variable. example:
export pystack_path=/home/barn/Documents/python/pystack 

#Create file "flask_postgres.env" and store it in top folder of the pystack working directory:
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=database_name

#Create file "flask.env" and store it in top folder of the pystack working directory:
APP_SECRET_KEY=your_flask_hash_secret
pystack_name=sample_app

-------------------------------------
-------------POSTGRES
-------------------------------------
#deploy postgres

sudo docker rm --force pystack_db0 && \
sudo rm -fr $pystack_path/dbdata && \
sudo docker run --name pystack_db0 \
--env-file=$pystack_path/flask_postgres.env \
-v $pystack_path/postgres/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
-v $pystack_path/dbdata:/var/lib/postgresql/data \
--network=pynet \
--hostname pystack_db0 \
--restart unless-stopped \
-d postgres



#check it
sudo docker exec -it pystack_db0 bash -c 'psql -U postgres pystack_db0 -c "select * from bulletin"'


-------------------------------------
-------------FLASK
-------------------------------------
#build flask

sudo docker rm --force pystack_flask0 && \
cd $pystack_path/flask && \
sudo docker build . -t pystack_flask && \
sudo docker run \
-p 5000:5000 \
--env-file=$pystack_path/flask_postgres.env \
--env-file=$pystack_path/flask.env \
--network=pynet \
--name pystack_flask0 \
--restart unless-stopped \
-d pystack_flask

#if needed for debugging, do something like this to run on console

sudo docker run --rm \
-p 5000:5000 \
--env-file=$pystack_path/flask_postgres.env \
--env-file=$pystack_path/flask.env \
--network=pynet \
--name pystack_flask0 \
pystack_flask

-------------------------------------
-------------NGINX
-------------------------------------
#build nginx

cd $pystack_path/nginx && \
sudo docker build . -t pystack_nginx && \
sudo docker rm --force pystack_nginx0 && \
sudo docker run -d -p 80:80 \
--network=pynet \
--restart unless-stopped \
--name pystack_nginx0 \
pystack_nginx

#debugger:
sudo docker run --rm -p 80:80 \
--network=pynet \
--name pystack_nginx0 \
pystack_nginx

