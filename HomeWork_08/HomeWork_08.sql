/*
 Navicat Premium Data Transfer

 Source Server         : HomeWork_08
 Source Server Type    : SQLite
 Source Server Version : 3035005
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005
 File Encoding         : 65001

 Date: 20/11/2022 17:25:36
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for disciplines
-- ----------------------------
DROP TABLE IF EXISTS "disciplines";
CREATE TABLE "disciplines" (
  "dsc_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "dsc_name" TEXT NOT NULL,
  "dsc_tch_id" INTEGER NOT NULL,
  CONSTRAINT "dsc_tch_id_fk" FOREIGN KEY ("dsc_tch_id") REFERENCES "teachers" ("tch_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Table structure for grade_list
-- ----------------------------
DROP TABLE IF EXISTS "grade_list";
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

-- ----------------------------
-- Table structure for grades
-- ----------------------------
DROP TABLE IF EXISTS "grades";
CREATE TABLE "grades" (
  "grd_id" INTEGER NOT NULL,
  "grd_name" TEXT NOT NULL,
  "grd_value" integer NOT NULL,
  PRIMARY KEY ("grd_id"),
  CONSTRAINT "grd_value_check" CHECK (grd_value between 1 and 5)
);

-- ----------------------------
-- Table structure for std_groups
-- ----------------------------
DROP TABLE IF EXISTS "std_groups";
CREATE TABLE "std_groups" (
  "grp_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "grp_name" TEXT NOT NULL
);

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS "students";
CREATE TABLE "students" (
  "std_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "std_full_name" TEXT NOT NULL,
  "std_grp_id" INTEGER NOT NULL,
  CONSTRAINT "std_grp_id_fk" FOREIGN KEY ("std_grp_id") REFERENCES "std_groups" ("grp_id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Table structure for teachers
-- ----------------------------
DROP TABLE IF EXISTS "teachers";
CREATE TABLE "teachers" (
  "tch_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "tch_name" TEXT NOT NULL
);

-- ----------------------------
-- Indexes structure for table disciplines
-- ----------------------------
CREATE UNIQUE INDEX "dsc_name_idx"
ON "disciplines" (
  "dsc_name" ASC
);

-- ----------------------------
-- Indexes structure for table grade_list
-- ----------------------------
CREATE INDEX """gls_date_of"""
ON "grade_list" (
  "gls_date_of" ASC
);

-- ----------------------------
-- Indexes structure for table grades
-- ----------------------------
CREATE UNIQUE INDEX """grd_name_idx"""
ON "grades" (
  "grd_name" ASC
);

-- ----------------------------
-- Indexes structure for table std_groups
-- ----------------------------
CREATE UNIQUE INDEX "grp_name_idx"
ON "std_groups" (
  "grp_name" ASC
);

-- ----------------------------
-- Indexes structure for table students
-- ----------------------------
CREATE UNIQUE INDEX "std_full_name_idx"
ON "students" (
  "std_full_name" ASC
);

-- ----------------------------
-- Indexes structure for table teachers
-- ----------------------------
CREATE UNIQUE INDEX "tch_name_idx"
ON "teachers" (
  "tch_name" ASC
);

PRAGMA foreign_keys = true;
