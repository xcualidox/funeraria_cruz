from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
class CompraAtaud(models.Model):
    _name = "ataud.compra"
    _description = "Compra de ataudes"
    ataud_id = fields.Many2one("funeraria.ataud",string = "Ataud",required=True)
    precio = fields.Float(string="Precio unitario",required=True)
    cantidad = fields.Integer(string="Cantidad",required=True)
    proveedor_id = fields.Many2one("funeraria.proveedor",required=True)
    proveedor_tel = fields.Char(related='proveedor_id.telefono')
    descuento = fields.Boolean(string="Descuento 10%",compute = "_calculate_total", store=True)
    total = fields.Float(string="Total (mayor a 12 unidades tiene descuento del 10%", compute="_calculate_total",default = False ,store=True , currency_field = "currency_id")
    notes = fields.Text(string="Observaciones")
    exists_db = fields.Boolean(compute="_check_record_database")
    purchase_date = fields.Char(string = "Fecha de compra", compute = "_format_date")
    purchase_code = fields.Char(string="Codigo de compra", compute = "_generate_code",unique=True ,store=True)
    currency_id = fields.Many2one("res.currency")
    @api.depends("purchase_date", "create_date")
    def _format_date(self):
        for record in self:
            fecha_original = record.create_date
            # fecha_objeto = datetime.strptime(fecha_original, "%Y-%m-%d %H:%M:%S.%f")
            record.purchase_date = fecha_original.strftime("%d/%m/%Y a las %H:%M")
    @api.depends("exists_db")
    def _check_record_database(self):
        self.exists_db=self.env["ataud.compra"].browse(self.id).exists()
    @api.depends("cantidad","precio")
    def _calculate_total(self):
        for record in self:
            if record.cantidad > 12:
                record.total = (record.cantidad * record.precio) - ((record.cantidad * record.precio) * 0.1)
                record.descuento = True
                return True
            record.total = record.cantidad * record.precio
            record.descuento = False
            return False
    @api.depends("ataud_id")
    def _generate_code(self):
        self.purchase_code = f'{self.ataud_id.codigo}-{str(self.id).zfill(2)}'

    @api.model 
    def default_get(self, fields_list):
        records = super(CompraAtaud,self).default_get(fields_list)
        records['notes'] = "Compra de ataud"
        records['ataud_id'] = self.env["funeraria.ataud"].search([],limit = 1)
        records['currency_id'] = self.env["res.currency"].search([("name","=","USD")], limit = 1)
        return records
    @api.model
    def create(self,vals):
        record = super(CompraAtaud, self).create(vals)
        if record :
            # record.ataud_id
            ataud = self.env["funeraria.ataud"].browse(record.ataud_id.id)
            ataud.update({
                "cantidad" : ataud.cantidad + record.cantidad
            })
            return record
        return False
            
