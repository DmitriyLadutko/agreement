# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _


class Agreement(models.Model):
    _name = 'agreement.agreement'
    _description = 'Agreement'

    number = fields.Char(
        string='Number',
        readonly=True,
        copy=False,
        tracking=True,
        default=lambda self: _('New'),
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Client',
        required=True,
    )
    kind_id = fields.Many2one(
        comodel_name='agreement.type',
        string='Agreement Type',
        required=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed')],
        string='Status',
        required=True,
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
    )
    author_id = fields.Many2one(
        comodel_name='res.users',
        string='Author',
        required=True,
        default=lambda self: self.env.user,
    )
    field_for_attrs = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ],
        compute='_compute_field_for_attrs',
    )

    @api.model
    def create(self, vals):
        if vals.get('number', _('New')) == _('New'):
            vals['number'] = self.env['ir.sequence'].next_by_code('agreement.agreement') or _('New')
        res = super(Agreement, self).create(vals)
        return res

    @api.depends('author_id', 'state')
    def _compute_field_for_attrs(self):
        """ A method to calculate the field that is used in the field attributes """
        uid = self.env.context.get('uid', False)
        agreement_manager = self.env['res.users'].browse(uid)
        for rec in self:
            if uid == rec.author_id.id and rec.state == 'draft':
                rec.field_for_attrs = '1'
            elif agreement_manager.has_group('agreement.group_agreement_manager') and rec.state == 'approved':
                rec.field_for_attrs = '2'
            else:
                rec.field_for_attrs = '3'

    def action_send_for_approval(self):
        for rec in self:
            if rec.state != 'approved':
                rec.write({'state': 'approved'})

    def action_agree(self):
        for rec in self:
            if rec.state != 'active':
                rec.write({'state': 'active'})

    def action_send_for_revision(self):
        """A method for changing the agreement status and sending a notification about it"""
        template = self.env.ref('agreement.email_template_for_revision_notification', False)
        subject = f'The agreement {self.number} has been sent back for revision'
        email_to = self.author_id.email
        body_html = f'<p>Dear {self.author_id.name}!</p> The agreement {self.number} has been sent back for revision'
        if template:
            for rec in self:
                rec.write({'state': 'draft'})
                template.send_mail(
                    res_id=rec.id,
                    force_send=True,
                    email_values={
                        'subject': subject,
                        'body_html': body_html,
                        'email_to': email_to}
                )

    def _cron_update_expired_agreements(self):
        """ A method to perform the cron task of updating the status of expired agreements """
        current_date = datetime.today().date()  # get the current date
        # look for agreements with an expiration date later than the current one and the status "Active"
        agreements_to_update = self.search([('state', '=', 'active'), ('end_date', '>', current_date)])
        # change the status of found agreements
        if agreements_to_update:
            agreements_to_update.write({'state': 'completed'})
        return True
