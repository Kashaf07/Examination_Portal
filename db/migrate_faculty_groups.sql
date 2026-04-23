-- Migration: Add Faculty_Email to faculty_groups and unique constraints
-- Run this in MySQL Workbench if you want to keep existing data

USE entrance_database;

-- Disable FK checks
SET FOREIGN_KEY_CHECKS = 0;

-- 1. Add Faculty_Email column to faculty_groups table
ALTER TABLE faculty_groups 
ADD COLUMN Faculty_Email varchar(100) NOT NULL DEFAULT 'system@internal' AFTER Group_Name;

-- 2. Update existing records with actual faculty emails
-- You need to map these to the correct faculty emails from your system
UPDATE faculty_groups SET Faculty_Email = 'dhavalm@nuv.ac.in' WHERE Group_Id = 1;
UPDATE faculty_groups SET Faculty_Email = 'dhavalm@nuv.ac.in' WHERE Group_Id = 2;
UPDATE faculty_groups SET Faculty_Email = 'kashaf.parkar@nuv.ac.in' WHERE Group_Id = 6;

-- 3. Add unique constraint to prevent duplicate group names per faculty
ALTER TABLE faculty_groups 
ADD CONSTRAINT unique_faculty_group UNIQUE (Group_Name, Faculty_Email);

-- 4. Add unique constraint to applicant_groups (if not already exists)
ALTER TABLE applicant_groups 
ADD CONSTRAINT unique_group_per_faculty UNIQUE (Group_Name, Faculty_Email);

-- Re-enable FK checks
SET FOREIGN_KEY_CHECKS = 1;

-- Verify changes
SELECT * FROM faculty_groups;
DESCRIBE faculty_groups;