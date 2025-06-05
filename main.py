# main.py

from JMinusOne import JMinusOne
from TwoJ import QuaterImaginary
from Binary import BinaryNumber

def quater_to_complex(qi: QuaterImaginary) -> complex:
    """
    Konwersja radix-(2j) na liczbę zespoloną.
    """
    z = 0+0j
    for power, digit in enumerate(qi.str_repr[::-1]):
        z += int(digit) * (2j)**power
    return z

def demo_jminusone():
    print("=== System radix-(j-1) ===")
    z1 = JMinusOne(real=2012, imag=0)
    z2 = JMinusOne(real=2, imag=2)

    for op, symbol in [(z1+z2, '+'), (z1-z2, '-'), (z1*z2, '*')]:
        # op to wynik typu JMinusOne, __repr__ wypisuje "a + bj"
        print(f"{z1} {symbol} {z2} \t= {op} \t= {op.binary}")
    print()

def demo_twoj():
    print("=== System radix-(2j) ===")
    qi1 = QuaterImaginary("1032")
    qi2 = QuaterImaginary("21")

    for func, symbol in [(lambda a, b: a+b, '+'),
                         (lambda a, b: a-b, '-'),
                         (lambda a, b: a*b, '*')]:
        result = func(qi1, qi2)
        cz = quater_to_complex(result)
        print(f"{qi1} {symbol} {qi2} \t= {cz.real:+.0f}{cz.imag:+.0f}j \t= {result}")
    print()

def demo_binary():
    print("=== System radix-(2) ===")
    bn1 = BinaryNumber("1101")   # 13
    bn2 = BinaryNumber("101")    # 5

    for func, symbol in [(lambda a, b: a+b, '+'),
                         (lambda a, b: a-b, '-'),
                         (lambda a, b: a*b, '*')]:
        result = func(bn1, bn2)
        # wynik w postaci int, a następnie 0j jako część urojona
        val = int(str(result), 2)
        print(f"{bn1} {symbol} {bn2} \t= {val:+.0f}+0j \t= {result}")
    print()

if __name__ == "__main__":
    demo_jminusone()
    demo_twoj()
    demo_binary()
