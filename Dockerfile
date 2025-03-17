# Stage 1 - Build dependencies
FROM python:3.12-slim as builder

# نصب پکیج‌های مورد نیاز برای کامپایل
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی و نصب requirements
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Stage 2 - Final image
FROM python:3.12-slim

LABEL maintainer="Mohammadroudbari2@gmail.com"

# نصب پکیج‌های مورد نیاز در محیط تولید
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ایجاد و تنظیم کاربر غیر root
RUN groupadd -r django && useradd -r -g django django

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=core.settings.prod

# تنظیم دایرکتوری کاری
WORKDIR /usr/src/app

# کپی wheels از مرحله قبل و نصب آنها
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder requirements.txt .
RUN pip install --no-cache /wheels/*

# کپی کد پروژه
COPY ./core/ .

# تغییر مالکیت فایل‌ها به کاربر django
RUN chown -R django:django /usr/src/app

# تغییر به کاربر غیر root
USER django

# مشخص کردن پورت
EXPOSE 8000

# اجرای دستورات نهایی
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]