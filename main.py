import random

def main():
    print("=================================")
    print("   GAME TEBAK ANGKA SEDERHANA    ")
    print("=================================")
    print("Saya memikirkan angka 1 sampai 100.")
    print("Coba tebak angka tersebut!")


    angka_rahasia = random.randint(1, 100)
    tebakan = None
    percobaan = 0


    while tebakan != angka_rahasia:
        try:

            input_user = input("\nMasukkan tebakanmu: ")
            tebakan = int(input_user) 
            percobaan += 1


            if tebakan < angka_rahasia:
                print("❌ Terlalu rendah! Coba lagi naikkan angkanya.")
            elif tebakan > angka_rahasia:
                print("❌ Terlalu tinggi! Coba turunkan angkanya.")
            else:
                print(f"\n🎉 SELAMAT! Angkanya adalah {angka_rahasia}.")
                print(f"Kamu berhasil menebak dalam {percobaan} kali percobaan.")
        
        except ValueError:
            
            print("⚠️ Error: Masukkan hanya angka bulat (integer)!")

if __name__ == "__main__":

    main()
