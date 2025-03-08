# Sử dụng image Python chính thức làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép toàn bộ mã nguồn và dữ liệu
COPY . .

# Tạo thư mục static/uploads nếu chưa có
RUN mkdir -p static/uploads

# Cài đặt các thư viện cần thiết trực tiếp
RUN pip install --no-cache-dir flask==2.3.2 werkzeug==2.3.6

# Mở cổng 5000 (cổng mặc định của Flask)
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app.py"]