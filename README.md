# Counter API with Python and Flask
This repo contains files needed to create an API using Python and Flask, in order to count webpage hits. The application is bundled into a container and deployed with docker-compose. The backend database is Redis.

# functionality

Description: Retrives and displays number of hits for the current deployment. Every 10 hits an extra message is displayed. A reset button leads to a reset/ url and resets the counter.

I didn't go into volumes, the data remains in the redis container until it is deleted. I didn't go into a "no refresh" option for the reset, because that would have required Ajax and js and started making the reset button extra complicated, but here are some examples: https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event

Request:       `GET /`  (Browse to localhost (port 80, not 5000) or in cli run `curl localhost`)

Response:     `HTTP/1.1 200 OK`
e.g: `I have been hit 9 times since deployment.`

Request:       `GET /reset` (Press the "Reset" button or Browse to localhost/reset or in cli run `curl localhost/reset`)

Response:     `HTTP/1.1 200 OK`
e.g: `Counter was resetit.`

# Building/testing steps

Download/pull this repository:
`git clone https://github.com/nashpaz123/hit-counter.git`

Go to the newly created directory
`cd hit-counter`

The docker-compose builds and tags the docker images before running the containers.

1. run `docker-compose up -d `

2. Browse to localhost (port 80, not 5000) , refresh 10 times, press the reset button and the go back button. 
In cli run ` curl localhost`, or `curl localhost\reset` to reset the counter.

3. Debug by running: `docker-compose ps`
    Name                     Command               State          Ports        
    ---------------------------------------------------------------------------------
    hit-counter_redis-lb_1   docker-entrypoint.sh redis ...   Up      6379/tcp            
    hit-counter_myapp_1      python ./app.py                  Up      0.0.0.0:80->5000/tcp

and `docker logs hit-counter_myapp_1`
    
### Making changes

If you'd like to make changes it's easiest to pipeline your changes like so:

`docker-compose down && docker rmi -f hit-counter_myapp && vim app.py` #This will take down the composition, remove the hit-counter_myapp image, and edit the app file.
`docker-compose up -d && sleep 2 && curl localhost` #This will bring up the composition, creating the hit-counter_myapp image (because we've removed it in the previous step) and 

`docker-compose up -d && sleep 2 && curl localhost` #This will bring up the composition, creating the hit-counter_myapp image (because we've removed it in the previous step) , wait for a couple of shniyot and run sanity.

In a full pipeline the build process can be done in a seperate stage. In prod the docker-compose.yaml file must not contain a build portion.
