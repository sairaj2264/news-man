# Supabase Database Setup Guide

## Step 1: Create .env file

Create a file named `.env` in the `backend` directory with the following content:

```env
# Supabase Configuration
# Replace these placeholder values with your actual Supabase project credentials

# Your Supabase project URL (found in Project Settings > API)
SUPABASE_URL=https://your-project-id.supabase.co

# Your Supabase service role key (found in Project Settings > API > service_role key)
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Your Supabase database connection string (found in Project Settings > Database)
# Format: postgresql://postgres:[password]@[host]:[port]/postgres
SUPABASE_DB_URI=postgresql://postgres:your-password@db.your-project-id.supabase.co:5432/postgres
```

## Step 2: Get Your Supabase Credentials

### 2.1 Get SUPABASE_URL and SUPABASE_SERVICE_KEY:
1. Go to your Supabase project dashboard
2. Navigate to **Settings** → **API**
3. Copy the **Project URL** (this is your SUPABASE_URL)
4. Copy the **service_role** key (this is your SUPABASE_SERVICE_KEY)

### 2.2 Get SUPABASE_DB_URI:
1. In your Supabase dashboard, go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Select **URI** format
4. Copy the connection string and replace `[YOUR-PASSWORD]` with your database password
5. This becomes your SUPABASE_DB_URI

## Step 3: Update .env file

Replace the placeholder values in your `.env` file with the actual credentials you copied.

## Step 4: Test the Connection

After setting up the `.env` file, run:
```bash
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

## Security Note

- Never commit your `.env` file to version control
- The `.env` file should already be in your `.gitignore`
- Keep your service role key secure as it has full database access
