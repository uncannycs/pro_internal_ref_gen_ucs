from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    auto_generate_code = fields.Boolean(
        string='Auto Generate Internal Reference',
        default=True,
        help='If checked, internal reference for this product will be automatically generated according to configuration.',
    )

    def _get_next_internal_reference(self):
        """Compute next internal reference using category sequence or company default sequence.
        Traverses parent category hierarchy if the direct category has no sequence configured.
        """
        self.ensure_one()
        company = self.company_id or self.env.company
        categ = self.categ_id

        sequence = False
        prefix = ''
        suffix = ''

        # Traverse category hierarchy upward to find a configured sequence
        current_categ = categ
        while current_categ:
            if current_categ.use_category_sequence and current_categ.sequence_id:
                sequence = current_categ.sequence_id
                prefix = current_categ.code_prefix or ''
                suffix = current_categ.code_suffix or ''
                break
            current_categ = current_categ.parent_id

        # Fallback to Company level configuration if no category sequence found
        if not sequence and company.ref_sequence_id:
            sequence = company.ref_sequence_id

        if not sequence:
            # Last resort: search for the default sequence by code
            sequence = self.env['ir.sequence'].search(
                [('code', '=', 'product.internal.reference')], limit=1
            )

        if sequence:
            seq_code = sequence.next_by_id() or ''
            return f"{prefix}{seq_code}{suffix}"

        return False

    def action_generate_internal_reference(self):
        """Manual action button to generate internal reference."""
        for template in self:
            ref = template._get_next_internal_reference()
            if ref:
                template.default_code = ref
                # Process variants
                template._generate_variant_internal_references()
        return True

    def _generate_variant_internal_references(self):
        """Generate variant internal references according to company policy pattern."""
        self.ensure_one()
        company = self.company_id or self.env.company
        pattern = company.ref_variant_pattern or 'template_sequence'

        if len(self.product_variant_ids) == 1:
            self.product_variant_ids[0].default_code = self.default_code
            return

        for variant in self.product_variant_ids:
            if pattern == 'attribute_suffix' and self.default_code:
                # Format: Template_Ref-AttrVal1-AttrVal2
                attr_codes = [ptav.name for ptav in variant.product_template_attribute_value_ids if ptav.name]
                if attr_codes:
                    variant.default_code = f"{self.default_code}-" + "-".join(attr_codes)
                else:
                    variant.default_code = self.default_code
            else:
                # template_sequence: generate unique sequence per variant if missing
                if company.ref_override_existing or not variant.default_code:
                    var_ref = self._get_next_internal_reference()
                    if var_ref:
                        variant.default_code = var_ref

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            company = template.company_id or self.env.company
            if company.auto_generate_ref and company.ref_generation_policy in ['on_create', 'on_write']:
                if template.auto_generate_code:
                    if company.ref_override_existing or not template.default_code:
                        ref = template._get_next_internal_reference()
                        if ref:
                            template.default_code = ref
                            template._generate_variant_internal_references()
        return templates

    def write(self, vals):
        res = super().write(vals)
        if 'categ_id' in vals:
            for template in self:
                company = template.company_id or self.env.company
                if company.auto_generate_ref and company.ref_generation_policy == 'on_write':
                    if template.auto_generate_code:
                        if company.ref_override_existing or not template.default_code:
                            ref = template._get_next_internal_reference()
                            if ref:
                                template.default_code = ref
                                template._generate_variant_internal_references()
        return res
