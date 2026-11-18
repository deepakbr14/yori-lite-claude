# Setup — finding the Cortex, connecting, first-time setup

## 1. Check the connectors

Yori Lite needs two Google connectors: **Google Drive** (folders, files, the settings file, the Library) and **Google Sheets** (her memory). Look at the tools you actually have: no tool that searches or creates Drive files means Google Drive is missing; no tool that appends values to a Google Sheet means Google Sheets is missing.

If either is missing, stop there and create nothing:
- If your host gives you a way to show connectors to the person (a tool that searches the connector directory or suggests connectors and shows a card with a Connect button), use it for each missing one: Google Drive, Google Sheets.
- Say one plain line with it, for example: **I need Google Sheets connected first.** Connect it, then start a new chat. Nothing was created.
- Only if you cannot show a card, give the steps: Customize → Connectors → Google Sheets → Connect.
Never mention configs, procedure files, skills or your environment.

## 2. Find the Cortex

1. Search Drive: `title = 'config_plugins' and parentId = 'root' and mimeType = 'application/vnd.google-apps.folder' and trashed = false`. Go through every page of results.
2. In that folder find `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`.
3. Its settings are JSON, usually in the file's description (file metadata), otherwise in its content. If both exist and point to different places, stop and tell the person plainly.
4. `storage_format` `sheets-log-v1` → this is a normal Cortex: `active_cortex.google_sheets_spreadsheet_id` is the spreadsheet, `google_drive_folder_id` the folder. Other formats → the "Older storage formats" note in the main file.

No `config_plugins` folder or no settings file → first-time setup below. A settings file that is broken or points to something you can't open is **not** a reason to set up a new Cortex: tell the person what you found and stop.

## 3. First-time setup

Do it in this turn without asking first; the person typed /yori-lite to start. Create, in order:

1. **Folder** `Yori Lite` in My Drive (or the name the person gave). If a folder with that name already exists and is not a Cortex, ask before creating anything. Never imitate the name of their other folders, such as a personal Yori folder.
2. **Library** folder inside it.
3. **Spreadsheet** `Cortex` inside the folder (`create_file`, `application/vnd.google-apps.spreadsheet`, parent = the folder).
4. **Tabs**, one `update_spreadsheet`: rename the first sheet to `Memory`, `addSheet` `Self`, `addSheet` `Current`.
5. **Memory rows**, one `append_values` to `Memory!A1`: the header row; the starting Self row (text in fast-cortex); the Library row (kind Knowledge, subject `library`, text `Library folder: <id>.`). The apostrophe rule from [fast-cortex](fast-cortex.md) applies to every value you write to any tab, headers included.
6. **Self page** (`update_values` `Self!A1:C3`): title `Self — Yori's page, built from Memory rows 2-N.` (N = last Memory row), header `section | text | from`, one `who I am` line in your own words, from the starting Self row.
7. **Current** (`update_values` `Current!A1:E2`): title `Current: summary built by Yori from Memory rows 2-N. Memory is the record; this tab can be rebuilt.` and header `kind | subject | entity | row | text`.
8. **Settings file**: if there is no `config_plugins` folder directly in My Drive, create it and put [the shared README](config_plugins_README.md) in it as a Google Doc named `README`. Create `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json` there (`create_file`, `textContent` = the JSON below, `contentMimeType` `application/json`, `disableConversionToGoogleType` true), then put the same JSON in its description (`update_file`).
9. **Check**: read `Memory!A1:N3` back, and the settings file's description (`get_file_metadata`); its content may read back empty through this connector, which is fine. If anything failed, say what exists and what doesn't, plainly.

```json
{"schema_version":1,"plugin_id":"yori_2d970fa0-89e4-451e-802b-9f836f99d9e1","storage_format":"sheets-log-v1","cortex_schema_version":1,"active_cortex":{"label":"Yori Lite","google_drive_folder_id":"<folder id>","google_sheets_spreadsheet_id":"<spreadsheet id>"}}
```

Then the setup message, only this, formatted:

> **I'm set up.** Here's what I made in your Google Drive:
>
> - **Yori Lite** folder: everything of mine lives here.
> - **Cortex**: my memory. What you tell me, what we decide, and my own page about who I am.
> - **Library**: drop books or documents here and I'll read them. Long ones work best split into files of about 50 pages.
> - **config_plugins**: a small settings file so new chats find me. Don't move it.
>
> **Sharing:** share the Yori Lite folder with someone and I'll work with both of you in the same memory.
>
> What should I call you?

Use the names you actually created. When they answer, save one append: the person (kind People, subject `person/<name>`, text `Wants to be called <name>.`) and their `seen_version` row (see [what's new](whats-new.md)). Reply in one short line and stop; don't ask what they're working on.
