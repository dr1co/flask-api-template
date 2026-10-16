FROM python:3.12-slim

ENV ACCEPT_EULA=Y

WORKDIR /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  python3-dev \
  libssl-dev \
  libffi-dev \
  libgssapi-krb5-2 \
  wget \
  gnupg2 \
  ca-certificates \
  unixodbc-dev \
  lsb-release \
  && rm -rf /var/lib/apt/lists/*

RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg

RUN rm -f /etc/apt/sources.list.d/mssql-release.list \
  && rm -f /etc/apt/sources.list.d/mssql-tools.list

RUN echo "deb [arch=amd64] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-tools.list

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  msodbcsql17 \
  && rm -rf /var/lib/apt/lists/*

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.app:app"]