import sqlite3
from datetime import datetime

# ==== 1. Verilənlər bazasına qoşulma və cədvəl yaratma ====
conn = sqlite3.connect("musteriler.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS musteriler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad TEXT,
    soyad TEXT,
    dogum_tarixi TEXT,
    hesab_no TEXT,
    balans REAL
)
""")

# ==== 2. 25 müştəri əlavə etmək ====
import random
from datetime import date

adlar = ["Ali", "Veli", "Nigar", "Aysel", "Ramil", "Fidan", "Orxan", "Günel", "Elvin", "Zaur",
         "Leyla", "Tural", "Aygün", "Murad", "Zəhra", "Səid", "Kəmalə", "Emin", "Nərgiz", "Rəvan",
         "Sevinc", "Kamran", "Gülnar", "Anar", "Lalə"]

soyadlar = ["Hüseynov", "Əliyeva", "Məmmədov", "Rzayev", "Əhmədov", "Quliyev", "İsmayılov", "Kərimov",
            "Rəhimov", "Salmanov", "Tağıyev", "Məmmədli", "Abdullayeva", "Ələkbərov", "Cəfərov",
            "Qasımov", "Səfərov", "Xəlilov", "Sadıqov", "Cahangirov", "İmanov", "Əlizadə", "Əlverdiyev", "Yusifov", "Babayev"]

def random_date(start_year=1980, end_year=2005):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return date(year, month, day).strftime("%Y-%m-%d")

# Əgər cədvəl boşdursa, 25 müştəri əlavə et
cursor.execute("SELECT COUNT(*) FROM musteriler")
count = cursor.fetchone()[0]
if count == 0:
    for i in range(25):
        ad = adlar[i]
        soyad = soyadlar[i]
        dogum_tarixi = random_date()
        hesab_no = str(random.randint(1000000000, 9999999999))
        balans = round(random.uniform(100, 10000), 2)
        cursor.execute("INSERT INTO musteriler (ad, soyad, dogum_tarixi, hesab_no, balans) VALUES (?, ?, ?, ?, ?)",
                       (ad, soyad, dogum_tarixi, hesab_no, balans))
    conn.commit()

# ==== 3. Müştəri adlarını və balanslarını çap edən funksiya ====
def musterileri_goster():
    cursor.execute("SELECT ad, balans FROM musteriler")
    melumatlar = cursor.fetchall()
    print("\n--- Müştəri adları və balansları ---")
    for ad, balans in melumatlar:
        print(f"{ad}: {balans} AZN")

# ==== 4. Balansı 5000 AZN-dən çox və 30 yaşdan kiçik müştəriləri göstərən funksiya ====
def genc_varli_musteriler():
    bugun = datetime.now().date()
    cursor.execute("SELECT ad, soyad, dogum_tarixi, balans FROM musteriler WHERE balans > 5000")
    secilmisler = []
    for ad, soyad, dogum_tarixi, balans in cursor.fetchall():
        yas = bugun.year - datetime.strptime(dogum_tarixi, "%Y-%m-%d").year
        if yas < 30:
            secilmisler.append((ad, soyad, balans, yas))
    print("\n--- Balansı >5000 və yaşı <30 olan müştərilər ---")
    for m in secilmisler:
        print(f"{m[0]} {m[1]} - Balans: {m[2]} AZN, Yaş: {m[3]}")
    return secilmisler

# ==== 5. İstifadəçi tərəfindən daxil edilmiş adla müştərinin balansını iki dəfə artırmaq və hesab nömrəsini dəyişmək ====
def balans_artir_ve_hesab_deyis():
    ad = input("\nBalansı iki dəfə artırmaq istədiyiniz müştərinin adını daxil edin: ")
    cursor.execute("SELECT id, balans FROM musteriler WHERE ad = ?", (ad,))
    netice = cursor.fetchone()
    if netice:
        id, balans = netice
        yeni_balans = balans * 2
        yeni_hesab_no = "4567464523"
        cursor.execute("UPDATE musteriler SET balans = ?, hesab_no = ? WHERE id = ?", (yeni_balans, yeni_hesab_no, id))
        conn.commit()
        print(f"{ad} adlı müştərinin balansı iki dəfə artırıldı və hesab nömrəsi dəyişdirildi.")
    else:
        print("Bu adda müştəri tapılmadı.")

# ==== 6. Balansı sıfır olan müştəriləri silmək ====
def balans_sifir_sil():
    cursor.execute("DELETE FROM musteriler WHERE balans = 0")
    conn.commit()
    print("\nBalansı 0 olan müştərilər silindi.")

# ==== Funksiyaları işə salmaq ====
musterileri_goster()
genc_varli_musteriler()
balans_artir_ve_hesab_deyis()
balans_sifir_sil()

# Bağlantını bağlayırıq
conn.close()