import random
import math

def circle_square_mk(r, n):
    if r <= 0:
        return 0.0
    inside = 0
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        
        if x*x + y*y <= r*r:
            inside += 1
    square = (inside / n) * (4 * r * r)
    return square


if __name__ == "__main__":
    r = 5.0
    exact = math.pi * r * r
    print(f"Точная площадь (π·r²) = {exact:.6f}\n")
    
    print(" n          |  оценка Монте-Карло  |  абсолютная погрешность  |  относительная погрешность")
    print("-" * 85)
    
    for n in [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]:
        approx = circle_square_mk(r, n)
        abs_err = abs(approx - exact)
        rel_err = abs_err / exact * 100 if exact != 0 else 0
        print(f"{n:10d} | {approx:18.6f} | {abs_err:20.6f} | {rel_err:18.4f}%")