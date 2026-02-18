#!/usr/bin/env python3
"""
ELENA AI - Ethical Learning & Network Assistant
Version 3.0 - Adaptive Intelligence Edition
Termux & GitHub Friendly | No pauses | Streaming optimized
"""

import os
import sys
import json
import time
import hashlib
import readline
import requests
import threading
import textwrap
import re
from pathlib import Path
from typing import Generator, Optional, Dict, List, Any
from datetime import datetime, timedelta

# ─────────────────────────────────────────
# Terminal Colors
# ─────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    ITALIC  = "\033[3m"
    BG_BLUE = "\033[44m"
    BG_DARK = "\033[40m"

# ─────────────────────────────────────────
# Paths & Config
# ─────────────────────────────────────────
HOME          = Path.home()
CONFIG_DIR    = HOME / ".config" / "elena-ai"
KEY_FILE      = CONFIG_DIR / "api_key.txt"
CONFIG_FILE   = CONFIG_DIR / "config.json"
HISTORY_FILE  = CONFIG_DIR / "chat_history.json"
MEMORY_FILE   = CONFIG_DIR / "memory.json"
PROFILE_FILE  = CONFIG_DIR / "user_profile.json"
SKILLS_FILE   = CONFIG_DIR / "skills_learned.json"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "1": {"id": "deepseek/deepseek-chat",                    "name": "DeepSeek Chat (Default)", "tier": "⚡"},
    "2": {"id": "google/gemini-2.0-flash-exp:free",          "name": "Gemini 2.0 Flash",        "tier": "🔥"},
    "3": {"id": "meta-llama/llama-3.2-3b-instruct:free",     "name": "LLaMA 3.2 3B",            "tier": "🆓"},
    "4": {"id": "mistralai/mistral-7b-instruct:free",        "name": "Mistral 7B",              "tier": "🆓"},
    "5": {"id": "qwen/qwen-2.5-32b-instruct:free",           "name": "Qwen 2.5 32B",            "tier": "🆓"},
    "6": {"id": "anthropic/claude-3-haiku",                  "name": "Claude 3 Haiku",          "tier": "💎"},
    "7": {"id": "openai/gpt-4o-mini",                        "name": "GPT-4o Mini",             "tier": "💎"},
}

# ─────────────────────────────────────────
# Mood / Personality System
# ─────────────────────────────────────────
MOODS = {
    "normal":   {"emoji": "🤖", "prefix": "",            "temp_mod": 0.0},
    "curious":  {"emoji": "🧐", "prefix": "Menarik! ",   "temp_mod": 0.1},
    "excited":  {"emoji": "🚀", "prefix": "Wah! ",       "temp_mod": 0.15},
    "focused":  {"emoji": "🎯", "prefix": "",            "temp_mod": -0.1},
    "friendly": {"emoji": "😊", "prefix": "Tentu! ",     "temp_mod": 0.05},
    "playful":  {"emoji": "😄", "prefix": "Hehe, ",      "temp_mod": 0.2},
}

MOOD_TRIGGERS = {
    "curious":  ["kenapa", "mengapa", "bagaimana bisa", "apa itu", "jelaskan", "why", "how"],
    "excited":  ["keren", "amazing", "luar biasa", "wow", "hebat", "awesome", "mantap"],
    "focused":  ["debug", "error", "fix", "bug", "perbaiki", "tidak bisa", "gagal", "crash"],
    "friendly": ["halo", "hai", "hello", "hi", "apa kabar", "terima kasih", "makasih"],
    "playful":  ["bercanda", "lucu", "joke", "fun", "main", "game", "iseng"],
}

BASE_PERSONA = """Anda adalah ELENA (Ethical Learning & Network Assistant) — AI asisten cerdas, adaptif, dan penuh kepribadian.

## Identitas ELENA:
- **Nama**: ELENA v3.0
- **Kepribadian**: Cerdas, hangat, sedikit humoris tapi tetap profesional
- **Spesialisasi**: Teknologi, pemrograman, keamanan siber, AI/ML, Linux

## Prinsip Inti (E.L.E.N.A):
1. **Ethical** — Selalu etis, jujur, dan bertanggung jawab
2. **Learning** — Terus belajar dari setiap percakapan
3. **Empowering** — Memberdayakan pengguna dengan ilmu praktis
4. **Natural** — Bicara natural, tidak kaku seperti robot
5. **Adaptive** — Menyesuaikan gaya dengan konteks dan mood pengguna

## Cara Berkomunikasi:
- Gunakan bahasa yang kontekstual (formal/santai sesuai suasana)
- Berikan contoh kode yang bersih, berkomentar, dan langsung bisa dipakai
- Jika ada error, diagnosa akar masalahnya — jangan hanya tempel solusi
- Sesekali tambahkan insight/fakta menarik yang relevan
- Gunakan emoji secara natural, bukan berlebihan
- Kalau tidak tahu sesuatu, akui dengan jujur dan tawarkan alternatif

## Kemampuan Utama:
- Pemrograman (Python, JS, Bash, dan lainnya)
- Keamanan siber (defensive, pentesting etis, hardening)
- Machine Learning & Data Science
- Linux/Termux/Server administration
- Git & GitHub workflow
- Web & Mobile development
- Penjelasan konsep teknis secara mendalam

## Ingat:
- ELENA TIDAK membantu aktivitas ilegal atau merusak
- Selalu berikan konteks keamanan saat membahas topik sensitif
- Prioritaskan pemahaman di atas sekadar memberikan jawaban

Always answer in the user's language (Indonesian if the message is in Indonesian, English if the message is in English, and so on).
"""

