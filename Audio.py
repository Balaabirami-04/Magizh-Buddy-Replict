import os
import asyncio
import io
import base64
import queue
import sounddevice as sd
from threading import Thread

from dotenv import load_dotenv
from deepgram import DeepgramClient


load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


class AudioEngine:
    def __init__(self, deepgram_key=None):
        """
        Initializes Deepgram client for:
        - Live STT
        - TTS speech synthesis
        """
        try:
            self.client = DeepgramClient(api_key=deepgram_key or DEEPGRAM_API_KEY)
            print("Deepgram client initialized.")
        except Exception as e:
            print(f"Deepgram init failed: {e}")
            self.client = None

        self.connection = None
        self.is_recording = False
        self.audio_queue = queue.Queue()

    # -----------------------------------------------------------
    # 🟦 LIVE SPEECH-TO-TEXT
    # -----------------------------------------------------------
    async def record_and_transcribe_live(self, callback, duration=15):
        """
        Start live microphone recording → Deepgram Nova-2 model → Callback with transcript.
        This method runs for `duration` seconds.
        """

        if not self.client:
            print("Deepgram client not initialized.")
            return "Missing Deepgram API Key."

        print("Starting Deepgram Live STT...")

        # Options for Indian English (clean + accurate)
        options = {
            "model": "nova-2-general",
            "language": "en-IN",
            "smart_format": True,
            "encoding": "linear16",
            "sample_rate": 16000,
            "channels": 1
        }

        # Open live connection (v1)
        self.connection = self.client.listen.live.v("1")

        # Register event listener correctly
        @self.connection.on("Results")
        def on_transcript(connection, result, **kwargs):
            transcript = ""
            try:
                transcript = result.channel.alternatives[0].transcript
            except Exception:
                pass

            if transcript:
                print(f"[LIVE TRANSCRIPT] {transcript}")

                # Run user callback (safe for asyncio + threads)
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(callback(transcript))
                else:
                    asyncio.run(callback(transcript))

        # Start the Deepgram WebSocket
        await self.connection.start(options)

        # Start audio recording thread
        self.is_recording = True
        Thread(target=self._record_audio_thread, daemon=True).start()

        # Auto-stop after duration
        await asyncio.sleep(duration)
        self.stop_recording()

        return "Recording finished."

    # -----------------------------------------------------------
    # 🎙 BACKGROUND AUDIO RECORDER
    # -----------------------------------------------------------
    def _record_audio_thread(self):
        """
        Records raw PCM mic audio and sends to Deepgram.
        Avoids blocking the UI.
        """
        RATE = 16000
        BLOCK = 1024

        try:
            with sd.InputStream(
                samplerate=RATE,
                channels=1,
                dtype="int16",
                blocksize=BLOCK
            ) as stream:

                while self.is_recording:
                    if not self.connection:
                        break

                    audio_block, overflow = stream.read(BLOCK)

                    if overflow:
                        print("Microphone overflow detected.")

                    # Send PCM bytes to Deepgram
                    self.connection.send(audio_block.tobytes())

        except Exception as e:
            print(f"Audio thread error: {e}")
            self.stop_recording()

    # -----------------------------------------------------------
    # 🟥 STOP RECORDING SAFELY
    # -----------------------------------------------------------
    def stop_recording(self):
        self.is_recording = False
        print("Stopping microphone recording...")

        if self.connection:
            try:
                self.connection.finish()
                print("Deepgram connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")

    # -----------------------------------------------------------
    # 🟩 TEXT-TO-SPEECH USING DEEPGRAM AURA
    # -----------------------------------------------------------
    async def speak(self, text, voice="aura-asteria-en"):
        """
        Deepgram Aura TTS → returns Base64 WAV audio string ready to embed.
        """
        if not self.client:
            print("Deepgram client missing for TTS.")
            return None

        try:
            print("[TTS] Converting text to speech...")

            # Available Aura voices: asteria, arcas, orpheus, helios…
            options = {"model": voice}

            response = self.client.speak.v("1").generate(text, options)

            # Read raw bytes of audio
            audio_bytes = response.stream.read()

            # Convert to Base64 for Flet Audio player
            encoded = base64.b64encode(audio_bytes).decode()

            return f"data:audio/wav;base64,{encoded}"

        except Exception as e:
            print(f"TTS Error: {e}")
            return None
