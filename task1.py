def caching_fibonacci():
    cache = {}  # кеш для вже обчислених значень

    def fibonacci(n):
        # базові випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # якщо вже є в кеші — повертаємо без перерахунку
        if n in cache:
            return cache[n]

        # обчислюємо рекурсивно, зберігаємо в кеш і повертаємо
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci  # повертаємо внутрішню функцію (замикання)


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(fib(10))  # 55
    print(fib(15))  # 610