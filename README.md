# Stress-management webpage for trial participants

This project contains the website used to provide **the control group's reading materials** in the Sonia research papers listed below. Participants in the control group received web-based information about mental health, while participants in the treatment group received access to Sonia, a voice-based AI emotional support companion.

The website shows a fixed guide called **“Managing Stress and Supporting Your Mental Health.”** Everyone using this website sees the same guide. Its subtitle says “Summarized by AI,” and its footer credits publicly available WHO mental health resources and illustrations by Humanities Studio.

**[Read the exact webpage content, with its illustrations →](docs/webpage-content.md)**

No login, installation, or coding knowledge is needed to read that copy. On GitHub, click the link above; if you see Markdown formatting symbols, select **Preview**. The words, punctuation, section order, and illustrations come directly from the webpage file. Only layout and extra whitespace differ.

## Related research papers

- **Short-term Evaluation of a Voice-Based Generative AI Emotional Support Companion: A Randomized Controlled Trial** — Nicolas Roever, with Lukas Wolf, Valerie Forman-Hoffman, Patricia Areán, and Bennet Feld. Evaluates Sonia against passive web-based psychoeducation based on WHO materials, with anxiety at two weeks as the primary outcome.
- **Therapy Without the Therapist? Experimental Evidence on Automating a Relational Service** — Nicolas Roever, with Bennet Feld. Examines AI-delivered cognitive behavioral therapy, including mental health outcomes at four weeks, demand for human therapy, and social connection.

See [Nicolas Roever's research page](https://www.nicolasroever.com/research) for more information about the papers.

## What participants saw

1. **Welcome:** enter a Trial Participant ID, such as `AB12-CD34`, and select “Continue.”
2. **Home-screen instructions:** iPhone and iPad users see instructions for adding the website to their home screen. Participants can select “Skip for now” or “Open app now” to continue.
3. **The guide:** read about stress, grounding techniques, daily habits, thoughts and emotions, and when to seek help. Returning visitors with a saved login go straight to the guide.

The app records the participant ID, first login, and visits in a database called Supabase. It attempts to record visit end times and duration when the page is hidden or closed. These records describe page visits; they do not establish whether someone read the whole guide.

## Where to find things

| What you want | Where to look |
| --- | --- |
| Read the complete guide without code | [Exact webpage content](docs/webpage-content.md) |
| Check the original guide file used by the website | [Guide page](api/templates/content.html) |
| Check the welcome text, ID field, and error messages | [Welcome page](api/templates/login.html) |
| Check the home-screen instructions | [Setup page](api/templates/onboarding.html) |
| View the original image files | [Illustrations and screenshots](api/static/images/) |
| Understand what the app records | [App code](api/index.py) and [database structure](sql/schema.sql) |

The readable guide reflects the website source in this repository. This repository alone does not establish which version was deployed on a particular trial date.

## For developers

The website uses Python and Flask, Supabase for visit records, and a Vercel deployment configuration.

### Run locally

1. Create a Supabase project and run [sql/schema.sql](sql/schema.sql) in its SQL editor.
2. Create a `.env` file in this folder with `SUPABASE_URL` and `SUPABASE_API_KEY`. The key needs permission to read and write the tables in the schema. Keep it server-side. **Never commit `.env`; it is already in `.gitignore`.**
3. Run:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   flask --app api.index run --debug
   ```

4. Open the local address printed in the terminal. This Flask command loads `.env` automatically. Login and visit recording require the database connection.

### Update the guide

Edit [api/templates/content.html](api/templates/content.html), which is the source of truth for the guide. Then regenerate the readable copy:

```bash
python3 scripts/export_webpage_content.py
```

Do not edit the generated copy directly. The exporter preserves the guide's text and links to the existing illustrations; it does not run the app or record a visit.

### Current limitations

- Visit timestamps currently use database date/time fields and ISO date/time strings. Duration also depends on a start time sent by the browser; timing has not yet been changed to backend-only Unix timestamps.
- Home-screen installation is supported, but the full guide is not explicitly cached for offline reading.
