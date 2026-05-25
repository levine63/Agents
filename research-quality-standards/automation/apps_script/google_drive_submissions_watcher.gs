/**
 * Project: research-quality-standards
 * File: automation/apps_script/google_drive_submissions_watcher.gs
 * Author: Codex
 * Created: 2026-05-13
 * Last updated: 2026-05-16
 *
 * Purpose:
 * Poll a Google Drive submissions folder, detect new files, log them to a
 * tracking Sheet, and generate per-submission review output Docs using OpenAI.
 *
 * Inputs:
 * - Script Properties:
 *   - SUBMISSIONS_FOLDER_ID
 *   - TRACKING_SHEET_ID
 *   - OPENAI_API_KEY
 *   - TRACKING_SHEET_NAME=Intake Log
 *   - OPENAI_MODEL=gpt-5-mini
 *   - INCLUDE_SUBFOLDERS=true
 *   - EXCLUDED_FOLDER_NAMES=99_Admin
 *   - REVIEW_OUTPUT_FOLDER_NAME=Review Outputs
 *   - CONVERTED_SOURCE_FOLDER_NAME=Converted Review Sources
 *   - KEEP_CONVERTED_SOURCES=true
 *   - EXCLUDED_FILE_IDS=comma,separated,file,ids
 *   - STANDARDS_BASE_URL=https://raw.githubusercontent.com/<owner>/<repo>/<branch>
 *   - STANDARDS_CACHE_MINUTES=20
 * - Drive submissions in supported formats:
 *   - native Google Docs
 *   - native Google Sheets
 *   - Word .docx
 *   - Excel .xlsx
 *   - PDF
 *
 * Outputs / side effects:
 * - Reads from the configured submissions folder and optional subfolders.
 * - Creates or updates rows in the tracking Sheet.
 * - Creates review-output Google Docs under the admin output folder.
 * - Converts .docx and .xlsx files into temporary Google-native review sources.
 * - Sends review requests to the OpenAI Responses API.
 * - Optionally fetches review standards from a GitHub raw-content URL.
 * - Optionally trashes converted temporary review-source files after review.
 *
 * Assumptions:
 * - The Drive folder structure follows the submissions workflow conventions.
 * - The Apps Script project has permission to read/write the target Drive and Sheet.
 * - OpenAI API access is available through the configured key.
 * - Folder-based genre detection is helpful but imperfect.
 *
 * Environment / dependencies:
 * - Google Apps Script, V8 runtime.
 * - Advanced Drive service enabled in the Apps Script project.
 * - External services: Google Drive, Google Docs, Google Sheets, OpenAI Responses API.
 *
 * How to run:
 * - Configure Script Properties.
 * - Add a time-based Apps Script trigger for scanSubmissionFolders().
 * - For deployment from local source, run clasp from the repo root.
 *
 * Notes:
 * - Long documents and spreadsheets are compressed into structured review inputs.
 * - PDFs are sent directly to the Responses API as file input.
 * - Side effects are intentional and should stay aligned with this header.
 */

var LOG_COLUMNS_ = [
  "logged_at",
  "file_id",
  "file_name",
  "genre_guess",
  "mime_type",
  "folder_name",
  "file_url",
  "status",
  "review_doc_url",
  "review_state",
  "notes"
];

var GOOGLE_DOC_MIME_ = "application/vnd.google-apps.document";
var GOOGLE_SHEET_MIME_ = "application/vnd.google-apps.spreadsheet";
var DOCX_MIME_ = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
var XLSX_MIME_ = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
var PDF_MIME_ = "application/pdf";
var OPENAI_RESPONSES_URL_ = "https://api.openai.com/v1/responses";

var MAX_DOC_REVIEW_CHARS_ = 26000;
var MAX_DOC_SECTION_CHARS_ = 1200;
var MAX_DOC_OPENING_CHARS_ = 4500;
var MAX_DOC_CLOSING_CHARS_ = 3000;
var MAX_DOC_HEADINGS_ = 18;

var MAX_SHEET_SUMMARY_CHARS_ = 20000;
var MAX_SHEET_SAMPLE_ROWS_ = 12;
var MAX_SHEET_TAIL_ROWS_ = 6;
var MAX_SHEET_SAMPLE_COLS_ = 12;
var MAX_SHEET_COUNT_ = 12;

