import urllib.request
import base64
import json
import random

# ۱. آدرس منبع کانفیگ‌ها
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
]

# لیست متنوعی از ایموجی‌های محبوب کیبورد
EMOJIS = [
    "🎀", "✨", "⚡", "🔥", "🚀", "💎", "⭐", "💫", "👑", "🌟", 
    "🎯", "🎲", "🔮", "🧿", "🍀", "🌺", "🌸", "🦋", "🦄", "🎨", 
    "🛸", "🪐", "🌐", "⚡️", "🌊", "🌙", "☀️", "🎧", "🎮", "⚜️"
]

NEW_NAME = "@Configvibes"
MAX_CONFIGS = 100

def fetch_configs():
    raw_lines = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8', errors='ignore').strip()
                
                try:
                    decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                    lines = decoded.splitlines()
                except Exception:
                    lines = content.splitlines()
                
                for line in lines:
                    line = line.strip()
                    if line.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                        raw_lines.append(line)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
    return list(dict.fromkeys(raw_lines))

def rename_config(config_str, new_remark):
    """تغییر نام رمارک کانفیگ"""
    if any(config_str.startswith(proto) for proto in ['vless://', 'trojan://', 'ss://']):
        if '#' in config_str:
            base = config_str.split('#')[0]
            return f"{base}#{new_remark}"
        else:
            return f"{config_str}#{new_remark}"
            
    elif config_str.startswith('vmess://'):
        try:
            b64_data = config_str[8:]
            b64_data += '=' * (-len(b64_data) % 4)
            data_json = json.loads(base64.b64decode(b64_data).decode('utf-8', errors='ignore'))
            data_json['ps'] = new_remark
            new_b64 = base64.b64encode(json.dumps(data_json).encode('utf-8')).decode('utf-8')
            return f"vmess://{new_b64}"
        except Exception:
            return config_str
            
    return config_str

def process_configs():
    configs = fetch_configs()
    processed = []
    
    # نمونه‌برداری تصادفی از لیست ایموجی‌ها برای داشتن تنوع بالا
    emoji_pool = random.choices(EMOJIS, k=MAX_CONFIGS)
    
    for i, cfg in enumerate(configs):
        if len(processed) >= MAX_CONFIGS:
            break
            
        emoji = emoji_pool[i]
        renamed = rename_config(cfg, f"{emoji} {NEW_NAME} | {i+1}")
        processed.append(renamed)
        
    # ذخیره متنی ساده
    with open("configs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(processed))
        
    # ذخیره به‌صورت Base64
    b64_encoded = base64.b64encode("\n".join(processed).encode("utf-8")).decode("utf-8")
    with open("sub_base64.txt", "w", encoding="utf-8") as f_b64:
        f_b64.write(b64_encoded)

    print(f"Successfully processed {len(processed)} configs with diverse emojis.")

if __name__ == "__main__":
    process_configs()
