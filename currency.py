from requests import get
from datetime import datetime

def getUSDcurrency():
    url = 'https://www.dolarhoy.com/cotizacion-dolar-blue'
    response = get(url)
    #Slices to get the currency exact position
    compra = response.text[response.text.find(">$")+1:response.text.find(">$")+8]
    first_value = response.text[response.text.find(">$")+8:]
    venta = first_value[first_value.find(">$")+1:first_value.find(">$")+8]
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return "Cotizacición al {} \nCompra: ARS {}\nVenta: ARS {} \nFuente {}".format(fecha_actual, compra, venta, url)

def getBTCcurrency():
    url = 'https://www.coindesk.com/price/bitcoin'
    response = get(url)

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Slices to get the currency exact position
    usd_value = response.text[response.text.find(">$")+9:response.text.find(">$")+18]
    return "Cotizacición al {} \n1 BTC = USD {} \nFuente {}".format(fecha_actual, usd_value, url)



getBTCcurrency()