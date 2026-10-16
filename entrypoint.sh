#!/bin/sh

# Usage: entrypoint.sh [project-name] [--mssql | --no-mssql]
APP_NAME=""
MSSQL=""

for ARG in "$@"; do
  case "$ARG" in
    --mssql) MSSQL="y" ;;
    --no-mssql) MSSQL="n" ;;
    *) APP_NAME=$ARG ;;
  esac
done

echo "============================================"
echo "========== FLASK PROJECT TEMPLATE =========="
echo "============================================"

if [ -z "$APP_NAME" ]; then
  printf "Enter your project name: "
  read -r INPUT_NAME

  APP_NAME=${INPUT_NAME:-main_app}
fi

if [ -z "$MSSQL" ]; then
  if [ -t 0 ]; then
    while true; do
      printf "Include the MSSQL ODBC driver? [y/N]: "
      read -r INPUT_MSSQL

      case "$INPUT_MSSQL" in
        [yY]|[yY][eE][sS]) MSSQL="y"; break ;;
        ""|[nN]|[nN][oO]) MSSQL="n"; break ;;
        *) echo "Please answer y or n." ;;
      esac
    done
  else
    MSSQL="n"
  fi
fi

echo "Creating project $APP_NAME..."
mkdir -p "$APP_NAME"
cd $APP_NAME

echo "Copying template files..."
cp -ar /app/generator/flask-template/. .

if [ "$MSSQL" = "y" ]; then
  echo "Including MSSQL ODBC driver..."
  sed -i '/^# [<>]\{3\} mssql$/d' Dockerfile .env.example
else
  echo "Skipping MSSQL ODBC driver..."
  sed -i '/^# >>> mssql$/,/^# <<< mssql$/d' Dockerfile .env.example
fi

echo "Setting up .env..."

cat << EOF > .env
DEBUG_MODE="True"
ALLOWED_HOSTS="*"
EOF

echo "Preparing repository and requirements.txt..."
if [ "$MSSQL" = "y" ]; then
  pip freeze > requirements.txt
else
  pip freeze | grep -iv '^pyodbc==' > requirements.txt
fi
git init

echo "============================================"
echo "=== ✨ Flask project created successfully! ==="
echo "============================================"

echo "Go to your new project folder with 'cd $APP_NAME/'."
