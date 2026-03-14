n, m = map(int, input().split())

items = []

for _ in range(m):
    name, weight, value = input().split()
    weight = int(weight)
    value = int(value)
    items.append((name, weight, value, value / weight if weight > 0 else 0))

items.sort(key=lambda x: x[3], reverse=True)

remaining = n
result = []

for name, w, v, density in items:
    if remaining <= 0:
        break

    if w <= remaining:
        result.append((name, float(w), float(v)))
        remaining -= w
    else:
        take_weight = remaining
        take_value = remaining * density
        result.append((name, take_weight, take_value))
        remaining = 0

result.sort(key=lambda x: x[2], reverse=True)

for name, weight, value in result:
    print(f"{name} {weight:.2f} {value:.2f}")