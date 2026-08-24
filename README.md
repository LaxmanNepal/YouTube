# Laxman Nepal Official — YouTube Growth Intelligence

A lightweight GitHub Pages dashboard for turning fresh YouTube/topic research into ranked content opportunities for **Laxman Nepal Official**.

## Current architecture

- Static frontend: `index.html`, `style.css`, `app.js`
- Live data source: `data/growth-data.json`
- No AI API is required by the website itself.
- The dataset can be refreshed by research/update work and committed to GitHub.

## Refresh model

When a new research cycle is performed, update `data/growth-data.json`. The website fetches that JSON with cache-busting, so the latest committed dataset appears after GitHub Pages publishes the commit.

Each topic is designed to contain:

- opportunity score
- demand
- competition
- channel fit
- reason to make it
- recommended title
- alternative titles
- description
- tags
- hashtags
- thumbnail text
- thumbnail concept
- thumbnail prompt

## Optional YouTube API integration

A YouTube Data API v3 key can later populate public channel/video/competitor data. **Never put the key in frontend JavaScript or JSON.** Use GitHub Actions secrets or a server-side worker for API calls.

Suggested future secret:

`YOUTUBE_API_KEY`

For private YouTube Analytics, OAuth is required and should remain server-side.

## GitHub Pages

Publish the repository root as the Pages source. The site is intentionally framework-free so it can run directly from GitHub Pages.
