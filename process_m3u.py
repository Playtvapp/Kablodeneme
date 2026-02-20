import requests
import re

# Ana M3U veri kaynağın
SOURCE_URL = "https://cdn.jsdelivr.net/gh/Playtvapp/Playtvlist@main/F%C4%B0LMLERFANT%C4%B0KAPPP.m3u"
OUTPUT_FILE = "guncel_liste.m3u"

def process_m3u():
    try:
        # Kaynak dosyayı çek
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        lines = response.text.splitlines()
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for line in lines:
                # Satır eski link formatıyla başlıyorsa dönüştür
                if line.startswith("https://vidmody.com/vs/"):
                    # Regex ile tt... şeklindeki ID'yi yakala
                    match = re.search(r'https://vidmody\.com/vs/(tt\d+)', line)
                    if match:
                        video_id = match.group(1)
                        # İstediğin yeni formatı oluştur
                        new_link = f"https://vidmody.com/mm/{video_id}/main/index-v1-a1.m3u8"
                        f.write(new_link + '\n')
                    else:
                        # Eğer ID bulunamazsa satırı orijinal haliyle bırak
                        f.write(line + '\n')
                else:
                    # Link olmayan tüm satırları (kategoriler, isimler vb.) olduğu gibi yaz
                    f.write(line + '\n')
                    
        print(f"İşlem başarılı! Dosya oluşturuldu: {OUTPUT_FILE}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    process_m3u()
