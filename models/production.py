from odoo import models, fields, api

class GarmentProduction(models.Model):
    _name = 'psm.production.order'
    _description = 'Lệnh sản xuất may mặc'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Mã đơn hàng', required=True, copy=False, readonly=True, default='Mới')
    product_id = fields.Many2one('product.product', string='Sản phẩm may')     
    # Trường liên đới: Tự động lấy fabric_thickness từ product_id ra
    fabric_thickness = fields.Char(related='product_id.fabric_thickness', string='Độ dày vải (mm)')
    quantity = fields.Integer(string='Số lượng (cái)', default=100)

    # --- THÊM PHẦN NÀY ---
    fabric_needed = fields.Float(string='Tổng vải cần (mét)', compute='_compute_fabric_needed', store=True)

    @api.depends('quantity')
    def _compute_fabric_needed(self):
        for record in self:
            # Giả sử định mức: 1 sản phẩm cần 1.5 mét vải
            record.fabric_needed = record.quantity * 1.5
    # ---------------------

    start_date = fields.Date(string='Ngày bắt đầu', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirm', 'Đang may'),
        ('done', 'Hoàn thành'),
    ], string='Trạng thái', default='draft', tracking=True)

    # Hàm chuyển trạng thái sang Đang may
    def action_confirm(self):
        for record in self:
            record.state = 'confirm'

    # Hàm chuyển trạng thái sang Hoàn thành
    def action_done(self):
        for record in self:
            record.state = 'done'
    
    # Hàm mở tab xem trước báo cáo
    def action_preview_report(self):
        self.ensure_one() # Đảm bảo chỉ thao tác trên 1 đơn hàng hiện tại
        return {
            'type': 'ir.actions.act_url',
            'target': 'new', # Lệnh mở sang một Tab mới trên trình duyệt
            'url': '/report/html/psm_garment_training.report_production_order_template/%s' % self.id,
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Nếu người dùng chưa nhập mã (đang là chữ 'Mới')
            if vals.get('name', 'Mới') == 'Mới':
                # Xin Odoo cấp 1 mã số mới dựa vào code 'psm.production.order'
                vals['name'] = self.env['ir.sequence'].next_by_code('psm.production.order')
        
        # Gọi lại hàm create gốc của Odoo để lưu vào Database
        return super().create(vals_list)