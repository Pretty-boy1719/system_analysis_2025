import json
from task import main


with open('функции-принадлежности-температуры.json', 'r', encoding='utf-8') as f:
    temp_membership_json = f.read()

with open('функции-принадлежности-управление.json', 'r', encoding='utf-8') as f:
    control_membership_json = f.read()

with open('функция-отображения.json', 'r', encoding='utf-8') as f:
    rules_json = f.read()

print("Test")
print("=" * 50)

test_cases = [
    (15.0, "холодно"),
    (20.0, "комфортно"),
    (23.0, "комфортно"),
    (26.0, "комфортно/жарко"),
    (28.0, "жарко")
]

for temp, desc in test_cases:
    result = main(temp_membership_json, control_membership_json, rules_json, temp)
    print(f"Температура {temp:4.1f}°C ({desc:25s}) -> Управление: {result:8.2f}")

print("=" * 50)
