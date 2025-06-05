class QuaterImaginary:
    """
    Klasa reprezentująca liczbę w bazie quater-urojonej.
    Operacje +, -, * realizowane są bezpośrednio na stringu str_repr.
    """

    def __init__(self, str_repr: str):
        self.str_repr = str_repr

    def __repr__(self) -> str:
        return f"{self.str_repr}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, QuaterImaginary):
            return NotImplemented
        return self.str_repr == other.str_repr

    def __add__(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        if not isinstance(other, QuaterImaginary):
            return NotImplemented
        return self.add(other)

    def __sub__(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        if not isinstance(other, QuaterImaginary):
            return NotImplemented
        return self.subtract(other)

    def __mul__(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        if not isinstance(other, QuaterImaginary):
            return NotImplemented
        return self.multiply(other)

    def add(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        a = list(map(int, self.str_repr[::-1]))
        b = list(map(int, other.str_repr[::-1]))
        n = max(len(a), len(b))
        a += [0]*(n-len(a))
        b += [0]*(n-len(b))

        result = [0]*(n+6)
        for i in range(n):
            result[i] += a[i] + b[i]
            if result[i] > 3:
                result[i] -= 4
                result[i+2] -= 1
            elif result[i] < 0:
                result[i] += 4
                result[i+2] += 1

        # normalizacja dalszych przeniesień
        for i in range(len(result)):
            while result[i] > 3:
                result[i] -= 4
                result[i+2] -= 1
            while result[i] < 0:
                result[i] += 4
                result[i+2] += 1

        # usuwanie wiodących zer
        while len(result)>1 and result[-1]==0:
            result.pop()
        return QuaterImaginary(''.join(map(str, result[::-1])))

    def subtract(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        a = list(map(int, self.str_repr[::-1]))
        b = list(map(int, other.str_repr[::-1]))
        n = max(len(a), len(b))
        a += [0]*(n-len(a))
        b += [0]*(n-len(b))

        result = [0]*(n+6)
        for i in range(n):
            result[i] += a[i] - b[i]
            if result[i] > 3:
                result[i] -= 4
                result[i+2] -= 1
            elif result[i] < 0:
                result[i] += 4
                result[i+2] += 1

        for i in range(len(result)):
            while result[i] > 3:
                result[i] -= 4
                result[i+2] -= 1
            while result[i] < 0:
                result[i] += 4
                result[i+2] += 1

        while len(result)>1 and result[-1]==0:
            result.pop()
        return QuaterImaginary(''.join(map(str, result[::-1])))

    def multiply(self, other: 'QuaterImaginary') -> 'QuaterImaginary':
        digits_a, zero_a = self._get_digits_and_point_pos(self.str_repr)
        digits_b, zero_b = self._get_digits_and_point_pos(other.str_repr)

        min_pow = -zero_a + -zero_b
        max_pow = (len(digits_a)-1-zero_a) + (len(digits_b)-1-zero_b)
        size = (max_pow - min_pow + 1) + 6
        result = [0]*size

        for i_b, db in enumerate(digits_b):
            if db==0: continue
            for i_a, da in enumerate(digits_a):
                idx = (i_a-zero_a + i_b-zero_b) - min_pow
                result[idx] += da*db

        # normalizacja
        for i in range(len(result)):
            while result[i] > 3:
                carry = result[i]//4
                result[i] %= 4
                result[i+2] -= carry
            while result[i] < 0:
                borrow = (-result[i]+3)//4
                result[i] += borrow*4
                result[i+2] += borrow

        # usuwanie zer i formatowanie
        while len(result)>1 and result[-1]==0:
            result.pop()
        total_zero = zero_a + zero_b
        s = ''.join(map(str, result[::-1]))
        if total_zero>0:
            pos = len(s)-total_zero
            s = s[:pos] + '.' + s[pos:]
        return QuaterImaginary(s.lstrip('0') or '0')

    def _get_digits_and_point_pos(self, s: str) -> tuple[list[int],int]:
        parts = s.split('.')
        frac = parts[1] if len(parts)>1 else ''
        whole = parts[0]
        digits = [int(d) for d in frac[::-1]] + [int(d) for d in whole[::-1]]
        return digits, len(frac)
