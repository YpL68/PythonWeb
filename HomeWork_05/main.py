from os import cpu_count
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool


def factorize(number_list: list) -> list:
    return list(map(factor, number_list))


def factorize_futures(number_list: list) -> list:
    with ProcessPoolExecutor(cpu_count()) as executor:
        result = list(executor.map(factor, number_list))
    return result


def factorize_pool(number_list: list) -> list:
    with Pool(cpu_count()) as pool:
        result = list(pool.map(factor, number_list))
    return result


def factor(num) -> list:
    result = []
    divisor = 1
    while divisor * divisor <= num:
        if num % divisor == 0:
            result.append(divisor)
            if divisor != num // divisor:
                result.append(num // divisor)
        divisor += 1
    result.sort()
    return result


def main():
    num_list = [256, 128]
    print(factorize(num_list))
    print(factorize_futures(num_list))
    print(factorize_pool(num_list))
