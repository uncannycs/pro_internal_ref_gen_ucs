from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_generate_ref = fields.Boolean(
        string='Auto Generate Product Internal Reference',
        default=True,
        help='Automatically generate internal reference code for new products.',
    )
    ref_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Default Product Reference Sequence',
        help='Sequence used to generate default internal references for products when no category sequence is defined.',
    )
    ref_generation_policy = fields.Selection(
        [
            ('on_create', 'On Product Creation'),
            ('on_write', 'On Creation and Category Change'),
            ('manual', 'Manual Only'),
        ],
        string='Reference Generation Policy',
        default='on_create',
        help='Determines when the internal reference number should be automatically generated.',
    )
    ref_override_existing = fields.Boolean(
        string='Override Existing Reference',
        default=False,
        help='If checked, auto-generation will overwrite existing internal reference codes on products.',
    )
    ref_variant_pattern = fields.Selection(
        [
            ('template_sequence', 'Unique Sequence per Variant'),
            ('attribute_suffix', 'Template Reference + Attribute Suffix'),
        ],
        string='Variant Reference Format Pattern',
        default='template_sequence',
        help='Select how internal references are generated for product variants.',
    )
