from flask import Flask

app = Flask(__name__)

@app.route("/") # / domowy adres                     # adres URL: http://localhost:5000/
def home(): #funkcje które mają się wykonać po wejściu
    return "Witaj w systemie monitoringu transakcji!"

@app.route("/hello")  #jakby podstrona                # GET /hello?name=Anna
def hello():
    name = request.args.get("name", "nieznajomy")#, type="string" domyślny)   # odczytaj parametr query
    return f"Cześć, {name}!"


# jak zaczyna się od @ to dekorator
if __name__ == "__main__": #uruchomienie serwera #te dwa podkreslniki to ze jakis obiekt pythona i nie modyfikowac
    app.run(host="0.0.0.0", port=5000)
