from kafka import KafkaConsumer
import json

# Konfiguracja konsumenta
# UWAGA: Używamy nowego group_id, żeby ten konsument działał 
# niezależnie od tego z zadania 3.1.
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='enrichment-group-julia'
)

print("Rozpoczynam wzbogacanie transakcji o poziom ryzyka...")

for message in consumer:
    tx = message.value
    
    # Logika transformacji - wyznaczamy poziom ryzyka
    if tx['amount'] > 3000:
        risk = "HIGH"
    elif tx['amount'] > 1000:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    
    # WZBOGACENIE: Dodajemy nowe pole do słownika
    tx['risk_level'] = risk
    
    # Wypisujemy wynik (cały słownik z nowym polem)
    print(f"ENRICHED: {tx}")