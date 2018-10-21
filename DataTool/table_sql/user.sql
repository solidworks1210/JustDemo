SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "main"."user";
CREATE TABLE "user" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT,
"name"  TEXT NOT NULL,
"password"  TEXT NOT NULL,
"role"  TEXT(1) NOT NULL DEFAULT 1
);
