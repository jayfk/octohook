[![Updates](https://pyup.io/repos/github/pyupio/octohook/shield.svg)](https://pyup.io/repos/github/pyupio/octohook/) [![Build Status](https://travis-ci.org/pyupio/octohook.svg?branch=master)](https://travis-ci.org/pyupio/octohook) [![codecov.io](https://codecov.io/github/pyupio/octohook/coverage.svg?branch=master)](https://codecov.io/github/pyupio/octohook?branch=master)

## About

Octohook is a server that listens for incoming webhooks, validates them and routes them to your code. The idea was to make it easier to write and deploy code that runs when something happens on your repo. Be it a new issue, a reverted commit or someone starring it.

### How it works

Octohook uses flask to serve incoming requests and to establish routes. When the server starts, it checks for files in the `repos/` folder, imports them and establishes a route to them by using the filename. Once a POST request hits the URL, the view function calls the appropiate function for the event in that module.


For example, if you create a file `repos/myrepo.py`, the server will listen for incoming webhooks at `/myrepo/`. When a webhook for the event `fork` hits `/myrepo/`, the `fork` function in `repo/myrepo.py` is called.

Or, if you have a repo called `foo` and you want to run some code on `pull_request` events you create a file `repos/foo.py` and implement a `pull_request(data)` in it. Your server now listens on `/foo/` and waits for hooks to come by.

## Get started (quick)

1. Clone the repo

        git clone https://github.com/pyupio/octohook.git

2. Add your code in `repos/whateveryouwant.py`.
  
3. Start the server

	**With vanilla python**

        mkvirtualenv octohook
        pip install -r requirements.txt
        export DEBUG=True
        python hook/hook.py
    
    **Or with docker**

        docker-compose -f dev.yml up 
    
4. Use ngrok during development to forward request to your local machine. The server listens on port `5000`. 



## Get started

First, clone the repo by running

    git clone https://github.com/pyupio/octohook.git
   
Now, take a look at the `repos/` folder. This is where incoming webhooks will be routed to. There's a file called `example.py` in that folder. Every function you see in there maps an event sent by Github. 

Move the file and name it eg. `myrepo.py`

    mv repos/example.py repos/myrepo.py
    
As an easy example to begin with we are going to listen to the `watch` event and print a message to the terminal once someone stars our repo. 

Open `myrepo.py` and delete all functions except for the `watch` function at the end of the file. We are going to add a simple print statement to the function that tells us who has starred the repo and how much stars the repo has in total.

    def watch(data):
        """Any time a User stars a Repository."""
        print("{user} just starred {repo_name}. The repo now has a total of {stars} stars".format(
            user=data["sender"]["login"],
            repo_name=data["repository"]["name"],
            stars=data["repository"]["watchers_count"]
        ))

Now we need to run the server. Octohook comes with built in docker support using docker-compose, and of course vanilla python. 

**Vanilla python**

    mkvirtualenv octohook
    pip install -r requirements.txt
    export DEBUG=True
    python hook/hook.py

**Or with docker**

	docker-compose -f dev.yml up    

You should see a warning telling you that you are running in `DEBUG` mode. That's because the `DEBUG` environment variable is set. There's no signature verification on `DEBUG`, take a look at [Security](###security) for more on that.

Since we are probably running on a local machine that isn't visible to Githubs servers, install [ngrok](https://ngrok.com/) that helps us to tunnel incoming webhooks to our dev machine.

Open a new terminal and run:

    ngrok 127.0.0.1:5000
    
*If you are using docker on OSX/Windows, replace `127.0.0.1` with the IP of your docker deamon. Run `docker-machine ip default` to get it.*

Create a new repo or use an existing one and go to click on `Settings` > `Webhooks & services` > `Add webhook`. 

Take a look at the terminal where you started `ngrok`, copy the forwarding URL into the Payload URL field and add `/myrepo/` to it, so that it looks like `http://783yk8fae.ngrok.com/myrepo/`. Leave the secret empty and make sure to click on *Send me everything*.

Now get back to your github repo. To trigger the `watch` event, click on the star button. (You might need to click twice if you already starred your repo).

The octohook server should now print

    jayfk just starred test-repo. The repo now has a total of 1 stars
    
And ngrok should tell you that it forwarded the request sucessfully

    POST /myrepo/                 200 OK
    
    
Not what you are seeing? Go to the `Webhooks & services` page again. And click on the webhook you just created. Check the `Recent Deliveries` Pane and check the `Response` tab to see the error.

## Security

Github signs the payload if you set a secret token during the creation of the webhook on the web interface. That's generally  a very good thing, because otherwise everyone could POST funny payloads to your server. 

Octohook verifies the signature by default and won't continue to process the request if it doesn't match. In fact, octohook will even refuse to start when the secret for a repo is not set.

To tell octohook the secret for your repo, you need set the environment variable `REPONAME_SECRET`. For example, if you have a file `repos/foo.py` you'll need to set the environment variable `FOO_SECRET`. If you have file `repos/bar.py`, you'll need to set `BAR_SECRET`.

The only exception where octohook won't verify incoming payloads, is when you set the `DEBUG` environment variable. That makes it easier during development, because you don't have to sign your payloads if you are developing.

## Deploy

When you are done with testing and you want to run that thing on a real server there's good news: Octohook comes with a docker-compose configuration that makes it easy to deploy your code to a live server.

The configuration uses nginx with a self signed certificate (that is auto generated during the build) and a gunicorn server that runs the code.

You can use whatever provider you prefer. For simplicity, we are going to use Digital Ocean. Make sure to check docker-machine`s [provider list](https://github.com/docker/machine/blob/master/docs/AVAILABLE_DRIVER_PLUGINS.md) if you want to use something else.  

    docker-machine create --driver digitalocean --digitalocean-access-token=<YOUR_DO_API_TOKEN> octohook

This creates a digital ocean droplet with 512mb for us, it takes a couple of minutes to run. 

In the meantime, open your `docker-compose.yml`. 

We need to set a secret for octohook to verify incoming webhooks. This is done through environment variables. The name of the environment variable depends on how you called the file you added. If you've added `myrepo.py`, you'll need to set `MYREPO_SECRET`. There's already a environment variable called `SOMEREPO_SECRET` defined. Replace that with yours.

Once docker-machine is ready, run:

    docker-machine ip octohook
    > 123.236.197.123
    
and copy the address, we need the it later to create the webhook. 
    
Now that we have the IP, switch the environment docker-machine is pointing to by running:

    eval $(docker-machine env octohook)
    
To push and build the stack on the server, run:

    docker-compose build
    

We are now ready to run the application on the virtual machine, type: 

    docker-compose up -d
    
to start the server in detached mode.

To check the logs, run:

    docker-compose logs
    
You should get an output similar to this

    hook_1  | [2016-02-19 08:56:12 +0000] [1] [INFO] Starting gunicorn 19.4.5
    hook_1  | [2016-02-19 08:56:12 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
    hook_1  | [2016-02-19 08:56:12 +0000] [1] [INFO] Using worker: sync
    hook_1  | [2016-02-19 08:56:12 +0000] [8] [INFO] Booting worker with pid: 8
    hook_1  | [2016-02-19 08:56:12 +0000] [9] [INFO] Booting worker with pid: 9
    hook_1  | [2016-02-19 08:56:12 +0000] [10] [INFO] Booting worker with pid: 10
    hook_1  | [2016-02-19 08:56:13 +0000] [11] [INFO] Booting worker with pid: 11
    
If you see an `AssertionError` popping up telling you that you don't have set the secret key, make sure you have set that correctly. Hit `CTRL+C`, change the secret key and run `docker-compose build` and `docker-compose up -d` again to rebuild and restart the server.    
    
Now, head over to your github repo and click on `Settings` > `Webhooks & services` > `Add webhook`

 - Payload URL is `https://<your_ip>/<your_repo>/`, for example `https://1.2.3.4/myrepo/`
 - Content type is `application/json`
 - Secret is the value of the secret key you set for that repo.  

Make sure to click `Disable SSL verification`. We need to do that because we are using a self signed certificate and Github isn't trusting our CA. That's perfectly fine since we just want that Github sends us all the payload over an encrypted connection.

Select which events you would like to be send to octohook and click on `Add webhook`.

Make sure that everything works by triggering an event you selected. Take a look at your logs, you should see an output similar to this:

    nginx_1 | 192.30.252.46 - - [19/Feb/2016:08:45:12 +0000] "POST /myrepo/ HTTP/1.1" 200 2 "-" "GitHub-Hookshot/21f57ba" "-"

 