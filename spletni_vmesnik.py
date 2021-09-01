import bottle
import os
from model import Kalodont

SKRIVNOST = "upamdabotolenakoncudelal"


@bottle.get("/")
def prva_stran():
    return bottle.template("Kalodont/views/prva_stran.html",
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("Kalodont/views/registracija.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(f'Kalodont/{uporabnisko_ime}'):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return bottle.template("Kalodont/views/registracija.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        Kalodont(uporabnisko_ime).zapisi_igre_v_datoteko()
        bottle.redirect("/osnovna/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("Kalodont/views/prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if not os.path.exists(f'Kalodont/{uporabnisko_ime}'):
        napake = {"uporabnisko_ime": "Uporabniško ime ne obstaja."}
        return bottle.template("Kalodont/views/prijava.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        bottle.redirect("/osnovna/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("piškotek uspešno pobrisan")
    bottle.redirect("/")


@bottle.get("/osnovna/")
def osnovna_stran():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    kalodont.nalozi_igre_iz_datoteke()
    return bottle.template("Kalodont/views/osnovna_stran.html",
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
                           slovar=kalodont.igre)


@bottle.post("/nova_igra/")
def nova_igra():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = kalodont.nova_igra()
    bottle.response.set_cookie("idigre", id_igre, secret=SKRIVNOST, path="/")
    bottle.redirect("/igra/")


@bottle.post("/nadaljuj_igro/")
def nadaljuj_igro():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    kalodont.nalozi_igre_iz_datoteke()
    id_igre = list(kalodont.igre)[-1]
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template("Kalodont/views/igra.html",
                           id_igre=id_igre,
                           igra=igra,
                           odziv=odziv,
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.get("/igra/")
def pokazi_igro():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = bottle.request.get_cookie("idigre", secret=SKRIVNOST)
    kalodont.nalozi_igre_iz_datoteke()
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template("Kalodont/views/igra.html",
                           id_igre=id_igre,
                           igra=igra,
                           odziv=odziv,
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.post("/igra/")
def ugibaj():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = bottle.request.get_cookie("idigre", secret=SKRIVNOST)
    beseda = bottle.request.forms.getunicode("beseda")
    kalodont.vnasanje(id_igre, beseda)
    bottle.redirect("/igra/")


@bottle.get("/zmaga/")
def zmaga():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = bottle.request.get_cookie("idigre", secret=SKRIVNOST)
    kalodont.nalozi_igre_iz_datoteke()
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template("Kalodont/views/zmaga.html",
                           igra=igra,
                           odziv=odziv,
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.get("/zmagab/")
def zmagab():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = bottle.request.get_cookie("idigre", secret=SKRIVNOST)
    kalodont.nalozi_igre_iz_datoteke()
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template("Kalodont/views/zmagab.html",
                           igra=igra,
                           odziv=odziv,
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.get("/poraz/")
def poraz():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    kalodont = Kalodont(uporabnisko_ime)
    id_igre = bottle.request.get_cookie("idigre", secret=SKRIVNOST)
    kalodont.nalozi_igre_iz_datoteke()
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template("Kalodont/views/poraz.html",
                           igra=igra,
                           odziv=odziv,
                           uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"))


@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='Kalodont/img')


bottle.run(reloader=True, debug=True)
