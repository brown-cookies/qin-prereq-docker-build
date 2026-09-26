# Dockerfile Note

I decided to use this sequence, just like the drill before, for the caching mechanics.
copy first the requirements.txt then run pip install so that it will be cached, since it rarely changes, 
instead of copying all, a single change on any other file makes the cached invalidated and re-run the
time consuming pip install. Also it was mention `After a one-line change to app.py, the rebuild is timed, and the step that installs your dependencies has to come from the build cache rather than run again.` so this decision passes that mark.


# Compose Note

This setup first starts the container db before the container app because container app depends on container db, then it app waits db to be healthy before starting it up, this was done to make sure that the app can access and container 
db and make sql queries.



# Anything that I could not get working 

I'll be honest, I don't know how to use http.server package so I had to be creative and use drill 4 as a template, then update
the app to complete the interface. My first mistake is forgetting to update my sql queries on each endpoints, I renamed 
the table but forgot to update my endpoint query to match that table, second, the requirement was to return a json, my initial
app returns content/type text/plain with string containing json, so I had to go back to material-fim/http depot_api.py on 
how to achieve that it works. It works now.
