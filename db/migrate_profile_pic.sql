-- Check which DB your backend uses and run this there
USE entrance_database;

-- Check if columns exist first
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'entrance_database' 
AND TABLE_NAME IN ('mst_admin', 'mst_faculty') 
AND COLUMN_NAME = 'Profile_Pic';

-- Add columns (ignore error if already exists)
ALTER TABLE mst_admin ADD COLUMN Profile_Pic VARCHAR(255) DEFAULT NULL;
ALTER TABLE mst_faculty ADD COLUMN Profile_Pic VARCHAR(255) DEFAULT NULL;
