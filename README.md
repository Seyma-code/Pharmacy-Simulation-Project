# Eczane Kuyruk Yönetimi ve Hizmet Optimizasyonu

Bu proje, eczanelerdeki müşteri yoğunluğunu analiz etmek ve hizmet süreçlerini optimize etmek amacıyla geliştirilmiş bir Olay-Ayrık Benzetim (Discrete-Event Simulation) modeli ve Dijital İkiz (Digital Twin) kontrol panelidir.

## Proje Özeti
Özellikle nöbetçi eczanelerde yaşanan belirsiz müşteri yoğunluğu, hem hastalar için uzun bekleme sürelerine hem de eczane personeli üzerinde aşırı yük oluşmasına neden olmaktadır. Bu proje, M/M/c kuyruk teorisini temel alarak, farklı personel sayıları, stok durumları ve geliş hızları altında sistemin nasıl tepki verdiğini ölçer, eczane yönetiminin stratejik kararlar almasına yardımcı olacak analitik çıktılar üretir.

---

## Öne Çıkan Gelişmiş Özellikler

* TÜİK Yoğunluk Verileri Uyumu: Gün içindeki hasta geliş oranları (Poisson Dağılımı), TÜİK'in dönemsel ve saatlik sağlık sektörü yoğunluk trendlerine uygun olarak dinamik bir şekilde simüle edilir.
* SGK Entegrasyon Simülasyonu: Reçeteli (SGK onay bekleyen) ve Reçetesiz hastaların işlem süreleri farklılaştırılarak gerçekçi bir iş yükü analizi sunulur.
* Gelişmiş Rol Yönetimi: Eczacı (Reçete Onay & Teslimat) ve Kalfa (İlaç Arama & Stok Kontrolü) süreçleri ayrı kuyruk hatları ve servis süreleri ile çok aşamalı (Multi-stage) olarak modellenmiştir.
* Stok Parametreli Model: İlaçların stokta bulunma olasılıkları parametrik hale getirilerek, stok eksikliğinin toplam bekleme sürelerine olan etkisi analiz edilir.

---

## Teknik Altyapı ve Kütüphaneler
Proje tamamen Python ekosistemi kullanılarak geliştirilmiştir:
* Simülasyon Motoru: SimPy (Süreç tabanlı kesikli olay benzetim motoru)
* Kullanıcı Arayüzü: Streamlit (Premium CSS entegrasyonu ile özelleştirilmiş interaktif panel)
* Veri Analizi: NumPy & Pandas (Simülasyon çıktılarının istatistiksel analizi)
* Görselleştirme: Matplotlib (Saatlik yoğunluk trend eğrileri ve ödeme türü dağılımları)

---

## Çalışma Mantığı ve Dağılımlar
Sistemde gerçekçiliği sağlamak adına şu istatistiksel modeller kullanılmıştır:
1. Müşteri Varışları: Poisson Dağılımı (Günlük saatlik yoğunluk eğrisine bağlı dinamik lambda).
2. Servis Süreleri: Normal Dağılım (Reçete türüne ve stok durumuna göre değişen parametreler).
3. Kuyruk Disiplini: İlk gelen ilk hizmeti alır (FCFS).

---

## Parametreler ve Kontrol Paneli
Kullanıcılar arayüz üzerinden aşağıdaki parametreleri dinamik olarak değiştirebilirler:
1. Personel Ayarları: Eczacı Sayısı ve Kalfa Sayısı optimizasyonu.
2. Stok Parametreleri: %50 - %100 arası İlaç Stokta Bulunma Oranı.
3. Zaman Yönetimi: 8, 12 veya 24 saatlik operasyonel simülasyon süreleri.

---

## Kurulum ve Kullanım
1. Depoyu Klonlayın: ```bash
   git clone [https://github.com/Seyma-code/Pharmacy-Simulation-Project.git](https://github.com/Seyma-code/Pharmacy-Simulation-Project.git)
