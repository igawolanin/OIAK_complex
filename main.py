from JMinusOne import JMinusOne
from TwoJ import QuaterImaginary
from Binary import BinaryComplexNumber

def quater_to_complex(qi: QuaterImaginary) -> complex:
    z = 0 + 0j
    for power, digit in enumerate(qi.str_repr[::-1]):
        z += int(digit) * (2j)**power
    return z

def demo_jminusone():
    print("=== System radix-(j-1) ===")
    z1 = JMinusOne(real=2012, imag=0)
    z2 = JMinusOne(real=2, imag=2)

    for op, symbol in [(z1+z2, '+'), (z1-z2, '-'), (z1*z2, '*')]:
        print(f"{z1} {symbol} {z2} \t= {op} \t= {op.binary}")
    print()

def demo_twoj():
    print("=== System radix-(2j) ===")
    qi1 = QuaterImaginary("1032")
    qi2 = QuaterImaginary("21")

    def to_decimal_str(qi: QuaterImaginary) -> str:
        z = quater_to_complex(qi)
        return f"{int(z.real)} + {int(z.imag)}j"

    for func, symbol in [(lambda a, b: a + b, '+'),
                         (lambda a, b: a - b, '-'),
                         (lambda a, b: a * b, '*')]:
        result = func(qi1, qi2)
        dec1 = to_decimal_str(qi1)
        dec2 = to_decimal_str(qi2)
        dec_res = to_decimal_str(result)

        bin1 = qi1.str_repr
        bin2 = qi2.str_repr
        bin_res = result.str_repr

        print(f"{dec1} {symbol} {dec2} \t= {bin1} {symbol} {bin2}j \t= {bin_res}")
    print()


def binary_to_complex(bc: BinaryComplexNumber) -> complex:
    real = int(bc.real, 2)
    imag = int(bc.imag, 2)
    return complex(real, imag)

def demo_binary():
    print("=== System radix-(2) (liczby zespolone) ===")
    bn1 = BinaryComplexNumber("1101", "10")   # 13 + 2j
    bn2 = BinaryComplexNumber("101", "1")     # 5 + 1j

    def format_decimal(real: int, imag: int) -> str:
        real_str = f"{real}"
        imag_str = f"{imag}j" if imag < 0 else f"+{imag}j"
        return f"{real_str}{imag_str}"

    def to_decimal_str(bc: BinaryComplexNumber) -> str:
        real = int(bc.real, 2)
        imag = int(bc.imag, 2)
        return format_decimal(real, imag)

    def to_binary_str(bc: BinaryComplexNumber) -> str:
        return f"{bc.real} + {bc.imag}j"

    for func, symbol in [(lambda a, b: a + b, '+'),
                         (lambda a, b: a - b, '-'),
                         (lambda a, b: a * b, '*')]:
        result = func(bn1, bn2)
        dec1 = to_decimal_str(bn1)
        dec2 = to_decimal_str(bn2)
        real_res = int(result.real, 2)
        imag_res = int(result.imag, 2)
        dec_res = format_decimal(real_res, imag_res)

        bin1 = to_binary_str(bn1)
        bin2 = to_binary_str(bn2)
        bin_res = to_binary_str(result)

        print(f"{bin1} {symbol} {bin2}\t= {dec_res}   \t= {bin_res}")
    print()

if __name__ == "__main__":
    demo_jminusone()
    demo_twoj()
    demo_binary()
