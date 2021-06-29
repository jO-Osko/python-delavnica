# Mypy in general

# Generatorji
def fib(a=0, b=1):
    while 1:
        r = yield a
        a, b = b, a + b
        if r and r > 10:
            a = 0
        print("rr", r)


def take_x(num, f):
    try:
        it = iter(f)
    except TypeError:
        it = f()
    for _ in range(num):
        try:  # Try catch dodaj pozneje
            yield next(it)
        except StopIteration:
            return


f = fib()
for j in range(10):
    print(next(f))

ff = take_x(10, fib)

print(list(ff))
print(list(take_x(100, take_x(10, fib))))

f = fib()
next(f)
print(f.send(10))
print(f.send(11))
print(f.send(12))
print(f.send(13))
l = (list(take_x(100, f)))
print(l)

# Vaja: Ki jo lahko vmes nastavimo na poljubno stanje

# Nested exceptions

# Dva custom classa + prikaz