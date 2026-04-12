from kafka import KafkaConsumer
from collections import defaultdict
import json

# Konfiguracja konsumenta
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='stats-group-julia'
)

# Inicjalizacja stanu: dla każdej nowej kategorii tworzymy słownik startowy
category_stats = defaultdict(lambda: {
    'count': 0,
    'total_revenue': 0.0,
    'min_amount': float('inf'), # Startujemy od nieskończoności, żeby każda kwota była mniejsza
    'max_amount': float('-inf') # Startujemy od minus nieskończoności
})

msg_count = 0

print("Rozpoczynam zbieranie statystyk per kategoria...")

for message in consumer:
    tx = message.value
    cat = tx['category']
    amt = tx['amount']
    
    # Pobieramy (lub tworzymy) statystyki dla aktualnej kategorii
    stats = category_stats[cat]
    
    # 1. Liczba transakcji
    stats['count'] += 1
    
    # 2. Łączny przychód
    stats['total_revenue'] += amt
    
    # 3. Min kwota
    if amt < stats['min_amount']:
        stats['min_amount'] = amt
        
    # 4. Max kwota
    if amt > stats['max_amount']:
        stats['max_amount'] = amt
        
    msg_count += 1
    
    # Co 10 wiadomości wypisz raport
    if msg_count % 10 == 0:
        print(f"\n--- STATYSTYKI KATEGORII (po {msg_count} wiadomościach) ---")
        header = f"{'Kategoria':<15} | {'Liczba':<7} | {'Suma':<10} | {'Min':<8} | {'Max':<8}"
        print(header)
        print("-" * len(header))
        
        for category, s in category_stats.items():
            print(f"{category:<15} | {s['count']:<7} | {s['total_revenue']:<10.2f} | {s['min_amount']:<8.2f} | {s['max_amount']:<8.2f}")