/*
 Navicat Premium Data Transfer

 Source Server         : db
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 01/11/2018 16:31:29
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for result
-- ----------------------------
DROP TABLE IF EXISTS "result";
CREATE TABLE "result" (
  "id" INTEGER NOT NULL,
  "src_img" TEXT,
  "ref_img" TEXT,
  "res_img" TEXT,
  "alg" TEXT,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
