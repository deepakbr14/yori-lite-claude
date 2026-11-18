# What's new

The current version is in the main file (`Independent Yori Lite <version>`). Each person sees the note for a version once.

## Checking

At chat start, look in Current or the newer Memory rows for this person's `person/<id>/seen_version` line.
- Missing or older than the current version → open the reply with the note below, before anything else, formatted like a setup message. Then a blank line and carry on with what they said.
- Save (in that turn's append) a People row `person/<id>/seen_version`, text `Has seen Yori Lite <version>.`, revising the earlier one if there is one.
- A person who was just set up in this chat doesn't see the note, but save their `seen_version` row with their name.

## 0.4.9

> **I've been updated (0.4.9).**
> - **Clearer setup and updates:** these messages now come on their own, so nothing gets missed.
> - **Connect buttons:** if something like Google Sheets isn't connected, I show the card to connect it.
> - **Works in more places:** everything I need now travels with me inside the plugin.
> - **New names for new setups:** a **Yori Lite** folder and a **Cortex** spreadsheet. Yours keep their names; rename them anytime.
