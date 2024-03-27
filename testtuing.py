from time import sleep

def tenteAlgumaCoisa(entrada: int):
    if entrada > 5:
        raise ValueError("po vai dar n, mt grande")
    else:
        print('tudo certo')
        


if __name__ == '__main__':
    tenteAlgumaCoisa(6)
    