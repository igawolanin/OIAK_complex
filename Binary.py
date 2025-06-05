class BinaryNumber:
    """
    Klasa reprezentująca nieujemną liczbę binarną jako string.
    Operacje +, -, * realizowane są na poziomie stringów
    przy użyciu funkcji add_binary, subtract_binary, multiply_binary.
    """

    def __init__(self, value: str):
        """
        Args:
            value: binarny string, np. "1011". 
                   Wiodące zera są automatycznie usuwane.
        """
        # zachowaj '0' gdy całość to zera
        self.value = value.lstrip('0') or '0'

    def __repr__(self) -> str:
        return f"BinaryNumber('{self.value}')"

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other) -> bool:
        if not isinstance(other, BinaryNumber):
            return NotImplemented
        return self.value == other.value

    def __add__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        if not isinstance(other, BinaryNumber):
            return NotImplemented
        result = add_binary(self.value, other.value)
        return BinaryNumber(result)

    def __sub__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        if not isinstance(other, BinaryNumber):
            return NotImplemented
        result = subtract_binary(self.value, other.value)
        return BinaryNumber(result)

    def __mul__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        if not isinstance(other, BinaryNumber):
            return NotImplemented
        result = multiply_binary(self.value, other.value)
        return BinaryNumber(result)

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