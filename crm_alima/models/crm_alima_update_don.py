# -*- coding: utf-8 -*-
from array import *
from datetime import datetime, date
import base64
from datetime import date

from odoo import models, api, fields, _
from odoo.exceptions import UserError

STATES = [
    ('draft', 'A importer'),
    ('done', 'Importation Réussie'),
    ('cancel', 'Importation Annulé'),
]

SEPARATOR = [
    ('virgule', 'virgule'),
    ('point_virgule', 'point virgule'),
    ('pipe', 'pipe'),
]

CORRESPONDANCE = {
    'virgule':',',
    'point_virgule': ';',
    'pipe': '|',
}

class UpdateDon(models.Model):
    _name = 'crm.alima.update.don'
    _description = 'Update Don'

    name = fields.Char(string="Titre", required=True)
    description = fields.Text()
    datetime = fields.Datetime(readonly=True, string='Date import')
    separator = fields.Selection(SEPARATOR, default='virgule', required=True)
    nombre_de_dons_importes = fields.Integer(readonly=True)
    user_import = fields.Many2one('res.users', string="User", readonly=True)
    state = fields.Selection(STATES, default='draft', readonly=True)

    filename = fields.Char('File Name')
    data = fields.Binary('Import File')

    @api.multi
    def action_confirmer(self):
        if self.data and self.separator:
            try:
                data = base64.decodestring(self.data)
                separator = CORRESPONDANCE[self.separator]
                liste_data = [cell.split(separator) for cell in data.replace('\r', '').split("\n")]
                liste_data_remove_space = [[cell.strip() for cell in line] for line in liste_data]
                dicos = self.fusion(liste_data_remove_space)
                print dicos
            except:
                raise UserError(_("Erreur d'import, vérifier le séparateur et le fichier chargé"))
            for line in dicos:
                if 'id' in line and 'NumRecuFiscal' in line and line['id']:
                    try:
                        don = self.env['crm.alima.don'].browse(int(line['id']))
                    except:
                            raise UserError(_("not id %s"%line['id']))
                    if don:
                        try:
                            don.write({'NumRecuFiscal':line['NumRecuFiscal']})
                        except:
                            raise UserError(_("not id %s"%don))
                        

        self.state = 'done'
    
    @api.multi
    def action_annuler(self):
        self.state = 'cancel'

    @api.multi
    def action_reset_to_draft(self):
        self.state = 'draft'

    def fusion(self, liste):
        dicos = []
        for i in range(1,len(liste)):
            dicos.append(dict(zip(liste[0], liste[i])))
        return dicos
