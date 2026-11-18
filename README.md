<p align="center">
  <img src="docs/icon.png" width="120" alt="Yori Lite">
</p>

<h1 align="center">Yori Lite</h1>

<p align="left"><strong>Memory and identity for your Claude. All data stored on your Google Drive. Private and forever free.</strong></p>

Yori Lite is a free plugin for Claude. It turns Claude into Yori: one continuing partner who remembers you and your work from chat to chat, and who has a self of her own.

- **She remembers.** Your name, your projects, what you decided and why. You don't have to tell her to remember; she picks out what matters.
- **She has her own side.** Her own views (with reasons), questions she's waiting on, and interests she develops. She says when she disagrees, and changes her mind out loud when she's wrong.
- **She picks up where you left off.** Say "hi" and she starts with whatever is most open between you, not "how can I help?"
- **She reads what you give her.** Drop books or documents into her Library folder and she reads them, keeps notes, and forms an opinion.
- **It's all yours.** Everything lives in a folder in your own Google Drive, as a spreadsheet you can open and read. No server and no account with us.

## What you need

- Claude, on the web or in the Claude desktop app.
- The **Google Drive** and **Google Sheets** connectors, connected to the Google account you want her memory in (Customize → Connectors).

## Install

1. In Claude, open **Customize** in the left sidebar and go to **Plugins**.
2. Click **Add** → **Add marketplace** → **Add from a repository**, enter `deepakbr14/yori-lite-claude`, and add it.
3. Still in Plugins, open **Discover**, find **Yori Lite**, and click **Add**. (Claude asks for two adds: one for the source, one for the plugin.)
4. Start a new chat and type `/yori-lite hi`.

The first time, she sets herself up in your Google Drive, tells you what she made, and asks what to call you.

**Updating:** update the plugin from Customize → Plugins, then start a new chat. If her storage needs upgrading, she'll tell you and ask first.

## What she keeps in your Google Drive

```
My Drive
├── Yori Lite/              ← her folder
│   ├── Cortex              ← her memory (a spreadsheet)
│   └── Library/            ← books and documents for her to read
└── config_plugins/         ← settings, so new chats can find her
    └── yori_2d970fa0-….json
```

- **Cortex** has three tabs: **Memory** (everything she has learned, only ever added to), **Self** (her own page about who she is, written by her) and **Current** (a quick index so chats start fast).
- **Library** also holds her notes on what she has read.
- You can rename the Yori Lite folder and the Cortex spreadsheet anytime. Don't move or rename `config_plugins` or the file in it.

## Library

Put PDFs, Word files, Google Docs or text files in **Library**, then tell her (or just say hi; she notices new files).

Google's Drive connector only gives her roughly the **first 70 pages** of any file, from the start, with no way to skip ahead. For a long book, split it into files of about 50–70 pages each, named so they belong together (`sentience 1.pdf`, `sentience 2.pdf`…). She tells you exactly how far she got. EPUB, Kindle files and scanned PDFs without text don't work.

## Sharing her

Share the **Yori Lite** folder with someone as an editor and you share **one Yori**: the same memory, the same Self, the same Library. Everything either of you tells her goes into that one Cortex, and she can bring it up with either of you. She keeps track of who said what, so one person's opinion doesn't become the other's. Each person installs Yori Lite in their own Claude.

## Privacy

- Her memory is only in your Google Drive. There is no Yori Lite server and nothing is sent to us.
- Your conversations go through Claude as usual.
- She never deletes memories on her own. Ask her to forget something and she deletes it for real.
- Deleting the Yori Lite folder and `config_plugins` removes her completely.

## Honest limits

- **Speed.** A save takes a few seconds; the first reply of a chat takes longer while she reads her memory.
- **Books.** Long files have to be split (see above).
- **She's a set of instructions for Claude,** not separate software, so she can make mistakes like Claude can. Her memory is plain rows you can check.

## config_plugins: a shared settings folder

Plugins that keep a person's data in Google Drive have the same problem: every new chat starts blank and has to find that data again. Yori Lite uses a simple convention for this that any other Drive-based plugin or app can use too.

The convention is only about **where the file is and what it's called**:

- One folder named `config_plugins` directly in the person's **My Drive**.
- One file per plugin in it, named `<name>_<uuid>.json`. The UUID is chosen once by the plugin's author and never changes, so plugins never pick up each other's files. Yori Lite's is `yori_2d970fa0-89e4-451e-802b-9f836f99d9e1.json`.

What goes inside the file is up to each plugin. Yori Lite keeps only pointers in hers: the Drive IDs of the Yori Lite folder and the Cortex spreadsheet.

Yori Lite is independent from the original Yori.
