"""
androidsec/reporting/html_formatter.py

Analiz sonuçlarını profesyonel HTML rapor formatında dışa aktarır.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class HTMLFormatter:
    """
    Analiz sonuçlarını güzel, responsive HTML raporu olarak üretir.

    Kullanım:
        formatter = HTMLFormatter()
        path = formatter.format(result_data, "output/reports/report.html")
    """

    SEVERITY_COLORS = {
        "CRITICAL": "#dc2626",
        "HIGH": "#ea580c",
        "MEDIUM": "#d97706",
        "LOW": "#2563eb",
        "INFO": "#6b7280",
    }

    SEVERITY_BADGES = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🔵",
        "INFO": "⚪",
    }

    def format(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Analiz verilerini HTML olarak dışa aktarır.

        Args:
            data: Analiz sonuç verisi
            output_path: Çıktı dosyası yolu

        Returns:
            Oluşturulan dosyanın yolu
        """
        logger.info("HTML raporu oluşturuluyor: %s", output_path)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        apk_info = data.get("apk_info", {})
        risk = data.get("risk", {})
        statistics = data.get("statistics", {})
        findings = data.get("findings", [])
        by_owasp = data.get("by_owasp", {})
        analysis_time = data.get("analysis_time", 0)

        html = self._build_html(
            apk_info=apk_info,
            risk=risk,
            statistics=statistics,
            findings=findings,
            by_owasp=by_owasp,
            analysis_time=analysis_time,
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info("HTML raporu oluşturuldu: %s", path)
        return str(path)

    def _build_html(self, **kwargs) -> str:
        apk_info = kwargs["apk_info"]
        risk = kwargs["risk"]
        statistics = kwargs["statistics"]
        findings = kwargs["findings"]
        by_owasp = kwargs["by_owasp"]
        analysis_time = kwargs["analysis_time"]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        risk_score = risk.get("score", 0)
        risk_level = risk.get("level", "NONE")
        risk_label = risk.get("label", "N/A")
        risk_color = self.SEVERITY_COLORS.get(risk_level, "#6b7280")

        severity_counts = statistics.get("by_severity", {})

        findings_html = self._build_findings_table(findings)
        owasp_html = self._build_owasp_section(by_owasp)

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AndroidSecAnalyzer — Güvenlik Raporu</title>
    <style>
        :root {{
            --bg: #0f172a;
            --surface: #1e293b;
            --card: #334155;
            --border: #475569;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --critical: #dc2626;
            --high: #ea580c;
            --medium: #d97706;
            --low: #2563eb;
            --info: #6b7280;
            --success: #22c55e;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

        /* Header */
        .header {{
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 2px solid var(--accent);
            margin-bottom: 2rem;
        }}
        .header h1 {{
            font-size: 2.2rem;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .header .subtitle {{ color: var(--text-muted); font-size: 1rem; }}
        .header .meta {{ color: var(--text-muted); font-size: 0.85rem; margin-top: 1rem; }}

        /* Cards Grid */
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; margin-bottom: 2rem; }}
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        .card .value {{ font-size: 2.5rem; font-weight: 700; }}
        .card .label {{ color: var(--text-muted); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.3rem; }}

        /* Risk Gauge */
        .risk-card {{
            background: var(--surface);
            border: 2px solid {risk_color};
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .risk-card .score {{
            font-size: 4rem;
            font-weight: 800;
            color: {risk_color};
        }}
        .risk-card .level {{
            font-size: 1.2rem;
            color: {risk_color};
            font-weight: 600;
            margin-top: 0.5rem;
        }}
        .risk-card .bar {{
            width: 100%;
            height: 12px;
            background: var(--card);
            border-radius: 6px;
            margin-top: 1rem;
            overflow: hidden;
        }}
        .risk-card .bar-fill {{
            height: 100%;
            width: {min(risk_score * 10, 100)}%;
            background: {risk_color};
            border-radius: 6px;
            transition: width 0.5s ease;
        }}

        /* Section titles */
        .section-title {{
            font-size: 1.4rem;
            font-weight: 700;
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--accent);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        /* Findings Table */
        .findings-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 2rem;
        }}
        .findings-table th {{
            background: var(--card);
            padding: 0.8rem 1rem;
            text-align: left;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            border-bottom: 2px solid var(--border);
        }}
        .findings-table td {{
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
            vertical-align: top;
        }}
        .findings-table tr:hover {{ background: rgba(56, 189, 248, 0.05); }}

        .badge {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-critical {{ background: rgba(220,38,38,0.2); color: #fca5a5; border: 1px solid rgba(220,38,38,0.4); }}
        .badge-high {{ background: rgba(234,88,12,0.2); color: #fdba74; border: 1px solid rgba(234,88,12,0.4); }}
        .badge-medium {{ background: rgba(217,119,6,0.2); color: #fcd34d; border: 1px solid rgba(217,119,6,0.4); }}
        .badge-low {{ background: rgba(37,99,235,0.2); color: #93c5fd; border: 1px solid rgba(37,99,235,0.4); }}
        .badge-info {{ background: rgba(107,114,128,0.2); color: #d1d5db; border: 1px solid rgba(107,114,128,0.4); }}

        .badge-correlated {{
            background: rgba(168,85,247,0.2);
            color: #c4b5fd;
            border: 1px solid rgba(168,85,247,0.4);
            margin-left: 0.3rem;
        }}

        /* OWASP Section */
        .owasp-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 1rem;
            overflow: hidden;
        }}
        .owasp-header {{
            padding: 1rem 1.2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            background: var(--card);
        }}
        .owasp-header:hover {{ background: rgba(56, 189, 248, 0.08); }}
        .owasp-header .cat-name {{ font-weight: 600; }}
        .owasp-header .count {{
            background: var(--accent);
            color: var(--bg);
            padding: 0.15rem 0.6rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
        }}
        .owasp-body {{ padding: 1rem 1.2rem; }}
        .owasp-finding {{
            padding: 0.6rem 0;
            border-bottom: 1px solid var(--border);
        }}
        .owasp-finding:last-child {{ border-bottom: none; }}

        /* APK Info */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .info-item {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
        }}
        .info-item .key {{ color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; }}
        .info-item .val {{ font-size: 1rem; font-weight: 600; margin-top: 0.3rem; word-break: break-all; }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.8rem;
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ AndroidSecAnalyzer</h1>
        <div class="subtitle">Android Application Security Analysis Report</div>
        <div class="meta">Oluşturulma: {now} &nbsp;|&nbsp; Analiz Süresi: {analysis_time:.2f}s</div>
    </div>

    <div class="container">

        <!-- APK Bilgileri -->
        <div class="section-title">📱 APK Bilgileri</div>
        <div class="info-grid">
            <div class="info-item">
                <div class="key">Dosya Adı</div>
                <div class="val">{apk_info.get('file_name', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="key">Paket Adı</div>
                <div class="val">{apk_info.get('package_name', 'N/A')}</div>
            </div>
            <div class="info-item">
                <div class="key">Versiyon</div>
                <div class="val">{apk_info.get('version_name', 'N/A')} (code: {apk_info.get('version_code', 'N/A')})</div>
            </div>
            <div class="info-item">
                <div class="key">Dosya Boyutu</div>
                <div class="val">{self._format_size(apk_info.get('file_size', 0))}</div>
            </div>
        </div>

        <!-- Risk Skoru -->
        <div class="risk-card">
            <div class="score">{risk_score}/10</div>
            <div class="level">{risk_label}</div>
            <div class="bar"><div class="bar-fill"></div></div>
        </div>

        <!-- Özet Kartları -->
        <div class="cards">
            <div class="card">
                <div class="value">{statistics.get('total_findings', len(findings))}</div>
                <div class="label">Toplam Bulgu</div>
            </div>
            <div class="card">
                <div class="value" style="color: var(--critical)">{severity_counts.get('CRITICAL', 0)}</div>
                <div class="label">Kritik</div>
            </div>
            <div class="card">
                <div class="value" style="color: var(--high)">{severity_counts.get('HIGH', 0)}</div>
                <div class="label">Yüksek</div>
            </div>
            <div class="card">
                <div class="value" style="color: var(--medium)">{severity_counts.get('MEDIUM', 0)}</div>
                <div class="label">Orta</div>
            </div>
            <div class="card">
                <div class="value" style="color: var(--low)">{severity_counts.get('LOW', 0)}</div>
                <div class="label">Düşük</div>
            </div>
        </div>

        <!-- Bulgular Tablosu -->
        <div class="section-title">🔍 Tüm Bulgular</div>
        {findings_html}

        <!-- OWASP Kategorileri -->
        <div class="section-title">🏷️ OWASP Mobile Top 10 Sınıflandırması</div>
        {owasp_html}

    </div>

    <div class="footer">
        🛡️ AndroidSecAnalyzer v1.0.0 — Android Application Security Analysis Tool<br>
        OWASP Mobile Top 10 standardına göre analiz raporu
    </div>
</body>
</html>"""

    def _build_findings_table(self, findings: List[Dict]) -> str:
        if not findings:
            return '<p style="color: var(--text-muted); text-align: center; padding: 2rem;">Bulgu bulunamadı.</p>'

        # Severity sırasına göre sırala
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        sorted_findings = sorted(
            findings,
            key=lambda f: severity_order.get(f.get("severity", "INFO"), 5)
        )

        rows = []
        for i, f in enumerate(sorted_findings, 1):
            sev = f.get("severity", "INFO")
            badge_class = f"badge-{sev.lower()}"
            badge = self.SEVERITY_BADGES.get(sev, "⚪")

            correlated_tag = ""
            if f.get("correlated", False):
                correlated_tag = ' <span class="badge badge-correlated">CORRELATED</span>'

            source_tag = ""
            source = f.get("source", "")
            if source:
                source_tag = f' <span style="color: var(--text-muted); font-size: 0.75rem;">({source})</span>'

            rows.append(f"""
                <tr>
                    <td style="text-align: center; color: var(--text-muted);">{i}</td>
                    <td><span class="badge {badge_class}">{badge} {sev}</span>{correlated_tag}</td>
                    <td><strong>{f.get('title', 'N/A')}</strong>{source_tag}</td>
                    <td>{f.get('category', 'N/A')}</td>
                    <td style="font-size: 0.85rem;">{f.get('description', '')[:150]}</td>
                </tr>""")

        return f"""
        <table class="findings-table">
            <thead>
                <tr>
                    <th style="width:40px">#</th>
                    <th style="width:130px">Severity</th>
                    <th>Başlık</th>
                    <th style="width:200px">OWASP Kategori</th>
                    <th>Açıklama</th>
                </tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
        </table>"""

    def _build_owasp_section(self, by_owasp: Dict[str, List]) -> str:
        if not by_owasp:
            return '<p style="color: var(--text-muted);">OWASP sınıflandırması bulunamadı.</p>'

        sections = []
        for category, cat_findings in by_owasp.items():
            count = len(cat_findings)
            if count == 0:
                count_style = "background: var(--border); color: var(--text-muted);"
            else:
                count_style = ""

            finding_items = []
            for f in cat_findings[:10]:  # En fazla 10 bulgu göster
                sev = f.get("severity", "INFO")
                badge = self.SEVERITY_BADGES.get(sev, "⚪")
                finding_items.append(
                    f'<div class="owasp-finding">{badge} <strong>{f.get("title", "N/A")}</strong> '
                    f'— {f.get("description", "")[:100]}</div>'
                )

            if count > 10:
                finding_items.append(
                    f'<div class="owasp-finding" style="color: var(--text-muted);">... ve {count - 10} fazla bulgu</div>'
                )

            body = "".join(finding_items) if finding_items else '<div style="color: var(--text-muted); padding: 0.5rem;">Bu kategoride bulgu bulunamadı.</div>'

            sections.append(f"""
            <div class="owasp-item">
                <div class="owasp-header">
                    <span class="cat-name">{category}</span>
                    <span class="count" style="{count_style}">{count}</span>
                </div>
                <div class="owasp-body">{body}</div>
            </div>""")

        return "".join(sections)

    def _format_size(self, size_bytes: int) -> str:
        if size_bytes == 0:
            return "N/A"
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
