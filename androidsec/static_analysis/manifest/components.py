"""
Component Analyzer
Android componentlerini (Activity, Service, Receiver, Provider) güvenlik açısından analiz eder

Ne kontrol ediyoruz?
1. Exported componentler (dışa açık → diğer uygulamalar erişebilir)
2. Intent filter güvenliği
3. Content Provider güvenliği (SQL injection, path traversal riski)
4. Service güvenliği (bind izinleri)
5. Broadcast Receiver güvenliği
"""

from typing import List, Dict, Any

from androidsec.core.constants import (
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    SEVERITY_MEDIUM,
    SEVERITY_LOW,
    SEVERITY_INFO,
)
from androidsec.utils.logger import get_logger

logger = get_logger(__name__)


class ComponentAnalyzer:
    """
    Android componentlerinin güvenlik analizini yapar

    Kullanım:
        analyzer = ComponentAnalyzer()
        findings = analyzer.analyze(manifest_data)
    """

    def __init__(self):
        """Initialize component analyzer"""
        logger.debug("ComponentAnalyzer initialized")

    def analyze(self, manifest_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Tüm componentleri analiz et

        Args:
            manifest_data: ManifestParser.parse() çıktısı

        Returns:
            Bulgular listesi
        """
        logger.info("Analyzing components...")

        findings = []

        # 1. Activity güvenliği
        activities = manifest_data.get("activities", [])
        findings.extend(self._analyze_activities(activities))

        # 2. Service güvenliği
        services = manifest_data.get("services", [])
        findings.extend(self._analyze_services(services))

        # 3. Broadcast Receiver güvenliği
        receivers = manifest_data.get("receivers", [])
        findings.extend(self._analyze_receivers(receivers))

        # 4. Content Provider güvenliği
        providers = manifest_data.get("providers", [])
        findings.extend(self._analyze_providers(providers))

        # 5. Genel güvenlik kontrolleri
        findings.extend(self._check_general_security(manifest_data))

        logger.info(f"Component analysis complete: {len(findings)} findings")
        return findings

    # ─── Activity Analizi ──────────────────────────────────────────

    def _analyze_activities(self, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Activity'leri güvenlik açısından analiz et

        Exported Activity riskleri:
        - Yetkilendirme atlatma (bypass)
        - Hassas ekranlara doğrudan erişim
        - Intent injection
        """
        findings = []

        exported_activities = [a for a in activities if a.get("exported", False)]

        if not exported_activities:
            return findings

        # Exported activity'leri raporla
        for activity in exported_activities:
            name = activity.get("name", "Unknown")
            has_filter = activity.get("has_intent_filter", False)

            # Hassas ekran isimleri (şüpheli)
            suspicious_names = [
                "admin", "settings", "config", "debug", "test",
                "internal", "private", "secret", "password",
                "login", "auth", "payment", "bank", "credit",
            ]

            is_suspicious = any(
                keyword in name.lower()
                for keyword in suspicious_names
            )

            if is_suspicious:
                findings.append({
                    "category": "M6: Insecure Authorization",
                    "severity": SEVERITY_HIGH,
                    "title": f"Sensitive Exported Activity: {self._short_name(name)}",
                    "description": (
                        f"Activity '{name}' is exported and its name suggests "
                        "it contains sensitive functionality. "
                        "Other apps can directly access this activity."
                    ),
                    "file": "AndroidManifest.xml",
                    "recommendation": (
                        "Set android:exported='false' or add proper permission checks. "
                        "Use android:permission attribute to restrict access."
                    )
                })
            elif not has_filter:
                # exported=true ama intent-filter yok → bilinçli açılmış
                findings.append({
                    "category": "M6: Insecure Authorization",
                    "severity": SEVERITY_MEDIUM,
                    "title": f"Exported Activity: {self._short_name(name)}",
                    "description": (
                        f"Activity '{name}' is explicitly exported without intent filters. "
                        "Verify that external access is intended."
                    ),
                    "file": "AndroidManifest.xml",
                    "recommendation": (
                        "If external access is not needed, set android:exported='false'."
                    )
                })

        # Toplam exported activity sayısı
        if len(exported_activities) > 5:
            findings.append({
                "category": "M1: Improper Platform Usage",
                "severity": SEVERITY_MEDIUM,
                "title": f"Many Exported Activities ({len(exported_activities)})",
                "description": (
                    f"Application exports {len(exported_activities)} activities. "
                    "Each exported activity increases the attack surface."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": "Minimize the number of exported activities."
            })

        return findings

    # ─── Service Analizi ───────────────────────────────────────────

    def _analyze_services(self, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Service'leri güvenlik açısından analiz et

        Exported Service riskleri:
        - Yetkisiz işlem tetikleme
        - Veri sızıntısı (bound service ile)
        - DoS (sürekli service başlatma)
        """
        findings = []

        exported_services = [s for s in services if s.get("exported", False)]

        for service in exported_services:
            name = service.get("name", "Unknown")

            findings.append({
                "category": "M6: Insecure Authorization",
                "severity": SEVERITY_MEDIUM,
                "title": f"Exported Service: {self._short_name(name)}",
                "description": (
                    f"Service '{name}' is exported. "
                    "Other applications can start or bind to this service, "
                    "potentially triggering unauthorized operations."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Set android:exported='false' or protect with a custom permission "
                    "using android:permission attribute."
                )
            })

        return findings

    # ─── Broadcast Receiver Analizi ────────────────────────────────

    def _analyze_receivers(self, receivers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Broadcast Receiver'ları güvenlik açısından analiz et

        Exported Receiver riskleri:
        - Broadcast spoofing (sahte broadcast gönderme)
        - Hassas bilgi sızıntısı
        - DoS (sürekli broadcast gönderme)
        """
        findings = []

        exported_receivers = [r for r in receivers if r.get("exported", False)]

        for receiver in exported_receivers:
            name = receiver.get("name", "Unknown")

            findings.append({
                "category": "M1: Improper Platform Usage",
                "severity": SEVERITY_MEDIUM,
                "title": f"Exported Broadcast Receiver: {self._short_name(name)}",
                "description": (
                    f"Broadcast Receiver '{name}' is exported. "
                    "Any application can send broadcasts to this receiver, "
                    "potentially triggering unintended behavior."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Set android:exported='false' or use android:permission to restrict. "
                    "Consider using LocalBroadcastManager for internal broadcasts."
                )
            })

        return findings

    # ─── Content Provider Analizi ──────────────────────────────────

    def _analyze_providers(self, providers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Content Provider'ları güvenlik açısından analiz et

        Exported Provider riskleri:
        - SQL Injection (query parametreleri manipüle edilebilir)
        - Path Traversal (URI manipulation ile dosya erişimi)
        - Hassas veri sızıntısı (doğrudan veri okuma)
        """
        findings = []

        exported_providers = [p for p in providers if p.get("exported", False)]

        for provider in exported_providers:
            name = provider.get("name", "Unknown")
            authorities = provider.get("authorities", "")

            findings.append({
                "category": "M2: Insecure Data Storage",
                "severity": SEVERITY_HIGH,
                "title": f"Exported Content Provider: {self._short_name(name)}",
                "description": (
                    f"Content Provider '{name}' (authority: {authorities}) is exported. "
                    "Other apps can query, insert, update, or delete data through this provider. "
                    "Risks include SQL injection and unauthorized data access."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Set android:exported='false' or add these protections:\n"
                    "1. Use android:readPermission and android:writePermission\n"
                    "2. Implement proper input validation in query(), insert(), update()\n"
                    "3. Use parameterized queries to prevent SQL injection\n"
                    "4. Restrict path access with android:pathPermission"
                )
            })

        return findings

    # ─── Genel Güvenlik Kontrolleri ────────────────────────────────

    def _check_general_security(self, manifest_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Genel manifest güvenlik kontrollerini yap

        1. Debuggable kontrolü
        2. AllowBackup kontrolü
        3. Cleartext traffic kontrolü
        4. Min SDK kontrolü
        """
        findings = []

        # 1. Debuggable mı?
        if manifest_data.get("is_debuggable", False):
            findings.append({
                "category": "M1: Improper Platform Usage",
                "severity": SEVERITY_CRITICAL,
                "title": "Debuggable Application",
                "description": (
                    "Application has android:debuggable='true' in the manifest. "
                    "A debuggable app allows:\n"
                    "- Attaching a debugger to inspect runtime behavior\n"
                    "- Accessing the app's data directory\n"
                    "- Bypassing security controls"
                ),
                "file": "AndroidManifest.xml",
                "line": 0,
                "recommendation": (
                    "NEVER release a debuggable app to production. "
                    "Set android:debuggable='false' or remove the attribute."
                )
            })

        # 2. AllowBackup mı?
        if manifest_data.get("allow_backup", True):
            findings.append({
                "category": "M2: Insecure Data Storage",
                "severity": SEVERITY_MEDIUM,
                "title": "Application Data Backup Allowed",
                "description": (
                    "Application allows data backup (android:allowBackup='true'). "
                    "An attacker with physical access can extract app data via 'adb backup'."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Set android:allowBackup='false' unless backup is required. "
                    "If backup is needed, implement BackupAgent with encryption."
                )
            })

        # 3. Cleartext traffic?
        if manifest_data.get("uses_cleartext_traffic", False):
            findings.append({
                "category": "M3: Insecure Communication",
                "severity": SEVERITY_HIGH,
                "title": "Cleartext (HTTP) Traffic Allowed",
                "description": (
                    "Application allows cleartext (unencrypted) network traffic. "
                    "HTTP traffic can be intercepted and modified by attackers (MITM)."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Set android:usesCleartextTraffic='false'. "
                    "Use HTTPS for all network communication. "
                    "Implement a Network Security Config for fine-grained control."
                )
            })

        # 4. Min SDK çok düşük mü?
        min_sdk = manifest_data.get("min_sdk", 0)
        if 0 < min_sdk < 21:
            findings.append({
                "category": "M1: Improper Platform Usage",
                "severity": SEVERITY_MEDIUM,
                "title": f"Low Minimum SDK Version (API {min_sdk})",
                "description": (
                    f"Application targets minimum SDK {min_sdk} (Android {self._sdk_to_android(min_sdk)}). "
                    "Older Android versions have known security vulnerabilities."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Increase minSdkVersion to at least 21 (Android 5.0) "
                    "for better security defaults."
                )
            })

        # 5. Target SDK kontrolü
        target_sdk = manifest_data.get("target_sdk", 0)
        if 0 < target_sdk < 28:
            findings.append({
                "category": "M1: Improper Platform Usage",
                "severity": SEVERITY_MEDIUM,
                "title": f"Low Target SDK Version (API {target_sdk})",
                "description": (
                    f"Application targets SDK {target_sdk}. "
                    "Lower target SDK versions opt out of newer security protections."
                ),
                "file": "AndroidManifest.xml",
                "recommendation": (
                    "Increase targetSdkVersion to the latest stable API level "
                    "to benefit from platform security improvements."
                )
            })

        return findings

    # ─── Yardımcı Methodlar ────────────────────────────────────────

    def _short_name(self, full_name: str) -> str:
        """
        Component adını kısalt

        com.example.app.ui.MainActivity → MainActivity
        """
        if "." in full_name:
            return full_name.split(".")[-1]
        return full_name

    def _sdk_to_android(self, sdk: int) -> str:
        """
        SDK versiyonunu Android versiyonuna çevir

        21 → "5.0", 28 → "9.0", 33 → "13"
        """
        sdk_map = {
            16: "4.1", 17: "4.2", 18: "4.3", 19: "4.4",
            21: "5.0", 22: "5.1", 23: "6.0", 24: "7.0",
            25: "7.1", 26: "8.0", 27: "8.1", 28: "9.0",
            29: "10", 30: "11", 31: "12", 32: "12L",
            33: "13", 34: "14", 35: "15",
        }
        return sdk_map.get(sdk, str(sdk))

    def get_component_summary(self, manifest_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Component özetini döndür

        Returns:
            {
                "total_activities": 10,
                "exported_activities": 3,
                "total_services": 5,
                "exported_services": 1,
                ...
            }
        """
        activities = manifest_data.get("activities", [])
        services = manifest_data.get("services", [])
        receivers = manifest_data.get("receivers", [])
        providers = manifest_data.get("providers", [])

        return {
            "total_activities": len(activities),
            "exported_activities": sum(1 for a in activities if a.get("exported")),
            "total_services": len(services),
            "exported_services": sum(1 for s in services if s.get("exported")),
            "total_receivers": len(receivers),
            "exported_receivers": sum(1 for r in receivers if r.get("exported")),
            "total_providers": len(providers),
            "exported_providers": sum(1 for p in providers if p.get("exported")),
        }

    def __repr__(self) -> str:
        return "ComponentAnalyzer()"
