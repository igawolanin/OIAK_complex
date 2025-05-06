class JMinusOne:
    """
    klasa reprezentująca liczbę zespoloną w systemie o bazie (j-1)
    """
    
    def __init__(self, value=None, real=0, imag=0):
        """
        inicjalizacja liczby zespolonej
        
        args:
            value: reprezentacja binarna w bazie (j-1) jako string
            real: część rzeczywista liczby zespolonej
            imag: część urojona liczby zespolonej
        """
        if value is not None:
            self.binary = value
            self.real, self.imag = self._to_decimal()
        else:
            self.real = real
            self.imag = imag
            self.binary = self._to_binary()
    
    def __repr__(self):
        """
        reprezentacja tekstowa liczby zespolonej
        """
        if self.imag >= 0:
            return f"{self.real} + {self.imag}j"
        else:
            return f"{self.real} - {abs(self.imag)}j"
    
    def __add__(self, other):
        """
        dodawanie dwóch liczb zespolonych w bazie (j-1)
        """
        if isinstance(other, JMinusOne):
            result_binary = JMinusOne.add_numbers(self.binary, other.binary)
            return JMinusOne(value=result_binary)
        return NotImplemented
    
    def __sub__(self, other):
        """
        odejmowanie dwóch liczb zespolonych w bazie (j-1)
        """
        if isinstance(other, JMinusOne):
            negative_other = JMinusOne.multiply_numbers(other.binary, "11101")  # 11101 to -1 w bazie (j-1)
            result_binary = JMinusOne.add_numbers(self.binary, negative_other)
            return JMinusOne(value=result_binary)
        return NotImplemented

    def __mul__(self, other):
        """
        mnożenie dwóch liczb zespolonych w bazie (j-1)
        """
        if isinstance(other, JMinusOne):
            result_binary = JMinusOne.multiply_numbers(self.binary, other.binary)
            return JMinusOne(value=result_binary)
        return NotImplemented
    
    def __eq__(self, other):
        """
        porównanie dwóch liczb zespolonych
        """
        if isinstance(other, JMinusOne):
            return self.real == other.real and self.imag == other.imag
        return NotImplemented
    
    def _to_decimal(self):
        """
        konwersja z bazy (j-1) do postaci dziesiętnej
        """
        if self.binary == "0":
            return 0, 0
        
        # odwracamy string, aby indeks 0 odpowiadał najmniej znaczącej cyfrze
        bits = self.binary[::-1]
        
        real_part = 0
        imag_part = 0
        
        # obliczamy wartość każdej pozycji
        for i, bit in enumerate(bits):
            if bit == '1':
                # obliczamy (-1+j)^i
                power_real, power_imag = self._power_j_minus_1(i)
                real_part += power_real
                imag_part += power_imag
        
        return real_part, imag_part
    
    def _power_j_minus_1(self, power):
        """
        oblicza wartość (-1+j)^power
        
        returns:
            część rzeczywista, część urojona
        """
        # dla małych potęg mamy stałe wartości
        if power == 0:
            return 1, 0
        elif power == 1:
            return -1, 1
        elif power == 2:
            return 0, -2
        elif power == 3:
            return 2, 2
        else:
            # dla większych potęg używamy wzoru rekurencyjnego
            # (-1+j)^n = (-1+j)^(n-4) * (-2)
            quotient, remainder = divmod(power, 4)
            base_real, base_imag = self._power_j_minus_1(remainder)
            factor = (-4) ** quotient
            return base_real * factor, base_imag * factor
    
    def _to_binary(self):
        """
        konwersja z postaci dziesiętnej do bazy (j-1)
        """
        if self.real == 0 and self.imag == 0:
            return "0"
        
        # konwersja do bazy 4
        def to_base4(num):
            if num == 0:
                return [0]
            result = []
            n = abs(num)
            while n > 0:
                result.append(n % 4)
                n //= 4
            return result
        
        # konwersja do bazy -4
        def to_base_neg4(digits, is_negative):
            neg4 = []
            for i, d in enumerate(digits):
                if i % 2 == 1:  # nieparzyste pozycje negujemy
                    neg4.append(-d)
                else:
                    neg4.append(d)
            if is_negative:
                neg4 = [-x for x in neg4]  # negujemy wszystkie elementy
            return neg4
        
        # normalizacja cyfr
        def normalize(digits):
            """
            przekształca listę cyfr w bazie -4 do zakresu 0-3 z propagacją przeniesień
            """
            normalized = digits.copy()
            i=0
            while i < len(normalized):
                if normalized[i] < 0:
                    normalized[i] += 4
                    if i + 1 < len(normalized):
                        normalized[i+1] += 1
                    else:
                        normalized.append(1)
                    i = max(0, i-1)
                elif normalized[i] >= 4:
                    normalized[i] -=4
                    if i+1 < len(normalized):
                        normalized[i+1] -= 1
                    else:
                        normalized.append(-1)
                else:
                    i += 1
            return normalized
        
        # konwersja do CBNS
        def to_cbns(normalized):
            cbns_map = {
                0: "0000",
                1: "0001",
                2: "1100",
                3: "1101"
            }
            
            cbns = []
            for digit in normalized[::-1]:
                cbns.append(cbns_map[digit])
            
            # usuwamy wiodące zera
            result = "".join(cbns)
            result = result.lstrip("0")
            
            if not result:
                return "0"
            
            return result
        
        # konwersja części rzeczywistej
        real_base4 = to_base4(self.real)
        real_base_neg4 = to_base_neg4(real_base4, self.real < 0)
        real_normalized = normalize(real_base_neg4)
        real_cbns = to_cbns(real_normalized)

        # konwersja części urojonej
        imag_base4 = to_base4(self.imag)
        imag_base_neg4 = to_base_neg4(imag_base4, self.imag < 0)
        imag_normalized = normalize(imag_base_neg4)
        imag_cbns = to_cbns(imag_normalized)

        # jeśli mamy tylko część rzeczywistą
        if self.imag == 0:
            return real_cbns
        
        # jeśli mamy tylko część urojoną
        if self.real == 0:
            # mnożymy przez j (11 w bazie j-1)
            return JMinusOne.multiply_numbers(imag_cbns, "11")
        
        # jeśli mamy obie części
        imag_with_j = JMinusOne.multiply_numbers(imag_cbns, "11")  # 11 to j w bazie (j-1)
        return JMinusOne.add_numbers(real_cbns, imag_with_j)
    
    def add_numbers(num1, num2):
        # odwracamy stringi tak, aby indeks 0 odpowiadał najmniej znaczącej cyfrze
        a = list(map(int, num1[::-1]))
        b = list(map(int, num2[::-1]))
        
        # rezerwujemy dodatkowe miejsca dla przeniesień
        n = max(len(a), len(b))
        extra = 10  # dodatkowe miejsce na przeniesienia
        size = n + extra
        
        # inicjalizacja list na wynik oraz przeniesienia
        result = [0] * size
        carry = [0] * size
        
        # dodawanie pozycyjnie
        for i in range(size):
            # pobieramy cyfrę na pozycji i, jeśli poza zakresem, to 0
            a_digit = a[i] if i < len(a) else 0
            b_digit = b[i] if i < len(b) else 0
            
            # dodajemy cyfry z danej pozycji a i b oraz przeniesienie
            s = a_digit + b_digit + carry[i]
            
            # liczymy ile razy mieści się dwójka w sumie:
            # wynik dzielenia przez 2 to liczba przeniesień, a reszta to wynik na danej pozycji
            times = s // 2
            remainder = s % 2
            result[i] = remainder
            
            if times > 0:
                # dodajemy przeniesienia "110" do odpowiednich pozycji
                if i + 2 < size:
                    carry[i+2] += times
                if i + 3 < size:
                    carry[i+3] += times
        
        # usuwamy nadmiar zer z końca wyniku zaczynając od najbardziej znaczącej pozycji
        # znajdujemy ostatni indeks, gdzie wynik jest niezerowy
        last = size - 1
        while last > 0 and result[last] == 0:
            last -= 1
        
        # odczytujemy wynik od ostatniego indeksu do 0 i budujemy z tego stringa
        final_result = "".join(str(result[i]) for i in range(last, -1, -1))
        
        return final_result

    def multiply_numbers(num1, num2):
        """
        mnożenie dwóch liczb w bazie (j-1)
        """
        # obsługa przypadku mnożenia przez zero
        if num1 == "0" or num2 == "0":
            return "0"
        
        result = "0"

        # iterujemy po mnożniku (num2) – pamiętając, że indeks 0 to cyfra najmniej znacząca
        # dlatego odwracamy num2 by iterować od najmniej do najbardziej znaczącej
        rev_num2 = num2[::-1]
        for i, digit in enumerate(rev_num2):
            if digit == '1':
                # przesunięcie liczby num1 o i pozycji w lewo (dodanie zer)
                partial = num1 + "0" * i
                # suma dotychczasowego wyniku z iloczynem częściowym
                result = JMinusOne.add_numbers(result, partial)
        
        return result

# przykład użycia
if __name__ == "__main__":
    # tworzenie liczb zespolonych
    z1 = JMinusOne(value="1110000000001110000010000")  # 2012
    z2 = JMinusOne(value="111000")  # 2-2j

    print(f"{'zmienna':<10}| {'wartość':<20}| {'w bazie (j-1)':<30}")
    print('-'*65)
    print(f"{'z1':<10}| {str(z1):<20}| {z1.binary:<30}")
    print(f"{'z2':<10}| {str(z2):<20}| {z2.binary:<30}")

    # dodawanie
    z3 = z1 + z2
    print(f"{'z3=z1+z2':<10}| {str(z3):<20}| {z3.binary:<30}")

    # odejmowanie
    z4 = z1 - z2
    print(f"{'z4=z1-z2':<10}| {str(z4):<20}| {z4.binary:<30}")

    # mnożenie
    z5 = z1 * z2
    print(f"{'z5=z1*z2':<10}| {str(z5):<20}| {z5.binary:<30}")

    # tworzenie liczby z części rzeczywistej i urojonej
    z6 = JMinusOne(real=123, imag=-321)
    print(f"{'z6':<10}| {str(z6):<20}| {z6.binary:<30}")