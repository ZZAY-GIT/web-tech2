adult_sum = 0.0
pensioner_sum = 0.0
child_sum = 0.0

with open('products.csv', encoding='utf-8') as f:
    next(f)
    
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(',')
        
        if len(parts) < 4:
            continue
            
        adult = float(parts[1])
        pensioner = float(parts[2])
        child = float(parts[3])
        
        adult_sum += adult
        pensioner_sum += pensioner
        child_sum += child
            
print(f"{adult_sum:.2f} {pensioner_sum:.2f} {child_sum:.2f}")