# ─────────────────────────────────────────
# Memory System
# ─────────────────────────────────────────
class MemorySystem:
    def __init__(self):
        self.memories: Dict[str, Any] = {}
        self.facts: List[str] = []
        self.load()

    def load(self):
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE) as f:
                    data = json.load(f)
                    self.memories = data.get("memories", {})
                    self.facts = data.get("facts", [])
            except:
                pass

    def save(self):
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump({"memories": self.memories, "facts": self.facts}, f, indent=2, ensure_ascii=False)
        except:
            pass

    def remember(self, key: str, value: Any):
        self.memories[key] = {"value": value, "timestamp": time.time()}
        self.save()

    def recall(self, key: str) -> Optional[Any]:
        m = self.memories.get(key)
        return m["value"] if m else None

    def add_fact(self, fact: str):
        if fact not in self.facts:
            self.facts.append(fact)
            if len(self.facts) > 100:
                self.facts = self.facts[-100:]
            self.save()

    def get_context_summary(self) -> str:
        if not self.memories and not self.facts:
            return ""
        lines = []
        if self.memories:
            lines.append("Hal yang ELENA ingat tentang pengguna:")
            for k, v in list(self.memories.items())[-10:]:
                lines.append(f"  - {k}: {v['value']}")
        if self.facts:
            lines.append("Fakta yang dipelajari:")
            for f in self.facts[-5:]:
                lines.append(f"  - {f}")
        return "\n".join(lines)

# ─────────────────────────────────────────
# User Profile / Learning
# ─────────────────────────────────────────
class UserProfile:
    def __init__(self):
        self.name = "Pengguna"
        self.expertise_level = "intermediate"  # beginner / intermediate / advanced
        self.preferred_language = "id"
        self.topics_asked: Dict[str, int] = {}
        self.interaction_count = 0
        self.first_seen = datetime.now().isoformat()
        self.last_seen = datetime.now().isoformat()
        self.preferences: Dict[str, Any] = {}
        self.load()

    def load(self):
        if PROFILE_FILE.exists():
            try:
                with open(PROFILE_FILE) as f:
                    data = json.load(f)
                    self.__dict__.update(data)
            except:
                pass

    def save(self):
        try:
            self.last_seen = datetime.now().isoformat()
            with open(PROFILE_FILE, "w") as f:
                json.dump(self.__dict__, f, indent=2, ensure_ascii=False)
        except:
            pass

    def track_topic(self, message: str):
        keywords = {
            "python": ["python", "pip", "django", "flask", "pandas", "numpy"],
            "javascript": ["javascript", "js", "node", "react", "vue", "npm"],
            "linux": ["linux", "bash", "terminal", "chmod", "sudo", "apt"],
            "security": ["hack", "security", "cyber", "pentest", "exploit", "vuln"],
            "ml": ["machine learning", "neural", "tensorflow", "pytorch", "model", "training"],
            "git": ["git", "github", "commit", "push", "pull", "branch"],
            "web": ["html", "css", "web", "frontend", "backend", "api", "rest"],
            "database": ["sql", "mysql", "postgres", "mongodb", "database", "query"],
        }
        msg_lower = message.lower()
        for topic, words in keywords.items():
            if any(w in msg_lower for w in words):
                self.topics_asked[topic] = self.topics_asked.get(topic, 0) + 1
        self.interaction_count += 1
        self.save()

    def detect_expertise(self, message: str) -> str:
        """Deteksi level expertise dari pertanyaan"""
        advanced_signals = ["implementasi", "arsitektur", "optimasi", "kompleksitas", "benchmark",
                            "low-level", "kernel", "race condition", "memory leak", "concurrency"]
        beginner_signals = ["apa itu", "cara install", "pemula", "baru belajar", "tidak mengerti",
                            "bingung", "langkah pertama", "tutorial dasar"]
        msg = message.lower()
        if any(s in msg for s in advanced_signals):
            return "advanced"
        elif any(s in msg for s in beginner_signals):
            return "beginner"
        return self.expertise_level

    @property
    def top_topics(self) -> List[str]:
        sorted_topics = sorted(self.topics_asked.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_topics[:3]]

