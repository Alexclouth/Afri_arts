-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS Afri_db;

-- Create the user if it doesn't exist
CREATE USER IF NOT EXISTS 'Afri_dev'@'localhost' IDENTIFIED BY 'Ala123.,';

-- Grant all privileges on the Afri_db database to the Afri_dev user
GRANT ALL PRIVILEGES ON Afri_db.* TO 'Afri_dev'@'localhost';

-- Grant SELECT privilege on the performance_schema to the Afri_dev user
GRANT SELECT ON performance_schema.* TO 'Afri_dev'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
