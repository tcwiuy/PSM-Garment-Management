# 🏭 PSM Garment Management - AI-Powered MES

Hệ thống Thực thi Sản xuất (MES - Manufacturing Execution System) dành riêng cho xưởng may mặc. Dự án tiên phong ứng dụng Trí tuệ Nhân tạo (AI Vision) để số hóa tự động quy trình chấm công và kiểm soát chất lượng từ bảng ghi chép viết tay của công nhân.

## 🌟 Điểm nổi bật của hệ thống
Hệ thống giải quyết bài toán nhập liệu thủ công tốn thời gian tại các xưởng may truyền thống bằng cách thiết lập một luồng tự động hóa hoàn toàn (End-to-End Automation):

* 🤖 **AI Vision OCR:** Đọc, hiểu và trích xuất dữ liệu từ giấy nháp viết tay của công nhân (Tên, Công đoạn, Số lượng Đạt/Lỗi, Loại lỗi) với độ chính xác cao bằng mô hình **Google Gemini**.
* ⚙️ **Tự động hóa luồng (Workflow):** Sử dụng **n8n** làm trái tim điều phối, nhận ảnh từ người dùng, gọi AI phân tích và đẩy dữ liệu vào Database.
* 📊 **Odoo ERP Dashboard:** Quản lý toàn diện Lệnh sản xuất (Production Order), Nhật ký MES, tính lương và trực quan hóa năng suất bằng biểu đồ (Graph/Pivot).
* 📲 **Real-time Feedback Loop:** Quản đốc chụp ảnh gửi qua **Telegram Bot** và nhận ngay tin nhắn phản hồi báo cáo kết quả nhập liệu thành công trong vài giây.

## 🏗️ Kiến trúc Hệ thống (System Architecture)


1. **Input:** Quản đốc xưởng may chụp ảnh tờ chấm công viết tay gửi vào Telegram Bot.
2. **Trigger:** Webhook của n8n bắt tín hiệu và tải bức ảnh về.
3. **AI Processing:** n8n gửi bức ảnh qua API của Google Gemini kèm theo Prompt kỹ thuật prompt engineering để AI nhận diện chữ viết và cấu trúc hóa thành định dạng JSON.
4. **ERP Integration:** n8n gọi API của Odoo, tìm kiếm Mã đơn hàng tương ứng và tự động tạo mới một bản ghi Nhật ký sản xuất (Production Log).
5. **Output:** n8n lấy ID kết quả từ Odoo, định dạng lại thành một tin nhắn báo cáo và gửi ngược về Telegram của Quản đốc.

## 💻 Công nghệ sử dụng (Tech Stack)
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
*(Ghi chú: Thêm hình ảnh Telegram Bot đang chat, hình ảnh n8n workflow và hình ảnh biểu đồ trong Odoo vào đây)*

---
*Dự án được phát triển nhằm mục đích tối ưu hóa quy trình quản lý xưởng may và ứng dụng công nghệ AI vào môi trường sản xuất thực tế.*
