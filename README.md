# TelcoX Usage Visualization Module

A production-grade usage/consumption visualization module for a telecom self-service portal.

## Tech Stack

- **Frontend**: Angular 17+
- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: MySQL 8.0 (Docker container)
- **Orchestration**: Docker Compose

---

## Project Status

**Current Phase**: Phase 1 - Infrastructure Setup ✅

- [x] Monorepo structure initialized
- [x] Git repository configured
- [x] Environment variables template created
- [x] Docker Compose configuration for MySQL
- [ ] Django backend (Phase 2)
- [ ] Angular frontend (Phase 4)
- [ ] Tests (Phase 6)
- [ ] Documentation (Phase 7)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**
- **Python** 3.10+ (for local development)
- **Node.js** 18+ and npm (for Angular development)

### Verify installations:

```bash
docker --version
docker-compose --version
git --version
python3 --version
node --version
npm --version
```

---

## Quick Start (Phase 1)

### 1. Clone or Initialize Repository

If starting fresh:

```bash
cd /path/to/your/projects
mkdir telcoX
cd telcoX
git init
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and update the passwords
# At minimum, change:
# - MYSQL_ROOT_PASSWORD
# - MYSQL_PASSWORD
# - SECRET_KEY
```

**Important**: Never commit `.env` to version control!

### 3. Start MySQL Database

```bash
# Start MySQL container in detached mode
docker-compose up -d mysql

# View logs to verify startup
docker-compose logs -f mysql

# Wait for "ready for connections" message
```

### 4. Verify MySQL Connection

**From inside the container:**

```bash
docker-compose exec mysql mysql -u telcox_user -p telcox_db
# Enter password when prompted (from your .env file)
```

**From host (using MySQL client):**

```bash
mysql -h 127.0.0.1 -P 3306 -u telcox_user -p telcox_db
# Or use MySQL Workbench/DBeaver with these credentials
```

---

## Docker Compose Commands

### Start all services:
```bash
docker-compose up -d
```

### Stop all services:
```bash
docker-compose down
```

### Stop and remove volumes (WARNING: deletes data):
```bash
docker-compose down -v
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mysql
```

### Restart a service:
```bash
docker-compose restart mysql
```

### Check service status:
```bash
docker-compose ps
```

---

## Directory Structure

```
telcoX/
├── README.md                    # This file
├── docker-compose.yml          # Docker orchestration
├── .env.example                # Environment template
├── .env                        # Local environment (gitignored)
├── .gitignore                  # Git ignore rules
├── backend/                    # Django backend (Phase 2)
├── frontend/                   # Angular frontend (Phase 4)
├── database/                   # Database scripts (Phase 2)
└── docs/                       # Documentation (Phase 7)
```

---

## Troubleshooting

### MySQL container won't start

1. Check if port 3306 is already in use:
   ```bash
   lsof -i :3306
   ```

2. Check Docker logs:
   ```bash
   docker-compose logs mysql
   ```

3. Ensure `.env` file exists and has correct values

### Connection refused errors

- Wait 30-60 seconds after starting MySQL for full initialization
- Verify healthcheck status: `docker-compose ps`
- Check if container is running: `docker ps`

### Reset database completely

```bash
docker-compose down -v
docker-compose up -d mysql
```

---

## Next Steps

After Phase 1 is complete:

1. **Phase 2**: Set up Django backend with models and migrations
2. **Phase 3**: Implement REST API endpoints
3. **Phase 4**: Create Angular frontend
4. **Phase 5**: Implement UI components
5. **Phase 6**: Add comprehensive tests
6. **Phase 7**: Write documentation

---

## License

This is a technical challenge project for TelcoX.

---

## Support

For issues or questions, please refer to the documentation in the `/docs` folder (coming in Phase 7).
