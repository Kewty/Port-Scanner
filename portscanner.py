import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import sys

init(autoreset=True)

THREADS = 1000  # Turbo hız


def clear():
    print("\033c", end="")


# --------------------- HIZLI TCP TARAMA --------------------- #
def tcp_kontrol(ip, port, timeout=0.15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))  # Hızlı non-blocking bağlantı
        s.close()

        if result == 0:
            return port, True
        return port, False

    except:
        return port, False


# --------------------- OPTİMİZE UDP TARAMA --------------------- #
def udp_kontrol(ip, port, timeout=0.35):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.sendto(b"hi", (ip, port))

        try:
            s.recvfrom(1024)
            return port, True
        except socket.timeout:
            return port, True
    except:
        return port, False


# --------------------- ORTAK TARAMA MOTORU --------------------- #
def port_tara(ip, portlar, tarama_tipi):
    print(Fore.CYAN + f"\n{tarama_tipi} Taraması Başlıyor...\n")
    acik_portlar = []

    kontrol_fonk = tcp_kontrol if tarama_tipi == "TCP" else udp_kontrol

    sayac = 0
    toplam = len(portlar)

    with ThreadPoolExecutor(max_workers=THREADS) as exe:
        futures = {exe.submit(kontrol_fonk, ip, p): p for p in portlar}

        for future in as_completed(futures):
            port, durum = future.result()
            sayac += 1

            if sayac % 150 == 0:  # CPU'yu yormadan ilerleme göstergesi
                print(Fore.YELLOW + f"Taranıyor… {sayac}/{toplam}", end="\r")

            if durum:
                acik_portlar.append(port)

    # -------- Güzel sonuç ekranı -------- #
    print("\n")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Fore.GREEN + f"      ✔ {tarama_tipi} Taraması Bitti")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    if acik_portlar:
        print(Fore.GREEN + f"Açık {tarama_tipi} Portlar:\n")
        for p in sorted(acik_portlar):
            print(Fore.GREEN + f"→ {p}")
    else:
        print(Fore.RED + f"Açık {tarama_tipi} port bulunamadı.")

    print()
    return acik_portlar


# ------------------ HEM TCP HEM UDP ------------------ #
def birleşik_tarama(ip, portlar):
    print(Fore.MAGENTA + "\nTCP + UDP Karışık Tarama Başlıyor...\n")

    acik_tcp = port_tara(ip, portlar, "TCP")
    acik_udp = port_tara(ip, portlar, "UDP")

    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Fore.GREEN + "           SONUÇ RAPORU")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print(Fore.GREEN + "Açık TCP Portlar: ", acik_tcp if acik_tcp else "Yok")
    print(Fore.GREEN + "Açık UDP Portlar: ", acik_udp if acik_udp else "Yok")

    print()
    sys.exit()


# --------------------- PORT GİRİŞ SİSTEMİ --------------------- #
def belirli_portlar():
    while True:
        giris = input(Fore.YELLOW + "Portları gir (örn: 80,443,22): ")
        try:
            return [int(p.strip()) for p in giris.split(",")]
        except:
            print(Fore.RED + "Hatalı giriş! Sadece sayı ve virgül.")


def tum_portlar():
    return list(range(1, 65536))


# --------------------- MENÜ --------------------- #
def menu():
    clear()
    print(Fore.CYAN + "==============================")
    print(Fore.MAGENTA + "       PORT SCANNER v4.0")
    print(Fore.CYAN + "==============================\n")

    print(Fore.GREEN + "1 - Belirli TCP portları tara")
    print(Fore.GREEN + "2 - Tüm TCP portlarını tara")
    print(Fore.GREEN + "3 - Belirli UDP portlarını tara")
    print(Fore.GREEN + "4 - Tüm UDP portlarını tara")
    print(Fore.GREEN + "5 - Hem TCP hem UDP karışık tara")
    print(Fore.RED   + "6 - Çıkış\n")

    return input(Fore.YELLOW + "Seçim yap: ")


# --------------------- ANA PROGRAM --------------------- #
def main():
    try:
        ip = input(Fore.YELLOW + "Hedef IP: ")

        while True:
            secim = menu()

            if secim == "1":
                portlar = belirli_portlar()
                port_tara(ip, portlar, "TCP")
                sys.exit()

            elif secim == "2":
                portlar = tum_portlar()
                port_tara(ip, portlar, "TCP")
                sys.exit()

            elif secim == "3":
                portlar = belirli_portlar()
                port_tara(ip, portlar, "UDP")
                sys.exit()

            elif secim == "4":
                portlar = tum_portlar()
                port_tara(ip, portlar, "UDP")
                sys.exit()

            elif secim == "5":
                portlar = tum_portlar()
                birleşik_tarama(ip, portlar)

            elif secim == "6":
                print(Fore.RED + "Program kapatıldı.")
                sys.exit()

            else:
                print(Fore.RED + "Geçersiz seçim!")

    except KeyboardInterrupt:
        print(Fore.RED + "\nTarama durduruldu. Çıkılıyor...")
        sys.exit()


