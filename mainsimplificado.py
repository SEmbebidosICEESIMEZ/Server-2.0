import network, uasyncio as asyncio
from machine import Pin
import time

# Configuración LED y Wi-Fi
led = Pin('LED', Pin.OUT)
wlan = network.WLAN(network.STA_IF); wlan.active(True); wlan.connect('Ingresar SSID aqui', 'Ingresar contraseña aqui')

while not wlan.isconnected(): time.sleep(1)
print("Conectado, IP:", wlan.ifconfig()[0])

# Manejo de solicitud HTTP
async def handle_request(r, w):
    req = await r.readline()
    led.value(1 if b'/on' in req else 0 if b'/off' in req else led.value())
    await w.awrite(f"HTTP/1.1 200 OK\r\n\r\n{'LED ON' if led.value() else 'LED OFF'}")
    await w.aclose()

# Servidor asincrónico
async def main():
    print("Servidor en puerto 80")
    await asyncio.start_server(handle_request, "0.0.0.0", 80)
    while True: await asyncio.sleep(1)

# Ejecuta el servidor
asyncio.run(main())

