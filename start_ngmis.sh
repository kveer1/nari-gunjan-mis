#!/bin/bash
echo "Starting Nari Gunjan MIS..."

# Start PostgreSQL
sudo service postgresql start

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

# Run the server
python manage.py runserver 0.0.0.0:8000
