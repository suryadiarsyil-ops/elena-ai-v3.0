# Changelog — ELENA AI

## [3.0.0] — 2025 — Adaptive Intelligence Edition

### ✨ Fitur Baru
- **Adaptive Memory System** — ELENA mengingat info pengguna antar sesi
- **User Profile & Learning** — Deteksi level keahlian otomatis (beginner/intermediate/advanced)
- **Mood System** — 6 mood dinamis (normal, curious, excited, focused, friendly, playful)
- **Auto-Learning** — Ekstrak nama, pekerjaan, bahasa favorit dari percakapan
- **Code Snippet Storage** — Semua kode tersimpan untuk referensi
- **Usage Statistics** — `/stats` dengan bar chart per topik
- **Export Markdown** — `/export` untuk simpan percakapan
- **Animated Thinking Indicator** — Dots animasi saat menunggu respons
- **Returning User Greeting** — Sapa pengguna berbeda jika sudah lama tidak chat

### 🛠️ Perbaikan Bug
- **Fixed: Streaming terpotong** — Respons kini mengalir tanpa jeda atau potongan
- **Fixed: Readline error di Termux** — Tangani `EOFError` dan `KeyboardInterrupt` dengan benar
- **Fixed: JSON parse error pada streaming** — Skip malformed chunks, tidak crash
- **Fixed: Timeout tidak ditangani** — Pesan error yang informatif alih-alih crash
- **Fixed: Conversation history membengkak** — Dibatasi 20 turns untuk efisiensi token
- **Fixed: Config tidak tersimpan** — Exception handling pada file write
- **Fixed: Model invalid tidak terdeteksi** — Validasi model menggunakan dict lookup

### ⚡ Peningkatan
- System prompt dinamis sesuai konteks, mood, dan expertise pengguna
- Temperature auto-adjust berdasarkan mood aktif
- Command router yang lebih clean dan extensible
- Tambahan 2 model baru (Claude 3 Haiku, GPT-4o Mini)
- Max tokens naik dari 2048 ke 4096
- History sesi naik dari 10 ke 15 sesi
- Simpan 50 snippet terakhir (naik dari tidak ada)

---

## [2.0.0] — ELENA Terminal Edition

### Fitur
- Streaming response
- Multiple model support
- Chat history per sesi
- API key management
- Basic system commands

---

## [1.0.0] — Initial Release

- Chat dasar dengan OpenRouter API
- Warna terminal
- Setup API key
