# Phase 1 Setup Guide - Complete Instructions

This guide provides all commands and steps to complete Phase 1 of the TelcoX project.

---

## 1. Final Directory Structure After Phase 1

```
telcoX/
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Environment template ✓
├── .gitignore                 # Git ignore rules ✓
├── README.md                  # Project documentation ✓
├── docker-compose.yml         # Docker orchestration ✓
├── SETUP_PHASE1.md           # This file ✓
├── checklist.md              # Your existing checklist
│
├── backend/                   # Django backend (Phase 2)
│   └── .gitkeep              ✓
│
├── frontend/                  # Angular frontend (Phase 4)
│   └── .gitkeep              ✓
│
├── database/                  # Database initialization scripts
│   └── .gitkeep              ✓
│
└── docs/                      # Documentation (Phase 7)
    └── .gitkeep              ✓
```

**Files created in Phase 1**: 8 files + 4 directories

---

## 2. Initialize Git Repository

Run these commands from the project root (`/Users/nathaliebohorquez/Documents/personal/telcoX`):

```bash
# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Phase 1: Initial project setup with Docker Compose and MySQL"

# (Optional) Add remote repository
# git remote add origin https://github.com/yourusername/telcoX.git
# git branch -M main
# git push -u origin main
```

---

## 3. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your preferred editor
nano .env
# OR
code .env
# OR
vim .env
```

**Minimum required changes in `.env`:**

```bash
# Change these passwords to something secure
MYSQL_ROOT_PASSWORD=your_secure_root_password_here
MYSQL_PASSWORD=your_secure_user_password_here

# Change the Django secret key (you can generate one with Python)
SECRET_KEY=your-django-secret-key-here
```

**Optional: Generate a Django secret key:**

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use an online generator: https://djecrety.ir/

---

## 4. Start MySQL Service with Docker Compose

### Start MySQL container:

```bash
# Start in detached mode (runs in background)
docker-compose up -d mysql

# Expected output:
# [+] Running 2/2
#  ✔ Network telcox_network      Created
#  ✔ Container telcox_mysql      Started
```

### View startup logs:

```bash
# Follow logs in real-time (press Ctrl+C to exit)
docker-compose logs -f mysql

# Look for this message indicating MySQL is ready:
# "mysqld: ready for connections. Version: '8.0.x'"
```

**Note**: First startup takes 30-60 seconds while MySQL initializes the database.

### Verify container is running:

```bash
docker-compose ps

# Expected output:
# NAME            IMAGE       STATUS        PORTS
# telcox_mysql    mysql:8.0   Up (healthy)  0.0.0.0:3306->3306/tcp
```

### Check health status:

```bash
docker inspect telcox_mysql --format='{{.State.Health.Status}}'

# Expected output: "healthy"
```

---

## 5. Connect to MySQL

### Option A: Connect from INSIDE the container

This is useful for quick checks and doesn't require a MySQL client on your host.

```bash
# Method 1: Using docker-compose exec
docker-compose exec mysql mysql -u telcox_user -p telcox_db

# Method 2: Using docker exec
docker exec -it telcox_mysql mysql -u telcox_user -p telcox_db

# When prompted, enter the password from your .env file (MYSQL_PASSWORD)
```

**Once connected, you can run SQL commands:**

```sql
-- Show all databases
SHOW DATABASES;

-- Use the telcox database
USE telcox_db;

-- Show tables (empty for now)
SHOW TABLES;

-- Check MySQL version
SELECT VERSION();

-- Exit MySQL
EXIT;
```

### Option B: Connect from HOST using exposed port 3306

**Prerequisites**: MySQL client installed on your host machine.

Install MySQL client (if not already installed):

```bash
# macOS (using Homebrew)
brew install mysql-client

# Add to PATH (add this to your ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Linux (Ubuntu/Debian)
sudo apt-get install mysql-client

# Linux (CentOS/RHEL)
sudo yum install mysql
```

**Connect using MySQL client:**

```bash
# Using mysql command-line client
mysql -h 127.0.0.1 -P 3306 -u telcox_user -p telcox_db

# Or specify password inline (not recommended for production)
mysql -h 127.0.0.1 -P 3306 -u telcox_user -pYOUR_PASSWORD telcox_db
```

**Connection parameters:**
- **Host**: `127.0.0.1` or `localhost`
- **Port**: `3306`
- **Username**: `telcox_user` (from .env)
- **Password**: (value of MYSQL_PASSWORD from .env)
- **Database**: `telcox_db`

### Option C: Connect using GUI tools

**MySQL Workbench:**
1. Open MySQL Workbench
2. Click "+" to create a new connection
3. Enter connection details:
   - Connection Name: `TelcoX Local`
   - Hostname: `127.0.0.1`
   - Port: `3306`
   - Username: `telcox_user`
   - Password: (click "Store in Keychain" and enter MYSQL_PASSWORD)
   - Default Schema: `telcox_db`
4. Click "Test Connection"
5. Click "OK" to save

**DBeaver:**
1. Click "New Database Connection"
2. Select "MySQL"
3. Enter connection details (same as above)
4. Click "Test Connection"
5. Click "Finish"

**TablePlus:**
1. Click "Create a new connection"
2. Select "MySQL"
3. Enter connection details
4. Click "Connect"

---

## 6. Verify MySQL Setup

Run these commands to verify everything is working:

```bash
# 1. Check container is running
docker-compose ps

# 2. Check container logs for errors
docker-compose logs mysql | grep -i error

# 3. Verify network exists
docker network ls | grep telcox

# 4. Verify volume exists
docker volume ls | grep telcox

# 5. Test connection from inside container
docker-compose exec mysql mysql -u telcox_user -p -e "SELECT 'MySQL is working!' AS status;"

