CREATE TABLE "disciplines" (
  "dsc_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "dsc_name" TEXT NOT NULL,
  "dsc_tch_id" INTEGER NOT NULL,
  CONSTRAINT "dsc_tch_id_fk" FOREIGN KEY ("dsc_tch_id") REFERENCES "teachers" ("tch_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);
INSERT INTO "sqlite_sequence" (name, seq) VALUES ('disciplines', '5');
CREATE UNIQUE INDEX "dsc_name_idx"
ON "disciplines" (
  "dsc_name" ASC
);

CREATE TABLE "grade_list" (
  "gls_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "gls_grd_id" INTEGER NOT NULL,
  "gls_dsc_id" INTEGER NOT NULL,
  "gls_std_id" INTEGER NOT NULL,
  "gls_date_of" DATE NOT NULL,
  CONSTRAINT "gls_grd_id_fk" FOREIGN KEY ("gls_grd_id") REFERENCES "grades" ("grd_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "gls_dsc_id_fk" FOREIGN KEY ("gls_dsc_id") REFERENCES "disciplines" ("dsc_id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "gls_std_id_fk" FOREIGN KEY ("gls_std_id") REFERENCES "students" ("std_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);
INSERT INTO "sqlite_sequence" (name, seq) VALUES ('grade_list', '264');
CREATE INDEX """gls_date_of"""
ON "grade_list" (
  "gls_date_of" ASC
);

CREATE TABLE "grades" (
  "grd_id" INTEGER NOT NULL,
  "grd_name" TEXT NOT NULL,
  "grd_value" integer NOT NULL,
  PRIMARY KEY ("grd_id"),
  CONSTRAINT "grd_value_check" CHECK (grd_value between 1 and 5)
);
CREATE UNIQUE INDEX """grd_name_idx"""
ON "grades" (
  "grd_name" ASC
);

CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

CREATE TABLE "std_groups" (
  "grp_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "grp_name" TEXT NOT NULL
);
INSERT INTO "sqlite_sequence" (name, seq) VALUES ('std_groups', '3');
CREATE UNIQUE INDEX "grp_name_idx"
ON "std_groups" (
  "grp_name" ASC
);

CREATE TABLE "students" (
  "std_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "std_full_name" TEXT NOT NULL,
  "std_grp_id" INTEGER NOT NULL,
  CONSTRAINT "std_grp_id_fk" FOREIGN KEY ("std_grp_id") REFERENCES "std_groups" ("grp_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);
INSERT INTO "sqlite_sequence" (name, seq) VALUES ('students', '30');
CREATE UNIQUE INDEX "std_full_name_idx"
ON "students" (
  "std_full_name" ASC
);

CREATE TABLE "teachers" (
  "tch_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "tch_name" TEXT NOT NULL
);
INSERT INTO "sqlite_sequence" (name, seq) VALUES ('teachers', '5');
CREATE UNIQUE INDEX "tch_name_idx"
ON "teachers" (
  "tch_name" ASC
);

