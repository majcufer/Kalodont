import random
import json


NE_OBSTAJA = "E"
NI_USTREZNA = "A"
ZE_UPORABLJENA = "U"
ZMAGA = "W"
ZMAGAB = "B"
PORAZ = "L"
ZACETEK = "S"


class Igra:
    def __init__(self, geslo=None, uporabljene_besede=[]):
        self.uporabljene_besede = uporabljene_besede
        self.geslo = geslo

    def obstaja(self):
        return self.geslo in bazen_besed

    def dodaj_na_seznam(self):
        return self.uporabljene_besede.append(self.geslo)

    def zadnja(self):
        if self.uporabljene_besede == []:
            return ""
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
        return self.geslo == "kalodont"

    def poraz(self):
        return self.geslo[-2:] == "ka"

    def izbor_besede(self):
        bazen_ustreznih = []
        for beseda in bazen_besed:
            if beseda[:2] == self.zadnja()[-2:] and beseda not in self.uporabljene_besede:
                bazen_ustreznih.append(beseda)
        if bazen_ustreznih == []:
            return None
        else:
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
            if self.izbor_besede() == None:
                return ZMAGAB
            else:
                self.geslo = rac_beseda
                self.dodaj_na_seznam()
                return rac_beseda


with open("besede.txt", "r", encoding="utf8") as f:
    bazen_besed = []
    for beseda in f.readlines():
        if len(beseda.strip().lower()) >= 3 and beseda.strip().lower()[-3:] != "ski" and "(" not in beseda.strip().lower():
            bazen_besed.append(beseda.strip().lower())


def nova_igra():
    return Igra()


class Kalodont:
    def __init__(self, datoteka_s_stanjem):
        self.igre = {}
        self.datoteka_s_stanjem = datoteka_s_stanjem

    def prost_id_igre(self):
        if self.igre == {}:
            return 0
        else:
            return max(self.igre.keys()) + 1

    def nova_igra(self):
        self.nalozi_igre_iz_datoteke()
        igra = Igra()
        id_igre = self.prost_id_igre()
        self.igre[id_igre] = (igra, ZACETEK)
        self.zapisi_igre_v_datoteko()
        return id_igre

    def vnasanje(self, id_igre, beseda):
        self.nalozi_igre_iz_datoteke()
        (igra, _) = self.igre[id_igre]
        odziv = igra.vnasanje(beseda)
        self.igre[id_igre] = (igra, odziv)
        self.zapisi_igre_v_datoteko()

    def zapisi_igre_v_datoteko(self):
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as f:
            igre_predelano = {id_igre: ((igra.geslo, igra.uporabljene_besede), odziv) for (
                id_igre, (igra, odziv)) in self.igre.items()}
            json.dump(igre_predelano, f, ensure_ascii=False)

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, "r", encoding="utf-8") as f:
            igre_predelano = json.load(f)
            self.igre = {int(id_igre): (Igra(geslo, uporabljene_besede), odziv) for (
                id_igre, ((geslo, uporabljene_besede), odziv)) in igre_predelano.items()}
