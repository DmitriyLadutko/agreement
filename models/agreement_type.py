# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models


class AgreementType(models.Model):
    _name = 'agreement.type'
    _description = 'agreement type'

    name = fields.Char(
        string='Name',
        required=True,
        index=True,
        tracking=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This type of agreement already exists!'),
    ]