function getConfig_() {
  var props = PropertiesService.getScriptProperties();
  return {
    submissionsFolderId: props.getProperty("SUBMISSIONS_FOLDER_ID"),
    trackingSheetId: props.getProperty("TRACKING_SHEET_ID"),
    trackingSheetName: props.getProperty("TRACKING_SHEET_NAME") || "Intake Log",
    includeSubfolders: (props.getProperty("INCLUDE_SUBFOLDERS") || "true").toLowerCase() === "true",
    excludedFolderNames: parseCsvProperty_(
      props.getProperty("EXCLUDED_FOLDER_NAMES") || "99_Admin"
    ),
    reviewOutputFolderName: props.getProperty("REVIEW_OUTPUT_FOLDER_NAME") || "Review Outputs",
    convertedSourceFolderName: props.getProperty("CONVERTED_SOURCE_FOLDER_NAME") || "Converted Review Sources",
    keepConvertedSources: (props.getProperty("KEEP_CONVERTED_SOURCES") || "true").toLowerCase() === "true",
    excludedFileIds: parseCsvProperty_(props.getProperty("EXCLUDED_FILE_IDS") || ""),
    openAiApiKey: props.getProperty("OPENAI_API_KEY"),
    openAiModel: props.getProperty("OPENAI_MODEL") || "gpt-5-mini",
    standardsBaseUrl: trimTrailingSlash_(props.getProperty("STANDARDS_BASE_URL") || ""),
    standardsCacheMinutes: parseInt(props.getProperty("STANDARDS_CACHE_MINUTES") || "20", 10)
  };
}

