import binascii
import struct

def example(express, result=None):
    if result == None:
        result = eval(express)
        print(express, ' ==> ', result)

if __name__ == '__main__':

    print('整數之間的進制轉換:')
    print("10進制轉16進制", end=': ');example("hex(16)")
    print("16進制轉10進制", end=': ');example("int('0x10', 16)")
    print("類似的還有oct()， bin()")

    print('\n-------------------\n')

    print('字元串轉整數:')
    print("10進制字元串", end=": ");example("int('10')")
    print("16進制字元串", end=": ");example("int('10', 16)")
    print("16進制字元串", end=": ");example("int('0x10', 16)")

    print('\n-------------------\n')

    print('位元組串轉整數:')

