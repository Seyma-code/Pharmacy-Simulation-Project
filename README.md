#  Eczane Kuyruk Yönetimi ve Hizmet Optimizasyonu

Bu proje, eczanelerdeki müşteri yoğunluğunu analiz etmek ve hizmet süreçlerini optimize etmek amacıyla geliştirilmiş bir **Olay-Ayrık Benzetim (Discrete-Event Simulation)** modelidir.

##  Proje Özeti
Özellikle nöbetçi eczanelerde yaşanan belirsiz müşteri yoğunluğu, hem hastalar için uzun bekleme sürelerine hem de eczane personeli üzerinde aşırı yük oluşmasına neden olmaktadır. Bu proje, **M/M/c kuyruk teorisini** temel alarak, farklı personel sayıları ve geliş hızları altında sistemin nasıl tepki verdiğini ölçer.

##  Teknik Altyapı
Proje tamamen Python ekosistemi kullanılarak geliştirilmiştir:
* [cite_start]**Simülasyon Motoru:** `SimPy` [cite: 106, 115]
* [cite_start]**Veri Analizi:** `NumPy` & `Pandas` [cite: 108, 117]
* [cite_start]**Kullanıcı Arayüzü:** `Streamlit` [cite: 111, 116]
* [cite_start]**Görselleştirme:** `Matplotlib` / `Plotly` [cite: 118]

##  Çalışma Mantığı ve Dağılımlar
Sistemde gerçekçiliği sağlamak adına şu istatistiksel modeller kullanılmıştır:
1. [cite_start]**Müşteri Varışları:** Poisson Dağılımı[cite: 98, 104].
2. [cite_start]**Servis Süreleri:** Normal Dağılım[cite: 98, 104].
3. [cite_start]**Kuyruk Disiplini:** İlk gelen ilk hizmeti alır (FCFS)[cite: 107].

##  Kurulum ve Kullanım
1. [cite_start]**Depoyu Klonlayın:** `git clone https://github.com/Seyma-code/Pharmacy-Simulation-Project.git` [cite: 128]
2. **Kütüphaneleri Yükleyin:** `pip install -r requirements.txt`
3. **Uygulamayı Başlatın:** `streamlit run app.py`