function scanSubmissionFolders() {
  var config = getConfig_();
  validateConfig_(config);

  var root = DriveApp.getFolderById(config.submissionsFolderId);
  var sheet = getOrCreateTrackingSheet_(config.trackingSheetId, config.trackingSheetName);
  var seen = getSeenFileIds_(sheet);
  var reviewOutputFolder = getOrCreateReviewOutputFolder_(root, config.reviewOutputFolderName);
  var convertedSourceFolder = getOrCreateConvertedSourceFolder_(root, config.convertedSourceFolderName);
  var rows = [];

  collectFolderFiles_(root, config, reviewOutputFolder, convertedSourceFolder, rows, seen);

  if (rows.length > 0) {
    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
}

function validateConfig_(config) {
  var missing = [];
  if (!config.submissionsFolderId) missing.push("SUBMISSIONS_FOLDER_ID");
  if (!config.trackingSheetId) missing.push("TRACKING_SHEET_ID");
  if (!config.openAiApiKey) missing.push("OPENAI_API_KEY");
  if (typeof Drive === "undefined") {
    missing.push("Advanced Drive service not enabled");
  }

  if (missing.length > 0) {
    throw new Error("Missing required setup: " + missing.join(", "));
  }
}

function collectFolderFiles_(folder, config, reviewOutputFolder, convertedSourceFolder, rows, seen) {
  if (isExcludedFolder_(folder, config)) {
    return;
  }

  var files = folder.getFiles();
  while (files.hasNext()) {
    var file = files.next();
    var fileId = file.getId();
    if (seen[fileId] || isExcludedFile_(file, config)) {
      continue;
    }

    var genre = detectGenreFromPath_(folder.getName());
    var reviewDoc = createReviewOutputDoc_(reviewOutputFolder, file, folder, genre);
    var reviewResult = reviewSubmission_(
      file,
      folder,
      genre,
      reviewDoc,
      config,
      convertedSourceFolder
    );

    rows.push([
      new Date(),
      fileId,
      file.getName(),
      genre,
      file.getMimeType(),
      folder.getName(),
      file.getUrl(),
      reviewResult.status,
      reviewDoc.getUrl(),
      reviewResult.reviewState,
      reviewResult.notes
    ]);
  }

  if (!config.includeSubfolders) {
    return;
  }

  var folders = folder.getFolders();
  while (folders.hasNext()) {
    collectFolderFiles_(folders.next(), config, reviewOutputFolder, convertedSourceFolder, rows, seen);
  }
}

function reviewSubmission_(file, sourceFolder, genre, reviewDoc, config, convertedSourceFolder) {
  var formatInfo = getFormatInfo_(file.getMimeType());

  if (!formatInfo.supported) {
    appendUnsupportedFormatNote_(reviewDoc, file, sourceFolder, genre, formatInfo);
    return {
      status: "QUEUED",
      reviewState: "UNSUPPORTED_FORMAT",
      notes: formatInfo.message
    };
  }

  var reviewSource = null;
  try {
    reviewSource = prepareReviewSource_(file, formatInfo, convertedSourceFolder, config.keepConvertedSources);
    var extracted = reviewSource.extractionKind === "pdf_file"
      ? { content: "", notice: "PDF reviewed directly as a file input." }
      : extractArtifactText_(reviewSource);
    var reviewText = callOpenAiReview_(file, genre, reviewSource, extracted, config);
    writeCompletedReview_(reviewDoc, file, sourceFolder, genre, reviewSource, extracted.notice, reviewText);
    cleanupConvertedSource_(reviewSource, config.keepConvertedSources);
    return {
      status: "REVIEWED",
      reviewState: reviewSource.converted ? "OPENAI_REVIEWED_CONVERTED" : "OPENAI_REVIEWED",
      notes: compactNotes_(reviewSource.conversionNotice, extracted.notice)
    };
  } catch (err) {
    appendReviewFailure_(reviewDoc, file, sourceFolder, genre, reviewSource || formatInfo, err);
    cleanupConvertedSource_(reviewSource, true);
    return {
      status: "REVIEW_FAILED",
      reviewState: "OPENAI_ERROR",
      notes: truncateForCell_(String(err && err.message ? err.message : err), 400)
    };
  }
}

function getFormatInfo_(mimeType) {
  if (mimeType === GOOGLE_DOC_MIME_) {
    return {
      supported: true,
      formatKey: "google_doc",
      formatLabel: "Google Doc",
      formatStandard: getFormatStandard_("google_doc"),
      extractionKind: "google_doc",
      requiresConversion: false
    };
  }

  if (mimeType === GOOGLE_SHEET_MIME_) {
    return {
      supported: true,
      formatKey: "google_sheet",
      formatLabel: "Google Sheet",
      formatStandard: getFormatStandard_("google_sheet"),
      extractionKind: "google_sheet",
      requiresConversion: false
    };
  }

  if (mimeType === MimeType.MICROSOFT_WORD || mimeType === DOCX_MIME_) {
    return {
      supported: true,
      formatKey: "docx",
      formatLabel: "Word DOCX",
      formatStandard: getFormatStandard_("docx"),
      extractionKind: "google_doc",
      requiresConversion: true,
      conversionTargetMimeType: GOOGLE_DOC_MIME_
    };
  }

  if (mimeType === MimeType.MICROSOFT_EXCEL || mimeType === XLSX_MIME_) {
    return {
      supported: true,
      formatKey: "xlsx",
      formatLabel: "Excel XLSX",
      formatStandard: getFormatStandard_("xlsx"),
      extractionKind: "google_sheet",
      requiresConversion: true,
      conversionTargetMimeType: GOOGLE_SHEET_MIME_
    };
  }

  if (mimeType === MimeType.PDF || mimeType === PDF_MIME_) {
    return {
      supported: true,
      formatKey: "pdf",
      formatLabel: "PDF",
      formatStandard: getFormatStandard_("pdf"),
      extractionKind: "pdf_file",
      requiresConversion: false
    };
  }

  return {
    supported: false,
    formatKey: "unknown",
    formatLabel: mimeType,
    message: "This version supports native Google Docs, native Google Sheets, Word .docx, Excel .xlsx, and PDF files."
  };
}

function prepareReviewSource_(file, formatInfo, convertedSourceFolder, keepConvertedSources) {
  if (!formatInfo.requiresConversion) {
    return {
      file: file,
      converted: false,
      formatKey: formatInfo.formatKey,
      sourceFormatLabel: formatInfo.formatLabel,
      reviewFormatLabel: formatInfo.formatLabel,
      extractionKind: formatInfo.extractionKind,
      formatStandard: formatInfo.formatStandard,
      cleanupFileId: "",
      conversionNotice: ""
    };
  }

  var convertedName = buildConvertedSourceName_(file.getName(), formatInfo);
  var metadata = {
    name: convertedName,
    mimeType: formatInfo.conversionTargetMimeType,
    parents: [convertedSourceFolder.getId()]
  };

  var converted = Drive.Files.create(metadata, file.getBlob(), { fields: "id,name,mimeType,parents" });
  var convertedFile = DriveApp.getFileById(converted.id);
  tryRemoveFromRoot_(convertedFile);

  return {
    file: convertedFile,
    converted: true,
    formatKey: formatInfo.formatKey,
    sourceFormatLabel: formatInfo.formatLabel,
    reviewFormatLabel: convertedFile.getMimeType() === GOOGLE_DOC_MIME_ ? "Converted Google Doc" : "Converted Google Sheet",
    extractionKind: formatInfo.extractionKind,
    formatStandard: formatInfo.formatStandard,
    cleanupFileId: converted.id,
    conversionNotice: "Original " + formatInfo.formatLabel + " was converted to " +
      (convertedFile.getMimeType() === GOOGLE_DOC_MIME_ ? "Google Doc" : "Google Sheet") +
      " for review."
  };
}

function cleanupConvertedSource_(reviewSource, keepConvertedSources) {
  if (!reviewSource || !reviewSource.converted || keepConvertedSources) {
    return;
  }

  try {
    DriveApp.getFileById(reviewSource.cleanupFileId).setTrashed(true);
  } catch (err) {
    // Non-fatal cleanup failure.
  }
}

function extractArtifactText_(reviewSource) {
  if (reviewSource.extractionKind === "google_doc") {
    return extractStructuredDocumentText_(reviewSource.file.getId());
  }

  if (reviewSource.extractionKind === "google_sheet") {
    return extractStructuredSpreadsheetText_(reviewSource.file.getId());
  }

  if (reviewSource.extractionKind === "pdf_file") {
    return {
      content: "",
      notice: "PDF reviewed directly as a file input."
    };
  }

  throw new Error("Unsupported extraction kind: " + reviewSource.extractionKind);
}

function extractStructuredDocumentText_(documentId) {
  var doc = DocumentApp.openById(documentId);
  var body = doc.getBody();
  var fullText = body.getText() || "";

  if (fullText.length <= MAX_DOC_REVIEW_CHARS_) {
    return {
      content: fullText,
      notice: ""
    };
  }

  var sections = collectDocumentSections_(body.getParagraphs());
  var parts = [];

  parts.push("[Structured extraction for long document]");
  parts.push("");
  parts.push("Opening excerpt:");
  parts.push(fullText.slice(0, MAX_DOC_OPENING_CHARS_));
  parts.push("");
  parts.push("Section excerpts:");

  var sectionCount = Math.min(sections.length, MAX_DOC_HEADINGS_);
  for (var i = 0; i < sectionCount; i++) {
    var section = sections[i];
    parts.push("## " + section.heading);
    parts.push(trimBlock_(section.text, MAX_DOC_SECTION_CHARS_));
    parts.push("");
  }

  parts.push("Closing excerpt:");
  parts.push(fullText.slice(Math.max(0, fullText.length - MAX_DOC_CLOSING_CHARS_)));

  return {
    content: trimToLimit_(parts.join("\n"), MAX_DOC_REVIEW_CHARS_),
    notice: "Long document reviewed using structured extraction with opening, section, and closing excerpts. Full length: " + fullText.length + " characters."
  };
}

function collectDocumentSections_(paragraphs) {
  var sections = [];
  var currentHeading = "Front matter";
  var currentParts = [];

  for (var i = 0; i < paragraphs.length; i++) {
    var paragraph = paragraphs[i];
    var text = String(paragraph.getText() || "").trim();
    if (!text) {
      continue;
    }

    if (isHeadingParagraph_(paragraph)) {
      if (currentParts.length > 0) {
        sections.push({
          heading: currentHeading,
          text: currentParts.join("\n")
        });
      }
      currentHeading = text;
      currentParts = [];
    } else {
      currentParts.push(text);
    }
  }

  if (currentParts.length > 0) {
    sections.push({
      heading: currentHeading,
      text: currentParts.join("\n")
    });
  }

  if (sections.length === 0) {
    sections.push({
      heading: "Document body",
      text: ""
    });
  }

  return sections;
}

function isHeadingParagraph_(paragraph) {
  var heading = paragraph.getHeading();
  return heading && heading !== DocumentApp.ParagraphHeading.NORMAL;
}

function extractStructuredSpreadsheetText_(spreadsheetId) {
  var summary = summarizeSpreadsheet_(spreadsheetId);
  return {
    content: trimToLimit_(summary, MAX_SHEET_SUMMARY_CHARS_),
    notice: buildSheetSummaryNotice_(summary)
  };
}

function summarizeSpreadsheet_(spreadsheetId) {
  var ss = SpreadsheetApp.openById(spreadsheetId);
  var sheets = ss.getSheets();
  var parts = [];
  var maxSheets = Math.min(sheets.length, MAX_SHEET_COUNT_);

  for (var i = 0; i < maxSheets; i++) {
    var sheet = sheets[i];
    var range = sheet.getDataRange();
    var values = range.getDisplayValues();
    var formulas = range.getFormulas();
    var rowCount = values.length;
    var colCount = rowCount > 0 ? values[0].length : 0;

    parts.push("Sheet: " + sheet.getName());
    parts.push("Rows: " + rowCount + ", Columns: " + colCount);
    parts.push("Non-empty formulas in sampled area: " + countSampledFormulas_(formulas));

    if (rowCount === 0 || colCount === 0) {
      parts.push("[Sheet is empty]");
      parts.push("");
      continue;
    }

    parts.push("Top sample:");
    appendSheetRows_(parts, values, 0, Math.min(rowCount, MAX_SHEET_SAMPLE_ROWS_));

    if (rowCount > MAX_SHEET_SAMPLE_ROWS_ + MAX_SHEET_TAIL_ROWS_) {
      parts.push("[Middle rows omitted]");
      parts.push("Bottom sample:");
      appendSheetRows_(parts, values, rowCount - MAX_SHEET_TAIL_ROWS_, rowCount);
    }

    parts.push("");
  }

  if (sheets.length > maxSheets) {
    parts.push("[Additional sheets omitted]");
  }

  return parts.join("\n");
}

function appendSheetRows_(parts, values, startRow, endRow) {
  for (var r = startRow; r < endRow; r++) {
    var row = [];
    var maxCols = Math.min(values[r].length, MAX_SHEET_SAMPLE_COLS_);
    for (var c = 0; c < maxCols; c++) {
      row.push(values[r][c]);
    }
    parts.push(row.join(" | "));
  }
}

function countSampledFormulas_(formulas) {
  var count = 0;
  var maxRows = Math.min(formulas.length, MAX_SHEET_SAMPLE_ROWS_);
  for (var r = 0; r < maxRows; r++) {
    var maxCols = Math.min(formulas[r].length, MAX_SHEET_SAMPLE_COLS_);
    for (var c = 0; c < maxCols; c++) {
      if (formulas[r][c]) {
        count++;
      }
    }
  }
  return count;
}

function buildSheetSummaryNotice_(summary) {
  if (summary.length <= MAX_SHEET_SUMMARY_CHARS_) {
    return "Spreadsheet reviewed from a structured tab summary rather than full cell export.";
  }
  return "Spreadsheet reviewed from a structured tab summary that was compressed to fit the review budget.";
}

function callOpenAiReview_(file, genre, reviewSource, extracted, config) {
  var input = buildReviewInput_(file, genre, reviewSource, extracted, config);
  var payload = {
    model: config.openAiModel,
    instructions: buildReviewerInstructions_(),
    input: input,
    reasoning: { effort: "low" }
  };

  var response = UrlFetchApp.fetch(OPENAI_RESPONSES_URL_, {
    method: "post",
    contentType: "application/json",
    headers: {
      Authorization: "Bearer " + config.openAiApiKey
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  var statusCode = response.getResponseCode();
  var bodyText = response.getContentText();
  if (statusCode < 200 || statusCode >= 300) {
    throw new Error("OpenAI API error " + statusCode + ": " + bodyText);
  }

  var parsed = JSON.parse(bodyText);
  var reviewText = extractResponseText_(parsed);
  if (!reviewText) {
    throw new Error("OpenAI response did not contain review text.");
  }
  return reviewText;
}

function buildReviewerInstructions_() {
  return [
    "You are Codex acting as a work-product reviewer.",
    "Apply the provided genre and format standards to the artifact content.",
    "Be direct, specific, and evidence-based.",
    "Do not invent missing content; label it missing.",
    "Return plain text with these sections in this order:",
    "Overall assessment",
    "Major issues",
    "Required fixes",
    "Suggested improvements",
    "Residual risks",
    "Disposition"
  ].join(" ");
}

function buildReviewInput_(file, genre, reviewSource, extracted, config) {
  if (reviewSource.extractionKind === "pdf_file") {
    return buildPdfReviewInput_(file, genre, reviewSource, extracted, config);
  }

  var genreStandard = getGenreStandard_(genre, config);
  var formatStandard = getFormatStandard_(reviewSource.formatKey || deriveFormatKeyFromReviewSource_(reviewSource), config);
  var lines = [
    "Artifact name: " + file.getName(),
    "Genre: " + genre,
    "Source format: " + reviewSource.sourceFormatLabel,
    "Review working format: " + reviewSource.reviewFormatLabel,
    "",
    "Genre standard:",
    genreStandard,
    "",
    "Format standard:",
    formatStandard,
    "",
    "Artifact content:",
    extracted.content
  ];

  var notes = compactNotes_(reviewSource.conversionNotice, extracted.notice);
  if (notes) {
    lines.splice(5, 0, "Content notice: " + notes, "");
  }

  return lines.join("\n");
}

function buildPdfReviewInput_(file, genre, reviewSource, extracted, config) {
  var genreStandard = getGenreStandard_(genre, config);
  var formatStandard = getFormatStandard_(
    reviewSource.formatKey || deriveFormatKeyFromReviewSource_(reviewSource),
    config
  );
  var notes = compactNotes_(reviewSource.conversionNotice, extracted.notice);
  var promptLines = [
    "Artifact name: " + file.getName(),
    "Genre: " + genre,
    "Source format: " + reviewSource.sourceFormatLabel,
    "Review working format: " + reviewSource.reviewFormatLabel,
    "Artifact content is attached as a PDF file input. Review the full PDF rather than assuming a text-only export.",
    "",
    "Genre standard:",
    genreStandard,
    "",
    "Format standard:",
    formatStandard
  ];

  if (notes) {
    promptLines.push("", "Content notice: " + notes);
  }

  return [
    {
      role: "user",
      content: [
        {
          type: "input_file",
          filename: file.getName(),
          file_data: Utilities.base64Encode(reviewSource.file.getBlob().getBytes())
        },
        {
          type: "input_text",
          text: promptLines.join("\n")
        }
      ]
    }
  ];
}

function writeCompletedReview_(reviewDoc, file, sourceFolder, genre, reviewSource, notice, reviewText) {
  var doc = DocumentApp.openById(reviewDoc.getId());
  var body = doc.getBody();
  body.clear();

  body.appendParagraph("Codex Review Output").setHeading(DocumentApp.ParagraphHeading.HEADING1);
  body.appendParagraph("");
  body.appendParagraph("Submission metadata").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Source file: " + file.getName());
  body.appendParagraph("Source folder: " + sourceFolder.getName());
  body.appendParagraph("Genre: " + genre);
  body.appendParagraph("Source format: " + reviewSource.sourceFormatLabel);
  body.appendParagraph("Review working format: " + reviewSource.reviewFormatLabel);
  body.appendParagraph("Submission URL: " + file.getUrl());
  body.appendParagraph("Review date: " + new Date());

  var notes = compactNotes_(reviewSource.conversionNotice, notice);
  if (notes) {
    body.appendParagraph("Extraction note: " + notes);
  }

  body.appendParagraph("");
  body.appendParagraph("Review").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  appendMultilineText_(body, reviewText);
  doc.saveAndClose();
}

function appendUnsupportedFormatNote_(reviewDoc, file, sourceFolder, genre, formatInfo) {
  var doc = DocumentApp.openById(reviewDoc.getId());
  var body = doc.getBody();
  body.clear();

  body.appendParagraph("Codex Review Output").setHeading(DocumentApp.ParagraphHeading.HEADING1);
  body.appendParagraph("");
  body.appendParagraph("Submission metadata").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Source file: " + file.getName());
  body.appendParagraph("Source folder: " + sourceFolder.getName());
  body.appendParagraph("Genre: " + genre);
  body.appendParagraph("Format: " + formatInfo.formatLabel);
  body.appendParagraph("Submission URL: " + file.getUrl());
  body.appendParagraph("");
  body.appendParagraph("Review status").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph(formatInfo.message);
  body.appendParagraph("");
  body.appendParagraph("Next step").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Keep this submission queued until the corresponding ingestion path is implemented.");
  doc.saveAndClose();
}

function appendReviewFailure_(reviewDoc, file, sourceFolder, genre, reviewContext, err) {
  var doc = DocumentApp.openById(reviewDoc.getId());
  var body = doc.getBody();
  body.clear();

  body.appendParagraph("Codex Review Output").setHeading(DocumentApp.ParagraphHeading.HEADING1);
  body.appendParagraph("");
  body.appendParagraph("Submission metadata").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Source file: " + file.getName());
  body.appendParagraph("Source folder: " + sourceFolder.getName());
  body.appendParagraph("Genre: " + genre);
  body.appendParagraph("Format: " + (reviewContext.sourceFormatLabel || reviewContext.formatLabel));
  body.appendParagraph("Submission URL: " + file.getUrl());
  body.appendParagraph("");
  body.appendParagraph("Review failure").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph(String(err && err.message ? err.message : err));
  doc.saveAndClose();
}

function appendMultilineText_(body, text) {
  var lines = String(text || "").split("\n");
  for (var i = 0; i < lines.length; i++) {
    body.appendParagraph(lines[i]);
  }
}

function getOrCreateTrackingSheet_(spreadsheetId, sheetName) {
  var ss = SpreadsheetApp.openById(spreadsheetId);
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }

  ensureHeader_(sheet, LOG_COLUMNS_);
  return sheet;
}

function ensureHeader_(sheet, headers) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    return;
  }

  var existingHeaders = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
  var needsUpdate = false;
  for (var i = 0; i < headers.length; i++) {
    if (existingHeaders[i] !== headers[i]) {
      needsUpdate = true;
      break;
    }
  }

  if (needsUpdate) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }
}

