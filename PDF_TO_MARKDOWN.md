# PDF to Markdown with ChatGPT

(authored by agents unless marked 🧑)

Use this workflow instead of `ocr_all.py`, Marker, and `done_ocr.txt` for each
new root-level PDF. Existing verified Markdown stays authoritative. A nonempty
`<stem>/<stem>.md` file is the completion record.

## prerequisites

Run from the `paper_collection` repository root. Confirm that Chrome is
available and that the installed ChatGPT helper supports PDF attachments:

```sh
pb-browser-cli smoke
pb-chatgpt-prompt-file --help | rg -- '--file'
command -v jq >/dev/null
command -v pdfinfo >/dev/null
```

Stop if any command fails or the helper does not show `--file PATH`.

## convert one PDF

For a root-level `<stem>.pdf`, write `<stem>/<stem>.md`. This is the repository's
existing PDF/Markdown layout. Set `pdf` to the exact root-level filename:

```sh
pdf='TITLE, AUTHORS, VENUE, YEAR.pdf'
paper_dir=${pdf%.pdf}
out="$paper_dir/$(basename "$paper_dir").md"
[[ $pdf == *.pdf && -f $pdf && ! -e $out ]] &&
mkdir -p -- "$paper_dir" &&
pb-chatgpt-prompt-file chatgpt_pdf_to_markdown.prompt.md \
  --effort 'Extra High' \
  --file "$pdf" \
  --output "$out" \
  --answer-wait-s 900 \
  --command-timeout-s 1080 &&
test -s "$out"
```

The helper opens a fresh temporary ChatGPT tab, attaches the PDF, asks for the
conversion, saves the assistant's Markdown response at `--output`, and closes
the tab. Its adjacent `*.private.json` file contains private diagnostics and is
ignored by Git.

## handle an incomplete command

Do not submit again after a nonzero exit until you inspect the diagnostic; the
original request may still be running:

```sh
diag="$out.private.json"
jq '{condition, job_status, job_handle, submitted, completion}' "$diag"
```

If the command printed a `resume_handle` and `job_status` is
`submission_unknown`, `submitted`, or `pending`, resume it without
resubmitting. Use a new diagnostic filename:

```sh
handle='pbtab_REPLACE_WITH_PRINTED_HANDLE'
pb-chatgpt-prompt-file \
  --resume "$handle" \
  --output "$out" \
  --diagnostic-output "$out.resume-1.private.json" \
  --command-timeout-s 1080 &&
test -s "$out"
```

Start a new submission only after the diagnostic shows a terminal or
precondition failure and no resumable job. Rerun the conversion command with a
new `--diagnostic-output "$out.retry-1.private.json"`; increment the retry
number if that file exists.

## verify and commit

The command and `test -s` must both succeed. Treat a response that says it could
not read the attachment as failure. `[unreadable]` is not automatically a
failure: compare it with the source and replace it only when the source is
clear.

Get the source page count, then confirm every PDF page's substantive content is
represented in the Markdown:

```sh
pages=$(pdfinfo -- "$pdf" | awk '$1 == "Pages:" {print $2}')
test "$pages" -gt 0
printf 'verify Markdown coverage for all %s source pages\n' "$pages"
```

Compare the first, middle, and final pages in detail. Also check the title and
authors, section order, tables, equations, figure captions, footnotes, and
references. Fix only confirmed conversion errors. Commit the verified Markdown,
not the PDF or private diagnostic.

Before committing, confirm that no PDF is staged:

```sh
git diff --cached --name-only -- '*.pdf'
```

The command must print nothing.
