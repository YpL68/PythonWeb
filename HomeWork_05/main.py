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
    # num_list = [128, 255, 99999, 10651060]
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