function getSeenFileIds_(sheet) {
  var values = sheet.getDataRange().getValues();
  var seen = {};
  for (var i = 1; i < values.length; i++) {
    var fileId = values[i][1];
    if (fileId) {
      seen[fileId] = true;
    }
  }
  return seen;
}

function getOrCreateReviewOutputFolder_(rootFolder, folderName) {
  var adminFolder = getOrCreateSubfolder_(rootFolder, "99_Admin");
  return getOrCreateSubfolder_(adminFolder, folderName);
}

function getOrCreateConvertedSourceFolder_(rootFolder, folderName) {
  var adminFolder = getOrCreateSubfolder_(rootFolder, "99_Admin");
  return getOrCreateSubfolder_(adminFolder, folderName);
}

function getOrCreateSubfolder_(parentFolder, folderName) {
  var folders = parentFolder.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return parentFolder.createFolder(folderName);
}

function createReviewOutputDoc_(reviewOutputFolder, file, sourceFolder, genre) {
  var title = buildReviewDocTitle_(file.getName());
  var doc = DocumentApp.create(title);
  var body = doc.getBody();

  body.appendParagraph("Codex Review Output").setHeading(DocumentApp.ParagraphHeading.HEADING1);
  body.appendParagraph("");
  body.appendParagraph("Submission metadata").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Source file: " + file.getName());
  body.appendParagraph("Source folder: " + sourceFolder.getName());
  body.appendParagraph("Genre guess: " + genre);
  body.appendParagraph("Submission URL: " + file.getUrl());
  body.appendParagraph("Logged at: " + new Date());
  body.appendParagraph("");
  body.appendParagraph("Review status").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph("Review queued.");

  doc.saveAndClose();

  var createdFile = DriveApp.getFileById(doc.getId());
  reviewOutputFolder.addFile(createdFile);
  tryRemoveFromRoot_(createdFile);
  return createdFile;
}

