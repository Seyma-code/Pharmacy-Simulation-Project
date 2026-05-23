import pandas as pd
import simpy
import random
import numpy as np

class Eczane(object):
    def __init__(self, env, num_eczaci, num_kalfa, stok_olasiligi):
        self.env = env
        # İki farklı çalışan kaynağı tanımlıyoruz (Eczacı ve Kalfa)
        self.eczaci_kaynak = simpy.Resource(env, num_eczaci)
        self.kalfa_kaynak = simpy.Resource(env, num_kalfa)
        self.stok_olasiligi = stok_olasiligi # İlacın bulunma olasılığı (Örn: %90)

    def servis_sureci(self, musteri_turu, odeme_turu):
        toplam_servis_suresi = 0
        
        # 1. Kalfa ilacı arıyor ve getiriyor
        toplam_servis_suresi += random.normalvariate(2, 0.5) # İlaç arama süresi (2 dk)
        
        # Stok kontrolü (Doktorun istediği ilaç arama mantığı)
        if random.random() > self.stok_olasiligi:
            # İlaç stokta yoksa sistemde arama/tedarik için ekstra zaman geçer
            toplam_servis_suresi += random.uniform(3, 5) 
            
        # 2. Reçete Türü (SGK Kontrolü)
        if musteri_turu == "Reçeteli (SGK)":
            toplam_servis_suresi += random.normalvariate(4, 1) # Medula sistemi onayı uzun sürer
        else:
            toplam_servis_suresi += random.normalvariate(1.5, 0.5) # Reçetesiz hızlı satış
            
        # 3. Ödeme Türü Etkisi
        if odeme_turu == "Kredi Kartı" or odeme_turu == "Mobil":
            toplam_servis_suresi += 0.5 # Kart çekim süresi
        else:
            toplam_servis_suresi += 1.0 # Nakit para üstü verme süresi
            
        yield self.env.timeout(max(1, toplam_servis_suresi))

def musteri_akisi(env, isim, eczane, bekleme_listesi, saat):
    gelis_zamani = env.now
    
    # Müşteri kategorizasyonu (Doktorun istediği Reçeteli/Reçetesiz durumu)
    musteri_turu = random.choices(["Reçeteli (SGK)", "Reçetesiz"], weights=[0.7, 0.3])[0]
    odeme_turu = random.choices(["Kredit Kartı", "Nakit", "Mobil"], weights=[0.6, 0.3, 0.1])[0]
    
    # Önce kalfa hizmet verir, sonra eczacı onaylar (Kalfa durumu entegrasyonu)
    with eczane.kalfa_kaynak.request() as istek_kalfa:
        yield istek_kalfa
        with eczane.eczaci_kaynak.request() as istek_eczaci:
            yield istek_eczaci
            
            bekleme_suresi = env.now - gelis_zamani
            bekleme_listesi.append({
                "Müşteri": isim,
                "Saat": saat,
                "Bekleme Süresi": bekleme_suresi,
                "Tür": musteri_turu,
                "Ödeme": odeme_turu
            })
            
            yield env.process(eczane.servis_sureci(musteri_turu, odeme_turu))

def gunluk_yoğunluk_orani(saat):
    # TÜİK ve saha verilerine göre saatlik yoğunluk fonksiyonu (Doktorun özellikle istediği zaman kavramı)
    if 8 <= saat < 12: return 4.0   # Sabah normal yoğunluk (4 dakikada bir müşteri)
    elif 12 <= saat < 14: return 2.0 # Öğle arası yoğun (2 dakikada bir müşteri)
    elif 14 <= saat < 17: return 5.0 # Öğleden sonra sakin
    elif 17 <= saat < 20: return 1.5 # Akşam iş çıkışı pik saat (En yoğun dönem)
    else: return 10.0                # Gece nöbetçi dönemi başlangıcı sakin

def simule_et(num_eczaci, num_kalfa, stok_orani, toplam_saat):
    env = simpy.Environment()
    eczane = Eczane(env, num_eczaci, num_kalfa, stok_orani / 100.0)
    bekleme_listesi = []
    
    def run(env):
        i = 0
        baslangic_saati = 8 # Eczane sabah 8'de açılıyor
        while True:
            mevcut_saat = baslangic_saati + (env.now / 60) % 24
            ort_gelis = gunluk_yoğunluk_orani(mevcut_saat)
            
            yield env.timeout(random.expovariate(1.0 / ort_gelis))
            i += 1
            env.process(musteri_akisi(env, f'Müşteri {i}', eczane, bekleme_listesi, mevcut_saat))
            
            if env.now >= toplam_saat * 60:
                break
                
    env.process(run(env))
    env.run(until=toplam_saat * 60)
    return pd.DataFrame(bekleme_listesi)