# 🏭 Garment Management - AI-Powered MES & ERP

Hệ thống Thực thi Sản xuất dành riêng cho xưởng may mặc. Dự án tiên phong ứng dụng Trí tuệ Nhân tạo để số hóa tự động quy trình chấm công và kiểm soát chất lượng từ bảng ghi chép viết tay của công nhân.

## 🌟 Điểm nổi bật của hệ thống
Hệ thống giải quyết bài toán nhập liệu thủ công tốn thời gian tại các xưởng may truyền thống bằng cách thiết lập một luồng tự động hóa hoàn toàn:

* 🤖 **AI Vision OCR:** Đọc, hiểu và trích xuất dữ liệu từ giấy nháp viết tay của công nhân (Tên, Công đoạn, Số lượng Đạt/Lỗi, Loại lỗi) với độ chính xác cao bằng mô hình **Google Gemini**.
* ⚙️ **Tự động hóa luồng:** Sử dụng **n8n** làm trái tim điều phối, nhận ảnh từ người dùng, gọi AI phân tích và đẩy dữ liệu vào Database.
* 📊 **Odoo ERP Dashboard:** Quản lý toàn diện Lệnh sản xuất, Nhật ký MES, tính lương và trực quan hóa năng suất bằng biểu đồ.
* 📲 **Real-time Feedback Loop:** Quản đốc chụp ảnh gửi qua **Telegram Bot** và nhận ngay tin nhắn phản hồi báo cáo kết quả nhập liệu thành công trong vài giây.

## 📋 Quy trình hoạt động của Lệnh Sản Xuất
Lệnh sản xuất (`psm.production.order`) là đối tượng trung tâm của module, quản lý toàn bộ vòng đời của một lô hàng từ khi lên kế hoạch đến khi hoàn thiện. Luồng nghiệp vụ được thiết kế chặt chẽ qua 3 trạng thái chính:

1. 📝 **Trạng thái Nháp - Lên Kế hoạch:**
   * Quản đốc tạo lệnh sản xuất mới, khai báo mã sản phẩm, số lượng cần may, loại vải và định mức nguyên phụ liệu.
   * Hệ thống tự động tính toán tổng nguyên liệu cần thiết (`total_material_needed`) dựa trên số lượng và định mức, giúp bộ phận kho chuẩn bị chính xác.
   * Cung cấp tính năng **"Xem trước bản in"** để xuất phiếu yêu cầu sản xuất giấy.

2. ⚙️ **Trạng thái Bắt đầu may - Thực thi MES:**
   * Khi quản đốc bấm nút **"Bắt đầu may"**, lệnh sản xuất chính thức được kích hoạt.
   * Lúc này, Lệnh sản xuất đóng vai trò là "Thùng chứa" để tiếp nhận dữ liệu thời gian thực từ Xưởng.
   * Thông qua Bot Telegram và AI Vision, dữ liệu chấm công từ giấy nháp của công nhân sẽ được tự động đẩy vào tab **Nhật ký MES & Tính lương** (`psm.production.log`) bên trong Lệnh sản xuất này. Hệ thống lập tức thống kê: Ai đang may công đoạn nào, đạt bao nhiêu cái, lỗi bao nhiêu cái, và tự động nhân đơn giá để ra tổng lương (`total_wage`).

3. ✅ **Trạng thái Hoàn thành - Đóng lệnh:**
   * Sau khi số lượng hàng đạt yêu cầu, quản đốc bấm **"Hoàn thành"** để khóa Lệnh sản xuất.
   * Dữ liệu từ Lệnh sản xuất này sẽ được trích xuất ra Dashboard để phân tích tỷ lệ lỗi, đánh giá năng suất chéo giữa các công nhân và làm căn cứ quyết toán lương cuối tháng.

## 🏗️ Kiến trúc Hệ thống


1. **Input:** Quản đốc xưởng may chụp ảnh tờ chấm công viết tay gửi vào Telegram Bot.
2. **Trigger:** Webhook của n8n bắt tín hiệu và tải bức ảnh về.
3. **AI Processing:** n8n gửi bức ảnh qua API của Google Gemini kèm theo Prompt kỹ thuật prompt engineering để AI nhận diện chữ viết và cấu trúc hóa thành định dạng JSON.
4. **ERP Integration:** n8n gọi API của Odoo, tìm kiếm Mã đơn hàng tương ứng và tự động tạo mới một bản ghi Nhật ký sản xuất.
5. **Output:** n8n lấy ID kết quả từ Odoo, định dạng lại thành một tin nhắn báo cáo và gửi ngược về Telegram của Quản đốc.

## 💻 Công nghệ sử dụng
* **ERP Framework:** Odoo 17 (Python, XML, PostgreSQL)
* **Automation Tool:** n8n (Node-based Workflow Automation)
* **AI Model:** Google Gemini 1.5/2.5 Flash (Multimodal & NLP)
* **Messaging API:** Telegram Bot API
* **Tunneling:** Ngrok (Dành cho môi trường phát triển cục bộ)

## 🚀 Cấu trúc Module Odoo
Module `psm_garment_training` được thiết kế theo hướng module hóa (Modular Design), bao gồm:
* `models/`: Định nghĩa các cấu trúc dữ liệu cho Lệnh sản xuất (`psm.production.order`) và Nhật ký MES (`psm.production.log`).
* `views/`: Chứa các file XML định nghĩa giao diện người dùng (Form, Tree, Graph, Pivot).
* Báo cáo thống kê năng suất tự động cập nhật theo thời gian thực (Real-time Dashboard).

## 📸 Hình ảnh minh họa (Screenshots)

