# Database Migration Guide

This guide explains how to manage database migrations for the News-Man backend application.

## 🗄️ Database Tables

The application currently has the following database tables:

### Articles Table
- **id**: String (Primary Key) - Article unique identifier
- **created_at**: DateTime - Timestamp when record was created
- **title**: Text - Article title
- **summary**: Text - Article summary
- **source_url**: Text - Original article URL (unique)
- **image_url**: Text - Article image URL (optional)
- **published_at**: DateTime - Original publication date (optional)
- **source_name**: Text - News source name (optional)

## 🚀 Migration Scripts

### 1. Simple Migration Script (`migrate.py`)

This script provides basic database operations:

```bash
# Check existing tables
python migrate.py check

# Create all tables
python migrate.py migrate

# Drop all tables (use with caution!)
python migrate.py drop
```

### 2. Flask-Migrate Setup (`flask_migrate_setup.py`)

For more advanced migration management:

```bash
# Set up Flask-Migrate
python flask_migrate_setup.py
```

After setup, you can use Flask-Migrate commands:

```bash
# Create a new migration
python -m flask db migrate -m "Description of changes"

# Apply migrations
python -m flask db upgrade

# Rollback to previous migration
python -m flask db downgrade

# Show current migration status
python -m flask db current

# Show migration history
python -m flask db history
```

## 📋 Migration Workflow

### Initial Setup
1. Ensure your `.env` file has the correct `SUPABASE_DB_URI`
2. Run the migration script: `python migrate.py migrate`
3. Verify tables were created: `python migrate.py check`

### Adding New Models
1. Create your new model in `app/models/`
2. Import the model in `app.py`
3. Create a new migration: `python -m flask db migrate -m "Add new model"`
4. Apply the migration: `python -m flask db upgrade`

### Modifying Existing Models
1. Update your model definition
2. Create a migration: `python -m flask db migrate -m "Update model"`
3. Review the generated migration file
4. Apply the migration: `python -m flask db upgrade`

## ⚠️ Important Notes

- **Always backup your database** before running migrations in production
- **Test migrations** on a development database first
- **Review generated migration files** before applying them
- **Never edit migration files** after they've been applied to production

## 🔧 Troubleshooting

### Connection Issues
- Verify your `.env` file has correct Supabase credentials
- Check that your Supabase project is active
- Ensure your database password is correct

### Migration Errors
- Check that all models are properly imported
- Verify database permissions
- Look for syntax errors in model definitions

### Table Already Exists
- Use `python migrate.py check` to see existing tables
- Use `python migrate.py drop` to remove all tables (development only)
- Or use Flask-Migrate for more controlled migrations

## 📊 Database Schema

```sql
CREATE TABLE articles (
    id VARCHAR NOT NULL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    source_url TEXT NOT NULL UNIQUE,
    image_url TEXT,
    published_at TIMESTAMP,
    source_name TEXT
);
```

## 🎯 Next Steps

1. **Add sample data** to test your API endpoints
2. **Create additional models** as needed (users, categories, etc.)
3. **Set up database indexes** for better performance
4. **Configure database backups** for production
