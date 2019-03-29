Python, Flask, Nginx, Postgres, Docker sample application.

To do:
- add docker compose

How to use:

#Pull the github project
#export the working directory to an env variable. example:
export pystack_path=/home/barn/Documents/python/pystack

#Create file "shared.env" and store it in top folder of the pystack working directory:
POSTGRES_USER=postgres_username
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=database_name

#Create file "pystack.env" and store it in top folder of the pystack working directory:
APP_SECRET_KEY=your_flask_hash_secret


#Next, deploy postgres
-------------------------------------
-------------POSTGRES
-------------------------------------
sudo docker rm --force pystack_db0 && \
sudo rm -fr $pystack_path/dbdata && \
sudo docker run --name pystack_db0 \
--restart unless-stopped \
--env-file=$pystack_path/shared.env \
-v $pystack_path/postgres/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
-v $pystack_path/dbdata:/var/lib/postgresql/data \
--network=pynet \
--hostname pystack_db0 \
-d postgres

#check it
docker exec -it pystack_db0 bash -c 'psql -U postgres pystack_db0 -c "select * from bulletin"'

#next, deploy flask and nginx
-------------------------------------
-------------FLASK & NGINX
-------------------------------------
cd $pystack_path/flask && \
sudo docker rm --force pystack_flask0 && \
sudo docker build . -t pystack_flask && \
sudo docker run -d \
-p 5000:5000 \
--env-file=$pystack_path/shared.env \
--env-file=$pystack_path/pyapp.env \
--restart unless-stopped \
--network=pynet \
--name pystack_flask0 \
pystack_flask && \
cd $pystack_path/nginx && \
sudo docker rm --force pystack_nginx0 && \
sudo docker build . -t pystack_nginx && \
sudo docker run -d -p 80:80 \
--network=pynet \
--restart unless-stopped \
--name pystack_nginx0 \
pystack_nginx

#if needed for debugging, do something like this to run on console
docker run -p 5000:5000 --rm --name pystack_flask0 pystack_flask