function tryRemoveFromRoot_(file) {
  try {
    DriveApp.getRootFolder().removeFile(file);
  } catch (err) {
    // Some Drive setups do not expose the root in a removable way.
  }
}

function buildReviewDocTitle_(fileName) {
  return "Review - " + fileName;
}

function buildConvertedSourceName_(fileName, formatInfo) {
  return "Converted for review - " + formatInfo.formatLabel + " - " + fileName;
}

function isExcludedFolder_(folder, config) {
  return config.excludedFolderNames.indexOf(folder.getName()) !== -1;
}

function isExcludedFile_(file, config) {
  return config.excludedFileIds.indexOf(file.getId()) !== -1;
}

function parseCsvProperty_(value) {
  return String(value || "")
    .split(",")
    .map(function(part) {
      return String(part || "").trim();
    })
    .filter(function(part) {
      return part.length > 0;
    });
}

function trimToLimit_(text, limit) {
  var value = String(text || "");
  if (value.length <= limit) {
    return value;
  }
  return value.slice(0, limit) + "\n\n[Compressed to fit review budget]";
}

function trimBlock_(text, limit) {
  var value = String(text || "");
  if (value.length <= limit) {
    return value;
  }
  return value.slice(0, limit) + "...";
}

function truncateForCell_(text, limit) {
  var value = String(text || "");
  if (value.length <= limit) {
    return value;
  }
  return value.slice(0, limit);
}

