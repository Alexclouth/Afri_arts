# Variables
DB_NAME="Afri_db"
DB_USER="Afri_dev"
DB_PASS="Ala123.,"

# Function to execute SQL commands
execute_sql() {
    mysql -u root -e "$1"
}

# Create database if it doesn't exist
execute_sql "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

# Create user if it doesn't exist
execute_sql "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';"

# Grant all privileges on hbnb_dev_db to hbnb_dev
execute_sql "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"

# Grant SELECT privilege on performance_schema to hbnb_dev
execute_sql "GRANT SELECT ON performance_schema.* TO '$DB_USER'@'localhost';"

# Apply the changes
execute_sql "FLUSH PRIVILEGES;"

echo "MySQL server setup is complete."
