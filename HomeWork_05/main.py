from os import cpu_count
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool
from time import time


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

    a, b, c, d = factorize([128, 255, 99999, 10651060])

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]

    num_list = [1283244343436, 2554565464778, 9999976761212, 4657465856767, 92676475678]

    t_start = time()
    factorize(num_list)
    print(f"Syn time - {time() - t_start}")

    t_start = time()
    factorize_futures(num_list)
    print(f"Futures time - {time() - t_start}")

    t_start = time()
    factorize_pool(num_list)
    print(f"Pool time - {time() - t_start}")


if __name__ == '__main__':
    main()
