# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api,exceptions,_
from openerp.exceptions import  except_orm 

class link_customer(models.Model):

    _name = 'link'
    name=fields.Many2one('res.partner',"Client")
    partner_id=fields.Many2one('res.partner')
    
    @api.model
    def create(self, values):
       
        vals = { 'name' : values['partner_id'],
                 'partner_id':values['name'],
            }
        record=super(link_customer, self).create(values)
       
        if not self.env['link.supplier'].search([('name','=',record.partner_id.id),('partner_id','=',record.name.id)]):
            self.env['link.supplier'].create(vals)
        return record
    @api.multi
    def unlink(self):
       
        search_ids=self.env['link.supplier'].search([('name','=',self.partner_id.id),('partner_id','=',self.name.id)])
        record=super(link_customer, self).unlink()
        if search_ids:
            search_ids[0].unlink()
        return record
    @api.multi
    def write(self,values):
        partner_old=self.name.id
        partner_new=values['name']
        if partner_old != partner_new:
            raise except_orm(_('SVP !!'), _("Tu ne peux pas modifier un client de la liste vente mais tu peux le supprimer"))


       

class link_supplier(models.Model):

    _name = 'link.supplier'
    name=fields.Many2one('res.partner',"Fournisseur")
    partner_id=fields.Many2one('res.partner')
    
    @api.model
    def create(self, values):
      
        vals = { 'name' : values['partner_id'],
                 'partner_id':values['name'],
            }
        record=super(link_supplier, self).create(values)
        if not self.env['link.customer'].search([('name','=',record.partner_id.id),('partner_id','=',record.name.id)]):
            self.env['link.customer'].create(vals)
        return record
    @api.multi
    def unlink(self):
        search_id = self.env['link.customer'].search([('name','=',self.partner_id.id),('partner_id','=',self.name.id)])
        record=super(link_supplier, self).unlink()
        if search_id:
            search_id[0].unlink()
        return record
    @api.multi
    def write(self,values):
        partner_old=self.name.id
        partner_new=values['name']
       
        if partner_old != partner_new:
            raise except_orm(_('SVP !!'), _("Tu ne peux pas modifier un fournisseur de la liste achat mais tu peux le supprimer"))

class res_partner(models.Model):

    _inherit = 'res.partner'
   
    customer_ids=fields.One2many('link.customer','partner_id',string="Vente")
    supplier_ids=fields.One2many('link.supplier','partner_id',string="Achat")
