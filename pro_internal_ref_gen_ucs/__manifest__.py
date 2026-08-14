{
    'name': 'Product Internal Reference Generator UCS | Automated Product Reference | Product Code Automation | Smart Product Code Generator | Product Ref Pro',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Auto Generate Internal Reference for Products and Variants at Product, Category, and Company level',
    'description': """
Product Internal Reference Generator
====================================
Automate creation of product internal references (default_code) in Odoo 18.
Key Features:
- Configure reference sequence per Company or per Product Category.
- Auto-generate reference on product template or variant creation.
- Manual reference override protection toggle per product.
- Bulk internal reference generator wizard for existing products.
- Product variant attribute reference formatting.
""",
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/res_company_views.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'wizard/ref_generator_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'website': 'https://uncannycs.com',
    'author': 'Uncanny Consulting Services LLP',
    'maintainer': 'Uncanny Consulting Services LLP',
    'license': 'Other proprietary',
    "images": ['static/description/banner.gif'],
    "price": 40,
    "currency": "USD",
}
