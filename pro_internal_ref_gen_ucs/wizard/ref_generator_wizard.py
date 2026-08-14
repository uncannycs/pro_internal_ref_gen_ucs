from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProInternalRefGenWizard(models.TransientModel):
    _name = 'pro.internal.ref.gen.wizard'
    _description = 'Product Internal Reference Generator Wizard'

    category_ids = fields.Many2many(
        'product.category',
        string='Product Categories',
        help='Select product categories to generate references for. Leave empty for all categories.',
    )
    product_ids = fields.Many2many(
        'product.template',
        string='Specific Products',
        help='Select specific product templates to generate references for. Leave empty to use category selection.',
    )
    only_missing = fields.Boolean(
        string='Only Missing References',
        default=True,
        help='If checked, references will only be generated for products that currently do not have an internal reference.',
    )
    overwrite_existing = fields.Boolean(
        string='Overwrite Existing References',
        default=False,
        help='If checked, existing internal references will be overwritten with new ones.',
    )

    @api.onchange('overwrite_existing')
    def _onchange_overwrite_existing(self):
        if self.overwrite_existing:
            self.only_missing = False

    @api.onchange('only_missing')
    def _onchange_only_missing(self):
        if self.only_missing:
            self.overwrite_existing = False

    def action_generate_references(self):
        """Perform bulk reference generation on targeted products."""
        self.ensure_one()
        domain = []

        if self.product_ids:
            domain.append(('id', 'in', self.product_ids.ids))
        elif self.category_ids:
            domain.append(('categ_id', 'child_of', self.category_ids.ids))

        if self.only_missing and not self.overwrite_existing:
            domain.append(('default_code', '=', False))

        templates = self.env['product.template'].search(domain)
        if not templates:
            raise UserError(_("No matching products found for the specified criteria."))

        updated_count = 0
        for template in templates:
            if not template.auto_generate_code:
                continue

            if self.overwrite_existing or not template.default_code:
                ref = template._get_next_internal_reference()
                if ref:
                    template.default_code = ref
                    template._generate_variant_internal_references()
                    updated_count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Bulk Reference Generation Completed'),
                'message': _('Successfully generated internal reference for %d product(s).') % updated_count,
                'sticky': False,
                'type': 'success',
            }
        }
