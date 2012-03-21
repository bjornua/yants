CREATE TABLE "document"(
    "id" TEXT,
    "peer_id" TEXT,
    "seq_id" INTEGER,
    "mtime" TEXT, 
    "content" TEXT,
    "xapian_id" INTEGER,
    "snippet" TEXT,
    "deleted" INTEGER
);

CREATE UNIQUE INDEX "idx_id"          ON "document" ("id" ASC);
CREATE UNIQUE INDEX "idx_xapian_id"   ON "document" ("xapian_id" ASC);
CREATE UNIQUE INDEX "idx_replication" ON "document" ("peer_id" ASC, "seq_id" ASC);
CREATE INDEX        "idx_latest"      ON "document" ("deleted" ASC, "mtime" DESC);

CREATE TABLE "settings"("key" TEXT, "value" TEXT);
CREATE UNIQUE INDEX "idx_key"         ON "settings" ("key" ASC);
