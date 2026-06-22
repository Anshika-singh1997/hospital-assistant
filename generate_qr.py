import qrcode
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip = get_local_ip()
url = f"http://{ip}:5000"
print(f"Your assistant URL: {url}")

qr = qrcode.make(url)
qr.save("hospital_qr.png")
print("QR code saved as hospital_qr.png")