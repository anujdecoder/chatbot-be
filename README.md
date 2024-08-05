# Hey👋, I'm Ava-server

I'm a chatbot-server implement in Python3 using FastAPI.

I have been deployed using GCP AppEngine and can be
accessed at: [https://chatbot-be.ew.r.appspot.com/docs](https://chatbot-be.ew.r.appspot.com/docs)

An online demo of the app can be found at [https://ava-chatbot-f2551.web.app/](https://ava-chatbot-f2551.web.app/).

## Salient Features

* **Google Authentication** - The app uses [Firebase](https://firebase.google.com/) for authenticating each request.
* **Persistence** - Your entire conversation with Ava is stored
  in [Firestore database](https://firebase.google.com/docs/firestore).
* **Restful** - Server is implemented using FastAPI and follows REST Architecture

Take a look at [Ava](https://ava-chatbot-f2551.web.app/).

### Project setup:

To run the code in local machine, you need to add `keys.json` in root folder.

`keys.json` will be provided by Firestore Database when you setup the project in Datastore mode. It contains secrets for
accessing firebase APIs

In the project directory, run:

* `pip3 install -r requirements.txt` To install the dependencies
* `fastapi dev main.py ` To run the project. Open [http://localhost:8000/docs](http://localhost:8000/docs) to view docs
  in the browser.
* `python3 main.py` To run and debug the application

### Limitations/Features missing:

I feel following features are missing from the app that could not be implemented because of time constraints

* **Testing**  - Could not explore testing as I am new to python
* **Logging** - Exception handling and logging is not satisfactory 