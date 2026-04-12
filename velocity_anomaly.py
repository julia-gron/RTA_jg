from kafka import KafkaConsumer
from collections import defaultdict
from datetime import datetime, timedelta
import json

# Konfiguracja konsumenta
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='anomaly-detector-julia'
)

# Pamięć: user_id -> lista timestampów ostatnich transakcji
user_windows = defaultdict(list)

print("System wykrywania anomalii prędkości aktywny...")

for message in consumer:
    tx = message.value
    user_id = tx['user_id']
    # Zamieniamy tekstowy timestamp na obiekt czasu
    now = datetime.fromisoformat(tx['timestamp'])
    
    # 1. Dodajemy aktualny czas do historii użytkownika
    user_windows[user_id].append(now)
    
    # 2. Usuwamy z historii czasy starsze niż 60 sekund
    limit_time = now - timedelta(seconds=60)
    user_windows[user_id] = [t for t in user_windows[user_id] if t > limit_time]
    
    # 3. Sprawdzamy warunek zadania (więcej niż 3 transakcje)
    transaction_count = len(user_windows[user_id])
    if transaction_count > 3:
        print(f"⚠️ ALERT: Anomalia prędkości! Użytkownik {user_id}")
        print(f"Wykonano {transaction_count} transakcji w ciągu ostatnich 60 sekund.")
        print(f"Ostatnia transakcja: {tx['tx_id']} | Kwota: {tx['amount']} PLN")
        print("-" * 30)