function compactNotes_() {
  var notes = [];
  for (var i = 0; i < arguments.length; i++) {
    var value = String(arguments[i] || "").trim();
    if (value) {
      notes.push(value);
    }
  }
  return notes.join(" ");
}

function trimTrailingSlash_(value) {
  return String(value || "").replace(/\/+$/, "");
}

function extractResponseText_(parsed) {
  if (!parsed) {
    return "";
  }

  if (parsed.output_text) {
    return parsed.output_text;
  }

  var output = parsed.output || [];
  var parts = [];

  for (var i = 0; i < output.length; i++) {
    var item = output[i];
    if (item.type !== "message" || !item.content) {
      continue;
    }
    for (var j = 0; j < item.content.length; j++) {
      var content = item.content[j];
      if (content.type === "output_text" && content.text) {
        parts.push(content.text);
      }
    }
  }

  return parts.join("\n\n").trim();
}

function detectGenreFromPath_(folderName) {
  var lower = String(folderName || "").toLowerCase();
  if (lower.indexOf("manuscript") !== -1) return "academic_paper";
  if (lower.indexOf("interview") !== -1) return "interview";
  if (lower.indexOf("statistical") !== -1) return "statistical_results";
  if (lower.indexOf("slide") !== -1) return "presentation";
  if (lower.indexOf("weekly") !== -1) return "weekly_goals";
  if (lower.indexOf("code") !== -1) return "code_export";
  return "unknown";
}

