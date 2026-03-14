def wrapper(f):
    def fun(l):
        cleaned = []
        for number in l:
            digits = ''.join(c for c in number if c.isdigit())
            if digits.startswith(('8', '7', '0')) and len(digits) == 11:
                digits = digits[1:]
            
            if len(digits) == 10:
                cleaned.append(digits)
            else:
                cleaned.append(digits[-10:])
        
        sorted_numbers = sorted(cleaned)
    
        formatted = []
        for num in sorted_numbers:
            formatted.append(
                f"+7 ({num[0:3]}) {num[3:6]}-{num[6:8]}-{num[8:10]}"
            )
        return formatted
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')
