#!/usr/bin/env python3
"""Statik Analiz Raporu - DOCX Oluşturucu"""

from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
import os

doc = Document()

# ─── Stil Ayarları ───
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

for i in range(1, 4):
    hs = doc.styles[f'Heading {i}']
    hs.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)

def add_table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers), style='Light Grid Accent 1')
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = h
        for p in c.paragraphs:
            p.runs[0].bold = True
            p.runs[0].font.size = Pt(9)
    for row_data in rows:
        row = t.add_row()
        for i, val in enumerate(row_data):
            row.cells[i].text = str(val)
            for p in row.cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9)
    return t

# ═══════════════════════════════════════════════════════
# KAPAK SAYFASI
# ═══════════════════════════════════════════════════════
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('İSTANBUL ATLAS ÜNİVERSİTESİ')
r.bold = True
r.font.size = Pt(22)
r.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('MÜHENDİSLİK FAKÜLTESİ\nYAZILIM MÜHENDİSLİĞİ BÖLÜMÜ')
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = RGBColor(0x0f, 0x34, 0x60)

doc.add_paragraph()
doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('BİTİRME PROJESİ İLERLEME RAPORU')
r.bold = True
r.font.size = Pt(14)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('AndroidSecAnalyzer:\nAndroid Uygulama Güvenlik Analiz Aracı')
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = RGBColor(0xe9, 0x45, 0x60)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Statik Analiz Modülü')
r.bold = True
r.font.size = Pt(15)
r.font.color.rgb = RGBColor(0x0f, 0x34, 0x60)

for _ in range(4):
    doc.add_paragraph()