function getGenreStandard_(genre, config) {
  var fallback = getFallbackGenreStandard_(genre);
  var pathMap = {
    academic_paper: "standards/genres/academic_paper/standards.md",
    interview: "standards/genres/interview/standards.md",
    statistical_results: "standards/genres/statistical_results/standards.md",
    presentation: "standards/genres/presentation/standards.md",
    weekly_goals: "standards/genres/weekly_goals/standards.md",
    unknown: ""
  };
  return fetchStandardWithFallback_(config, "genre", genre, pathMap[genre] || "", fallback);
}

function getFallbackGenreStandard_(genre) {
  var standards = {
    academic_paper: [
      "- State the research question, main claim, and contribution clearly.",
      "- Claims should match the evidence provided.",
      "- Note missing citations, unsupported claims, or weak structure.",
      "- Identify missing context, methods, or limitations where they block understanding."
    ].join("\n"),
    interview: [
      "- Preserve metadata, speaker clarity, and separation of quotes from interpretation.",
      "- Flag missing context, ambiguous references, and weak evidence anchoring.",
      "- Look for pseudonymization or privacy risks when relevant."
    ].join("\n"),
    statistical_results: [
      "- Check that results are interpretable, labeled, and traceable.",
      "- Flag missing sample definitions, missing units, unlabeled tables, or claims that overreach the displayed evidence.",
      "- Focus on whether the artifact supports sound interpretation and review."
    ].join("\n"),
    presentation: [
      "- Titles should communicate purpose or takeaway.",
      "- Slides should prioritize clarity, legibility, and evidence integrity over decoration.",
      "- Flag stale statistics, overcrowding, or unclear visuals."
    ].join("\n"),
    weekly_goals: [
      "- Tasks should tie to a parent goal, produce a visible artifact, and have a definition of done.",
      "- Flag vague deliverables, hidden blockers, unrealistic scope, or repeated carryover without explanation."
    ].join("\n"),
    code_export: [
      "- Focus on reproducibility, clarity, and whether the artifact is reviewable in its current submitted form."
    ].join("\n"),
    unknown: [
      "- Identify the most likely artifact type.",
      "- Focus on clarity, completeness, obvious risks, and whether the submission is reviewable."
    ].join("\n")
  };

  return standards[genre] || standards.unknown;
}

