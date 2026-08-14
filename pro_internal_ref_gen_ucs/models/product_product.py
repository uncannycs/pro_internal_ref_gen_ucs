from odoo import api, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        for product in products:
            company = product.company_id or product.product_tmpl_id.company_id or self.env.company
            if company.auto_generate_ref and company.ref_generation_policy in ['on_create', 'on_write']:
                if product.product_tmpl_id.auto_generate_code and not product.default_code:
                    product.action_generate_internal_reference()
        return products

    def action_generate_internal_reference(self):
        """Manual action button to generate variant internal reference."""
        for product in self:
            company = product.company_id or self.env.company
            pattern = company.ref_variant_pattern or 'template_sequence'

            if pattern == 'attribute_suffix':
                if not product.product_tmpl_id.default_code:
                    tmpl_ref = product.product_tmpl_id._get_next_internal_reference()
                    if tmpl_ref:
                        product.product_tmpl_id.default_code = tmpl_ref
                if product.product_tmpl_id.default_code:
                    attr_codes = [ptav.name for ptav in product.product_template_attribute_value_ids if ptav.name]
                    if attr_codes:
                        product.default_code = f"{product.product_tmpl_id.default_code}-" + "-".join(attr_codes)
                    else:
                        product.default_code = product.product_tmpl_id.default_code
            else:
                ref = product.product_tmpl_id._get_next_internal_reference()
                if ref:
                    product.default_code = ref
        return True
