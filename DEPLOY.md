# Deploying to Streamlit Community Cloud

You've done this before for the multi-school dashboard. This is the same flow, just shorter — there are no API secrets to configure.

**Total time:** ~15 minutes first time. After that, every code change pushes in seconds via GitHub Desktop.

---

## Step 1 — Add this folder to GitHub Desktop

1. Open **GitHub Desktop**.
2. **File → Add Local Repository**.
3. Choose the folder `~/Claude Projects/komodo-flashcards`.
4. If GitHub Desktop says "This directory does not appear to be a Git repository", click the **create a repository** link in that warning.
5. Repository name: `komodo-flashcards` (suggested). Leave the rest as default. Click **Create Repository**.

## Step 2 — Make the first commit

1. In the bottom-left of GitHub Desktop, the summary box is auto-filled with "Initial commit" — or type one in.
2. Click the blue **Commit to main** button at the bottom-left.

## Step 3 — Publish to GitHub

1. Click the big **Publish repository** button at the top of GitHub Desktop.
2. Repository name: `komodo-flashcards` (keep default).
3. **Important:** untick **Keep this code private** if you want a free Streamlit Cloud deploy. *(Free tier requires public repos. If you want it private, you'd need a Streamlit Cloud paid plan — for an internal trainer prototype, public is fine since none of the activities or code is sensitive.)*
4. Click **Publish Repository**.

## Step 4 — Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io** in your browser.
2. Sign in with the same GitHub account you've already used for the dashboard.
3. Click the blue **Create app** button (top right).
4. Choose **Deploy a public app from GitHub**.
5. Fill in:
   - **Repository:** `<your-github-username>/komodo-flashcards`
   - **Branch:** `main`
   - **Main file path:** `Browse_all.py`  ← this is the important one
   - **App URL:** pick a slug like `komodo-flashcards` (the live URL will be `https://komodo-flashcards.streamlit.app` — or you'll get a suggested suffix if that's taken).
6. Click **Deploy**.

Streamlit will install Python, install `streamlit` from `requirements.txt`, and start the app. First boot takes 2–3 minutes. After that, every push to GitHub redeploys in under a minute.

## Step 5 — Send the link

Once it says "Your app is live!", copy the URL from the address bar (e.g. `https://komodo-flashcards.streamlit.app`) and send it to your team member. They open it in any browser — no install, no Python, nothing.

---

## After the first deploy

Any time you change the code on your Mac:

1. Open GitHub Desktop.
2. You'll see the changed files listed in the left panel.
3. Write a short summary in the bottom-left box (e.g. "Added new card" or "Fixed typo").
4. Click **Commit to main**.
5. Click **Push origin** at the top.

Streamlit Cloud picks up the push automatically and rebuilds. Refresh the URL after ~30 seconds and your changes are live.

## Pausing the app

If you want to pause it (e.g. during a school holiday) so it's not running 24/7:

1. Go to https://share.streamlit.io
2. Click the **⋯** menu next to your app → **Pause**.

Unpause the same way when you need it back.

## Troubleshooting

- **Build fails with "module not found"** → check `requirements.txt` has the missing package.
- **App boots but pages don't show** → make sure `Browse_all.py` is in the repo root (not inside a subfolder) and that `pages/` is a sibling.
- **Logo doesn't appear** → verify `assets/logo-primary.png` was committed (check it in GitHub Desktop's file list). The `.gitignore` doesn't exclude it.
