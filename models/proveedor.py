# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import logging
_logger = logging.getLogger(__name__)
class Proveedor (models.Model):
    _name = 'funeraria.proveedor'
    _description = "Datos del proveedor"
    cedula = fields.Integer("Cédula del proveedor", required=True, unique = True)
    name = fields.Char(string = "Nombres", required=True)
    last_name = fields.Char(string = "Apellidos", required=True)
    telefono = fields.Char(string = "Número de teléfono",required=True)
    direccion = fields.Text(string = "Dirección", required=True)
    photo = fields.Binary(string = "Foto del proveedor")

    def name_get(self):
        result = []
        for record in self:
            name = f"Cedula:{record.cedula} | Nombre:{record.name} {record.last_name}"
            result.append((record.id, name))
        return result
    def print_proveedor_report(self):
        return self.env.ref("funeraria_cruz.proveedor_report_test_action").report_action(self)

    def prueba_context(self):
        _logger.info(self.sudo().env.context.get('params')["id"])
        _logger.info("Ahora usando env: %s" %str(self.id))
    @api.model
    def default_get(self, fields_lis):
        records = super(Proveedor, self).default_get(fields_lis)
        records['direccion'] = 'Acarigua...'
        return records
    @api.model
    def _name_search(self, name ="", args=None, operator='ilike', limit=100, name_get_uid=None):
        # _logger.info(self._search([("name","ilike","ale")]))

        return self._search(["|","|",("name",operator,name),("last_name",operator,name),("cedula",operator,name)])

        # return self.env['funeraria.proveedor'].search([])
    def print_hello(self):
        price = self.env["funeraria.ataud"].browse(1)
        price.update({
            "cantidad": price.cantidad + 5
        })
        _logger.info(self.env["funeraria.proveedor"].search([])[0].name)
        _logger.info(self.ensure_one())
    @api.constrains('telefono','cedula')
    def validate(self):
        for record in self:
            if  not re.match(r'^(04|02)\d{2}\d{7}$', str(record.telefono)):
                raise ValidationError("El número de teléfono no es válido")
            if  len(str(record.cedula)) < 7:
                raise ValidationError("El número de cédula no es válido")
    @api.model
    def create(self,vals):
        if "name" in vals:
            vals["name"] = str(vals["name"]).title()
        if "last_name" in vals:
            vals["last_name"] = str(vals["last_name"]).title()
        if "direccion" in vals:
            vals["direccion"] = str(vals["direccion"]).capitalize() + "." if str(vals["direccion"])[-1] != "." else ""
        return super(Proveedor,self).create(vals)
    
            