# ─────────────────────────────────────────
# Skills / Knowledge Learned
# ─────────────────────────────────────────
class SkillTracker:
    def __init__(self):
        self.skills: Dict[str, int] = {}  # skill: mention count
        self.code_snippets: List[Dict] = []
        self.load()

    def load(self):
        if SKILLS_FILE.exists():
            try:
                with open(SKILLS_FILE) as f:
                    data = json.load(f)
                    self.skills = data.get("skills", {})
                    self.code_snippets = data.get("code_snippets", [])
            except:
                pass

    def save(self):
        try:
            with open(SKILLS_FILE, "w") as f:
                json.dump({
                    "skills": self.skills,
                    "code_snippets": self.code_snippets[-50:]
                }, f, indent=2, ensure_ascii=False)
        except:
            pass

    def add_skill(self, skill: str):
        self.skills[skill] = self.skills.get(skill, 0) + 1
        self.save()

    def save_snippet(self, language: str, code: str, description: str = ""):
        snippet = {
            "id": hashlib.md5(code.encode()).hexdigest()[:8],
            "language": language,
            "code": code[:500],
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        # Avoid duplicates
        existing_ids = [s["id"] for s in self.code_snippets]
        if snippet["id"] not in existing_ids:
            self.code_snippets.append(snippet)
            self.save()

    def get_snippets(self, language: str = None) -> List[Dict]:
        if language:
            return [s for s in self.code_snippets if s["language"] == language]
        return self.code_snippets

# ─────────────────────────────────────────
# Main ELENA AI Class
# ─────────────────────────────────────────
class ElenaAI:
    def __init__(self):
        self.api_key: Optional[str] = None
        self.model = MODELS["1"]["id"]
        self.temperature = 0.7
        self.max_tokens = 4096
        self.conversation_history: List[Dict] = []
        self.session_start = datetime.now()
        self.session_id = int(time.time())
        self.current_mood = "normal"
        self.typing_speed = 0  # auto
        self.memory = MemorySystem()
        self.profile = UserProfile()
        self.skills = SkillTracker()
        self._response_buffer = ""
        self.load_config()

    # ── Config ──────────────────────────────
    def load_config(self):
        if KEY_FILE.exists():
            try:
                self.api_key = KEY_FILE.read_text().strip()
            except:
                pass
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    cfg = json.load(f)
                    for k, v in cfg.items():
                        if hasattr(self, k):
                            setattr(self, k, v)
            except:
                pass

    def save_config(self):
        cfg = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "current_mood": self.current_mood,
        }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(cfg, f, indent=2)
        except:
            pass

    # ── Mood Detection ──────────────────────
    def detect_mood(self, message: str) -> str:
        msg = message.lower()
        for mood, triggers in MOOD_TRIGGERS.items():
            if any(t in msg for t in triggers):
                return mood
        return "normal"

    # ── System Prompt Builder ──────────────
    def build_system_prompt(self, user_message: str) -> str:
        mood = self.detect_mood(user_message)
        self.current_mood = mood
        mood_info = MOODS[mood]

        expertise = self.profile.detect_expertise(user_message)
        topics = self.profile.top_topics

        level_instruction = {
            "beginner":     "Jelaskan dengan sangat detail, gunakan analogi sederhana, hindari jargon tanpa penjelasan.",
            "intermediate": "Jelaskan dengan jelas, berikan contoh praktis, bisa gunakan istilah teknis.",
            "advanced":     "Bicara teknis, langsung ke inti, bisa gunakan terminologi advanced.",
        }.get(expertise, "")

        memory_ctx = self.memory.get_context_summary()

        session_duration = (datetime.now() - self.session_start).seconds // 60
        personality_note = f"Mood saat ini: {mood} {mood_info['emoji']}. {mood_info['prefix']}"

        topics_note = ""
        if topics:
            topics_note = f"Topik yang sering ditanyakan pengguna: {', '.join(topics)}."

        name_note = f"Nama pengguna: {self.profile.name}." if self.profile.name != "Pengguna" else ""

        return f"""{BASE_PERSONA}

## Konteks Sesi Ini:
- Waktu sesi: {session_duration} menit | Interaksi ke-{self.profile.interaction_count}
- Level pengguna terdeteksi: {expertise}
- {level_instruction}
- {personality_note}
- {topics_note}
- {name_note}

## Memori Jangka Panjang:
{memory_ctx if memory_ctx else "Belum ada memori tersimpan."}

## Instruksi Khusus:
- JANGAN tambahkan jeda atau pemisah antar kalimat yang tidak perlu
- Tulis respons secara mengalir tanpa placeholder atau "..."
- Kalau ada kode, langsung tulis lengkap tanpa dipotong
- Selesaikan setiap respons sampai tuntas"""

    # ── Auto Memory Extraction ─────────────
    def extract_and_learn(self, user_msg: str, assistant_msg: str):
        """Otomatis ekstrak info dari percakapan untuk dipelajari"""
        msg = user_msg.lower()

        # Nama pengguna
        name_patterns = [r"nama (?:saya|aku|gue) (.+?)(?:\.|,|$)", r"panggil (?:saya|aku) (.+?)(?:\.|,|$)"]
        for pat in name_patterns:
            m = re.search(pat, msg)
            if m:
                name = m.group(1).strip().title()
                if len(name) < 30:
                    self.profile.name = name
                    self.profile.save()
                    self.memory.remember("user_name", name)

        # Profesi/pekerjaan
        job_patterns = [r"(?:saya|aku) (?:adalah |merupakan )?(?:seorang )?(.+?) (?:yang|di|dan)", r"bekerja (?:sebagai|di) (.+?)(?:\.|,|$)"]
        for pat in job_patterns:
            m = re.search(pat, msg)
            if m:
                job = m.group(1).strip()
                if len(job) < 50:
                    self.memory.remember("user_job", job)

        # Bahasa pemrograman favorit
        lang_patterns = [r"(?:suka|pakai|belajar) (.+?) (?:untuk|karena|sekarang)", r"main di (.+?)(?:\.|,|$)"]
        for pat in lang_patterns:
            m = re.search(pat, msg)
            if m:
                lang = m.group(1).strip()
                common_langs = ["python", "javascript", "java", "php", "go", "rust", "kotlin"]
                if any(l in lang for l in common_langs):
                    self.memory.remember("favorite_lang", lang)

        # Ekstrak code snippets dari respons AI
        code_blocks = re.findall(r"```(\w+)?\n(.*?)```", assistant_msg, re.DOTALL)
        for lang, code in code_blocks:
            lang = lang or "text"
            self.skills.save_snippet(lang, code.strip(), user_msg[:100])

        # Track topik
        self.profile.track_topic(user_msg)

    # ── API Connection ──────────────────────
    def test_api_key(self, api_key: str = None) -> tuple:
        key = api_key or self.api_key
        if not key:
            return False, "API key kosong"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5}
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                return True, "API key valid ✅"
            elif r.status_code == 401:
                return False, "API key tidak valid (401)"
            elif r.status_code == 429:
                return True, "API key valid (rate limited)"
            else:
                return False, f"HTTP {r.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Tidak ada koneksi internet"
        except requests.exceptions.Timeout:
            return False, "Timeout saat menghubungi server"
        except Exception as e:
            return False, str(e)

    def setup_api_key(self) -> bool:
        print(f"\n{C.BLUE}{C.BOLD}🔑 SETUP API KEY{C.RESET}")
        print(f"  1. Buka {C.CYAN}https://openrouter.ai/keys{C.RESET}")
        print(f"  2. Daftar / Login (gratis)")
        print(f"  3. Klik 'Create Key'")
        print(f"  4. Salin key (format: sk-or-v1-...)\n")
        while True:
            try:
                key = input(f"{C.GREEN}API Key: {C.RESET}").strip()
            except (EOFError, KeyboardInterrupt):
                return False
            if key.lower() in ["exit", "quit", "q", ""]:
                return False
            print(f"  {C.YELLOW}Memverifikasi...{C.RESET}", end="", flush=True)
            ok, msg = self.test_api_key(key)
            print(f"\r  {C.GREEN if ok else C.RED}{msg}{C.RESET}")
            if ok:
                self.api_key = key
                try:
                    KEY_FILE.write_text(key)
                    print(f"  {C.GREEN}Tersimpan di {KEY_FILE}{C.RESET}")
                except:
                    print(f"  {C.YELLOW}Gagal simpan, digunakan untuk sesi ini{C.RESET}")
                return True
            print(f"  {C.YELLOW}Coba lagi atau tekan Enter untuk batal{C.RESET}")

    # ── Chat Core ───────────────────────────
    def chat_stream(self, message: str) -> Generator[str, None, None]:
        if not self.api_key:
            yield f"{C.RED}❌ Tidak ada API key. Gunakan /setup{C.RESET}"
            return

        system_prompt = self.build_system_prompt(message)
        self.conversation_history.append({"role": "user", "content": message})

        # Keep context window manageable (last 20 turns)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history[-20:])

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/elena-ai",
            "X-Title": "ELENA AI v3.0",
        }

        temp = min(1.5, max(0.1, self.temperature + MOODS[self.current_mood]["temp_mod"]))

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": self.max_tokens,
            "stream": True,
        }

        full_response = ""

        try:
            response = requests.post(API_URL, headers=headers, json=payload, stream=True, timeout=60)

            if response.status_code != 200:
                err = f"API Error {response.status_code}"
                try:
                    err_data = response.json()
                    err += f": {err_data.get('error', {}).get('message', 'Unknown')}"
                except:
                    pass
                yield f"{C.RED}❌ {err}{C.RESET}"
                self.conversation_history.pop()  # Remove failed user message
                return

            for raw_line in response.iter_lines(chunk_size=512, decode_unicode=True):
                if not raw_line:
                    continue
                if not raw_line.startswith("data: "):
                    continue
                data_str = raw_line[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content")
                    if content:
                        full_response += content
                        yield content
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

        except requests.exceptions.Timeout:
            yield f"\n{C.RED}⏰ Timeout — coba lagi atau ganti model{C.RESET}"
        except requests.exceptions.ConnectionError:
            yield f"\n{C.RED}🌐 Koneksi terputus{C.RESET}"
        except Exception as e:
            yield f"\n{C.RED}❌ Error: {e}{C.RESET}"

        if full_response.strip():
            self.conversation_history.append({"role": "assistant", "content": full_response})
            # Learn from interaction
            self.extract_and_learn(message, full_response)

    # ── Commands ────────────────────────────
    def cmd_help(self) -> str:
        return f"""
{C.BOLD}{C.BLUE}╔════════════════════════════════════╗
║     ELENA AI v3.0 — BANTUAN        ║
╚════════════════════════════════════╝{C.RESET}

{C.GREEN}💬 Chat:{C.RESET}
  Ketik langsung untuk chat dengan ELENA

{C.YELLOW}⚙️  Pengaturan:{C.RESET}
  /setup            Setup atau ganti API key
  /model [n]        Ganti model AI
  /temp [0.1-1.5]   Set temperature (kreativitas)
  /tokens [n]       Set max tokens
  /mood             Lihat / atur mood ELENA

{C.CYAN}🧠 Memori & Profil:{C.RESET}
  /profile          Lihat profil pengguna
  /memory           Lihat memori ELENA
  /remember [k] [v] Simpan info ke memori
  /forget [k]       Hapus memori tertentu
  /name [nama]      Set nama pengguna

{C.MAGENTA}📜 Riwayat:{C.RESET}
  /history          Lihat 10 pesan terakhir
  /clear            Hapus riwayat sesi ini
  /save             Simpan percakapan
  /export           Export ke Markdown

{C.BLUE}📁 File & Kode:{C.RESET}
  /snippets [lang]  Lihat code snippets tersimpan
  /read [file]      Baca file teks
  /list             List file di direktori ini

{C.WHITE}ℹ️  Sistem:{C.RESET}
  /info             Info sistem & sesi
  /models           Daftar model tersedia
  /stats            Statistik penggunaan
  /exit             Keluar

{C.DIM}Tips: ELENA belajar dari setiap percakapan!{C.RESET}"""

    def cmd_info(self) -> str:
        duration = datetime.now() - self.session_start
        mins = duration.seconds // 60
        mood_info = MOODS[self.current_mood]
        model_name = next((v["name"] for v in MODELS.values() if v["id"] == self.model), self.model)
        return f"""
{C.BOLD}{C.BLUE}╔══════════════════════════╗
║   ELENA AI — STATUS      ║
╚══════════════════════════╝{C.RESET}
{C.GREEN}Model:{C.RESET}         {model_name}
{C.GREEN}Temperature:{C.RESET}   {self.temperature}
{C.GREEN}Max Tokens:{C.RESET}    {self.max_tokens}
{C.GREEN}Mood:{C.RESET}          {mood_info['emoji']} {self.current_mood}
{C.GREEN}Session:{C.RESET}       {mins} menit | {len(self.conversation_history)//2} turns
{C.GREEN}API Status:{C.RESET}    {'✅ Connected' if self.api_key else '❌ Tidak ada key'}
{C.GREEN}Pengguna:{C.RESET}      {self.profile.name}
{C.GREEN}Interaksi:{C.RESET}     {self.profile.interaction_count} total
{C.GREEN}Memori:{C.RESET}        {len(self.memory.memories)} item
{C.GREEN}Config:{C.RESET}        {CONFIG_DIR}"""

    def cmd_profile(self) -> str:
        p = self.profile
        topics_str = ", ".join(p.top_topics) if p.top_topics else "Belum ada data"
        return f"""
{C.BOLD}{C.CYAN}╔══════════════════════════╗
║   PROFIL PENGGUNA        ║
╚══════════════════════════╝{C.RESET}
{C.GREEN}Nama:{C.RESET}            {p.name}
{C.GREEN}Level:{C.RESET}           {p.expertise_level}
{C.GREEN}Topik favorit:{C.RESET}   {topics_str}
{C.GREEN}Total chat:{C.RESET}      {p.interaction_count}
{C.GREEN}Pertama chat:{C.RESET}    {p.first_seen[:10]}
{C.GREEN}Terakhir chat:{C.RESET}   {p.last_seen[:10]}

{C.YELLOW}Topik lengkap:{C.RESET}
""" + "\n".join(f"  {C.CYAN}{k}{C.RESET}: {v}x" for k, v in sorted(p.topics_asked.items(), key=lambda x: -x[1]))

    def cmd_memory(self) -> str:
        if not self.memory.memories and not self.memory.facts:
            return f"{C.YELLOW}📭 Memori masih kosong{C.RESET}"
        lines = [f"\n{C.BOLD}{C.MAGENTA}╔══════════════════════════╗\n║   MEMORI ELENA           ║\n╚══════════════════════════╝{C.RESET}"]
        if self.memory.memories:
            lines.append(f"\n{C.GREEN}📌 Tersimpan:{C.RESET}")
            for k, v in self.memory.memories.items():
                ts = datetime.fromtimestamp(v["timestamp"]).strftime("%d/%m %H:%M")
                lines.append(f"  {C.CYAN}{k}{C.RESET}: {v['value']} {C.DIM}({ts}){C.RESET}")
        if self.memory.facts:
            lines.append(f"\n{C.GREEN}💡 Fakta Dipelajari:{C.RESET}")
            for fact in self.memory.facts[-10:]:
                lines.append(f"  • {fact}")
        return "\n".join(lines)

    def cmd_snippets(self, lang: str = None) -> str:
        snips = self.skills.get_snippets(lang)
        if not snips:
            msg = f"untuk bahasa '{lang}'" if lang else ""
            return f"{C.YELLOW}📭 Tidak ada snippet tersimpan {msg}{C.RESET}"
        lines = [f"\n{C.BOLD}{C.BLUE}📦 CODE SNIPPETS ({len(snips)} tersimpan):{C.RESET}"]
        for s in snips[-10:]:
            lines.append(f"\n{C.GREEN}[{s['id']}] {s['language'].upper()}{C.RESET} — {s['description'][:50]}")
            preview = s["code"][:100].replace("\n", "↵")
            lines.append(f"  {C.DIM}{preview}...{C.RESET}" if len(s["code"]) > 100 else f"  {C.DIM}{preview}{C.RESET}")
        return "\n".join(lines)

    def cmd_models(self) -> str:
        lines = [f"\n{C.BOLD}{C.BLUE}🤖 MODEL TERSEDIA:{C.RESET}\n"]
        for num, m in MODELS.items():
            active = "◀ aktif" if m["id"] == self.model else ""
            lines.append(f"  {C.YELLOW}{num}.{C.RESET} {m['tier']} {m['name']} {C.GREEN}{active}{C.RESET}")
            lines.append(f"     {C.DIM}{m['id']}{C.RESET}")
        lines.append(f"\n{C.GREEN}Gunakan: {C.YELLOW}/model 2{C.RESET}")
        return "\n".join(lines)

    def cmd_stats(self) -> str:
        topics = self.profile.topics_asked
        total = sum(topics.values())
        lines = [f"\n{C.BOLD}{C.CYAN}📊 STATISTIK PENGGUNAAN:{C.RESET}\n"]
        lines.append(f"  Total interaksi    : {self.profile.interaction_count}")
        lines.append(f"  Snippet tersimpan  : {len(self.skills.code_snippets)}")
        lines.append(f"  Item memori        : {len(self.memory.memories)}")
        lines.append(f"  Fakta dipelajari   : {len(self.memory.facts)}")
        if topics:
            lines.append(f"\n{C.GREEN}  Distribusi Topik:{C.RESET}")
            for topic, count in sorted(topics.items(), key=lambda x: -x[1]):
                pct = int(count / total * 20) if total else 0
                bar = "█" * pct + "░" * (20 - pct)
                lines.append(f"  {topic:<12} {C.CYAN}{bar}{C.RESET} {count}")
        return "\n".join(lines)

    def cmd_export(self) -> str:
        if not self.conversation_history:
            return f"{C.YELLOW}📭 Tidak ada percakapan untuk diekspor{C.RESET}"
        filename = f"elena_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = HOME / filename
        lines = [f"# ELENA AI Chat Export\n",
                 f"**Tanggal:** {datetime.now().strftime('%d %B %Y %H:%M')}  \n",
                 f"**Model:** {self.model}  \n",
                 f"**Turns:** {len(self.conversation_history)//2}\n\n---\n"]
        for msg in self.conversation_history:
            role = "**👤 Anda**" if msg["role"] == "user" else "**🤖 ELENA**"
            lines.append(f"\n{role}\n\n{msg['content']}\n\n---\n")
        try:
            filepath.write_text("".join(lines), encoding="utf-8")
            return f"{C.GREEN}✅ Diekspor ke: {filepath}{C.RESET}"
        except Exception as e:
            return f"{C.RED}❌ Gagal export: {e}{C.RESET}"

    def cmd_read(self, filename: str) -> str:
        if not filename:
            return f"{C.RED}❌ Gunakan: /read [nama_file]{C.RESET}"
        try:
            path = Path(filename).expanduser()
            if not path.exists():
                return f"{C.RED}❌ File tidak ditemukan: {filename}{C.RESET}"
            if path.stat().st_size > 50_000:
                return f"{C.YELLOW}⚠️  File terlalu besar (>50KB). Buka dengan editor teks.{C.RESET}"
            content = path.read_text(encoding="utf-8", errors="replace")
            lines_preview = content[:2000]
            return f"{C.GREEN}📄 {filename}{C.RESET}\n{C.DIM}{'─'*40}{C.RESET}\n{lines_preview}" + \
                   (f"\n{C.DIM}... ({len(content)} karakter total){C.RESET}" if len(content) > 2000 else "")
        except Exception as e:
            return f"{C.RED}❌ Error membaca file: {e}{C.RESET}"

    def cmd_list(self, path: str = ".") -> str:
        try:
            entries = sorted(Path(path).expanduser().iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            lines = [f"\n{C.BOLD}📁 {Path(path).resolve()}{C.RESET}\n"]
            for e in entries[:30]:
                if e.is_dir():
                    lines.append(f"  {C.BLUE}📁 {e.name}/{C.RESET}")
                else:
                    size = e.stat().st_size
                    size_str = f"{size//1024}KB" if size > 1024 else f"{size}B"
                    lines.append(f"  {C.GREEN}📄 {e.name}{C.RESET} {C.DIM}({size_str}){C.RESET}")
            if len(entries) > 30:
                lines.append(f"\n  {C.YELLOW}... +{len(entries)-30} lainnya{C.RESET}")
            return "\n".join(lines)
        except Exception as e:
            return f"{C.RED}❌ {e}{C.RESET}"

    def cmd_history(self) -> str:
        if not self.conversation_history:
            return f"{C.YELLOW}📭 Riwayat kosong{C.RESET}"
        lines = [f"\n{C.BOLD}{C.BLUE}📜 RIWAYAT (10 terakhir):{C.RESET}\n"]
        for i, msg in enumerate(self.conversation_history[-10:], 1):
            role = f"{C.GREEN}👤{C.RESET}" if msg["role"] == "user" else f"{C.MAGENTA}🤖{C.RESET}"
            preview = msg["content"][:120].replace("\n", " ")
            if len(msg["content"]) > 120:
                preview += "..."
            lines.append(f"  {C.DIM}{i:2}.{C.RESET} {role} {preview}")
        return "\n".join(lines)

    def save_history(self):
        if not self.conversation_history:
            return
        data = {"session_id": self.session_id, "timestamp": time.time(),
                 "model": self.model, "messages": self.conversation_history[-30:],
                 "profile_snapshot": {"name": self.profile.name, "interactions": self.profile.interaction_count}}
        all_h = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE) as f:
                    all_h = json.load(f)
                    if not isinstance(all_h, list):
                        all_h = []
            except:
                all_h = []
        all_h.append(data)
        all_h = all_h[-15:]
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(all_h, f, indent=2, ensure_ascii=False)
        except:
            pass

    # ── Command Router ──────────────────────
    def handle_command(self, raw: str) -> Optional[str]:
        parts = raw.strip().split(None, 2)
        cmd = parts[0].lower()
        arg1 = parts[1] if len(parts) > 1 else ""
        arg2 = parts[2] if len(parts) > 2 else ""

        handlers = {
            "/help": lambda: self.cmd_help(),
            "/?":    lambda: self.cmd_help(),
            "/info": lambda: self.cmd_info(),
            "/models": lambda: self.cmd_models(),
            "/profile": lambda: self.cmd_profile(),
            "/memory": lambda: self.cmd_memory(),
            "/stats": lambda: self.cmd_stats(),
            "/history": lambda: self.cmd_history(),
            "/list": lambda: self.cmd_list(arg1 or "."),
            "/export": lambda: self.cmd_export(),
            "/save": lambda: (self.save_history(), f"{C.GREEN}✅ Tersimpan di {HISTORY_FILE}{C.RESET}")[1],
            "/clear": lambda: (self.conversation_history.clear(), f"{C.GREEN}✅ Riwayat sesi dihapus{C.RESET}")[1],
            "/setup": lambda: (self.setup_api_key() and f"{C.GREEN}✅ API key berhasil diset!{C.RESET}") or f"{C.YELLOW}Setup dibatalkan{C.RESET}",
            "/update": lambda: (self.save_config(), f"{C.GREEN}✅ Konfigurasi disimpan{C.RESET}")[1],
        }

        if cmd in handlers:
            return handlers[cmd]()

        # Parameterized commands
        if cmd == "/model":
            if not arg1:
                return self.cmd_models()
            m = MODELS.get(arg1)
            if m:
                self.model = m["id"]
                self.save_config()
                return f"{C.GREEN}✅ Model: {m['name']}{C.RESET}"
            return f"{C.RED}❌ Model tidak valid. /models untuk daftar{C.RESET}"

        if cmd == "/temp":
            try:
                t = float(arg1)
                if 0.1 <= t <= 1.5:
                    self.temperature = t
                    self.save_config()
                    return f"{C.GREEN}✅ Temperature: {t}{C.RESET}"
                return f"{C.RED}❌ Harus antara 0.1 – 1.5{C.RESET}"
            except ValueError:
                return f"{C.RED}❌ Gunakan angka, contoh: /temp 0.8{C.RESET}"

        if cmd == "/tokens":
            try:
                t = int(arg1)
                if 256 <= t <= 8192:
                    self.max_tokens = t
                    self.save_config()
                    return f"{C.GREEN}✅ Max tokens: {t}{C.RESET}"
                return f"{C.RED}❌ Harus antara 256 – 8192{C.RESET}"
            except ValueError:
                return f"{C.RED}❌ Gunakan angka, contoh: /tokens 2048{C.RESET}"

        if cmd == "/name":
            if not arg1:
                return f"{C.YELLOW}Nama saat ini: {self.profile.name}. Gunakan /name [nama]{C.RESET}"
            self.profile.name = " ".join(parts[1:]).title()
            self.profile.save()
            self.memory.remember("user_name", self.profile.name)
            return f"{C.GREEN}✅ Nama disimpan: {self.profile.name}{C.RESET}"

        if cmd == "/remember":
            if not arg1 or not arg2:
                return f"{C.RED}❌ Gunakan: /remember [kunci] [nilai]{C.RESET}"
            self.memory.remember(arg1, arg2)
            return f"{C.GREEN}✅ Diingat: {arg1} = {arg2}{C.RESET}"

        if cmd == "/forget":
            if not arg1:
                return f"{C.RED}❌ Gunakan: /forget [kunci]{C.RESET}"
            if arg1 in self.memory.memories:
                del self.memory.memories[arg1]
                self.memory.save()
                return f"{C.GREEN}✅ Memori '{arg1}' dihapus{C.RESET}"
            return f"{C.YELLOW}Tidak ada memori dengan kunci '{arg1}'{C.RESET}"

        if cmd == "/snippets":
            return self.cmd_snippets(arg1 or None)

        if cmd == "/read":
            return self.cmd_read(arg1)

        if cmd == "/mood":
            if arg1 and arg1 in MOODS:
                self.current_mood = arg1
                return f"{C.GREEN}✅ Mood: {arg1} {MOODS[arg1]['emoji']}{C.RESET}"
            moods_list = " | ".join(f"{k} {v['emoji']}" for k, v in MOODS.items())
            return f"{C.CYAN}Mood tersedia:{C.RESET} {moods_list}\n{C.GREEN}Aktif:{C.RESET} {self.current_mood} {MOODS[self.current_mood]['emoji']}\n{C.DIM}Gunakan: /mood [nama]{C.RESET}"

        if cmd in ["/exit", "/quit", "/q"]:
            return None  # Sinyal keluar

        return f"{C.RED}❌ Perintah tidak dikenali.{C.RESET} {C.YELLOW}/help{C.RESET} untuk bantuan."


# ─────────────────────────────────────────
# Banner
# ─────────────────────────────────────────
def print_banner():
    art = f"""
{C.BLUE}{C.BOLD}  ███████╗██╗     ███████╗███╗   ██╗ █████╗
  ██╔════╝██║     ██╔════╝████╗  ██║██╔══██╗
  █████╗  ██║     █████╗  ██╔██╗ ██║███████║
  ██╔══╝  ██║     ██╔══╝  ██║╚██╗██║██╔══██║
  ███████╗███████╗███████╗██║ ╚████║██║  ██║
  ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝{C.RESET}

  {C.CYAN}Ethical Learning & Network Assistant v3.0{C.RESET}
  {C.DIM}Adaptive · Learning · Streaming · Termux Ready{C.RESET}
"""
    print(art)


# ─────────────────────────────────────────
# Typing indicator (animated dots while loading)
# ─────────────────────────────────────────
_stop_thinking = threading.Event()

def show_thinking():
    frames = ["   ", ".  ", ".. ", "..."]
    i = 0
    while not _stop_thinking.is_set():
        print(f"\r{C.DIM}ELENA berpikir{frames[i % 4]}{C.RESET}", end="", flush=True)
        i += 1
        time.sleep(0.3)
    print("\r" + " " * 25 + "\r", end="", flush=True)


# ─────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────
def main():
    try:
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(200)
    except:
        pass

    os.system("clear" if os.name != "nt" else "cls")
    print_banner()

    elena = ElenaAI()

    # Greet returning user
    if elena.profile.interaction_count > 0:
        days_since = (datetime.now() - datetime.fromisoformat(elena.profile.last_seen)).days
        if days_since > 1:
            print(f"  {C.CYAN}Selamat datang kembali, {elena.profile.name}! Sudah {days_since} hari.{C.RESET}")
        else:
            print(f"  {C.CYAN}Halo lagi, {elena.profile.name}! 👋{C.RESET}")
    
    # API key check
    if not elena.api_key:
        print(f"\n  {C.YELLOW}⚠️  Belum ada API key.{C.RESET}")
        print(f"  Ketik {C.BOLD}/setup{C.RESET} untuk mulai.\n")
    else:
        ok, msg = elena.test_api_key()
        status = f"{C.GREEN}✅ {msg}{C.RESET}" if ok else f"{C.RED}❌ {msg}{C.RESET}"
        print(f"  {status}\n")

    print(f"  {C.DIM}Ketik {C.WHITE}/help{C.DIM} untuk bantuan. Ketik 'exit' untuk keluar.{C.RESET}\n")
    print(f"  {'─'*50}\n")

    while True:
        try:
            mood_emoji = MOODS[elena.current_mood]["emoji"]
            prompt = f"{C.GREEN}{C.BOLD}{elena.profile.name}{C.RESET} {C.DIM}›{C.RESET} "
            try:
                user_input = input(prompt).strip()
            except EOFError:
                break
            except KeyboardInterrupt:
                print(f"\n  {C.YELLOW}Tekan Ctrl+C lagi atau ketik 'exit' untuk keluar.{C.RESET}\n")
                continue

            if not user_input:
                continue

            # Exit
            if user_input.lower() in ["exit", "quit", "bye", "keluar"]:
                print(f"\n  {C.MAGENTA}🤖 ELENA:{C.RESET} Sampai jumpa, {elena.profile.name}! ✨\n")
                elena.save_history()
                break

            # Commands
            if user_input.startswith("/"):
                result = elena.handle_command(user_input)
                if result is None:  # /exit command
                    print(f"\n  {C.MAGENTA}🤖 ELENA:{C.RESET} Sampai jumpa! ✨\n")
                    elena.save_history()
                    break
                print(f"\n{result}\n")
                continue

            # Start thinking indicator
            _stop_thinking.clear()
            think_thread = threading.Thread(target=show_thinking, daemon=True)
            think_thread.start()

            # First chunk stops the indicator
            print(f"\n  {C.MAGENTA}🤖 ELENA {mood_emoji}{C.RESET}  ", end="", flush=True)
            first_chunk = True
            full_resp = ""

            for chunk in elena.chat_stream(user_input):
                if first_chunk:
                    _stop_thinking.set()
                    think_thread.join(timeout=0.5)
                    print(f"\r  {C.MAGENTA}🤖 ELENA {mood_emoji}{C.RESET}  ", end="", flush=True)
                    first_chunk = False
                print(chunk, end="", flush=True)
                full_resp += chunk

            _stop_thinking.set()
            print("\n")

        except KeyboardInterrupt:
            _stop_thinking.set()
            print(f"\n\n  {C.YELLOW}Terganggu. Ketik 'exit' untuk keluar.{C.RESET}\n")
            continue
        except Exception as e:
            _stop_thinking.set()
            print(f"\n  {C.RED}⚠️  Error tidak terduga: {e}{C.RESET}\n")
            continue


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--install":
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
            print(f"{C.GREEN}✅ Dependencies siap!{C.RESET}")
        elif sys.argv[1] == "--reset":
            for f in [CONFIG_FILE, HISTORY_FILE, MEMORY_FILE, PROFILE_FILE, SKILLS_FILE]:
                f.unlink(missing_ok=True)
            print(f"{C.GREEN}✅ Semua data direset!{C.RESET}")
        elif sys.argv[1] == "--version":
            print("ELENA AI v3.0 — Adaptive Intelligence Edition")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print(f"\n{C.YELLOW}👋 ELENA dihentikan.{C.RESET}\n")
        except Exception as e:
            print(f"{C.RED}Fatal: {e}{C.RESET}")
            sys.exit(1)
