"""
androidsec/dynamic_analysis/collectors/storage.py

Logcat içinden veri saklama ile ilgili basit güvenlik bulgularını çıkarır.
"""

import logging
import re

logger = logging.getLogger(__name__)


class StorageCollector:
    def __init__(self):
        self.patterns = [
            (r"password", "Log içinde 'password' geçiyor", "HIGH",
             "M2: Insecure Data Storage",
             "Loglarda parola bilgisi tespit edildi. Hassas veriler asla loglanmamalıdır."),
            (r"token", "Log içinde 'token' geçiyor", "HIGH",
             "M2: Insecure Data Storage",
             "Loglarda token bilgisi tespit edildi. Token'lar güvenli depolanmalıdır."),
            (r"secret", "Log içinde 'secret' geçiyor", "HIGH",
             "M2: Insecure Data Storage",
             "Loglarda gizli anahtar bilgisi tespit edildi."),
            (r"api_key|apikey", "Log içinde API anahtarı geçiyor", "HIGH",
             "M9: Reverse Engineering",
             "API anahtarı loglarda tespit edildi. Anahtarlar güvenli saklanmalıdır."),
            (r"private_key|privatekey", "Log içinde private key geçiyor", "HIGH",
             "M5: Insufficient Cryptography",
             "Özel anahtar loglarda tespit edildi. Kriptografik anahtarlar keystore'da saklanmalıdır."),
            (r"sqlite|\.db", "SQLite veritabanı erişimi tespit edildi", "MEDIUM",
             "M2: Insecure Data Storage",
             "SQLite veritabanı erişimi gözlemlendi. Hassas veriler şifrelenerek saklanmalıdır."),
            (r"sharedpreferences", "SharedPreferences erişimi tespit edildi", "MEDIUM",
             "M2: Insecure Data Storage",
             "SharedPreferences erişimi tespit edildi. MODE_PRIVATE kullanıldığından emin olun."),
            (r"database", "Veritabanı erişimi tespit edildi", "MEDIUM",
             "M2: Insecure Data Storage",
             "Veritabanı erişimi tespit edildi. Hassas veriler şifrelenerek saklanmalıdır."),
            (r"external.?storage|sdcard", "Harici depolama erişimi tespit edildi", "MEDIUM",
             "M2: Insecure Data Storage",
             "Harici depolama erişimi tespit edildi. Harici depolama herkes tarafından okunabilir."),
            (r"world.?readable|world.?writable|mode_world",
             "Dosya herkese açık modda oluşturuluyor olabilir", "HIGH",
             "M2: Insecure Data Storage",
             "World-readable/writable dosya modu tespit edildi. MODE_PRIVATE kullanılmalıdır."),
            (r"cache", "Cache erişimi tespit edildi", "LOW",
             "M2: Insecure Data Storage",
             "Önbellek erişimi gözlemlendi — bilgi amaçlı."),
            (r"write.*file|file.*write", "Dosyaya yazma işlemi tespit edildi", "LOW",
             "M2: Insecure Data Storage",
             "Dosya yazma işlemi gözlemlendi — bilgi amaçlı."),
            (r"<script>|javascript:|alert\(", "XSS Payload Tespiti (Log Leak)", "HIGH",
             "M7: Client Code Quality",
             "Kullanıcı girdisine ait bir XSS payload'u loglara yansıdı. Girdi doğrulaması ve encoding eksik olabilir."),
            (r"' or 1=1|drop table|select \* from", "SQLi/Injection Payload Tespiti (Log Leak)", "HIGH",
             "M7: Client Code Quality",
             "Kullanıcı girdisine ait SQL enjeksiyon denemesi loglara yansıdı. Girdi doğrulaması (Input Validation) eksik olabilir."),
        ]

    def analyze(self, logs):
        if not logs:
            logger.warning("Analiz edilecek log bulunamadı.")
            return []

        findings = []
        seen = set()

        lines = logs.splitlines()

        for line in lines:
            line_lower = line.lower()

            for pattern, title, severity, category, recommendation in self.patterns:
                if re.search(pattern, line_lower):
                    key = title

                    if key not in seen:
                        seen.add(key)

                        findings.append({
                            "category": category,
                            "severity": severity,
                            "title": title,
                            "description": f"Logcat'te en az bir kere tespit edildi: {line.strip()[:200]}",
                            "detail": line.strip(),
                            "recommendation": recommendation,
                        })

        logger.info("Storage analizi tamamlandı. Bulgu sayısı: %d", len(findings))
        return findings

    def summarize(self, findings):
        summary = {
            "total": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }

        summary["total"] = len(findings)

        for finding in findings:
            severity = finding["severity"]

            if severity == "HIGH":
                summary["high"] += 1
            elif severity == "MEDIUM":
                summary["medium"] += 1
            elif severity == "LOW":
                summary["low"] += 1

        return summary
