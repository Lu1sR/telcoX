#!/bin/sh
# wait_for_db.sh - Wait for MySQL to be ready before starting Django

set -e

# Use environment variables for host/port
host="${DB_HOST:-mysql}"
port="${DB_PORT:-3306}"
max_tries=30
count=0

echo "Waiting for MySQL at $host:$port..."

until nc -z "$host" "$port" || [ $count -eq $max_tries ]; do
  count=$((count+1))
  echo "MySQL is unavailable ($count/$max_tries) - sleeping"
  sleep 2
done

if [ $count -eq $max_tries ]; then
  echo "Failed to connect to MySQL after $max_tries attempts"
  exit 1
fi

echo "MySQL is up - ready to proceed"
