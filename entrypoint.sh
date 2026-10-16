#!/bin/sh

ARG_1=$1

if [ -z "$ARG_1" ]; then
  echo "============================================"
  echo "========== FLASK PROJECT TEMPLATE =========="
  echo "============================================"

  printf "Enter your project name: "
  read -r INPUT_NAME

  APP_NAME=${INPUT_NAME:-main_app}
else
  APP_NAME=$ARG_1
fi

echo "Creating project $APP_NAME..."
mkdir -p "$APP_NAME"
cd $APP_NAME

echo "Copying template files..."
cp -ar /app/generator/flask-template/. .

echo "Setting up .env..."

cat << EOF > .env
DEBUG_MODE="True"
ALLOWED_HOSTS="*"
EOF

echo "Preparing repository and requirements.txt..."
pip freeze > requirements.txt
git init

echo "============================================"
echo "=== ✨ Flask project created successfully! ==="
echo "============================================"

echo "Go to your new project folder with 'cd $APP_NAME/'."
