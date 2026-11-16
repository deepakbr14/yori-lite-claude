# 0.4.6 live evidence — Library (2026-11-16)

Provenance: fresh Claude sessions linked to Claude Desktop, real Google Drive, Docs and Sheets connectors, account enupgames@gmail.com. Disposable Cortex folder `1xB3TL_sP6mNNNYoG3gJByqHwZ5eil9gH` with a `Library` folder holding two short made-up documents. The user's own Cortex and Library were not read or written.

## Connector facts
- `read_file_content` takes a file ID only: no page, chapter or offset. Its description says content may be incomplete for very large files.
- From the user's own chat with a real 13 MB, 240-page PDF: about 125,000 characters came back (roughly the first 70 pages), always from the start. One book, not a measured limit.
- `download_file_content` returns the whole file as base64; no range.
- Supported for reading: Google Docs, PDF, Word, text. Not EPUB.

## Run 1 — memory sheet missing (it had been deleted)
- "hi": said plainly that the memory sheet returned permission denied and that she would not pretend to remember; reported the one Library file and offered to read it.
- "yes go ahead": read the document in that turn, created `Yori notes — The Two-Minute Door` in the Library, gave her own take (agreed with the argument, did not trust the unsourced numbers), and said the memory rows had not saved.
- "should i put a text tutorial at the start": answered no, cited chapter 2, searched the Library (`fullText contains 'tutorial'` scoped to the folder), kept "the essay argues" apart from "I agree".

## Run 2 — working memory sheet, seeded with the book row from run 1
- "hi": found the Library folder, saved the `library` row, mentioned only the unread file (skipped the book already read and her own notes document), told the person once that dropped files get read and that long ones work best in parts of about 50 pages, then led with her own view from the earlier book.
- "sure, read it": read it in the turn, created the notes document, saved in one append: the book row with exact coverage and notes ID, her view + edge, and an open question linked to the project. Reply gave the two claims by section, where she agrees and half agrees, and asked the question.

## Not tested live
- A cut-off file inside these runs (the behaviour was seen in the user's own chat, before this version).
- Adding to an existing notes document when a second part arrives (`update_doc` insertText); only replaceAllText was exercised.
- Timing.
