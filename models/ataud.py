# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
from lxml import etree
_logger = logging.getLogger(__name__)
class Ataud(models.Model):
    _name = "funeraria.ataud"
    _description = "Datos del ataud"
    codigo = fields.Char(String = "Código del ataud", compute = "_generate_code", store=True)
    tipo = fields.Selection([("c","Cedro"),("p","Pino"),("m","Metal"),("cr","Cremación")],"Tipo de ataud")
    cantidad = fields.Integer(string="Cantidad disponible",required=True)
    precio = fields.Float(string = "Precio unitario")
    descripcion = fields.Text(string = "Descripción del ataud")
    exists_db = fields.Boolean(compute="_check_record_database")
    currency_id = fields.Many2one("res.currency")
    def open_wizard(self):
        return {
            "type":"ir.actions.act_window",
            "res_model":'ataud.update.price.wizard',
            "view_mode":"form",
            "target":"new"
        }
    @api.depends("exists_db")
    def _check_record_database(self):
        self.exists_db=self.env["funeraria.ataud"].browse(self.id).exists()
    def _get_ataud_string(self,tipo):
        ataud = {
            "c":"Cedro",
            "p":"Pino",
            "m":"Metal",
            "cr":"Cremación",
        }
        return ataud[tipo]
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        r = super(Ataud,self).fields_view_get(view_id, view_type, toolbar, submenu)
        if view_type == "form":
            doc = etree.XML(r["arch"])
            name_field = doc.xpath("//field[@name='descripcion']")
            if name_field:
                name_field[0].addnext(etree.Element("label",{"string":"Prueba etree"}))
                r["arch"] = etree.tostring(doc, encoding = "unicode")
        
        return r
    def name_get(self):
        return [(record.id, f"Código: {record.codigo} | Tipo: {record._get_ataud_string(record.tipo)}") for record in self]
    @api.depends('tipo')

    def _generate_code(self):
        for record in self:
            record.codigo = f"Ataud-{str(record.tipo).upper()}-{str(record.id).zfill(2)}"
    @api.model
    def default_get(self, fields_list):
        fields = super(Ataud,self).default_get(fields_list)
        fields["currency_id"] = self.env["res.currency"].search([("name","=","USD")])
        return fields