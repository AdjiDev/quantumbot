import requests
from telebot import TeleBot

def handle_infogempa_command(bot: TeleBot):
    @bot.message_handler(commands=['infogempa'])
    def infogempa_command(m):
        try:
            response = requests.get("https://api.junn4.my.id/tools/infogempa")
            response.raise_for_status()
            data = response.json()

            if data['status'] == 200 and 'result' in data and data['result']:
                result = data['result']
                message = f"ℹ️ **Info Gempa Hari Ini**\n\n" \
                          f"📅 Tanggal: {result['tanggal']}\n" \
                          f"🌍 Magnitudo: {result['magnitudo']}\n" \
                          f"🌊 Kedalaman: {result['kedalaman']}\n" \
                          f"📍 Koordinat: {result['koordinat']}\n" \
                          f"📍 Lokasi: {result['lokasi']}\n" \
                          f"🔔 Wilayah Dirasakan: {result['wilayahDirasakan']}\n" \
                          f"📢 Arahan: {result['arahan']}\n" \
                          f"🚨 Saran: {result['saran']}\n" \
                          f"🗺️ [Link Peta]( {result['linkPeta']} )\n" \
                          f"🕒 Waktu Pemutakhiran: {result['waktuPemutakhiran']}\n"

                bot.reply_to(m, message, parse_mode='Markdown')
            else:
                bot.reply_to(m, "Tidak ada informasi gempa saat ini.")

        except requests.RequestException as e:
            bot.reply_to(m, f"Terjadi kesalahan saat mengambil data gempa: {e}")
