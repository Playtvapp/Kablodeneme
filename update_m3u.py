import sys
import requests
import json
import re

VAVOO_DOMAIN = "vavoo.to"

def getAuthSignature():
    headers = {
        "user-agent": "okhttp/4.11.0",
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "content-length": "1106",
        "accept-encoding": "gzip"
    }
    data = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "reason": "app-blur",
        "locale": "de",
        "theme": "dark",
        "metadata": {
            "device": {"type": "Handset", "brand": "google", "model": "Nexus", "name": "21081111RG", "uniqueId": "d10e5d99ab665233"},
            "os": {"name": "android", "version": "7.1.2", "abis": ["arm64-v8a", "armeabi-v7a", "armeabi"], "host": "android"},
            "app": {"platform": "android", "version": "3.1.20", "buildId": "289515000", "engine": "hbc85", "signatures": ["6e8a975e3cbf07d5de823a760d4c2547f86c1403105020adee5de67ac510999e"], "installer": "app.revanced.manager.flutter"},
            "version": {"package": "tv.vavoo.app", "binary": "3.1.20", "js": "3.1.20"}
        },
        "appFocusTime": 0, "playerActive": False, "playDuration": 0, "devMode": False,
        "hasAddon": True, "castConnected": False, "package": "tv.vavoo.app", "version": "3.1.20",
        "process": "app", "firstAppStart": 1743962904623, "lastAppStart": 1743962904623,
        "ipLocation": "", "adblockEnabled": True,
        "proxy": {"supported": ["ss", "openvpn"], "engine": "ss", "ssVersion": 1, "enabled": True, "autoServer": True, "id": "pl-waw"},
        "iap": {"supported": False}
    }
    try:
        resp = requests.post("https://www.vavoo.tv/api/app/ping", json=data, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json().get("addonSig")
    except Exception as e:
        print(f"[HATA] Imza alinamadi: {e}")
        return None

def main():
    print("[BİLGİ] Vavoo Guncel Imza (Token) Aliniyor...")
    signature = getAuthSignature()
    
    if not signature:
        print("[HATA] Token alinamadi, islem iptal edildi.")
        sys.exit(1)
        
    print(f"[BİLGİ] Imza Alindi: {signature[:15]}...")

    headers = {
        "user-agent": "okhttp/4.11.0",
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "mediahubmx-signature": signature
    }

    groups = [
        "Turkey", "Germany", "Albania", "Arabia", "Balkans", "Bulgaria", "France", 
        "Italy", "Netherlands", "Poland", "Portugal", "Romania", "Russia", "Spain", 
        "United Kingdom", "United States"
    ]
    
    all_channels = []

    print("[BİLGİ] Kanallar cekiliyor, lutfen bekleyin...")
    for g in groups:
        cursor = 0
        while True:
            data = {
                "language": "de", "region": "AT", "catalogId": "iptv", "id": "iptv",
                "adult": False, "search": "", "sort": "name", "filter": {"group": g},
                "cursor": cursor, "clientVersion": "3.0.2"
            }
            try:
                resp = requests.post(f"https://{VAVOO_DOMAIN}/mediahubmx-catalog.json", json=data, headers=headers, timeout=12)
                resp.raise_for_status()
                r = resp.json()
                items = r.get("items", [])
                for item in items:
                    item['group'] = g # Grubu kaydet
                all_channels.extend(items)
                cursor = r.get("nextCursor")
                if not cursor:
                    break
            except Exception:
                break

    # M3U Dosyasını Oluştur
    print(f"[BİLGİ] Toplam {len(all_channels)} kanal bulundu. M3U olusturuluyor...")
    
    with open("guncel_liste.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in all_channels:
            name = ch.get("name", "Bilinmeyen").strip()
            
            # Kanal ID'sini al ve imzayı linke yerleştir
            if isinstance(ch.get("ids"), dict) and ch["ids"].get("id"):
                ch_id = ch["ids"]["id"]
                # EN KRİTİK NOKTA: Token linkin sonuna ekleniyor
                play_url = f"https://vavoo.to/vavoo-iptv/play/{ch_id}?n=1&b=5&vavoo_auth={signature}"
                
                group = ch.get("group", "General")
                logo = ch.get("logo", "")
                
                f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f"{play_url}\n")

    print("[BAŞARILI] guncel_liste.m3u dosyasi uretildi!")

if __name__ == "__main__":
    main()
