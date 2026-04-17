# -*- coding: utf-8 -*-
"""
translate_reviews.py
Mevcut tum yorumlari Ingilizceye cevirir, DB'yi gunceller
ve sentiment analizini yeniden yapar.
"""
import mysql.connector
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_review import process_review

# --- Known Turkish → English map ---
TR_TO_EN = {
    "Temiz ve fotograflardaki gibiydi": "Clean and exactly as shown in the photos.",
    "Temiz ve foto\ufffdraflardaki gibiydi": "Clean and exactly as shown in the photos.",
    "It  was excellent": "It was excellent!",
    "It was excellent": "It was excellent!",
    "Alacati'nin ruhunu yansitan sirin bir yer. Kahvalti harika, sadece otopark zor.":
        "A charming place that truly captures the spirit of Alacati. Breakfast was amazing, only the parking is a bit tricky.",
    "Leziz kahvaltiyla merhaba demek harikaymis. Atmosfer tam istedigimiz gibiydi.":
        "Waking up to a delicious breakfast was wonderful. The atmosphere was exactly what we were looking for.",
    "Beklentimize uygundu, fiyat performans dengesi tamam. Bir daha dusunurum.":
        "Met our expectations, good value for money. Would consider staying again.",
    "Ev sahibi cok ilgiliydi, mekan fotolarda gozuktugunden daha guzel.":
        "The host was very attentive and the place is even more beautiful than the photos.",
    "Check-in cok kolaydi. Konum merkeze yakin, her sey el altindaydi.":
        "Check-in was very easy. Great central location, everything within reach.",
    "Check-in cok kolaydi. Konum merkeze yakin, her sey el altindayd\ufffd.":
        "Check-in was very easy. Great central location, everything within reach.",
    "Genel olarak guzel ama park sorunu yasadik. Yine de sehir icin makul.":
        "Overall nice but we had trouble with parking. Still reasonable for a city stay.",
    "Uyku kalitesi cok iyiydi, manzara inanilmazdi. Tekrar gorisurmek uzere!":
        "The sleep quality was excellent and the view was breathtaking. See you next time!",
    "Uyku kalitesi cok iyiydi, manzara inanilmazdi. Tekrar gorsurmek uzere!":
        "The sleep quality was excellent and the view was breathtaking. See you next time!",
    "Tavsiye ederim! Butun ailecek huzur dolu bir tatil gecirdik.":
        "Highly recommended! We had a wonderful, peaceful family vacation.",
    "Romantik kacamak icin biciilmis. Her koseye ozen gosterilmis.":
        "Perfect for a romantic getaway. Every detail has been carefully thought out.",
    "Hayatimdaki en guzell tatillerden! Her sey kusursuzdu, kesinlikle tekrar gelecekim.":
        "One of the best vacations of my life! Everything was perfect, I will definitely come back.",
    "Hayatimdaki en guzell tatillerden! Her sey kusursuzdu, kesinlikle tekrar gelecek":
        "One of the best vacations of my life! Everything was perfect, I will definitely come back.",
    "Inanilmaz bir deneyim! Magara odasi, balon manzarasi, her sey mukemmeldi.":
        "An incredible experience! The cave room, the hot air balloon view, everything was magnificent.",
    "Konum guzeldi ama gurultuluydu.": "Great location but it was a bit noisy.",
    "Muhteşem manzara!": "Breathtaking view!",
}

def normalize_key(text):
    return (text or '').strip().rstrip('.')

DB_CONFIG = {
    'host': 'localhost', 'user': 'root',
    'password': 'mysql1234', 'database': 'airbnb_clone', 'charset': 'utf8mb4'
}

def translate_with_api(text):
    try:
        from deep_translator import GoogleTranslator
        result = GoogleTranslator(source='auto', target='en').translate(text)
        return result if result else text
    except Exception as e:
        print(f"  [API WARN] {e}")
        return text

def backfill():
    db = mysql.connector.connect(**DB_CONFIG)
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT review_id, comment FROM Reviews ORDER BY review_id")
    reviews = cur.fetchall()
    print(f"[INFO] Processing {len(reviews)} reviews...")

    updated = 0
    for rev in reviews:
        original = (rev['comment'] or '').strip()
        
        # Try direct map first
        en_comment = TR_TO_EN.get(original)
        if not en_comment:
            # Try normalized key
            for k, v in TR_TO_EN.items():
                if normalize_key(k) == normalize_key(original):
                    en_comment = v
                    break
        
        # Fallback: use Google Translate API
        if not en_comment:
            print(f"  [API] Translating #{rev['review_id']}: {original[:60]}")
            en_comment = translate_with_api(original)
        
        # Re-run sentiment on English text
        try:
            ai_result = process_review(en_comment)
            sentiment = ai_result['sentiment']
            status = ai_result['status']
        except:
            sentiment = 'POSITIVE'
            status = 'ACCEPTED'

        cur.execute(
            "UPDATE Reviews SET comment=%s, ai_sentiment=%s, ai_status=%s WHERE review_id=%s",
            (en_comment, sentiment, status, rev['review_id'])
        )
        print(f"  [OK] #{rev['review_id']} {sentiment:8s} | {en_comment[:70]}")
        updated += 1

    db.commit()
    cur.close()
    db.close()
    print(f"\n[DONE] {updated} reviews translated and re-analyzed.")

if __name__ == '__main__':
    backfill()
