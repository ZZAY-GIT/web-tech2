def fun(s):
    if '@' not in s:
        return False
    
    username, rest = s.split('@', 1)
    
    if '.' not in rest:
        return False
    
    website, extension = rest.rsplit('.', 1)
    
    
    if not username:
        return False
    if not all(c.isalnum() or c in '-_' for c in username):
        return False
    
    if not website:
        return False
    if not all(c.isalnum() for c in website):
        return False
    
    if not extension:
        return False
    if not (1 <= len(extension) <= 3):
        return False
    if not extension.isalpha():
        return False
    
    return True


def filter_mail(emails):
    return list(filter(fun, emails))


if __name__ == '__main__':
    n = int(input())
    emails = []
    for _ in range(n):
        emails.append(input())
    
    filtered_emails = filter_mail(emails)
    filtered_emails.sort()
    print(filtered_emails)