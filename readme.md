### Distributed System - Schiper-Eggli-Sandoz Algorithm
Đồng bộ đồng hồ là một yếu tố quan trọng để hệ thống phân tán có thể hoạt
động đúng, có thứ tự và tổ chức. Có hai loại đồng hộ là đồng hồ vật lý và đồng
hộ logic. Đồng bộ đồng hộ vật lý là điều vô cùng khó khăn và gần như không thể
đạt được độ chính xác tuyệt đối. Do đó, đồng hồ logic được tạo ra như một bộ
đánh số các sự kiện xảy ra, đảm bảo tính thứ tự hay quan hệ giữa các sự kiện.
Có rất nhiều cấu trúc dữ liệu và giao thức để mô tả và cập nhật đồng hộ giữa
các nút trong hệ thống, trong đó Schiper-Eggli-Sandoz (SES) là một giao thức
đơn giản nhưng hiệu quả để mô tả đồng hồ, đảm bảo quan hệ nhân quả của các
sự kiện xảy ra trên các máy tính trong hệ thống. 

Để chạy chương trình: 

* Bước 1: Mở thư mục chứa chương trình.
* Bước 2: Chạy bằng lệnh
```sudo bash ./run.sh <số-process-cần-chạy>```
* Bước 3: Quan sát log nhận tin trên màn hình, hoặc quan sát rõ các log trong
thư mục ./static/log.
* Bước 4: Tắt chương trình bằng "Ctrl+C", cần tắt thủ công từng process,
chương trình đã xử lí được việc một process ngừng hoạt động và thực hiện
việc đóng các kết nối, giải phóng port,...

Chi tiết về chương trình trong file "./Distributed_System_Report_01.pdf"