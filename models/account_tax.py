from odoo import _, api, exceptions, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def get_avalara_tax(self, tax_rate, doc_type):
        # Overwrite method from OCA/account-fiscal-rule/account_avatax
        domain = self._get_avalara_tax_domain(tax_rate, doc_type)
        tax = self.with_context(active_test=False).search(domain, limit=1)
        if tax and not tax.active:
            tax.active = True
        if not tax:
            domain = self._get_avalara_tax_domain(0, doc_type)
            tax_template = self.search(domain, limit=1)
            if not tax_template:
                raise exceptions.UserError(
                    _("Please configure Avatax Tax for Company %s:")
                    % self.env.company.name
                )
            # If you get a unique constraint error here,
            # check the data for your existing Avatax taxes.
            vals = {
                "amount": tax_rate,
                "name": "AVATAX", #self._get_avalara_tax_name(tax_rate, doc_type),
            }
            tax = tax_template.sudo().copy(default=vals)
            # Odoo core does not use the name set in default dict
            tax.name = vals.get("name")
        return tax
