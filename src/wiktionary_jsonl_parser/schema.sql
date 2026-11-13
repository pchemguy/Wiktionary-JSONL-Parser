CREATE TABLE batch_log (
    batch_id            INTEGER PRIMARY KEY,
    line_count          INTEGER NOT NULL
);

CREATE TABLE entries (
    id                  INTEGER PRIMARY KEY,
    word                TEXT NOT NULL,
    lang_code           TEXT NOT NULL,
    lang                TEXT NOT NULL,
    pos                 TEXT,
    pos_title           TEXT,
    literal_meaning     TEXT COLLATE UTF_CI,
    etymology_texts     TEXT,                -- JSON array
    categories          TEXT,                -- JSON array
    raw_tags            TEXT,                -- JSON array
    tags                TEXT                 -- JSON array
);

CREATE TABLE anagrams (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE antonyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE coordinate_terms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE derived (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE holonyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE hypernyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE hyponyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE meronyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE metagrams (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE proverbs (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE related (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE synonyms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE variants (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT,
    sense               TEXT COLLATE UTF_CI,
    sense_index         INTEGER CHECK (sense_index IS NULL OR sense_index >= 0),
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE forms (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    form                TEXT NOT NULL,
    raw_tags            TEXT, -- JSON array
    tags                TEXT, -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE senses (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    glosses             TEXT, -- JSON array
    form_of             TEXT, -- JSON array
    categories          TEXT, -- JSON array
    topics              TEXT, -- JSON array
    raw_tags            TEXT, -- JSON array
    tags                TEXT, -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE examples (
    sense_entry_id            INTEGER NOT NULL,
    sense_idx                 INTEGER NOT NULL CHECK (sense_idx >= 0),
    idx                       INTEGER NOT NULL CHECK (idx >= 0),
    text                      TEXT COLLATE UTF_CI NOT NULL,
    translation               TEXT COLLATE UTF_CI,
    ref                       TEXT COLLATE UTF_CI,
    bold_text_offsets         TEXT, -- JSON array of [start, end] arrays
    bold_translation_offsets  TEXT, -- JSON array of [start, end] arrays
    FOREIGN KEY (sense_entry_id, sense_idx) REFERENCES senses(entry_id, idx) ON DELETE CASCADE,
    PRIMARY KEY (sense_entry_id, sense_idx, idx)
) WITHOUT ROWID;

CREATE TABLE translations (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    word                TEXT NOT NULL,
    lang                TEXT NOT NULL,
    lang_code           TEXT,
    roman               TEXT COLLATE UTF_CI,
    sense               TEXT COLLATE UTF_CI,
    other               TEXT COLLATE UTF_CI,
    raw_tags            TEXT,                -- JSON array
    tags                TEXT,                -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE sounds (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    audio               TEXT,
    ipa                 TEXT,
    rhymes              TEXT,
    homophones          TEXT, -- JSON array
    urls                TEXT, -- JSON object (flac_url, mp3_url, oga_url, ogg_url, opus_url, wav_url)
    raw_tags            TEXT, -- JSON array
    tags                TEXT, -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;

CREATE TABLE hyphenations (
    entry_id            INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
    idx                 INTEGER NOT NULL CHECK (idx >= 0),
    parts               TEXT, -- JSON array
    raw_tags            TEXT, -- JSON array
    tags                TEXT, -- JSON array
    PRIMARY KEY (entry_id, idx)
) WITHOUT ROWID;