if __name__ == "__main__":
    main()
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import sys

init(autoreset=True)

THREADS = 1000  # Turbo hız


def clear():
    print("\033c", end="")


# --------------------- HIZLI TCP TARAMA --------------------- #
def tcp_kontrol(ip, port, timeout=0.15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))  # Hızlı non-blocking bağlantı
        s.close()

        if result == 0:
            return port, True
        return port, False

    except:
        return port, False


# --------------------- OPTİMİZE UDP TARAMA --------------------- #
def udp_kontrol(ip, port, timeout=0.35):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(b"hi", (ip, port))

        try:
            s.recvfrom(1024)
            return port, True
        except socket.timeout:
            return port, True
    except:
        return port, False


# --------------------- ORTAK TARAMA MOTORU --------------------- #
def port_tara(ip, portlar, tarama_tipi):
    print(Fore.CYAN + f"\n{tarama_tipi} Taraması Başlıyor...\n")
    acik_portlar = []

    kontrol_fonk = tcp_kontrol if tarama_tipi == "TCP" else udp_kontrol

    sayac = 0
    toplam = len(portlar)

    with ThreadPoolExecutor(max_workers=THREADS) as exe:
        futures = {exe.submit(kontrol_fonk, ip, p): p for p in portlar}

        for future in as_completed(futures):
            port, durum = future.result()
            sayac += 1

            if sayac % 150 == 0:  # CPU'yu yormadan ilerleme göstergesi
                print(Fore.YELLOW + f"Taranıyor… {sayac}/{toplam}", end="\r")

            if durum:
                acik_portlar.append(port)

    # -------- Güzel sonuç ekranı -------- #
    print("\n")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Fore.GREEN + f"      ✔ {tarama_tipi} Taraması Bitti")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    if acik_portlar:
        print(Fore.GREEN + f"Açık {tarama_tipi} Portlar:\n")
        for p in sorted(acik_portlar):
            print(Fore.GREEN + f"→ {p}")
    else:
        print(Fore.RED + f"Açık {tarama_tipi} port bulunamadı.")

    print()
    return acik_portlar


# ------------------ HEM TCP HEM UDP ------------------ #
def birleşik_tarama(ip, portlar):
    print(Fore.MAGENTA + "\nTCP + UDP Karışık Tarama Başlıyor...\n")

    acik_tcp = port_tara(ip, portlar, "TCP")
    acik_udp = port_tara(ip, portlar, "UDP")

    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(Fore.GREEN + "           SONUÇ RAPORU")
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print(Fore.GREEN + "Açık TCP Portlar: ", acik_tcp if acik_tcp else "Yok")
    print(Fore.GREEN + "Açık UDP Portlar: ", acik_udp if acik_udp else "Yok")

    print()
    sys.exit()


# --------------------- PORT GİRİŞ SİSTEMİ --------------------- #
def belirli_portlar():
    while True:
        giris = input(Fore.YELLOW + "Portları gir (örn: 80,443,22): ")
        try:
            return [int(p.strip()) for p in giris.split(",")]
        except:
            print(Fore.RED + "Hatalı giriş! Sadece sayı ve virgül.")


def tum_portlar():
    return list(range(1, 65536))


# --------------------- MENÜ --------------------- #
def menu():
    clear()
    print(Fore.CYAN + "==============================")
    print(Fore.MAGENTA + "       PORT SCANNER v4.0")
    print(Fore.CYAN + "==============================\n")

    print(Fore.GREEN + "1 - Belirli TCP portları tara")
    print(Fore.GREEN + "2 - Tüm TCP portlarını tara")
    print(Fore.GREEN + "3 - Belirli UDP portlarını tara")
    print(Fore.GREEN + "4 - Tüm UDP portlarını tara")
    print(Fore.GREEN + "5 - Hem TCP hem UDP karışık tara")
    print(Fore.RED   + "6 - Çıkış\n")

    return input(Fore.YELLOW + "Seçim yap: ")


# --------------------- ANA PROGRAM --------------------- #
def main():
    try:
        ip = input(Fore.YELLOW + "Hedef IP: ")

        while True:
            secim = menu()

            if secim == "1":
                portlar = belirli_portlar()
                port_tara(ip, portlar, "TCP")
                sys.exit()

            elif secim == "2":
                portlar = tum_portlar()
                port_tara(ip, portlar, "TCP")
                sys.exit()

            elif secim == "3":
                portlar = belirli_portlar()
                port_tara(ip, portlar, "UDP")
                sys.exit()

            elif secim == "4":
                portlar = tum_portlar()
                port_tara(ip, portlar, "UDP")
                sys.exit()

            elif secim == "5":
                portlar = tum_portlar()
                birleşik_tarama(ip, portlar)

            elif secim == "6":
                print(Fore.RED + "Program kapatıldı.")
                sys.exit()

            else:
                print(Fore.RED + "Geçersiz seçim!")

    except KeyboardInterrupt:
        print(Fore.RED + "\nTarama durduruldu. Çıkılıyor...")
        sys.exit()


if __name__ == "__main__":
    main()
