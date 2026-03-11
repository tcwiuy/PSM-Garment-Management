{
    'name': 'PSM Garment Management',
    'version': '1.0',
    'summary': 'Quản lý sản xuất may mặc PSM',
    'description': """
    Module được xây dựng trong quá trình thực tập, bao gồm các tính năng:
    - Quản lý Lệnh sản xuất (Production Order).
    - Tự động tính toán định mức vải.
    - Tích hợp quy trình Workflow & Chatter.
    - Báo cáo PDF & Mã tự động (Sequence).
    """,
    'author': 'Minh',
    'category': 'Manufacturing',
    'depends': ['base', 'product', 'mail'],    
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/production_view.xml',
        'views/product_inherit_view.xml',
        'report/production_report.xml',
    ],
    'installable': True,
    'application': True,
}