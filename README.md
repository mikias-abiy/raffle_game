# Live TikTok Raffle Game

## 1. What is Live TikTok Raffle Game ?

This a self hosted raffle game that a live streamer could play with it's viewers. Where there will be a specific gift that is eligible for the raffle and when a user gifts that specific type of gift they will enter the raffle list and after the gift number has reached some point then the game will choose a user randomly from the eligible ones. And then the collected gift will be sent to that user.

## 2. Installation


First Clone the repo using this command.
```
git clone https://github.com/mikias-abiy/raffle_game.git
```

Then, Navigate to the directory you cloned.
```
cd raffle_game
```

Then host the client page with a simple http python server.
```
cd client
python3 -m http.server 3000
```

Then file up a browser and enter this link in the URL section `localhost:3000`.
If you followed the steps successfuly you should be greet with this page.

![Landing Page](/images/landing_page.png)

If all is good we are gonna make our front end a wait little until we setup our backend.

Then go ahead and open another terminal 
Then run the backend script with this simple steps. Assuming you are in the cloned directory.
First navigate to the server directory
```
cd server
```
Then create a python virtual enviroment. It's recommended to use virtual enviroment to not mess with the version of other projects dependencies (but keep in mind this optional)
```
python3 -m venv .venv
```

Then activate the virtual enviroment by executing this command (assuming you are using linux)
you can look the documentation for venv [here](https://docs.python.org/3/library/venv.html).
```
. .venv/bin/activate
```

Then, install all the necessary third party libraries by executing the following command.
```
pip install -r server/requirements.txt
```

Finally run the app script with this command.
```
python3 app.py
```

## 3. Configuring The Game Setting

There are three variable you can configure in this game.
You can configure this settings here: `raffle_game/server/raffle_config.py`

* `RAFFLE_GIFT_TYPE`: Type of gift is eligible to enter the game

* `MINIMUM_GIFT_AMOUNT`: Minimun amount of gift a user can gift to be eligible for the game.

* `MIN_PARTICIPANT`: Minimum number of participants.

## 4. How To Play

Go to the page you've host on the installation step. Enter the user name you are using to live stream.
Then you'll be greated with a page like this.

![Game Page](/image/game_page.png)

Have a Great time playing this game with your viewers.

### Thank You