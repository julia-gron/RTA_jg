from kafka import KafkaConsumer
import json

# Konfiguracja konsumenta
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Nasłuchuję na duże transakcje (amount > 3000)...")

for message in consumer:
    # 1. Pobieramy dane transakcji (już jako słownik dzięki value_deserializer)
    tx = message.value
    
    # 2. Sprawdzamy warunek z zadania
    if tx['amount'] > 3000:
        # 3. Wypisujemy alert w wymaganym formacie
        print(f"ALERT: {tx['tx_id']} | {tx['amount']:.2f} PLN | {tx['store']} | {tx['category']}")