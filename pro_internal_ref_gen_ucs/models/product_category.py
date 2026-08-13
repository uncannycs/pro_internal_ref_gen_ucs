from odoo import fields, models, _
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    use_category_sequence = fields.Boolean(
        string='Use Category Specific Reference Sequence',
        default=False,
        help='If enabled, products in this category will generate internal references using this category sequence/prefix.',
    )
    sequence_id = fields.Many2one(
        'ir.sequence',
        string='Category Reference Sequence',
        help='Sequence used specifically for products in this category.',
    )
    code_prefix = fields.Char(
        string='Category Code Prefix',
        help='Prefix added before the generated sequence number (e.g. ELEC-).',
    )
    code_suffix = fields.Char(
        string='Category Code Suffix',
        help='Suffix added after the generated sequence number (e.g. -PRD).',
    )

    def action_generate_category_references(self):
        """Action button to trigger reference generation for all products in this category."""
        self.ensure_one()
        templates = self.env['product.template'].search([('categ_id', '=', self.id)])
        if not templates:
            raise UserError(_("No products found in category '%s'.") % self.name)
        
        count = 0
        for template in templates:
            if template.auto_generate_code:
                template.action_generate_internal_reference()
                count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Reference Generation Complete'),
                'message': _('Generated internal reference for %d products in category %s.') % (count, self.name),
                'sticky': False,
                'type': 'success',
            }
        }
