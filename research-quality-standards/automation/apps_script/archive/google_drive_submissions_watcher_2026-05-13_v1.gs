/**
 * Archived working version saved before DOCX/XLSX conversion support,
 * smarter extraction, and clasp deployment files were added.
 */

/**
 * Google Drive submissions watcher with OpenAI review support.
 *
 * Purpose:
 * Poll a Drive submissions folder, detect new files, and log them to a
 * Google Sheet. For supported native Google Docs and Google Sheets files,
 * call the OpenAI Responses API, generate a review, and write the review
 * into a per-submission Google Doc.
 *
 * Required Script Properties:
 * - SUBMISSIONS_FOLDER_ID
 * - TRACKING_SHEET_ID
 * - OPENAI_API_KEY
 *
 * Recommended Script Properties:
 * - TRACKING_SHEET_NAME=Intake Log
 * - OPENAI_MODEL=gpt-5-mini
 * - INCLUDE_SUBFOLDERS=true
 * - EXCLUDED_FOLDER_NAMES=99_Admin
 * - REVIEW_OUTPUT_FOLDER_NAME=Review Outputs
 * - EXCLUDED_FILE_IDS=comma,separated,file,ids
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
var OPENAI_RESPONSES_URL_ = "https://api.openai.com/v1/responses";
var MAX_DOC_TEXT_CHARS_ = 20000;
var MAX_SHEET_TEXT_CHARS_ = 16000;

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
    excludedFileIds: parseCsvProperty_(props.getProperty("EXCLUDED_FILE_IDS") || ""),
    openAiApiKey: props.getProperty("OPENAI_API_KEY"),
    openAiModel: props.getProperty("OPENAI_MODEL") || "gpt-5-mini"
  };
}

function scanSubmissionFolders() {
  var config = getConfig_();
  validateConfig_(config);

  var root = DriveApp.getFolderById(config.submissionsFolderId);
  var sheet = getOrCreateTrackingSheet_(config.trackingSheetId, config.trackingSheetName);
  var seen = getSeenFileIds_(sheet);
  var reviewOutputFolder = getOrCreateReviewOutputFolder_(root, config.reviewOutputFolderName);
  var rows = [];

  collectFolderFiles_(root, config, reviewOutputFolder, rows, seen);

  if (rows.length > 0) {
    sheet.getRange(sheet.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
}

function validateConfig_(config) {
  var missing = [];
  if (!config.submissionsFolderId) missing.push("SUBMISSIONS_FOLDER_ID");
  if (!config.trackingSheetId) missing.push("TRACKING_SHEET_ID");
  if (!config.openAiApiKey) missing.push("OPENAI_API_KEY");
  if (missing.length > 0) {
    throw new Error("Missing required Script Properties: " + missing.join(", "));
  }
}

function collectFolderFiles_(folder, config, reviewOutputFolder, rows, seen) {
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
    var reviewResult = reviewSubmission_(file, folder, genre, reviewDoc, config);

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
    collectFolderFiles_(folders.next(), config, reviewOutputFolder, rows, seen);
  }
}

function reviewSubmission_(file, sourceFolder, genre, reviewDoc, config) {
  var mimeType = file.getMimeType();
  var formatInfo = getFormatInfo_(mimeType);

  if (!formatInfo.supported) {
    appendUnsupportedFormatNote_(reviewDoc, file, sourceFolder, genre, formatInfo);
    return {
      status: "QUEUED",
      reviewState: "UNSUPPORTED_FORMAT",
      notes: formatInfo.message
    };
  }

  try {
    var extracted = extractArtifactText_(file, formatInfo);
    var reviewText = callOpenAiReview_(file, genre, formatInfo, extracted, config);
    writeCompletedReview_(reviewDoc, file, sourceFolder, genre, formatInfo, extracted.notice, reviewText);
    return {
      status: "REVIEWED",
      reviewState: "OPENAI_REVIEWED",
      notes: extracted.notice || ""
    };
  } catch (err) {
    appendReviewFailure_(reviewDoc, file, sourceFolder, genre, formatInfo, err);
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
      formatStandard: getFormatStandard_("google_doc")
    };
  }

  if (mimeType === GOOGLE_SHEET_MIME_) {
    return {
      supported: true,
      formatKey: "google_sheet",
      formatLabel: "Google Sheet",
      formatStandard: getFormatStandard_("google_sheet")
    };
  }

  if (
    mimeType === MimeType.MICROSOFT_WORD ||
    mimeType === "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  ) {
    return {
      supported: false,
      formatKey: "docx",
      formatLabel: "Word DOCX",
      message: "Word .docx review is on the to-do list but not implemented in this first Google-native version."
    };
  }

  if (
    mimeType === MimeType.MICROSOFT_EXCEL ||
    mimeType === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  ) {
    return {
      supported: false,
      formatKey: "xlsx",
      formatLabel: "Excel XLSX",
      message: "Excel .xlsx review is on the to-do list but not implemented in this first Google-native version."
    };
  }

  return {
    supported: false,
    formatKey: "unknown",
    formatLabel: mimeType,
    message: "Only native Google Docs and Google Sheets are reviewed automatically in this version."
  };
}

function extractArtifactText_(file, formatInfo) {
  if (formatInfo.formatKey === "google_doc") {
    var doc = DocumentApp.openById(file.getId());
    var text = doc.getBody().getText() || "";
    return {
      content: trimToLimit_(text, MAX_DOC_TEXT_CHARS_),
      notice: buildTruncationNotice_(text, MAX_DOC_TEXT_CHARS_)
    };
  }

  if (formatInfo.formatKey === "google_sheet") {
    var summary = summarizeSpreadsheet_(file.getId());
    return {
      content: trimToLimit_(summary, MAX_SHEET_TEXT_CHARS_),
      notice: buildTruncationNotice_(summary, MAX_SHEET_TEXT_CHARS_)
    };
  }

  throw new Error("Unsupported extraction format: " + formatInfo.formatKey);
}

function summarizeSpreadsheet_(spreadsheetId) {
  var ss = SpreadsheetApp.openById(spreadsheetId);
  var sheets = ss.getSheets();
  var parts = [];

  for (var i = 0; i < sheets.length; i++) {
    var sheet = sheets[i];
    var range = sheet.getDataRange();
    var values = range.getDisplayValues();
    var maxRows = Math.min(values.length, 30);
    var maxCols = values.length > 0 ? Math.min(values[0].length, 12) : 0;

    parts.push("Sheet: " + sheet.getName());
    parts.push("Rows: " + values.length + ", Columns: " + (values.length > 0 ? values[0].length : 0));

    for (var r = 0; r < maxRows; r++) {
      var row = [];
      for (var c = 0; c < maxCols; c++) {
        row.push(values[r][c]);
      }
      parts.push(row.join(" | "));
    }

    if (values.length > maxRows) {
      parts.push("[Additional rows omitted]");
    }
    parts.push("");
  }

  return parts.join("\n");
}

function callOpenAiReview_(file, genre, formatInfo, extracted, config) {
  var payload = {
    model: config.openAiModel,
    instructions: buildReviewerInstructions_(),
    input: buildReviewInput_(file, genre, formatInfo, extracted),
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

function buildReviewInput_(file, genre, formatInfo, extracted) {
  var genreStandard = getGenreStandard_(genre);
  var lines = [
    "Artifact name: " + file.getName(),
    "Genre: " + genre,
    "Format: " + formatInfo.formatLabel,
    "",
    "Genre standard:",
    genreStandard,
    "",
    "Format standard:",
    formatInfo.formatStandard,
    "",
    "Artifact content:",
    extracted.content
  ];

  if (extracted.notice) {
    lines.splice(4, 0, "Content notice: " + extracted.notice, "");
  }

  return lines.join("\n");
}

function writeCompletedReview_(reviewDoc, file, sourceFolder, genre, formatInfo, notice, reviewText) {
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
  body.appendParagraph("Review date: " + new Date());
  if (notice) {
    body.appendParagraph("Extraction note: " + notice);
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

function appendReviewFailure_(reviewDoc, file, sourceFolder, genre, formatInfo, err) {
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
  return value.slice(0, limit) + "\n\n[Content truncated for review]";
}

function buildTruncationNotice_(text, limit) {
  var value = String(text || "");
  if (value.length <= limit) {
    return "";
  }
  return "Artifact text was truncated from " + value.length + " to " + limit + " characters before review.";
}

function truncateForCell_(text, limit) {
  var value = String(text || "");
  if (value.length <= limit) {
    return value;
  }
  return value.slice(0, limit);
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

function getGenreStandard_(genre) {
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

function getFormatStandard_(formatKey) {
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
    ].join("\n")
  };

  return standards[formatKey] || "- Apply general clarity, auditability, and reviewability standards.";
}
