class BinaryComplexNumber:
    """
    Klasa reprezentująca liczbę zespoloną w postaci binarnej.
    Zarówno część rzeczywista, jak i urojona są binarnymi stringami.
    """

    def __init__(self, real: str, imag: str = '0'):
        self.real = real.lstrip('0') or '0'
        self.imag = imag.lstrip('0') or '0'

    def __repr__(self):
        return f"BinaryComplexNumber(real='{self.real}', imag='{self.imag}')"

    def __str__(self):
        return f"{self.real} + {self.imag}j"

    def __eq__(self, other):
        if not isinstance(other, BinaryComplexNumber):
            return NotImplemented
        return self.real == other.real and self.imag == other.imag

    def __add__(self, other: 'BinaryComplexNumber') -> 'BinaryComplexNumber':
        real_part = add_binary(self.real, other.real)
        imag_part = add_binary(self.imag, other.imag)
        return BinaryComplexNumber(real_part, imag_part)

    def __sub__(self, other: 'BinaryComplexNumber') -> 'BinaryComplexNumber':
        real_part = subtract_binary(self.real, other.real)
        imag_part = subtract_binary(self.imag, other.imag)
        return BinaryComplexNumber(real_part, imag_part)

    def __mul__(self, other: 'BinaryComplexNumber') -> 'BinaryComplexNumber':
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        ac = multiply_binary(self.real, other.real)
        bd = multiply_binary(self.imag, other.imag)
        ad = multiply_binary(self.real, other.imag)
        bc = multiply_binary(self.imag, other.real)

        real_part = subtract_binary(ac, bd)
        imag_part = add_binary(ad, bc)
        return BinaryComplexNumber(real_part, imag_part)


def add_binary(a: str, b: str) -> str:
    """
    Dodaje dwa binarne napisy a i b, zwraca sumę w postaci binarnej.
    """
    # Dopasowanie długości przez dopełnienie zerami z lewej
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    carry = 0
    result = []
    # Przechodzimy od najmniej znaczącego bitu
    for i in range(max_len - 1, -1, -1):
        total = carry + int(a[i]) + int(b[i])
        bit = total % 2
        carry = total // 2
        result.append(str(bit))
    if carry:
        result.append('1')
    # Wynik odwracamy, usuwamy wiodące zera
    return ''.join(reversed(result)).lstrip('0') or '0'


def twos_complement(b: str, bits: int) -> str:
    """
    Zwraca dwójkowe dopełnienie napisu b w długości bits.
    """
    # Inwersja bitów
    inverted = ''.join('1' if bit == '0' else '0' for bit in b.zfill(bits))
    # Dodanie 1
    return add_binary(inverted, '1').zfill(bits)


def subtract_binary(a: str, b: str) -> str:
    """
    Odejmowanie a - b przez dodanie dwójkowego dopełnienia b.
    """
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    # Dwójkowe dopełnienie b w tej samej długości
    b_comp = twos_complement(b, max_len)
    sum_ab = add_binary(a, b_comp)
    # Jeżeli powstało przepełnienie, usuwamy najstarszy bit
    if len(sum_ab) > max_len:
        sum_ab = sum_ab[1:]
    return sum_ab.lstrip('0') or '0'


def multiply_binary(a: str, b: str) -> str:
    """
    Mnożenie dwóch liczb binarnych a i b przez algorytm długiego mnożenia.
    """
    result = '0'
    # Przechodzimy po bitach b od końca (LSB)
    for i, bit in enumerate(reversed(b)):
        if bit == '1':
            # Dodajemy a przesunięte o i miejsc w lewo
            partial = a + '0' * i
            result = add_binary(result, partial)
    return result.lstrip('0') or '0'