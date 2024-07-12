# Weekly Aspects and Retrogrades API

This repository contains a Python script that fetches astrological aspects and retrogrades for the upcoming week using NASA's Horizon API and Skyfield. The data is then saved to a JSON file which can be used by other applications, such as an iOS app, to display the astrological forecast.

## Overview

The API fetches the following data for each day of the upcoming week:
- **Retrogrades:** Information about planetary retrogrades including planet name, start and end dates, and the house ruler.
- **Aspects:** Information about planetary aspects including involved planets, aspect type (e.g., conjunction, trine), and the angle.
- **Recommendations:** Suggestions on what to do and what not to do during specific astrological events.
- **Notifications:** Alerts for upcoming retrogrades and daily tips.
- **Educational Content:** Links to articles and resources to understand astrological events better.

## Example Data

Here is an example of the JSON data structure:

```json
{
  "weekly_forecast": [
    {
      "date": "2024-07-11",
      "retrogrades": [
        {
          "planet": "Mercury",
          "start_date": "2024-07-07",
          "end_date": "2024-07-28",
          "house_ruler": "Gemini",
          "days_left": 17
        }
      ],
      "aspects": [
        {
          "planet1": "mercury",
          "planet2": "jupiter",
          "aspect": "sextile",
          "angle": 63.02317846146141
        },
        {
          "planet1": "mercury",
          "planet2": "uranus",
          "aspect": "quintile",
          "angle": 77.21180578205254
        }
      ],
      "recommendations": {
        "do": ["Reflect on past decisions", "Backup important data", "Communicate clearly"],
        "dont": ["Start new projects", "Sign important contracts", "Make major purchases"]
      },
      "notifications": {
        "upcoming_retrograde_alert": "Mercury retrograde starting in 2 days",
        "daily_tip": "Today, avoid making big purchases as Mercury is retrograde."
      },
      "educational_content": [
        {
          "title": "Understanding Mercury Retrograde",
          "url": "https://example.com/mercury-retrograde"
        },
        {
          "title": "How to Navigate Retrogrades",
          "url": "https://example.com/navigate-retrogrades"
        }
      ]
    }
  ]
}
