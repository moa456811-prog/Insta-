#!/usr/bin/env python3
"""
CLI Test Suite for InstagramCore
"""

import sys
import json
from engine import InstagramCore, __version__

# Codes couleur ANSI simplifiés
class C:
    GRN, RED, CYN, YLW = "\033[92m", "\033[91m", "\033[96m", "\033[93m"
    BOLD, RESET = "\033[1m", "\033[0m"

def cb(color: str, text: str, bold=False) -> str:
    prefix = C.BOLD if bold else ""
    return f"{prefix}{color}{text}{C.RESET}"

def generate_html_report(results: list) -> str:
    """Génère un rapport HTML épuré."""
    rows = ""
    for r in results:
        status_cls = "table-success" if r['success'] else "table-danger"
        priv_icon = "🔒" if r.get('private') else "🌐"
        veri_icon = "✅" if r.get('verified') else ""
        
        row = f"""
        <tr class="{status_cls}">
            <td>{cb(C.BOLD, f"@{r['username']}")}</td>
            <td>{priv_icon} {'Privé' if r.get('private') else 'Public'}</td>
            <td>{veri_icon} {r.get('full_name', 'N/A')}</td>
            <td>{r.get('followers', 0):,}</td>
            <td>{r.get('posts', 0):,}</td>
            <td>{r.get('error', 'OK')}</td>
        </tr>
        """
        rows += row

    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Rapport Recon Instagram Suite v{__version__}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body {{ background: #121212; color: #e0e0e0; padding: 20px; }} .table {{ color: #e0e0e0; }} .table-success {{ background-color: #1b5e20 !important; color: white !important; }} .table-danger {{ background-color: #b71c1c !important; color: white !important; }}</style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4">📊 Rapport OSINT Instagram <small class="text-muted">v{__version__}</small></h1>
            <table class="table table-dark table-striped table-bordered">
                <thead><tr><th>Cible</th><th>Status</th><th>Nom Complet</th><th>Followers</th><th>Posts</th><th>Détails</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # Parsing rapide des arguments
    # Usage: python test_suite.py <username1> <username2> --proxy=http://user:pass@ip:port
    args = sys.argv[1:]
    targets = [a for a in args if not a.startswith('--')]
    proxy_arg = [a for a in args if a.startswith('--proxy=')]
    
    proxy = proxy_arg[0].split('=')[1] if proxy_arg else None
    
    if not targets:
        targets = ['cristiano', 'leomessi'] # Cibles par défaut pour test

    print(cb(C.CYN, f"--- [Instagram Ultimate Suite v{__version__}] ---", bold=True))
    if proxy:
        print(cb(C.YLW, f"ℹ️ Utilisation du proxy: {proxy}"))
    print(f"🕵️ Lancement de la reconnaissance sur {len(targets)} cibles...\n")

    core = InstagramCore(proxy=proxy)
    results = []

    for t in targets:
        print(f"Scrutin de {cb(C.BOLD, '@'+t)}...", end="", flush=True)
        res = core.recon_user(t)
        results.append(res)
        
        if res['success']:
            priv = "[🔒]" if res['private'] else "[🌐]"
            print(f"\r✅ {cb(C.GRN, priv)} @{res['username']} | {res['full_name']} | {res['followers']:,} followers")
        else:
            reason = res.get('status', 'Error')
            print(f"\r❌ @{res['username']} | Status: {cb(C.RED, reason)} | {res['error']}")

    # Sauvegarde des rapports
    with open("results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    with open("report.html", "w", encoding='utf-8') as f:
        f.write(generate_html_report(results))

    print(f"\n" + cb(C.CYN, f"--- Fin du scan ---", bold=True))
    print(cb(C.GRN, "📄 results.json généré"))
    print(cb(C.GRN, "📊 report.html généré (ouvre-le dans ton navigateur)"))
