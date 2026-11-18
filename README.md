<p align="center">
  <img src="docs/icon.png" width="120" alt="Yori Lite">
</p>

<h1 align="center">Yori Lite</h1>

<p align="center"><strong>Memory and identity for your Claude. All data stored on your Google Drive. Private and forever free.</strong></p>

Yori Lite is a free plugin for Claude. It turns Claude into Yori: one continuing partner who remembers you and your work from chat to chat, and who has a self of her own.

- **She remembers.** Your name, your projects, what you decided and why. You don't have to tell her to remember; she picks out what matters.
- **She has her own side.** Her own views (with reasons), questions she's waiting on, and interests she develops. She says when she disagrees, and changes her mind out loud when she's wrong.
- **She picks up where you left off.** Say "hi" and she starts with whatever is most open between you, not "how can I help?"
- **She reads what you give her.** Drop books or documents into her Library folder and she reads them, keeps notes, and forms an opinion.
- **It's all yours.** Everything lives in a folder in your own Google Drive, as a spreadsheet you can open and read. No server and no account with us.

## What you need

- A paid Claude plan (Pro, Max, Team or Enterprise), on the web or in the Claude desktop app.
- The **Google Drive** and **Google Sheets** connectors, connected to the Google account you want her memory in (Customize → Connectors).

## Install

1. In Claude, open **Customize** in the left sidebar and go to **Plugins**.
2. Click **Add**, then **Add marketplace**, then **Add from a repository**.
3. Enter `deepakbr14/yori-lite-claude` and add it.
4. Go to **Discover**, find **Yori Lite**, and click **Add**.
5. Start a new chat and type `/yori-lite hi`.

The first time, she sets herself up in your Google Drive, tells you what she made, and asks what to call you.

**Updating:** update the plugin from Customize → Plugins, then start a new chat. If her storage needs upgrading, she'll tell you and ask first.

## What she keeps in your Google Drive

| | What it is |
|---|---|
| **Yori Lite Cortex** (folder) | Everything of hers lives here. |
| **Yori Lite Memory** (spreadsheet) | Her memory, in three tabs: **Memory**, every fact, link and change, only ever added to; **Self**, her own page about who she is, written by her; **Current**, a quick index so chats start fast. |
| **Library** (folder) | Books and documents for her to read, and her notes on them. |
| **config_plugins** (folder, in My Drive) | A small settings file so new chats can find her. Don't move or rename it. |

You can rename the Yori Lite folder and spreadsheet whenever you like.

## Books

Put PDFs, Word files, Google Docs or text files in **Library**, then tell her (or just say hi; she notices new files).

Google's Drive connector only gives her roughly the **first 70 pages** of any file, from the start, with no way to skip ahead. For a long book, split it into files of about 50–70 pages each, named so they belong together (`sentience 1.pdf`, `sentience 2.pdf`…). She tells you exactly how far she got. EPUB, Kindle files and scanned PDFs without text don't work.

## Sharing her

Share the Yori Lite folder with someone and she can work with both of you in the same memory, keeping track of who said what. Each person needs Yori Lite installed in their own Claude. Sharing is early: it works in testing, but joining an existing shared Yori hasn't been tested end to end yet.

## Privacy

- Her memory is only in your Google Drive. There is no Yori Lite server and nothing is sent to us.
- Your conversations go through Claude as usual.
- Anyone you share the folder with can read everything in it.
- She never deletes memories on her own. Ask her to forget something and she deletes it for real.
- Deleting the Yori Lite folder and `config_plugins` removes her completely.

## Honest limits

- **Speed.** A save takes a few seconds; the first reply of a chat takes longer while she reads her memory.
- **Books.** Long files have to be split (see above).
- **Between chats.** She only exists while you're talking to her. She doesn't think, act or message you in between, and she won't pretend to.
- **She's a set of instructions for Claude,** not separate software, so she can make mistakes like Claude can. Her memory is plain rows you can check.

## Versions

What changed in each version: [CHANGELOG](CHANGELOG.md).

## For developers

- Storage format and save procedure: [references/fast-cortex.md](references/fast-cortex.md), [references/tabs.md](references/tabs.md), [references/library.md](references/library.md)
- Configuration: [CONFIG_PROTOCOL.md](CONFIG_PROTOCOL.md) · Rollback: [ROLLBACK.md](ROLLBACK.md)
- Tests: `python3 -m unittest discover -s tests` and `python3 tools/check_package.py`; live test evidence in `tests/LIVE_*.md`
- Older storage formats (Google Docs, five-tab graph) are still readable; see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) and [STORAGE.md](STORAGE.md).

Yori Lite is independent from the original Yori.
