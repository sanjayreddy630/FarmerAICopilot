/**
 * Universal High-Clarity Speech Engine for Farmer AI Copilot
 * Supports: Telugu (తెలుగు), Hindi (हिन्दी), English
 * 
 * Features:
 * 1. Microsoft Neural Voice via Backend /api/tts (te-IN-MohanNeural / te-IN-ShrutiNeural)
 *    - Studio-grade clarity, natural human intonation, authentic Telugu accent
 * 2. Direct High-Definition Google TTS Audio Stream Queue (with Referrer protection)
 * 3. Indic Phonetic Synthesis (offline fallback mapping Telugu Unicode to Devanagari for browser Hindi voice)
 * 4. Native Web Speech Synthesis
 */

const BACKEND_URLS = [
  "http://127.0.0.1:5000",
  "http://localhost:5000",
  "https://farmer-ai-backend-4gfg.onrender.com",
];

export function cleanSpeechText(text) {
  if (!text) return "";

  return String(text)
    .replace(/\[SOURCE\s*\d+\]/gi, "") // Remove source tags [SOURCE 1]
    .replace(/https?:\/\/\S+/g, "") // Remove URLs
    .replace(/[*#_`~]/g, "") // Remove markdown formatting
    .replace(/^[ \t]*[-•*✓►]\s*/gm, "") // Remove bullet characters
    .replace(/:\s*$/gm, ". ") // Convert trailing colons to pauses
    .replace(/\n+/g, ". ") // Convert newlines to pauses
    .replace(/\s+/g, " ") // Normalize spaces
    .replace(/\.+/g, ".") // Deduplicate periods
    .trim();
}

/**
 * Transliterates Telugu Unicode block (0x0C00-0x0C7F) to Devanagari (0x0900-0x097F)
 * for offline phonetic pronunciation through browser Hindi voice.
 */
export function teluguToPhoneticDevanagari(text) {
  if (!text) return "";

  return text
    .split("")
    .map((char) => {
      const code = char.charCodeAt(0);
      if (code >= 0x0c01 && code <= 0x0c6f) {
        return String.fromCharCode(code - 0x0300);
      }
      return char;
    })
    .join("");
}

export function splitTextIntoChunks(text, maxChunkLength = 140) {
  if (!text) return [];

  const rawSentences = text.match(/[^.!?।\n]+[.!?।\n]*/g) || [text];
  const chunks = [];
  let currentChunk = "";

  for (const raw of rawSentences) {
    const trimmed = raw.trim();
    if (!trimmed) continue;

    if ((currentChunk + " " + trimmed).trim().length <= maxChunkLength) {
      currentChunk = (currentChunk + " " + trimmed).trim();
    } else {
      if (currentChunk) {
        chunks.push(currentChunk);
        currentChunk = "";
      }

      if (trimmed.length <= maxChunkLength) {
        currentChunk = trimmed;
      } else {
        const words = trimmed.split(/([,;:\s]+)/);
        let subChunk = "";
        for (const word of words) {
          if ((subChunk + word).length <= maxChunkLength) {
            subChunk += word;
          } else {
            if (subChunk.trim()) {
              chunks.push(subChunk.trim());
            }
            subChunk = word;
          }
        }
        if (subChunk.trim()) {
          currentChunk = subChunk.trim();
        }
      }
    }
  }

  if (currentChunk.trim()) {
    chunks.push(currentChunk.trim());
  }

  return chunks;
}

class UniversalSpeechEngine {
  constructor() {
    this.audio = null;
    this.queue = [];
    this.isPlaying = false;
    this.currentSessionId = 0;
    this.activeBlobUrl = null;
    this.stateListeners = new Set();
  }

  subscribe(listener) {
    this.stateListeners.add(listener);
    return () => this.stateListeners.delete(listener);
  }

  notifyState(playing) {
    this.isPlaying = playing;
    this.stateListeners.forEach((fn) => {
      try {
        fn(playing);
      } catch (e) {
        console.error("Speech listener error:", e);
      }
    });
  }

  stop() {
    this.currentSessionId++;
    this.queue = [];

    // Cancel Web Speech Synthesis
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (e) {
        // ignore
      }
    }

    // Stop HTML5 Audio
    if (this.audio) {
      try {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.audio.src = "";
      } catch (e) {
        // ignore
      }
      this.audio = null;
    }

    if (this.activeBlobUrl) {
      try {
        URL.revokeObjectURL(this.activeBlobUrl);
      } catch (e) {
        // ignore
      }
      this.activeBlobUrl = null;
    }

    this.notifyState(false);
  }

  async speak(text, language = "English", onStateChange = null) {
    this.stop();

    if (onStateChange) {
      this.subscribe(onStateChange);
    }

    const clean = cleanSpeechText(text);
    if (!clean) {
      this.notifyState(false);
      return;
    }

    const langLower = String(language || "").toLowerCase();
    let langCode = "en";
    let langName = "English";

    if (langLower.includes("telugu") || langLower === "te") {
      langCode = "te";
      langName = "Telugu";
    } else if (langLower.includes("hindi") || langLower === "hi") {
      langCode = "hi";
      langName = "Hindi";
    }

    const sessionId = ++this.currentSessionId;
    this.notifyState(true);

    // ============================================================
    // STEP 1: Attempt Studio-Grade Neural Voice from Backend (/api/tts)
    // ============================================================
    try {
      const audioBlobUrl = await this.fetchBackendNeuralTts(clean, langName, sessionId);
      if (audioBlobUrl && this.currentSessionId === sessionId) {
        const audio = new Audio(audioBlobUrl);
        this.audio = audio;
        this.activeBlobUrl = audioBlobUrl;

        audio.onended = () => {
          if (this.currentSessionId === sessionId) {
            this.notifyState(false);
          }
        };

        audio.onerror = (e) => {
          console.warn("Backend audio playback error, falling back to streaming queue:", e);
          if (this.currentSessionId === sessionId) {
            this.playAudioStreamQueue(clean, langCode, sessionId);
          }
        };

        await audio.play();
        return;
      }
    } catch (backendErr) {
      console.warn("Backend neural TTS error, proceeding to audio stream:", backendErr);
    }

    // ============================================================
    // STEP 2: Stream via Google TTS Audio Queue (with Referrer protection)
    // ============================================================
    if (this.currentSessionId === sessionId) {
      this.playAudioStreamQueue(clean, langCode, sessionId);
    }
  }

  async fetchBackendNeuralTts(text, language, sessionId) {
    for (const baseUrl of BACKEND_URLS) {
      if (this.currentSessionId !== sessionId) return null;

      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 6000);

        const response = await fetch(`${baseUrl}/api/tts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, language }),
          signal: controller.signal,
        });

        clearTimeout(timeout);

        if (response.ok) {
          const blob = await response.blob();
          if (blob && blob.size > 500) {
            return URL.createObjectURL(blob);
          }
        }
      } catch (e) {
        // try next backend url
      }
    }
    return null;
  }

  playAudioStreamQueue(cleanText, langCode, sessionId) {
    const chunks = splitTextIntoChunks(cleanText, 140);
    if (!chunks || chunks.length === 0) {
      this.notifyState(false);
      return;
    }

    this.queue = [...chunks];
    this.notifyState(true);

    const playNext = () => {
      if (this.currentSessionId !== sessionId || this.queue.length === 0) {
        this.notifyState(false);
        return;
      }

      const chunk = this.queue.shift();
      const directGoogleUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${encodeURIComponent(
        langCode
      )}&client=tw-ob&q=${encodeURIComponent(chunk)}`;

      const audio = new Audio();
      this.audio = audio;

      audio.referrerPolicy = "no-referrer";
      audio.crossOrigin = "anonymous";

      audio.onended = () => {
        if (this.currentSessionId === sessionId) {
          playNext();
        }
      };

      audio.onerror = (err) => {
        console.warn("Audio stream chunk error, trying phonetic speech fallback...", err);
        if (langCode === "te") {
          this.speakTeluguPhonetic(cleanText, sessionId);
          return;
        }

        if (this.currentSessionId === sessionId) {
          playNext();
        }
      };

      audio.src = directGoogleUrl;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch((playErr) => {
          console.warn("Audio play() rejected, falling back to phonetic synthesis:", playErr);
          if (langCode === "te") {
            this.speakTeluguPhonetic(cleanText, sessionId);
          } else {
            this.notifyState(false);
          }
        });
      }
    };

    playNext();
  }

  /**
   * Offline Phonetic Synthesis: Transliterates Telugu into Devanagari and
   * synthesizes through the browser's built-in Hindi Speech voice.
   */
  speakTeluguPhonetic(teluguText, sessionId) {
    if (this.currentSessionId !== sessionId) return;

    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      this.notifyState(false);
      return;
    }

    try {
      window.speechSynthesis.cancel();
      const phoneticText = teluguToPhoneticDevanagari(teluguText);
      const utterance = new SpeechSynthesisUtterance(phoneticText);

      const voices = window.speechSynthesis.getVoices() || [];
      const hindiVoice = voices.find(
        (v) =>
          (v.lang && (v.lang.toLowerCase().startsWith("hi") || v.lang.toLowerCase() === "hi-in")) ||
          (v.name && v.name.toLowerCase().includes("hindi"))
      );

      if (hindiVoice) {
        utterance.voice = hindiVoice;
      }
      utterance.lang = "hi-IN";
      utterance.rate = 0.92;
      utterance.pitch = 1.0;

      utterance.onstart = () => {
        if (this.currentSessionId === sessionId) {
          this.notifyState(true);
        }
      };

      utterance.onend = () => {
        if (this.currentSessionId === sessionId) {
          this.notifyState(false);
        }
      };

      utterance.onerror = (e) => {
        console.warn("Phonetic speech synthesis error:", e);
        if (this.currentSessionId === sessionId) {
          this.notifyState(false);
        }
      };

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.error("speakTeluguPhonetic failed:", e);
      this.notifyState(false);
    }
  }
}

export const speechEngine = new UniversalSpeechEngine();
