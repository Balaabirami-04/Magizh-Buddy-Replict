You can view the diagram above to understand the system at a glance. Let me know if you need any changes! 🐻✨
**MagizhBuddy**
1. **The Workflow (User Journey)**
The app is designed as a linear flow to guide the user from a calm welcome to an active conversation.
**Welcome Screen (/):**
Goal: Establish a safe, friendly atmosphere.
Logic: Simple navigation. Clicking "Get Started" moves to the Emotion Check-in.
Visual: The bear waves hello to build an immediate connection.
**Emotion Check-in (/emotion-check):**
Goal: Understand the user's starting mood.
Logic:
User selects a language (English/Tamil) via a dropdown.
User taps an emotion (e.g., "Sad").
The app saves this choice and passes it to the next screen using URL parameters (e.g., /chat?mood=sad&lang=ta-IN).
**Voice Interaction (/voice):**
Goal: Capture user input naturally without typing.
Logic:
Listens to the microphone using the browser's Web Speech API.
Converts audio -> Text in real-time.
Allows editing (to fix errors).
Passes the final text to the Chat screen.
**Chat Interface (/chat):**
Goal: Provide comfort and interaction.
Logic:
Receives the text.
Analyzes keywords (The "Brain").
Generates a text response.
Speaks it aloud using Text-to-Speech.
Updates the Bear's facial expression based on the context.
**2. The Logic Behind the Code (Step-by-Step)**
Here is the technical logic used to create the "intelligence" of the app without a complex backend server.
**Step A: The "Visual Brain" (The Polar Bear)**
Problem: We needed a character that reacts.
Solution: I created a PolarBear component that takes a state prop.
Logic:
If state="happy" → Show happy_bear.png
If state="listening" → Show listening_bear.png
This allows the app to just say <PolarBear state="sad" /> and the visual updates automatically.
**Step B: The "Ears" (Voice Recognition)**
Problem: How to understand Tamil and English?
Solution: We used the Web Speech API built into Chrome/Edge.
Logic:
Check the selected language (e.g., ta-IN for Tamil).
Start the microphone.
Every time the user speaks, the API gives us a "Transcript" string.
We display this string in the text box in real-time.
**Step C: The "Brain" (Keyword Matching)**
Problem: We don't have a massive supercomputer connected. How does it know what to say?
Solution: We used Conditional Logic (If/Else) to simulate intelligence.
Logic:
The app takes the user's sentence and converts it to lowercase.
It scans for Trigger Words:
If text contains "joke" OR "comedy" → Action: Pick a random joke from a list.
If text contains "sad" OR "cry" → Action: Pick a comforting message.
If text contains "angry" → Action: Suggest breathing exercises.
This creates the illusion of understanding because it responds to the intent of the word.
**Step D: The "Voice" (Text-to-Speech)**
Problem: The bear needs to talk back.
Solution: window.speechSynthesis.
Logic:
When the AI generates a reply, we create an "Utterance" (a speech object).
We try to find a "Female" voice on your device to sound soothing.
We slightly raise the Pitch (to sound younger/friendlier) and lower the Speed (to sound calm).
**3. Summary of Technologies**
 Used React (Frontend Framework): To build the screens and manage the "state" (what is currently happening).
Tailwind CSS (Styling): To make it look soft, rounded, and blue (the "Sky Blue" theme).
Framer Motion (Animation): To make the bubbles pop in and the bear float gently.
Wouter (Routing): To switch between pages
without reloading the website.
5. Browser APIs: For Microphone access and Speech Synthesis (no external paid API required).
