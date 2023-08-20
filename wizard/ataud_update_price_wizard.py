# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ataud_update_price_wizard(models.TransientModel):
    _name = "ataud.update.price.wizard"
    update_precio = fields.Float(string = "Precio unitario")
    def update_price(self):
        self.env["funeraria.ataud"].browse(self._context.get("active_ids")).update({"precio": self.update_precio})
        return True
