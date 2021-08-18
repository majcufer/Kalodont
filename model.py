import random


NE_OBSTAJA = 'E'
NI_USTREZNA = 'A'
ZE_UPORABLJENA = 'U'
ZMAGA = 'W'
PORAZ = 'L'


class Igra:
    def __init__(self, geslo=None):
        self.uporabljene_besede = []
        self.geslo = geslo

    def obstaja(self):
        return self.geslo in bazen_besed

    def dodaj_na_seznam(self):
        return self.uporabljene_besede.append(self.geslo)
    
    def zadnja(self):
        if self.uporabljene_besede == []:
            return ''
        else:
            return self.uporabljene_besede[-1]

    def ustrezna(self):
        if self.uporabljene_besede == []:
            return True
        else:
            return self.geslo[:2] == self.zadnja()[-2:]
    
    def ze_uporabljena(self):
        return self.geslo in self.uporabljene_besede
        
    def zmaga(self):
        return self.geslo == 'kalodont'

    def poraz(self):
        return self.geslo[-2:] == 'ka'

    def izbor_besede(self):
        bazen_ustreznih = []
        for beseda in bazen_besed:
            if beseda[:2] == self.zadnja()[-2:]:
                bazen_ustreznih.append(beseda)
            else:
                pass
        return random.choice(bazen_ustreznih)

    def vnasanje(self, beseda):
        self.geslo = beseda.lower()
        if not self.obstaja():
            return NE_OBSTAJA
        elif not self.ustrezna():
            return NI_USTREZNA
        elif self.ze_uporabljena():
            return ZE_UPORABLJENA
        elif self.zmaga():
            return ZMAGA
        elif self.poraz():
            return PORAZ
        else:
            self.dodaj_na_seznam()
            rac_beseda = self.izbor_besede()
            self.geslo = rac_beseda
            self.dodaj_na_seznam()
            return rac_beseda


with open('Kalodont/besede.txt', 'r', encoding='utf8') as f:
    bazen_besed = []
    for beseda in f.readlines():
        if len(beseda.strip().lower()) >= 3:
            bazen_besed.append(beseda.strip().lower())


def nova_igra():
    return Igra()