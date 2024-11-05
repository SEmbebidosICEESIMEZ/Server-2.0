import network
import uasyncio as asyncio
from machine import Pin

# Configuración del LED en el pin 'LED'
led = Pin('LED', Pin.OUT)

# Credenciales de Wi-Fi
ssid = 'Ingresar SSID aqui'
password = 'Ingresar contraseña aqui'

# Conectar a Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Espera a que se conecte
while not wlan.isconnected():
    print("Conectando a Wi-Fi...")
    time.sleep(1)

print("Conexión exitosa, IP:", wlan.ifconfig()[0])

# Función para manejar las solicitudes HTTP
async def handle_request(reader, writer):
    request_line = await reader.readline()
    print("Solicitud:", request_line)
    
    # Procesar la solicitud para encender o apagar el LED
    if b'/on' in request_line:
        led.value(1)
        estado_led = "LED ON"
    elif b'/off' in request_line:
        led.value(0)
        estado_led = "LED OFF"
    else:
        estado_led = "Comando no reconocido. Use /on o /off."

    # Responder con texto plano
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{estado_led}"
    await writer.awrite(response)
    await writer.aclose()

# Inicia el servidor de manera asíncrona
async def main():
    server = await asyncio.start_server(handle_request, "0.0.0.0", 80)
    print("Servidor corriendo en el puerto 80")
    await server.wait_closed()

# Ejecuta el servidor
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor detenido")
