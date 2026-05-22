# Komodo Wellbeing Flash Cards — Interactive Trainer

An interactive Streamlit app for running the Komodo Wellbeing Flash Cards live in school staff training sessions. Browse all 23 activities, filter by age and props, run pre-built themed playlists, or draw a random card.

## What's inside

- **Browse all** (`Browse_all.py`) — Grid of all 23 activities, each with a hero icon, age/supplies/purpose pills, and a preview of the instructions. Filter by age (Jr/Sr/All), supplies, purpose, or search. Click any card to open it in presentation mode with an interactive widget tailored to that activity (animated breath circle, bilateral tap pulse, weather picker, list inputs, stepped flow, countdown timer, or colour pulse).
- **Themed sets** — 8 curated playlists for common school moments (morning regulation, in-the-moment anxiety, energy release, gratitude & connection, end-of-day reflection, building self-worth, mindfulness practice, creative expression). Walk teachers through one set end-to-end.
- **Random picker** — Draw a random card from the (optionally filtered) deck. Good for closing energisers in a training session.
- **Training guide** — A short trainer's reference: how to run a session, three ways to structure it, and live-use tips.

## Run it

```bash
cd ~/Claude\ Projects/komodo-flashcards
./run.sh
```

Or directly:

```bash
pip3 install -r requirements.txt
streamlit run Browse_all.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

## For training projection

- The presentation-mode card uses large text and a big visible timer — readable from the back of the room.
- Click **Open card for training** on any card to enter presentation mode.
- Use the sidebar page menu (**Browse activities / Themed Sets / Random Picker / Training Guide**) to switch views.

## Source

Activities written by Komodo Wellbeing's in-house Child & Family Psychologist, based on research-backed methods. Designed for both *prevention* (building emotional resilience) and *early intervention* (managing distress as it appears).

## Files

| File | Purpose |
|------|---------|
| `Browse_all.py` | Browse all + presentation mode (the entry point) |
| `widgets.py` | Interactive widget HTML/JS per activity type |
| `pages/1_Themed_Sets.py` | Curated playlists |
| `pages/2_Random_Picker.py` | Random card draw |
| `pages/3_Training_Guide.py` | Trainer's reference |
| `activities.py` | All 23 activity definitions |
| `themed_sets.py` | 8 curated playlists |
| `branding.py` | Shared Komodo brand styling |
| `.streamlit/config.toml` | Streamlit theme |
| `assets/logo-primary.png` | Komodo logo |
