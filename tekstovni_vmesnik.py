import model


PONOVNI_ZAGON = 'p'
IZHOD = 'i'


def izpis_igre(igra):
    tekst = f'''####################################\n
    Že uporabljene besede: {igra.uporabljene_besede}\n
    Predhodna beseda: {igra.zadnja()}\n
    Iščete besedo na: {igra.zadnja()[-2:]}\n
####################################\n'''
    return tekst

def izpis_zmage():
    tekst = f'''####################################\n
    Bravo! Zmagali ste!\n
    Prvi ste rekli Kalodont.\n
####################################\n'''
    return tekst

def izpis_poraza():
    tekst = f'''####################################\n
    KALODONT\n
    Žal vas je računalnik premagal.\n
    Izbrali ste besedo, ki se je končala na KA.\n
####################################\n'''
    return tekst

def ne_obstaja(beseda):
    tekst = f'''####################################\n
    Beseda "{beseda}" ne obstaja!\n
    Preverite, če ste se kje zatipkali in poskusite ponovno.\n
####################################\n'''
    return tekst

def ni_ustrezna(beseda):
    tekst = f'''####################################\n
    Beseda "{beseda}" se ne začne na zadnji dve črki prejšnje besede!\n
    Poskusite ponovno!\n
####################################\n'''
    return tekst

def ze_uporabljena(beseda):
    tekst = f'''####################################\n
    Beseda "{beseda}" je bila že uporabljena!\n
    Poskusite ponovno!\n
####################################\n'''
    return tekst

def zahtevaj_vnos():
    return input('Vnesite besedo:')

def zahtevaj_moznost():
    return input('Vnesite možnost:')

def ponudi_moznosti():
    tekst = """ Vpišite črko za izbor naslednjih možnosti:\n
    p : ponovni zagon igre\n
    i : izhod\n
    """
    return tekst

def izberi_ponovitev():
    print(ponudi_moznosti())
    moznost = zahtevaj_moznost().strip().lower()
    if moznost == PONOVNI_ZAGON:
            igra = model.nova_igra()
            print(izpis_igre(igra))
            return igra
    else:
        return IZHOD

def pozeni_vmesnik():
    igra = model.nova_igra()
    print(izpis_igre(igra))
    while True:
        beseda = zahtevaj_vnos()
        odziv = igra.vnasanje(beseda)
        if odziv == model.NE_OBSTAJA:
            print(ne_obstaja(beseda)) #tle je treba še par funkcij definirat
        elif odziv == model.NI_USTREZNA:
            print(ni_ustrezna(beseda))
        elif odziv == model.ZE_UPORABLJENA:
            print(ze_uporabljena(beseda))
        elif odziv == model.ZMAGA:
            print(izpis_zmage())
            igra = izberi_ponovitev()
            if igra == IZHOD:
                break
        elif odziv == model.PORAZ:
            print(izpis_poraza())
            igra = izberi_ponovitev()
            if igra == IZHOD:
                break
        else:
            print(odziv)
            print(izpis_igre(igra))


pozeni_vmesnik()