# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models,fields
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    separation_status = fields.Selection(
        string='Estado de Separación',
        selection=[('draft', 'Por Separar'), ('done', 'Separado')],default='draft'
    )



    def separation_status_done(self):
        for rec in self:
            rec.separation_status='done'

    def separation_status_draft(self):
        for rec in self:
            rec.separation_status='draft'
    
    def button_validate(self):
        relock = False
        if 'active_model' in self._context.keys():
            if self._context['active_model'] == 'sale.order' and self.move_type in ['direct'] and self.picking_type_id.code in ['outgoing']:
                sale = self.env[self._context['active_model']].browse(self._context['active_id'])
                sale._ztyres_check_account_status()
                if sale.state in ['done']:
                    sale.action_unlock()
                    relock = True
                if not sale.state in ['sale']:
                    raise UserError('No se puede realizar esta salida.\nLa el documento origen debe ser una Orden de Venta, por favor confirmelo antes.')
                if relock:
                    sale.action_done()

        elif self.move_type in ['direct'] and self.picking_type_id.code in ['outgoing']:
            self.sale_id._ztyres_check_account_status
            if self.sale_id.state in ['done']:                
                sale.action_unlock()
                relock = True
            if relock:
                sale.action_done()              
            if not self.sale_id.state in ['sale']:
                    raise UserError('No se puede realizar esta salida.\nEl documento origen %s debe ser una Orden de Venta, por favor confirmelo antes.'%(self.sale_id.name))

        return super(StockPicking, self).button_validate()