import time
import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis-lb', port=6379)
#def
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def multiple(m, n):
    return 'The hit numner is divisible by 10! Madhim!' if m % n == 0 else "" #else False

#web
@app.route('/')
def hit():
    count = get_hit_count() #try 5 times to increment a count and reg it to redis
    debugTenHits = multiple(count, 10) #count divided by 10 
    return render_template("index.html", count=count, debugTenHits=debugTenHits)
#return ('This page has been visited %i times since deployment.\n' % int(count) + debugTenHits ) #'debug level is %s .' % str(debug) )

@app.route('/reset') #either this reset url or an Ajax + js function to reset the counter without refreshing. Ze ma yesh
def reset_hits():
    cache.set('hits', 0)
    return render_template("reset.html", count="0", debugTenHits="go back and refresh you page")

if __name__ == "__main__":
    app.run(host="0.0.0.0")