# 6. Check MySQL variables
docker-compose exec mysql mysql -u root -p -e "SHOW VARIABLES LIKE 'character_set%';"
```

---

## 7. Common Docker Compose Commands

### Start services:
```bash
# Start all services (only mysql for now)
docker-compose up -d

# Start with logs visible
docker-compose up

# Start specific service
docker-compose up -d mysql
```

### Stop services:
```bash
# Stop all services
docker-compose down

# Stop but keep volumes (data persists)
docker-compose stop
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mysql

# Last N lines
docker-compose logs --tail=100 mysql
```

### Restart services:
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart mysql
```

### Remove everything (including volumes):
```bash
# WARNING: This deletes all database data!
docker-compose down -v

# Remove containers and networks but keep volumes
docker-compose down
```

### Execute commands in container:
```bash
# MySQL shell
docker-compose exec mysql mysql -u root -p

# Bash shell
docker-compose exec mysql bash

# Run one-off command
docker-compose exec mysql mysqladmin -u root -p status
```

---

## 8. Development Notes and Gotchas

### ⚠️ Important Gotchas

1. **First startup is slow**
   - MySQL initialization takes 30-60 seconds on first run
   - Wait for "ready for connections" in logs before connecting
   - Healthcheck will show "starting" then "healthy"

2. **Password in .env must match**
   - `MYSQL_PASSWORD` and `DB_PASSWORD` should be the same
   - Both are used by different services but refer to the same MySQL user

3. **Port 3306 conflicts**
   - If you have MySQL installed locally, it may use port 3306
   - Either stop local MySQL or change port mapping in docker-compose.yml:
     ```yaml
     ports:
       - "3307:3306"  # Map to different host port
     ```

4. **Volume persistence**
   - Data persists even after `docker-compose down`
   - To completely reset: `docker-compose down -v`
   - Volume location: Docker's volume storage (managed by Docker)

5. **Container hostname**
   - Inside Docker network: use `mysql` as hostname
   - From host machine: use `127.0.0.1` or `localhost`
   - Django will use `mysql` (the service name)

### 💡 Useful Tips

1. **Check if port is available:**
   ```bash
   # macOS/Linux
   lsof -i :3306
   
   # If something is using it:
   sudo lsof -i :3306
   kill -9 <PID>
   ```

2. **View real-time resource usage:**
   ```bash
   docker stats telcox_mysql
   ```

3. **Inspect container details:**
   ```bash
   docker inspect telcox_mysql
   ```

4. **Access MySQL data files (from container):**
   ```bash
   docker-compose exec mysql ls -la /var/lib/mysql
   ```

5. **Backup database (for later use):**
   ```bash
   docker-compose exec mysql mysqldump -u root -p telcox_db > backup.sql
   ```

6. **Restore database (for later use):**
   ```bash
   docker-compose exec -T mysql mysql -u root -p telcox_db < backup.sql
   ```

### 🔧 Development Best Practices

1. **Always use .env for secrets**
   - Never commit `.env` to git
   - Keep `.env.example` updated as a template
   - Use different values for development and production

2. **Named volumes for persistence**
   - `mysql_data` volume persists data between container restarts
   - Survives `docker-compose down` (but not `down -v`)

3. **Healthchecks**
   - Docker Compose healthcheck ensures MySQL is ready
   - Other services can use `depends_on` with `condition: service_healthy`

4. **Character set configuration**
   - Configured for UTF-8 (utf8mb4) to support emojis and international characters
   - Important for customer names with special characters

5. **MySQL native password plugin**
   - Using `mysql_native_password` for compatibility
   - Required for some MySQL clients and Django

### 🐛 Troubleshooting

**Problem**: Container exits immediately after starting

```bash
# Check logs for error
docker-compose logs mysql

# Common issues:
# - Invalid .env values
# - Port already in use
# - Corrupted volume data
```

**Solution**: Remove volume and restart
```bash
docker-compose down -v
docker-compose up -d mysql
```

---

**Problem**: "Can't connect to MySQL server on '127.0.0.1'"

**Solution**:
1. Check container is running: `docker-compose ps`
2. Wait for healthcheck: `docker inspect telcox_mysql --format='{{.State.Health.Status}}'`
3. Check logs: `docker-compose logs mysql`
4. Verify port mapping: `docker port telcox_mysql`

---

**Problem**: "Access denied for user 'telcox_user'"

**Solution**:
1. Verify password in `.env` matches what you're using
2. Reset database: `docker-compose down -v && docker-compose up -d mysql`
3. Wait for full initialization (30-60 seconds)

---

## 9. Next Steps (Phase 2)

After Phase 1 is complete and MySQL is running:

1. ✓ Verify MySQL container is healthy
2. ✓ Can connect to database from both inside container and host
3. → Set up Django project structure
4. → Create Django apps (customers, usage)
5. → Define models and create migrations
6. → Seed test data

---

## 10. Quick Reference

### Project Info
- **Database**: telcox_db
- **User**: telcox_user
- **Container**: telcox_mysql
- **Network**: telcox_network
- **Volume**: telcox_mysql_data

### Ports
- MySQL: 3306 (host) → 3306 (container)
- Backend: 8000 (Phase 3)
- Frontend: 4200 (Phase 4)

### Key Files
- `docker-compose.yml` - Service orchestration
- `.env` - Environment variables (gitignored)
- `.env.example` - Environment template
- `.gitignore` - Git ignore rules

---

**Phase 1 Complete!** 🎉

You now have:
- ✅ Clean monorepo structure
- ✅ Git repository initialized
- ✅ MySQL running in Docker
- ✅ Environment configuration
- ✅ Documentation

Ready for Phase 2: Django Backend Setup