function getFormatStandard_(formatKey, config) {
  var fallback = getFallbackFormatStandard_(formatKey);
  var pathMap = {
    google_doc: "standards/formats/docx/standards.md",
    google_sheet: "standards/formats/xlsx/standards.md",
    docx: "standards/formats/docx/standards.md",
    xlsx: "standards/formats/xlsx/standards.md",
    pdf: "standards/formats/pdf/standards.md"
  };
  return fetchStandardWithFallback_(config, "format", formatKey, pathMap[formatKey] || "", fallback);
}

function getFallbackFormatStandard_(formatKey) {
  var standards = {
    google_doc: [
      "- Treat the document as a structured writing artifact, not just plain text.",
      "- Prioritize scoped, content-preserving review rather than stylistic rewriting.",
      "- Flag missing headings, weak structure, broken references, or unclear prose that blocks use."
    ].join("\n"),
    google_sheet: [
      "- Treat the sheet as a computational and data artifact.",
      "- Flag ambiguous tabs, hidden assumptions, unlabeled columns, mixed raw and output regions, and formulas or layouts that are hard to audit.",
      "- Focus on whether a stranger could understand and safely reuse the workbook."
    ].join("\n"),
    docx: [
      "- Treat the document as a structured Word artifact, not just plain text.",
      "- Preserve document integrity, citations, references, section logic, and layout-sensitive meaning.",
      "- Flag missing structure, weak rendering assumptions, or content that depends on hidden formatting not visible in the converted text."
    ].join("\n"),
    xlsx: [
      "- Treat the workbook as a computational and data artifact.",
      "- Flag undocumented transformations, ambiguous tabs, hidden assumptions, broken logic, and mixed raw/output regions.",
      "- Focus on whether the workbook is auditable and safely reusable by someone other than the creator."
    ].join("\n"),
    pdf: [
      "- Treat the PDF as a review artifact whose pagination, tables, figures, and layout may matter.",
      "- Flag places where formatting, legibility, references, or embedded visuals create ambiguity or weaken reviewability.",
      "- Do not assume the PDF is editable; focus on integrity, clarity, and whether the content can be reviewed accurately as submitted."
    ].join("\n")
  };

  return standards[formatKey] || "- Apply general clarity, auditability, and reviewability standards.";
}

function fetchStandardWithFallback_(config, standardType, standardKey, relativePath, fallbackText) {
  if (!config || !config.standardsBaseUrl || !relativePath) {
    return fallbackText;
  }

  var cache = CacheService.getScriptCache();
  var cacheMinutes = isFinite(config.standardsCacheMinutes) && config.standardsCacheMinutes > 0
    ? config.standardsCacheMinutes
    : 20;
  var cacheKey = "std:" + standardType + ":" + standardKey + ":" + hashKeyFragment_(config.standardsBaseUrl + "/" + relativePath);

  var cached = cache.get(cacheKey);
  if (cached) {
    return cached;
  }

  try {
    var url = config.standardsBaseUrl + "/" + relativePath;
    var response = UrlFetchApp.fetch(url, {
      method: "get",
      muteHttpExceptions: true
    });
    if (response.getResponseCode() >= 200 && response.getResponseCode() < 300) {
      var text = String(response.getContentText() || "").trim();
      if (text) {
        cache.put(cacheKey, text, Math.min(cacheMinutes * 60, 21600));
        return text;
      }
    }
  } catch (err) {
    // Fall back quietly to embedded defaults.
  }

  return fallbackText;
}

function hashKeyFragment_(text) {
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, text);
  return Utilities.base64EncodeWebSafe(digest).slice(0, 12);
}

function deriveFormatKeyFromReviewSource_(reviewSource) {
  if (!reviewSource || !reviewSource.reviewFormatLabel) {
    return "google_doc";
  }
  var label = String(reviewSource.reviewFormatLabel).toLowerCase();
  if (label.indexOf("sheet") !== -1 || label.indexOf("xlsx") !== -1) {
    return "xlsx";
  }
  if (label.indexOf("doc") !== -1 || label.indexOf("word") !== -1) {
    return "docx";
  }
  if (label.indexOf("pdf") !== -1) {
    return "pdf";
  }
  return "google_doc";
}
