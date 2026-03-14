from functools import wraps
from datetime import datetime
import os


def function_logger(logfile):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()

            result = func(*args, **kwargs)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            lines = [
                func.__name__,
                start_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                str(args),
                str(kwargs) if kwargs else '{}',
                str(result) if result is not None else '-',
                end_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                str(duration)
            ]
            with open(logfile, 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n\n')
            
            return result
        
        return wrapper
    
    return decorator


@function_logger("test.log")
def greeting_format(name, greeting="Hello"):
    return f"{greeting}, {name}!"


if __name__ == "__main__":
    if os.path.exists("test.log"):
        os.remove("test.log")
    
    print(greeting_format("John"))
    print(greeting_format("Anna", greeting="Привет"))
    print(greeting_format(name="Мария", greeting="Добрый день"))