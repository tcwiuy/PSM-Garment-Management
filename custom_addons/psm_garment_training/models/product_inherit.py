from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # 1. Phân loại vật tư cho xưởng may
    garment_type = fields.Selection([
        ('product', 'Thành phẩm (Áo/Quần)'),
        ('material', 'Nguyên phụ liệu (Vải/Chỉ)')
    ], string='Phân loại may mặc', default='product')

    # 2. Định mức cơ bản (BOM)
    bom_norm = fields.Float(string='Định mức vải (m/cái)', default=1.0)
    fabric_thickness = fields.Char(string='Độ dày vải (mm)')

    # 3. Quản lý Kho (Thêm dòng này)
    current_stock = fields.Float(string='Tồn kho hiện tại', default=0.0)