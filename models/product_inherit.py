from odoo import models, fields

class ProductTemplate(models.Model):
    # Dùng _inherit để nối thêm vào bảng gốc của Odoo thay vì tạo bảng mới (_name)
    _inherit = 'product.template'

    # Thêm trường dữ liệu mới
    fabric_thickness = fields.Char(string='Độ dày vải (mm)')