def add_numbers(num1: str, num2: str) -> str:
    # odracamy stringi tak, aby indeks 0 odpowiadał najmniej znaczącej cyfrze
    a = list(map(int, num1[::-1]))
    b = list(map(int, num2[::-1]))
    
    # rezerwujemy dodatkowe miejsca dla przeniesień.
    n = max(len(a), len(b))
    extra = 10
    size = n + extra
    
    # inicjalizacja list na wynik oraz przeniesienia
    result = [0] * size
    carry = [0] * size
    
    # dodawanie pozycyjnie
    for i in range(size):
        # pobieramy cyfrę na pozycji i, jeśli poza zakresem, to 0.
        a_digit = a[i] if i < len(a) else 0
        b_digit = b[i] if i < len(b) else 0
        
        # dodajemy cyfry z na danej pozycji a i b oraz przeniesienie
        s = a_digit + b_digit + carry[i]

        # liczymy ile razy mieści się dwójka w sumie:
        # wynik dzielenia przez 2 to liczba przeniesień, a reszta to wynik na danje pozycji 
        times = s // 2
        remainder = s % 2
        result[i] = remainder
        if times > 0:
            # dodajemy przeniesienia "110" do odpowiednich pozycji
            if i + 2 < size:
                carry[i+2] += times
            if i + 3 < size:
                carry[i+3] += times

    # usuamy nadmiar zer z końca wyniku zaczynając od najbardziej znaczącej pozycji oraz
    # znajdujemy ostatni indeks, gdzie wynik jest niezerowy.
    last = size - 1
    while last > 0 and result[last] == 0:
        last -= 1
    final_result = "".join(str(result[i]) for i in range(last, -1, -1)) # odczytujemy wynik od ostatniego indeksu do 0 i budujemy z tego stringa
    return final_result


def multiply_numbers(num1: str, num2: str) -> str:
    result = "0"

    # iterujemy po mnożniku (num2) – pamiętając, że indeks 0 to cyfra najmniej znacząca.
    # dlatego odwracamy num2 by iterować od najmniej do najbardziej znaczącej.
    rev_num2 = num2[::-1]
    for i, digit in enumerate(rev_num2):
        if digit == '1':
            partial = num1 + "0" * i # przesunięcie liczby num1 o i pozycji w lewo
            result = add_numbers(result, partial) # suma dotychczasowego wyniku z iloczynem częściowym
    return result


# testy
import unittest

class TestNumeralSystemOperations(unittest.TestCase):
    def test_addition_example(self):
        # (101)_{j-1} + (1)_{j-1} = (111000)_{j-1}.
        A = "101"
        B = "1"
        self.assertEqual(add_numbers(A, B), "111000")
    
    def test_addition_with_carry_chain(self):
        # sprawdzenie wielokrotnych przeniesień (1101)_{j-1} + (1011)_{j-1} = (111011010)_{j-1}
        A = "1101"
        B = "1011"
        result1 = add_numbers(A, B)
        result2 = add_numbers(B, A)
        self.assertEqual(result1, "111011010")
        # sprawdzenie czy A + B = B + A
        self.assertEqual(result1, result2)
    
    def test_multiplication_example(self):
        # (11)_{j-1} * (101)_{j-1}: (1111)_{j-1}.
        X = "11"
        Y = "101"
        expected = "1111"
        self.assertEqual(multiply_numbers(X, Y), expected)
    
    def test_multiplication_with_zero(self):
        # mnożenie przez zero.
        self.assertEqual(multiply_numbers("101101", "0"), "0")
        self.assertEqual(multiply_numbers("0", "1101"), "0")
    
    def test_combined_operations(self):
        # sprawdzamy czy mnożenie przez "1" daje tę samą liczbę.
        for number in ["0", "1", "101", "111000"]:
            self.assertEqual(multiply_numbers(number, "1"), number)
            

if __name__ == "__main__":
    unittest.main()
