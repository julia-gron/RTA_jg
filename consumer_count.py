from kafka import KafkaConsumer
from collections import Counter
import json

# Konfiguracja konsumenta
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='aggregation-group-julia'
)

# Nasz "stan" (pamięć programu)
store_counts = Counter()  # Licznik transakcji per sklep
total_amount = {}        # Suma kwot per sklep
msg_count = 0            # Globalny licznik wiadomości

print("Rozpoczynam agregację stanową (per sklep)...")

for message in consumer:
    tx = message.value
    store = tx['store']
    amount = tx['amount']
    
    # 1. Zwiększamy licznik dla danego sklepu
    store_counts[store] += 1
    
    # 2. Dodajemy kwotę do sumy dla danego sklepu
    total_amount[store] = total_amount.get(store, 0) + amount
    
    # Zwiększamy licznik wszystkich odebranych wiadomości
    msg_count += 1
    
    # 3. Co 10 wiadomości wypisz tabelę
    if msg_count % 10 == 0:
        print(f"\n--- RAPORT (po {msg_count} wiadomościach) ---")
        print(f"{'Sklep':<15} | {'Liczba':<8} | {'Suma':<10} | {'Średnia':<8}")
        print("-" * 50)
        
        for s in store_counts:
            count = store_counts[s]
            suma = total_amount[s]
            srednia = suma / count
            print(f"{s:<15} | {count:<8} | {suma:<10.2f} | {srednia:<8.2f}")