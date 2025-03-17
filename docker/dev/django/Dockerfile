FROM python:3.12-slim

LABEL maintainer="Mohammadroudbari2@gmail.com"

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ایجاد و تنظیم کاربر غیر root
RUN groupadd -r django && useradd -r -g django django

# تنظیم دایرکتوری کاری
WORKDIR /usr/src/app

# کپی و نصب requirements
COPY requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# کپی کد پروژه
COPY ./core/ .

# تغییر مالکیت فایل‌ها به کاربر django
RUN chown -R django:django /usr/src/app

# تغییر به کاربر غیر root
USER django

# مشخص کردن پورت
EXPOSE 8000

# دستور اجرای برنامه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# collecting static files
CMD python3 manage.py collectstatic --no-input