import bottle
import model

SKRIVNOST = 'upamdabotolenakoncudelal'
kalodont = model.Kalodont('stanje.json')


@bottle.get("/")
def osnovna_stran():
    return bottle.template('Kalodont/views/osnovna_stran.html')


@bottle.post("/nova_igra/")
def nova_igra():
    id_igre = kalodont.nova_igra()
    bottle.response.set_cookie('idigre', id_igre, secret=SKRIVNOST, path='/')
    bottle.redirect("/igra/")


@bottle.get("/igra/")
def pokazi_igro():
    id_igre = bottle.request.get_cookie('idigre', secret=SKRIVNOST)
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template('Kalodont/views/igra.html',
                           id_igre=id_igre,
                           igra=igra,
                           odziv=odziv)


@bottle.post("/igra/")
def ugibaj():
    id_igre = bottle.request.get_cookie('idigre', secret=SKRIVNOST)
    beseda = bottle.request.forms.getunicode("beseda")
    kalodont.vnasanje(id_igre, beseda)
    bottle.redirect("/igra/")


@bottle.get("/zmaga/")
def zmaga():
    id_igre = bottle.request.get_cookie('idigre', secret=SKRIVNOST)
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template('Kalodont/views/zmaga.html',
                           igra=igra,
                           odziv=odziv)


@bottle.get("/poraz/")
def poraz():
    id_igre = bottle.request.get_cookie('idigre', secret=SKRIVNOST)
    (igra, odziv) = kalodont.igre[id_igre]
    return bottle.template('Kalodont/views/poraz.html',
                           igra=igra,
                           odziv=odziv)


bottle.run(reloader=True, debug=True)