cover_info = [
    ('Hazırlayan', 'Damla YÜKSEL'),
    ('Danışman', 'Adem ÖZYAVAŞ'),
    ('Tarih', '9 Nisan 2026'),
]
t = doc.add_table(rows=3, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (k, v) in enumerate(cover_info):
    t.rows[i].cells[0].text = k
    t.rows[i].cells[1].text = v
    for c in t.rows[i].cells:
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(12)
                run.bold = True

doc.add_page_break()

# ═══════════════════════════════════════════════════════
# İÇİNDEKİLER
# ═══════════════════════════════════════════════════════
doc.add_heading('İÇİNDEKİLER', level=1)
toc_items = [
    '1. Giriş ve Proje Tanımı',
    '2. Projenin Amacı ve Kapsamı',
    '3. Kullanılan Teknolojiler ve Araçlar',
    '4. Proje Mimarisi ve Dizin Yapısı',
    '5. Statik Analiz Modülü — Detaylı Teknik Açıklama',
    '   5.1. Statik Analiz Orkestratörü',
    '   5.2. Manifest Analizi',
    '   5.3. Kaynak Kod Analizi',
    '   5.4. Sertifika Analizi',
    '   5.5. Native Kod Analizi',
    '6. Destekleyici Altyapı Modülleri',
    '7. OWASP Mobile Top 10 Entegrasyonu',
    '8. Test Altyapısı',
    '9. Kod İstatistikleri',
    '10. Mevcut Durum ve Sonraki Adımlar',
    '11. Sonuç',
]
for item in toc_items:
    doc.add_paragraph(item, style='List Number' if not item.startswith('   ') else 'List Bullet')

doc.add_page_break()

# ═══════════════════════════════════════════════════════
# BÖLÜM 1
# ═══════════════════════════════════════════════════════
doc.add_heading('1. Giriş ve Proje Tanımı', level=1)
doc.add_paragraph(
    'Bu rapor, İstanbul Atlas Üniversitesi Yazılım Mühendisliği Bölümü bitirme projesi kapsamında '
    'geliştirilen AndroidSecAnalyzer projesinin statik analiz modülüne ilişkin gerçekleştirilen '
    'çalışmaları detaylı olarak sunmaktadır.'
)
doc.add_paragraph(
    'AndroidSecAnalyzer, Android uygulamalarının (APK dosyalarının) güvenlik açıklarını otomatik olarak '
    'tespit etmek amacıyla geliştirilmekte olan kapsamlı bir güvenlik analiz aracıdır. Proje, iki temel '
    'analiz yaklaşımını bütünleşik bir platformda birleştirmektedir:'
)
doc.add_paragraph('Statik Analiz (bu raporun konusu): APK dosyasının çalıştırılmadan, kaynak kodu ve yapılandırma dosyaları üzerinden güvenlik açıklarının tespit edilmesi.', style='List Bullet')
doc.add_paragraph('Dinamik Analiz (proje ortağı tarafından geliştirilmektedir): Uygulamanın çalışma zamanında (runtime) davranışlarının izlenmesi ve güvenlik açıklarının tespit edilmesi.', style='List Bullet')

# ═══════════════════════════════════════════════════════
# BÖLÜM 2
# ═══════════════════════════════════════════════════════
doc.add_heading('2. Projenin Amacı ve Kapsamı', level=1)
doc.add_heading('2.1. Amaç', level=2)
doc.add_paragraph(
    'Projenin temel amacı, Android uygulamalarındaki güvenlik açıklarını OWASP Mobile Top 10 standartları '
    'çerçevesinde otomatik olarak tespit eden, raporlayan ve sınıflandıran bir güvenlik analiz aracı geliştirmektir.'
)
doc.add_heading('2.2. Statik Analiz Kapsamı', level=2)
doc.add_paragraph('Statik analiz modülü, bir APK dosyasını çalıştırmadan aşağıdaki dört ana alan üzerinden güvenlik analizi yapmaktadır:')
add_table(
    ['Analiz Alanı', 'Açıklama', 'Tespit Edilen Zafiyet Örnekleri'],
    [
        ('Manifest Analizi', 'AndroidManifest.xml dosyasının güvenlik kontrolü', 'Tehlikeli izinler, exported componentler, debuggable flag'),
        ('Kaynak Kod Analizi', 'Java/Kotlin kaynak kodlarının taranması', 'Zayıf kriptografi, hardcoded secrets, SQL injection'),
        ('Sertifika Analizi', 'APK imza sertifikasının doğrulanması', 'Debug sertifikası, zayıf algoritma, süresi dolmuş sertifika'),
        ('Native Kod Analizi', '.so (C/C++) kütüphanelerinin analizi', 'Tehlikeli fonksiyonlar, hardcoded IP/URL, güvenlik bayrakları'),
    ]
)

# ═══════════════════════════════════════════════════════
# BÖLÜM 3
# ═══════════════════════════════════════════════════════
doc.add_heading('3. Kullanılan Teknolojiler ve Araçlar', level=1)
add_table(
    ['Teknoloji/Araç', 'Kullanım Alanı', 'Versiyon'],
    [
        ('Python', 'Ana geliştirme dili', '3.x'),
        ('Click', 'Komut satırı arayüzü (CLI) framework', '≥ 8.0.0'),
        ('PyYAML', 'Konfigürasyon dosyası yönetimi', '≥ 6.0.0'),
        ('Pytest', 'Birim ve entegrasyon testleri', '≥ 7.0.0'),
        ('xml.etree.ElementTree', 'AndroidManifest.xml parsing', 'Python stdlib'),
        ('zipfile', 'APK dosya okuma (ZIP formatı)', 'Python stdlib'),
        ('struct', 'ELF binary header parsing', 'Python stdlib'),
        ('re', 'Regex tabanlı pattern matching', 'Python stdlib'),
        ('subprocess', 'Harici araç entegrasyonu (keytool)', 'Python stdlib'),
        ('hashlib', 'Sertifika parmak izi hesaplama', 'Python stdlib'),
        ('logging', 'Merkezi log yönetim sistemi', 'Python stdlib'),
        ('keytool', 'Sertifika bilgisi çıkarma (Java JDK)', 'JDK bağımlı'),
    ]
)

# ═══════════════════════════════════════════════════════
# BÖLÜM 4
# ═══════════════════════════════════════════════════════
doc.add_heading('4. Proje Mimarisi ve Dizin Yapısı', level=1)
doc.add_heading('4.1. Genel Mimari', level=2)
doc.add_paragraph(
    'Proje, modüler mimari prensibiyle tasarlanmıştır. Her bir analiz alanı bağımsız bir alt modül olarak '
    'geliştirilmiş olup, StaticAnalyzer orkestratör sınıfı tarafından koordine edilmektedir. Bu yaklaşım, '
    'kodun bakımını, test edilebilirliğini ve genişletilebilirliğini sağlamaktadır.'
)
doc.add_paragraph(
    'Mimari Yapı:\n'
    '• AndroidSecAnalyzer (Ana Motor)\n'
    '  ├── StaticAnalyzer (Orkestratör) — [Bu rapordaki çalışma]\n'
    '  │   ├── Manifest Analizi (ManifestParser, PermissionAnalyzer, ComponentAnalyzer)\n'
    '  │   ├── Kod Analizi (CodeScanner, CryptoAnalyzer, SecretsDetector)\n'
    '  │   ├── Sertifika Analizi (CertificateExtractor, CertificateValidator)\n'
    '  │   └── Native Kod Analizi (SOAnalyzer, StringsExtractor)\n'
    '  └── DynamicAnalyzer (Proje ortağı tarafından geliştiriliyor)'
)

doc.add_heading('4.2. Dizin Yapısı', level=2)
dirs = """AndroidSecAnalyzer/
├── androidsec/                     # Ana Python paketi
│   ├── __init__.py                 # Paket tanımı (v0.1.0)
│   ├── core/                       # Çekirdek modüller
│   │   ├── analyzer.py             # Ana analiz motoru
│   │   ├── config_manager.py       # YAML konfigürasyon yönetimi
│   │   ├── constants.py            # Proje sabitleri
│   │   └── exceptions.py           # Özel hata sınıfları
│   ├── static_analysis/            # ★ STATİK ANALİZ MODÜLÜ ★
│   │   ├── analyzer.py             # Orkestratör
│   │   ├── manifest/               # Manifest analizi
│   │   │   ├── parser.py           # XML parser
│   │   │   ├── permissions.py      # İzin analizi
│   │   │   └── components.py       # Component analizi
│   │   ├── code/                   # Kaynak kod analizi
│   │   │   ├── scanner.py          # Kod tarayıcı
│   │   │   ├── crypto_analyzer.py  # Kriptografi analizi
│   │   │   └── secrets_detector.py # Secret tespiti
│   │   ├── certificate/            # Sertifika analizi
│   │   │   ├── extractor.py        # Sertifika çıkarma
│   │   │   └── validator.py        # Sertifika doğrulama
│   │   └── native/                 # Native kod analizi
│   │       ├── so_analyzer.py      # SO dosya analizi
│   │       └── strings_extractor.py # String çıkarma
│   ├── dynamic_analysis/           # Dinamik analiz (proje ortağı)
│   ├── cli/                        # Komut satırı arayüzü
│   ├── utils/                      # Yardımcı araçlar
│   ├── decompiler/                 # APK dekompilasyon
│   ├── vulnerabilities/            # Zafiyet veritabanı
│   ├── correlation/                # Bulgu korelasyonu
│   ├── reporting/                  # Rapor oluşturma
│   └── database/                   # Veritabanı modülü
├── config/                         # Konfigürasyon dosyaları
├── tests/                          # Test dosyaları
├── docs/                           # Dokümantasyon
├── scripts/                        # Yardımcı betikler
└── requirements.txt                # Bağımlılıklar"""
p = doc.add_paragraph()
r = p.add_run(dirs)
r.font.size = Pt(8)
r.font.name = 'Consolas'

doc.add_page_break()

# ═══════════════════════════════════════════════════════
# BÖLÜM 5
# ═══════════════════════════════════════════════════════
doc.add_heading('5. Statik Analiz Modülü — Detaylı Teknik Açıklama', level=1)

# 5.1
doc.add_heading('5.1. Statik Analiz Orkestratörü (StaticAnalyzer)', level=2)
doc.add_paragraph('Dosya: androidsec/static_analysis/analyzer.py (464 satır)').runs[0].italic = True
doc.add_paragraph(
    'StaticAnalyzer sınıfı, tüm statik analiz sürecini yöneten merkezi orkestratör bileşenidir. '
    'Dört analiz fazını sırasıyla yürütür ve tüm bulguları birleştirilmiş bir liste olarak döndürür.'
)
doc.add_paragraph('Analiz Akışı:', style='List Bullet')
doc.add_paragraph('Faz 1: Manifest Analizi → AndroidManifest.xml parsing, izin ve component kontrolü', style='List Bullet 2')
doc.add_paragraph('Faz 2: Kod Analizi → Java/Kotlin kaynak kodlarının güvenlik taraması', style='List Bullet 2')
doc.add_paragraph('Faz 3: Sertifika Analizi → APK imza sertifikasının çıkarılması ve doğrulanması', style='List Bullet 2')
doc.add_paragraph('Faz 4: Native Kod Analizi → .so kütüphanelerinin ELF ve string analizi', style='List Bullet 2')

doc.add_paragraph('Temel Özellikler:')
doc.add_paragraph('Çift modlu çalışma: Hem sadece APK dosyasıyla hem de dekompile edilmiş klasörle birlikte analiz yapabilir.', style='List Bullet')
doc.add_paragraph('Hata toleransı: Her analiz fazı bağımsız try-except blokları içerisindedir; bir fazda oluşan hata diğer fazların çalışmasını engellemez.', style='List Bullet')
doc.add_paragraph('İstatistik üretimi: get_statistics() metodu ile bulgular severity ve OWASP kategorisine göre gruplanarak istatistiksel özet çıkarılır.', style='List Bullet')

doc.add_paragraph('Bulgu (Finding) Veri Yapısı:')
p = doc.add_paragraph()
r = p.add_run(
    '{\n'
    '    "category": "OWASP M2",        # OWASP kategorisi\n'
    '    "severity": "HIGH",             # CRITICAL/HIGH/MEDIUM/LOW/INFO\n'
    '    "title": "Insecure Data",       # Kısa başlık\n'
    '    "description": "...",           # Detaylı açıklama\n'
    '    "file": "MainActivity.java",   # İlgili dosya\n'
    '    "line": 42,                    # Satır numarası\n'
    '    "recommendation": "..."        # Çözüm önerisi\n'
    '}'
)
r.font.size = Pt(9)
r.font.name = 'Consolas'

# 5.2
doc.add_heading('5.2. Manifest Analizi', level=2)
doc.add_paragraph(
    'Manifest analizi, Android uygulamasının "kimlik belgesi" olan AndroidManifest.xml dosyasını '
    'güvenlik açısından inceler. Bu modül üç bileşenden oluşmaktadır.'
)

doc.add_heading('5.2.1. ManifestParser', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/manifest/parser.py (291 satır)').runs[0].italic = True
doc.add_paragraph(
    'ManifestParser, AndroidManifest.xml dosyasını XML olarak parse ederek yapılandırılmış bir Python '
    'sözlüğüne dönüştürür. Python standart kütüphanesi olan xml.etree.ElementTree kullanılır.'
)
add_table(
    ['Çıkarılan Alan', 'Açıklama', 'Güvenlik Önemi'],
    [
        ('package', 'Uygulama paket adı', 'Kimlik tanıma'),
        ('version_name / version_code', 'Uygulama versiyonu', 'Versiyon takibi'),
        ('min_sdk / target_sdk', 'SDK versiyonları', 'Eski SDK → güvenlik açıkları'),
        ('permissions', 'Talep edilen izinler', 'Aşırı yetki, gizlilik riski'),
        ('activities', 'Activity listesi ve exported durumu', 'Yetkisiz erişim riski'),
        ('services', 'Service listesi', 'Yetkisiz işlem tetikleme'),
        ('receivers', 'Broadcast Receiver listesi', 'Broadcast spoofing'),
        ('providers', 'Content Provider listesi', 'SQL injection, veri sızıntısı'),
        ('is_debuggable', 'Debug modu aktif mi?', 'Çok kritik güvenlik riski'),
        ('allow_backup', 'Veri yedekleme izni', 'ADB ile veri çıkarma'),
        ('uses_cleartext_traffic', 'HTTP trafiği izinli mi?', 'MITM saldırısı riski'),
    ]
)
doc.add_paragraph()
doc.add_paragraph(
    'Exported component tespiti: Bir component exported="true" olarak işaretlenmemiş olsa bile, '
    'bir intent-filter içermesi durumunda Android sistemi tarafından otomatik olarak exported kabul edilir. '
    'Parser bu durumu algılamaktadır.'
)

doc.add_heading('5.2.2. PermissionAnalyzer', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/manifest/permissions.py (451 satır)').runs[0].italic = True
doc.add_paragraph('PermissionAnalyzer, uygulamanın talep ettiği Android izinlerini güvenlik açısından kapsamlı olarak analiz eder. Altı farklı kontrol mekanizması uygulanmaktadır:')

doc.add_paragraph('1. Tehlikeli İzin Tespiti: Android\'in resmi "dangerous" kategorisindeki izinleri tespit eder. Bu izinler kullanıcının çalışma zamanında açıkça onay vermesini gerektirir.', style='List Bullet')
doc.add_paragraph('2. Gizlilik İzin Analizi: SMS/MMS erişim izinleri (yüksek risk), konum izinleri (arka plan konum erişimi kritik), kamera + mikrofon kombinasyonu (gözetleme riski).', style='List Bullet')
doc.add_paragraph('3. Cihaz Yöneticisi İzinleri: BIND_DEVICE_ADMIN, SYSTEM_ALERT_WINDOW, REQUEST_INSTALL_PACKAGES gibi çok güçlü yetkilerin tespiti.', style='List Bullet')
doc.add_paragraph('4. Tehlikeli İzin Kombinasyonları: INTERNET+READ_CONTACTS (kişi sızıntısı), INTERNET+READ_SMS (OTP sızıntısı), RECEIVE_BOOT_COMPLETED+INTERNET (kalıcı malware).', style='List Bullet')
doc.add_paragraph('5. İzin Sayısı Kontrolü: 20\'den fazla izin → "aşırı yetkilendirilmiş" uyarısı.', style='List Bullet')
doc.add_paragraph('6. Özel (Custom) İzin Kontrolü: Uygulamanın kendi tanımladığı izinlerin protectionLevel kontrolü.', style='List Bullet')

doc.add_heading('5.2.3. ComponentAnalyzer', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/manifest/components.py (436 satır)').runs[0].italic = True
doc.add_paragraph('ComponentAnalyzer, Android uygulamasının dört temel bileşenini güvenlik açısından analiz eder:')
doc.add_paragraph('Activity Analizi: Exported activity tespiti, hassas isimlendirme kontrolü (admin, settings, login, payment vb.), 5\'ten fazla exported activity uyarısı.', style='List Bullet')
doc.add_paragraph('Service Analizi: Exported service tespiti → yetkisiz işlem tetikleme, DoS riski.', style='List Bullet')
doc.add_paragraph('Broadcast Receiver Analizi: Exported receiver tespiti → broadcast spoofing riski.', style='List Bullet')
doc.add_paragraph('Content Provider Analizi: Exported provider → HIGH seviyesinde raporlanır (SQL Injection, Path Traversal riski).', style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Genel Güvenlik Kontrolleri:')
add_table(
    ['Kontrol', 'Koşul', 'Severity'],
    [
        ('Debuggable', 'android:debuggable="true"', 'CRITICAL'),
        ('AllowBackup', 'android:allowBackup="true"', 'MEDIUM'),
        ('Cleartext Traffic', 'android:usesCleartextTraffic="true"', 'HIGH'),
        ('Düşük Min SDK', 'minSdkVersion < 21', 'MEDIUM'),
        ('Düşük Target SDK', 'targetSdkVersion < 28', 'MEDIUM'),
    ]
)

doc.add_page_break()

# 5.3
doc.add_heading('5.3. Kaynak Kod Analizi', level=2)
doc.add_paragraph(
    'Kaynak kod analizi, APK\'nın dekompile edilmesiyle elde edilen Java ve Kotlin kaynak dosyalarını '
    'güvenlik açıkları için tarar. Bu modül üç bileşenden oluşmaktadır.'
)

doc.add_heading('5.3.1. CodeScanner', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/code/scanner.py (263 satır)').runs[0].italic = True
doc.add_paragraph('CodeScanner, ana tarama orkestratörüdür. .java ve .kt dosyalarını bulur ve beş farklı güvenlik kontrolü uygular:')
doc.add_paragraph('Kriptografi analizi → CryptoAnalyzer alt modülü', style='List Bullet')
doc.add_paragraph('Hardcoded secret tespiti → SecretsDetector alt modülü', style='List Bullet')
doc.add_paragraph('SQL Injection kontrolü: execSQL() ve rawQuery() metotlarında string concatenation tespiti', style='List Bullet')
doc.add_paragraph('WebView güvenlik kontrolü: setJavaScriptEnabled(true) → XSS riski, setAllowFileAccess(true) → dosya erişimi riski', style='List Bullet')
doc.add_paragraph('Hassas veri loglama kontrolü: Log.d/i/v/w/e ifadelerinde password, token, api_key gibi hassas kelimelerin aranması', style='List Bullet')

doc.add_heading('5.3.2. CryptoAnalyzer', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/code/crypto_analyzer.py (253 satır)').runs[0].italic = True
doc.add_paragraph('CryptoAnalyzer, kriptografi ile ilgili güvenlik açıklarını tespit eder:')
add_table(
    ['Kontrol', 'Tespit Edilen', 'Severity', 'Güvenli Alternatif'],
    [
        ('Zayıf Hash', 'MD5, SHA1, SHA-1', 'CRITICAL', 'SHA-256, SHA-3'),
        ('Zayıf Şifreleme', 'DES, RC4, RC2, Blowfish', 'CRITICAL', 'AES-256'),
        ('Güvensiz Mod', 'ECB (Electronic Codebook)', 'HIGH', 'CBC, GCM'),
        ('Güvensiz Random', 'java.util.Random', 'MEDIUM', 'SecureRandom'),
        ('Hardcoded Key', 'byte[] key = {...}', 'CRITICAL', 'Android Keystore'),
    ]
)

doc.add_heading('5.3.3. SecretsDetector', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/code/secrets_detector.py (167 satır)').runs[0].italic = True
doc.add_paragraph('SecretsDetector, kaynak kodda gömülü (hardcoded) hassas bilgileri tespit eder:')
add_table(
    ['Secret Türü', 'Pattern', 'Severity'],
    [
        ('AWS Access Key', 'AKIA[0-9A-Z]{16}', 'CRITICAL'),
        ('Google API Key', 'AIza[0-9A-Za-z-_]{35}', 'CRITICAL'),
        ('Firebase URL', 'https://[...].firebaseio.com', 'HIGH'),
        ('Generic API Key', 'api_key = "..."', 'HIGH'),
        ('Hardcoded Password', 'password = "..."', 'CRITICAL'),
        ('Private Key', '-----BEGIN PRIVATE KEY-----', 'CRITICAL'),
        ('Database URL', 'jdbc:[a-z]+://...', 'HIGH'),
    ]
)
doc.add_paragraph()
doc.add_paragraph('Akıllı filtreleme: Yorum satırlarındaki eşleşmeler göz ardı edilir (false positive önleme). Tespit edilen değerler maskelenerek raporlanır.')

doc.add_page_break()

# 5.4
doc.add_heading('5.4. Sertifika Analizi', level=2)

doc.add_heading('5.4.1. CertificateExtractor', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/certificate/extractor.py (480 satır)').runs[0].italic = True
doc.add_paragraph(
    'CertificateExtractor, APK dosyasının ZIP yapısı içindeki META-INF/ klasöründen sertifika dosyasını '
    '(.RSA, .DSA, .EC) bulur ve bilgilerini çıkarır. İki aşamalı çıkarma stratejisi kullanılır:'
)
doc.add_paragraph('1. keytool ile çıkarma: Java JDK\'nın keytool -printcert komutu kullanılarak tam sertifika bilgileri elde edilir. Çıktı regex ile parse edilir.', style='List Bullet')
doc.add_paragraph('2. Manuel çıkarma: keytool mevcut değilse, DER/PKCS#7 formatındaki binary sertifika verisinden hash fingerprint\'leri hesaplanır ve CN=, O=, OU= gibi alanlar regex ile çıkarılır.', style='List Bullet')
doc.add_paragraph()
doc.add_paragraph('Çıkarılan bilgiler: subject, issuer, valid_from/valid_to, serial_number, signature_algorithm, version, fingerprint_sha256/sha1/md5, common_name, organization.')

doc.add_heading('5.4.2. CertificateValidator', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/certificate/validator.py (280 satır)').runs[0].italic = True
add_table(
    ['Kontrol', 'Koşul', 'Severity', 'Açıklama'],
    [
        ('Self-Signed', 'subject == issuer', 'MEDIUM', 'Güvenilir CA tarafından imzalanmamış'),
        ('Süresi Dolmuş', 'valid_to < now()', 'CRITICAL', 'Sertifika artık geçerli değil'),
        ('Zayıf Algoritma', 'MD5withRSA, SHA1withRSA', 'HIGH', 'Kriptografik olarak kırılmış'),
        ('Debug Sertifikası', 'CN=Android Debug', 'CRITICAL', 'Production\'da olmamalı'),
        ('Kısa Geçerlilik', '< 25 yıl', 'MEDIUM', 'Google Play minimum gerekliliği'),
    ]
)

doc.add_page_break()

# 5.5
doc.add_heading('5.5. Native Kod Analizi', level=2)

doc.add_heading('5.5.1. SOAnalyzer', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/native/so_analyzer.py (451 satır)').runs[0].italic = True
doc.add_paragraph(
    'SOAnalyzer, .so dosyalarının ELF (Executable and Linkable Format) yapısını analiz eder. '
    'ELF header\'dan class (32/64-bit), endianness, PIE durumu ve machine type bilgileri çıkarılır. '
    'PIE kapalıysa ASLR çalışmaz ve HIGH seviyesinde raporlanır.'
)
doc.add_paragraph('Tehlikeli C Fonksiyonları Tespiti:')
add_table(
    ['Fonksiyon', 'Risk', 'Severity', 'Güvenli Alternatif'],
    [
        ('system()', 'Komut çalıştırma', 'CRITICAL', 'Spesifik API\'ler'),
        ('exec()', 'Program çalıştırma', 'HIGH', 'Doğrudan API kullanımı'),
        ('gets()', 'Sınırsız input → Buffer overflow', 'CRITICAL', 'fgets()'),
        ('strcpy()', 'Buffer overflow', 'MEDIUM', 'strncpy()'),
        ('strcat()', 'Buffer overflow', 'MEDIUM', 'strncat()'),
        ('sprintf()', 'Format string açığı', 'MEDIUM', 'snprintf()'),
    ]
)
doc.add_paragraph()
doc.add_paragraph('Ek olarak: Mimari analizi (arm64-v8a desteği kontrolü) ve bilinen zafiyetli kütüphane tespiti (libssl.so, libcrypto.so, libsqlite.so) gerçekleştirilir.')

doc.add_heading('5.5.2. StringsExtractor', level=3)
doc.add_paragraph('Dosya: androidsec/static_analysis/native/strings_extractor.py (500 satır)').runs[0].italic = True
doc.add_paragraph(
    'StringsExtractor, binary dosyalardan okunabilir ASCII stringlerini çıkararak güvenlik açısından analiz eder. '
    'Linux strings komutu gibi çalışır. Beş farklı güvenlik kontrolü uygular:'
)
doc.add_paragraph('URL Kontrolü: HTTP URL\'ler → HIGH (MITM riski), HTTPS → INFO (altyapı ifşası)', style='List Bullet')
doc.add_paragraph('IP Adresi Kontrolü: Genel IP adresleri → MEDIUM (C&C sunucu iletişimi göstergesi)', style='List Bullet')
doc.add_paragraph('API Anahtarı Kontrolü: AWS, Google API, generic key/secret/token → CRITICAL', style='List Bullet')
doc.add_paragraph('Dosya Yolu Kontrolü: /sdcard/, /data/data/, /proc/ erişimleri', style='List Bullet')
doc.add_paragraph('Şüpheli Komut Kontrolü: su, chmod, mount, pm install gibi sistem komutları', style='List Bullet')

doc.add_page_break()

# ═══════════════════════════════════════════════════════
# BÖLÜM 6
# ═══════════════════════════════════════════════════════
doc.add_heading('6. Destekleyici Altyapı Modülleri', level=1)

doc.add_heading('6.1. Core Modülü', level=2)
doc.add_paragraph('constants.py (101 satır): Severity seviyeleri (CRITICAL→10.0, HIGH→7.5, MEDIUM→5.0, LOW→2.5, INFO→1.0), OWASP Mobile Top 10 kategorileri, tehlikeli izinler listesi, dosya uzantıları ve dizin yolları.', style='List Bullet')
doc.add_paragraph('exceptions.py (124 satır): AndroidSecError ana sınıfından türeyen hiyerarşik hata sınıfları: ConfigurationError, StaticAnalysisError, DynamicAnalysisError, FridaError, ADBError vb.', style='List Bullet')
doc.add_paragraph('config_manager.py (154 satır): YAML dosyalarından konfigürasyon okuma, nokta notasyonuyla nested erişim, runtime değişiklik desteği.', style='List Bullet')
doc.add_paragraph('analyzer.py (343 satır): Ana analiz motoru — APK doğrulama, statik/dinamik analiz orkestrasyon ve risk skoru hesaplaması (0-10 normalizasyon).', style='List Bullet')

doc.add_heading('6.2. Utils ve CLI Modülleri', level=2)
doc.add_paragraph('logger.py (99 satır): Merkezi log sistemi — console ve dosya çıktı, duplicate handler önleme, otomatik log dizini oluşturma.', style='List Bullet')
doc.add_paragraph('CLI (main.py — 58 satır): Click framework tabanlı komut satırı arayüzü: androidsec scan app.apk, --static-only, --output html seçenekleri.', style='List Bullet')

# ═══════════════════════════════════════════════════════
# BÖLÜM 7
# ═══════════════════════════════════════════════════════
doc.add_heading('7. OWASP Mobile Top 10 Entegrasyonu', level=1)
doc.add_paragraph('Tüm bulgular OWASP Mobile Top 10 standartları çerçevesinde kategorize edilmektedir:')
add_table(
    ['OWASP Kategorisi', 'Kontrol Edilen Alanlar'],
    [
        ('M1: Improper Platform Usage', 'Debuggable flag, düşük SDK, aşırı izinler, cihaz yönetici izinleri'),
        ('M2: Insecure Data Storage', 'AllowBackup, SMS/konum izinleri, hassas veri loglama'),
        ('M3: Insecure Communication', 'Cleartext traffic, HTTP URL\'ler (native), hardcoded IP'),
        ('M5: Insufficient Cryptography', 'MD5/SHA1 hash, DES/RC4, ECB mode, insecure Random, hardcoded key'),
        ('M6: Insecure Authorization', 'Exported activity/service, hassas ekranların dışa açılması'),
        ('M7: Client Code Quality', 'SQL injection, PIE eksikliği, tehlikeli C fonksiyonları'),
        ('M8: Code Tampering', 'Debug sertifikası, süresi dolmuş sertifika, zayıf imza algoritması'),
        ('M9: Reverse Engineering', 'Hardcoded API keys/secrets/passwords, native kodda gömülü URL'),
        ('M10: Extraneous Functionality', 'Boot-completed+internet kombinasyonu, şüpheli native komutlar'),
    ]
)

# ═══════════════════════════════════════════════════════
# BÖLÜM 8
# ═══════════════════════════════════════════════════════
doc.add_heading('8. Test Altyapısı', level=1)
doc.add_paragraph(
    'Statik analiz modülünün güvenilirliğini sağlamak amacıyla kapsamlı bir test altyapısı hazırlanmıştır. '
    'Pytest fixture sistemi kullanılarak test verileri merkezi olarak yönetilmektedir (conftest.py — 155 satır).'
)
add_table(
    ['Fixture Kategorisi', 'İçerik'],
    [
        ('Manifest Fixture\'ları', 'Zafiyetli, güvenli ve minimal AndroidManifest.xml dosyaları'),
        ('APK Fixture\'ları', 'Sertifika ve native kütüphane içeren/içermeyen yapay APK dosyaları'),
        ('Decompiled Dir Fixture\'ları', 'Güvenli ve zafiyetli Java kodu içeren yapay dekompile klasörleri'),
        ('Sertifika Fixture\'ları', 'Normal, süresi dolmuş, debug, zayıf algoritmalı sertifikalar'),
    ]
)
doc.add_paragraph()
doc.add_paragraph('Birim Testleri: test_static_analysis.py (38.828 byte) — tüm alt bileşenler için hem pozitif hem negatif senaryoları kapsayan testler.')

doc.add_page_break()

# ═══════════════════════════════════════════════════════
# BÖLÜM 9
# ═══════════════════════════════════════════════════════
doc.add_heading('9. Kod İstatistikleri', level=1)
add_table(
    ['Metrik', 'Değer'],
    [
        ('Toplam Python dosyası', '80'),
        ('Toplam kod satırı', '~6.989'),
        ('Statik analiz modülü dosya sayısı', '10'),
        ('Statik analiz modülü toplam satır', '~4.036'),
        ('Tespit edilen benzersiz zafiyet türü', '30+'),
        ('Desteklenen OWASP kategorisi', '10/10'),
        ('Severity seviyeleri', '5 (CRITICAL, HIGH, MEDIUM, LOW, INFO)'),
    ]
)
doc.add_paragraph()
doc.add_paragraph('Modül Bazlı Satır Dağılımı:')
add_table(
    ['Dosya', 'Satır', 'İşlev'],
    [
        ('static_analysis/analyzer.py', '464', 'Orkestratör'),
        ('manifest/parser.py', '291', 'XML parsing'),
        ('manifest/permissions.py', '451', 'İzin analizi'),
        ('manifest/components.py', '436', 'Component analizi'),
        ('code/scanner.py', '263', 'Kod tarayıcı'),
        ('code/crypto_analyzer.py', '253', 'Kriptografi analizi'),
        ('code/secrets_detector.py', '167', 'Secret tespiti'),
        ('certificate/extractor.py', '480', 'Sertifika çıkarma'),
        ('certificate/validator.py', '280', 'Sertifika doğrulama'),
        ('native/so_analyzer.py', '451', 'SO analizi'),
        ('native/strings_extractor.py', '500', 'String çıkarma'),
        ('TOPLAM', '4.036', ''),
    ]
)

# ═══════════════════════════════════════════════════════
# BÖLÜM 10
# ═══════════════════════════════════════════════════════
doc.add_heading('10. Mevcut Durum ve Sonraki Adımlar', level=1)
doc.add_heading('10.1. Tamamlanan Çalışmalar', level=2)
completed = [
    'Proje mimarisi tasarımı ve modüler yapı oluşturulması',
    'Çekirdek altyapı modüllerinin geliştirilmesi (constants, exceptions, config, logger)',
    'StaticAnalyzer orkestratör sınıfının implementasyonu',
    'ManifestParser — AndroidManifest.xml parsing motoru',
    'PermissionAnalyzer — 6 farklı izin kontrol mekanizması',
    'ComponentAnalyzer — 4 component türünün güvenlik analizi ve 5 genel kontrol',
    'CodeScanner — Java/Kotlin kaynak kod tarama altyapısı',
    'CryptoAnalyzer — 5 farklı kriptografi güvenlik kontrolü',
    'SecretsDetector — 10 farklı secret pattern tespiti',
    'CertificateExtractor — keytool ve manuel olmak üzere çift aşamalı çıkarma',
    'CertificateValidator — 5 farklı sertifika doğrulama kontrolü',
    'SOAnalyzer — ELF header analizi, tehlikeli fonksiyon tespiti, mimari analizi',
    'StringsExtractor — URL, IP, API key, dosya yolu ve komut analizi',
    'CLI arayüzü (Click framework)',
    'Test altyapısı ve fixture sistemi',
    'Birim testleri',
]
for item in completed:
    doc.add_paragraph(f'✅ {item}', style='List Bullet')

doc.add_heading('10.2. Sonraki Adımlar', level=2)
next_steps = [
    'Proje ortağının dinamik analiz modülünü tamamlaması',
    'Statik ve dinamik analiz sonuçlarının korelasyon modülü ile birleştirilmesi',
    'Entegrasyon testlerinin tamamlanması',
    'Uçtan uca (end-to-end) testlerin gerçekleştirilmesi',
    'HTML/JSON rapor oluşturma modülünün tamamlanması',
    'Gerçek APK dosyaları üzerinde kapsamlı test aşaması',
]
for item in next_steps:
    doc.add_paragraph(f'⬜ {item}', style='List Bullet')

p = doc.add_paragraph()
r = p.add_run(
    '\nÖNEMLİ NOT: Projenin dinamik analiz kısmı proje ortağı tarafından geliştirilmektedir. '
    'Dinamik analiz modülü tamamlandığında, her iki modülün entegrasyonu ve kapsamlı test aşaması başlayacaktır.'
)
r.bold = True
r.font.color.rgb = RGBColor(0xc0, 0x39, 0x2b)

# ═══════════════════════════════════════════════════════
# BÖLÜM 11
# ═══════════════════════════════════════════════════════
doc.add_heading('11. Sonuç', level=1)
doc.add_paragraph(
    'Bu raporda, AndroidSecAnalyzer projesinin statik analiz modülünün tasarım, geliştirme ve '
    'implementasyon sürecini detaylı olarak açıkladım. Geliştirdiğim statik analiz modülü, bir '
    'Android uygulamasının güvenlik durumunu dört farklı perspektiften (manifest, kaynak kod, '
    'sertifika, native kod) kapsamlı olarak değerlendirebilmektedir.'
)
doc.add_paragraph(
    'Modül, toplamda 30\'dan fazla benzersiz güvenlik kontrolü gerçekleştirmekte ve tüm bulguları '
    'OWASP Mobile Top 10 standartları çerçevesinde kategorize etmektedir. Modüler mimari tasarımı '
    'sayesinde, her bir alt bileşen bağımsız olarak genişletilebilir ve test edilebilir durumdadır.'
)
doc.add_paragraph(
    'Projenin dinamik analiz kısmı da tamamlandığında, her iki analiz yaklaşımının bulguları '
    'korelasyon modülü aracılığıyla birleştirilerek kapsamlı bir güvenlik raporu üretilecektir. '
    'Bu aşamada gerçek APK dosyaları üzerinde detaylı test çalışmaları gerçekleştirilecektir.'
)

# Footer
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Bu rapor, İstanbul Atlas Üniversitesi Yazılım Mühendisliği Bölümü Bitirme Projesi kapsamında hazırlanmıştır.\n© 2026 — Damla YÜKSEL')
r.italic = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# ═══════════════════════════════════════════════════════
# KAYDET
# ═══════════════════════════════════════════════════════
output_path = os.path.expanduser('~/Desktop/Siber Proje/AndroidSecAnalyzer/Statik_Analiz_Raporu.docx')
doc.save(output_path)
print(f'✅ Rapor oluşturuldu: {output_path}')
