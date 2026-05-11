from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/") # / domowy adres                     # adres URL: http://localhost:5000/
def home(): #funkcje które mają się wykonać po wejściu
    return "Witaj w systemie monitoringu transakcji!"

@app.route("/hello")  #jakby podstrona                # GET /hello?name=Anna
def hello():
    name = request.args.get("name", "nieznajomy")   # odczytaj parametr query
    return f"Cześć, {name}!"

@app.route("/suma")
def suma():
    a = request.args.get("a", 0, type=float)
    b = request.args.get("b", 0, type=float)
    return f"suma {a} i {b} to {a+b}"

@app.route("/transaction/<tx_id>")    # GET /transaction/TX0042
def get_transaction(tx_id):
    return jsonify({"tx_id": tx_id, "status": "znaleziono"})

@app.route("/echo", methods=["POST"])  # akceptuj tylko POST
def echo():
    data = request.get_json()           # odczytaj ciało JSON
    return jsonify({
        "otrzymalem": data,
        "liczba_pol": len(data),
    })

@app.route("/iloczyn", methods=["POST"])
def iloczyn():
    data = request.get_json()
    return jsonify({
        "otrzymalem": data,
        "liczba_pol": len(data),
        "iloczyn": data[0]*data[1]
    })
    
# jak zaczyna się od @ to dekorator
if __name__ == "__main__": #uruchomienie serwera #te dwa podkreslniki to ze jakis obiekt pythona i nie modyfikowac
    app.run(host="0.0.0.0", port=5000)
