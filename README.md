# 🤖 ELENA AI — Ethical Learning & Network Assistant

<div align="center">

```
  ███████╗██╗     ███████╗███╗   ██╗ █████╗
  ██╔════╝██║     ██╔════╝████╗  ██║██╔══██╗
  █████╗  ██║     █████╗  ██╔██╗ ██║███████║
  ██╔══╝  ██║     ██╔══╝  ██║╚██╗██║██╔══██║
  ███████╗███████╗███████╗██║ ╚████║██║  ██║
  ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
```

**Adaptive · Intelligent · Streaming · Termux Ready**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Termux](https://img.shields.io/badge/Termux-Compatible-green?logo=android)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Version](https://img.shields.io/badge/Version-3.0-red)

</div>

---

## ✨ Fitur Baru di v3.0

| Fitur | Keterangan |
|-------|------------|
| 🧠 **Adaptive Memory** | ELENA mengingat nama, profesi, dan preferensi pengguna antar sesi |
| 👤 **User Profile** | Deteksi otomatis level keahlian (beginner/intermediate/advanced) |
| 😊 **Mood System** | ELENA punya 6 mood yang berubah otomatis sesuai konteks percakapan |
| 📦 **Code Snippet Storage** | Semua kode yang dibahas tersimpan otomatis untuk referensi |
| 📊 **Usage Statistics** | Tracking topik, frekuensi, dan pola penggunaan |
| ⚡ **No-Pause Streaming** | Response mengalir tanpa jedah atau potongan aneh |
| 🔄 **Auto Learning** | Ekstrak otomatis info pengguna dari percakapan |
| 📝 **Export Markdown** | Export percakapan ke file `.md` yang rapi |
| 🎯 **Context-Aware Prompt** | System prompt berubah dinamis sesuai konteks sesi |

---

## 🚀 Quick Start

### 1. Install di Termux

```bash
# Install Python (jika belum)
pkg install python python-pip -y

# Clone repo
git clone https://github.com/username/elena-ai-v3.0.git
cd elena-ai-v3.0

# Install dependencies
pip install requests

# Atau pakai script auto-install
python elena.py --install
```

### 2. Dapatkan API Key (GRATIS)

1. Buka [openrouter.ai/keys](https://openrouter.ai/keys)
2. Daftar dengan email (gratis, tidak perlu kartu kredit)
3. Klik **"Create Key"**
4. Salin key yang muncul (format: `sk-or-v1-...`)

### 3. Jalankan ELENA

```bash
python elena.py
```

Pertama kali berjalan, ELENA akan minta API key:

```
API Key: sk-or-v1-xxxxxxxx
  ✅ API key valid
```

---

## 💬 Cara Penggunaan

### Chat Biasa
Ketik langsung tanpa awalan `/`:
```
Kamu › Buatkan fungsi Python untuk cek palindrome
🤖 ELENA 🎯  Tentu! Berikut implementasinya...
```

### Perintah Sistem

```
/help           → Tampilkan semua perintah
/setup          → Setup atau ganti API key
/model [1-7]    → Ganti model AI
/temp [0.1-1.5] → Atur kreativitas respons
/tokens [n]     → Atur panjang respons maksimal
```

### Perintah Memori & Profil

```
/profile        → Lihat profil + statistik topik
/memory         → Lihat semua memori tersimpan
/remember [k] [v] → Simpan info manual
/forget [k]     → Hapus memori tertentu
/name [nama]    → Set nama pengguna
```

### Perintah Riwayat & File

```
/history        → Lihat 10 pesan terakhir
/clear          → Hapus riwayat sesi ini
/save           → Simpan percakapan
/export         → Export ke file Markdown
/snippets [lang] → Lihat code snippets tersimpan
/read [file]    → Baca isi file teks
/list [path]    → List file di direktori
```

### Mengatur Mood ELENA

```
/mood           → Lihat mood tersedia
/mood excited   → Set mood ke "excited" 🚀
/mood focused   → Mode fokus debug 🎯
/mood playful   → Mode santai 😄
```

---

## 🤖 Model AI Tersedia

| # | Model | Tier |
|---|-------|------|
| 1 | DeepSeek Chat | ⚡ Default |
| 2 | Gemini 2.0 Flash | 🔥 Cepat |
| 3 | LLaMA 3.2 3B | 🆓 Gratis |
| 4 | Mistral 7B | 🆓 Gratis |
| 5 | Qwen 2.5 32B | 🆓 Gratis |
| 6 | Claude 3 Haiku | 💎 Premium |
| 7 | GPT-4o Mini | 💎 Premium |

> 💡 Model dengan 🆓 sepenuhnya gratis. Model 💎 butuh kredit OpenRouter.

---

## 🧠 Sistem Pembelajaran Adaptif

ELENA secara otomatis mempelajari:

- **Nama pengguna** dari kalimat seperti *"nama saya Budi"*
- **Pekerjaan** dari kalimat seperti *"saya bekerja sebagai developer"*
- **Bahasa favorit** dari topik yang paling sering ditanyakan
- **Level keahlian** dari kompleksitas pertanyaan yang diajukan
- **Code snippets** dari setiap kode yang dihasilkan dalam percakapan

Semua data disimpan lokal di `~/.config/elena-ai-v3.0/` dan **tidak dikirim ke mana pun**.

---

## 📂 Struktur File

```
~/.config/elena-ai-v3.0/
├── api_key.txt       → API key (terenkripsi di filesystem)
├── config.json       → Preferensi model, temperature, dll
├── chat_history.json → 15 sesi terakhir
├── memory.json       → Memori jangka panjang
├── user_profile.json → Profil & statistik pengguna
└── skills_learned.json → Code snippets tersimpan
```

---

## 🔧 Opsi Command Line

```bash
python elena.py           # Jalankan normal
python elena.py --install # Install dependencies
python elena.py --reset   # Reset semua data
python elena.py --version # Tampilkan versi
```

---

## 🛡️ Etika & Keamanan

ELENA dirancang dengan prinsip **ethical AI**:

- ✅ Membantu pemrograman, debug, belajar teknologi
- ✅ Keamanan siber **defensif** (hardening, best practices)
- ✅ Semua data tersimpan **100% lokal** di device kamu
- ❌ Tidak membantu aktivitas ilegal atau merusak
- ❌ Tidak menyimpan data ke server eksternal

---

## 🤝 Kontribusi

Pull request sangat disambut! Beberapa ide fitur:

- [ ] Plugin system untuk integrasi eksternal
- [ ] Web UI berbasis FastAPI
- [ ] Voice input dengan Whisper
- [ ] Integration dengan GitHub Copilot-style suggestion
- [ ] Multi-agent conversation mode

---

## 📄 Lisensi

MIT License — bebas digunakan, dimodifikasi, dan didistribusikan.

---

<div align="center">
Dibuat dengan ❤️ untuk komunitas developer Indonesia<br>
<strong>ELENA AI v3.0 — Adaptive Intelligence Edition</strong>
</div>
