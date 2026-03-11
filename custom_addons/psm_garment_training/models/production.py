from odoo import models, fields, api

class GarmentProduction(models.Model):
    _name = 'psm.production.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Lệnh sản xuất may mặc'

    name = fields.Char(string='Mã đơn hàng', required=True, copy=False, readonly=True, default='Mới')
    
    # 1. Liên kết Thành phẩm (Chỉ cho phép chọn các mã có garment_type là 'product')
    product_id = fields.Many2one(
        'product.product', 
        string='Sản phẩm cần may', 
        domain="[('garment_type', '=', 'product')]", 
        required=True
    )
    
    fabric_thickness = fields.Char(related='product_id.fabric_thickness', string='Độ dày vải (mm)')
    quantity = fields.Integer(string='Số lượng đặt may (cái)', default=100, tracking=True)

    # 2. Liên kết Nguyên liệu (Chỉ cho phép chọn các mã có garment_type là 'material')
    material_id = fields.Many2one(
        'product.product', 
        string='Loại vải sử dụng', 
        domain="[('garment_type', '=', 'material')]"
    )

    # 3. Tự động "kéo" định mức từ hồ sơ sản phẩm gốc ra đây
    bom_norm = fields.Float(related='product_id.bom_norm', string='Định mức vải (m/cái)', readonly=True)

    # 4. Hàm tự động tính tổng mét vải cần xuất kho
    total_material_needed = fields.Float(string='Tổng vải dự kiến (m)', compute='_compute_total_material', store=True)

    start_date = fields.Date(string='Ngày bắt đầu', default=fields.Date.today)
    
    # Cập nhật thêm trạng thái "Đang cắt vải"
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('cutting', 'Đang cắt vải'),
        ('sewing', 'Đang may'),
        ('done', 'Hoàn thành')
    ], string='Trạng thái', default='draft', tracking=True)

    # Liên kết với bảng Nhật ký (1 Lệnh sản xuất có nhiều dòng nhật ký)
    log_ids = fields.One2many('psm.production.log', 'production_id', string='Nhật ký năng suất')

    @api.depends('quantity', 'bom_norm')
    def _compute_total_material(self):
        for order in self:
            order.total_material_needed = order.quantity * order.bom_norm
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
        for order in self:
            # 1. Kiểm tra xem có chọn vải chưa
            if not order.material_id:
                raise models.ValidationError("Vui lòng chọn Loại vải sử dụng trước khi Hoàn thành lệnh may!")

            # 2. TRỪ KHO NGUYÊN LIỆU (Vải)
            # Lấy tồn kho hiện tại trừ đi tổng vải dự kiến
            order.material_id.current_stock -= order.total_material_needed
            
            # 3. CỘNG KHO THÀNH PHẨM (Áo)
            order.product_id.current_stock += order.quantity

            # 4. Chuyển trạng thái sang Hoàn thành
            order.state = 'done'
    
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

class GarmentProductionLog(models.Model):
    _name = 'psm.production.log'
    _description = 'Nhật ký năng suất công nhân (MES)'

    production_id = fields.Many2one('psm.production.order', string='Lệnh Sản Xuất', ondelete='cascade')
    worker_name = fields.Char(string='Tên công nhân', required=True)
    date = fields.Date(string='Ngày ghi nhận', default=fields.Date.context_today)
    
    # 1. Bổ sung Công đoạn (Operation)
    operation = fields.Selection([
        ('cut', 'Cắt vải'),
        ('collar', 'May cổ (Collar)'),
        ('sleeve', 'May tay (Sleeve)'),
        ('body', 'May thân (Body)'),
        ('assemble', 'Ráp áo'),
        ('qc', 'Kiểm tra QC'),
        ('pack', 'Đóng gói')
    ], string='Công đoạn', required=True, default='collar')

    # 2. Tách bạch Sản lượng Đạt và Lỗi
    good_qty = fields.Integer(string='Sản phẩm ĐẠT', required=True, default=0)
    defect_qty = fields.Integer(string='Sản phẩm LỖI', default=0)

    # 3. Phân loại Lỗi (Defect Type) để tính DHU
    defect_type = fields.Selection([
        ('none', 'Không có lỗi'),
        ('broken_stitch', 'Đứt chỉ / Lỗi đường may'),
        ('fabric', 'Lỗi vải / Rách'),
        ('size', 'Sai lệch kích thước'),
        ('dirt', 'Bẩn / Lem màu')
    ], string='Loại lỗi', default='none')

    # Đơn giá sẽ thay đổi tùy theo Công đoạn (may cổ khác may tay)
    unit_price = fields.Float(string='Đơn giá (VNĐ)', default=5000.0)
    total_wage = fields.Float(string='Thành tiền (VNĐ)', compute='_compute_total_wage', store=True)

    @api.depends('good_qty', 'unit_price')
    def _compute_total_wage(self):
        for log in self:
            # QUAN TRỌNG: Công nhân chỉ được trả tiền cho Sản phẩm ĐẠT
            log.total_wage = log.good_qty * log.unit_price