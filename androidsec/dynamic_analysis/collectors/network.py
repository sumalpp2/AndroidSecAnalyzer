"""
androidsec/dynamic_analysis/collectors/network.py

Logcat içinden basit network ile ilgili bulguları çıkarır.
"""

import logging
import re

logger = logging.getLogger(__name__)


class NetworkCollector:
    def __init__(self):
        self.patterns = [
            (r"http://[^\s\"']+", "Şifresiz HTTP trafiği", "HIGH",
             "M3: Insecure Communication",
             "Uygulama şifresiz HTTP protokolü kullanıyor. Tüm iletişim HTTPS üzerinden yapılmalıdır."),
            (r"cleartext", "Cleartext traffic tespit edildi", "HIGH",
             "M3: Insecure Communication",
             "Cleartext trafik tespit edildi. android:usesCleartextTraffic=false olarak ayarlanmalıdır."),
            (r"ssl.*error|ssl.*exception|sslhandshakeexception", "SSL hatası tespit edildi", "HIGH",
             "M3: Insecure Communication",
             "SSL/TLS hatası tespit edildi. Sertifika yapılandırması kontrol edilmelidir."),
            (r"trust.*anchor|certificate.*not.*trusted|unable to find valid certification",
             "Sertifika doğrulama hatası", "HIGH",
             "M3: Insecure Communication",
             "Sertifika güven zinciri doğrulanamadı. Certificate pinning uygulanmalıdır."),
            (r"hostname.*not.*verified|hostnameverifier",
             "Hostname doğrulaması ile ilgili şüpheli durum", "HIGH",
             "M3: Insecure Communication",
             "Hostname doğrulama bypass edilmiş olabilir. Custom HostnameVerifier kontrol edilmelidir."),
            (r"x509trustmanager|trustallcerts|trust_all",
             "Tüm sertifikalara güveniliyor olabilir", "HIGH",
             "M3: Insecure Communication",
             "TrustAllCerts veya custom TrustManager kullanılıyor. MITM saldırılarına açık olabilir."),
            (r"handshake", "SSL/TLS handshake logu", "LOW",
             "M3: Insecure Communication",
             "SSL/TLS handshake işlemi gözlemlendi."),
            (r"https://[^\s\"']+", "HTTPS trafiği gözlemlendi", "LOW",
             "M3: Insecure Communication",
             "Şifreli HTTPS trafiği gözlemlendi — bilgi amaçlı."),
            (r"connect(ion)? (to|refused|reset|closed)", "Ağ bağlantı olayı", "LOW",
             "M3: Insecure Communication",
             "Ağ bağlantı durumu değişikliği gözlemlendi."),
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

        logger.info("Network analizi tamamlandı. Bulgu sayısı: %d", len(findings))
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
