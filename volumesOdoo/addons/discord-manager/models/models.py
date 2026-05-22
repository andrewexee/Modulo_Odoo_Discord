# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class DiscordServer(models.Model):
    _name = 'discord.manager.server'
    _description = 'Servidor de Discord'

    name = fields.Char(required=True)
    guild_id = fields.Char(string='Guild ID')
    description = fields.Text()
    active = fields.Boolean(default=True)
    channel_ids = fields.One2many('discord.manager.channel', 'server_id', string='Canales')
    webhook_ids = fields.One2many('discord.manager.webhook', 'server_id', string='Webhooks')
    message_count = fields.Integer(string='Mensajes', compute='_compute_message_count')

    @api.depends('channel_ids')
    def _compute_message_count(self):
        for server in self:
            server.message_count = self.env['discord.manager.message'].search_count([
                ('server_id', '=', server.id),
            ])

    def action_open_channels(self):
        self.ensure_one()
        action = self.env.ref('discord_manager.action_discord_channel_tree').read()[0]
        action['domain'] = [('server_id', '=', self.id)]
        return action


class DiscordChannel(models.Model):
    _name = 'discord.manager.channel'
    _description = 'Canal de Discord'

    name = fields.Char(required=True)
    channel_id = fields.Char(string='Channel ID')
    channel_type = fields.Selection(
        [
            ('text', 'Texto'),
            ('voice', 'Voz'),
            ('category', 'Categoría'),
        ],
        string='Tipo de canal',
        default='text',
        required=True,
    )
    server_id = fields.Many2one('discord.manager.server', string='Servidor', ondelete='cascade', required=True)
    message_ids = fields.One2many('discord.manager.message', 'channel_id', string='Mensajes')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('discord_channel_unique', 'unique(server_id, channel_id)', 'El canal debe ser único dentro del servidor.'),
    ]


class DiscordWebhook(models.Model):
    _name = 'discord.manager.webhook'
    _description = 'Webhook de Discord'

    name = fields.Char(required=True)
    webhook_url = fields.Char(string='URL del Webhook', required=True)
    server_id = fields.Many2one('discord.manager.server', string='Servidor', ondelete='cascade')
    channel_id = fields.Many2one('discord.manager.channel', string='Canal')
    active = fields.Boolean(default=True)
    last_sent = fields.Datetime(string='Último envío')
    description = fields.Text()

    def action_send_test(self):
        self.ensure_one()
        self.last_sent = fields.Datetime.now()
        return True


class DiscordMessage(models.Model):
    _name = 'discord.manager.message'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Mensaje de Discord'

    name = fields.Char(string='Asunto', required=True)
    author = fields.Char(string='Autor')
    content = fields.Text(string='Contenido', required=True)
    discord_message_id = fields.Char(string='Discord Message ID')
    channel_id = fields.Many2one('discord.manager.channel', string='Canal', ondelete='restrict', required=True)
    server_id = fields.Many2one('discord.manager.server', string='Servidor', compute='_compute_server_id', store=True)
    webhook_id = fields.Many2one('discord.manager.webhook', string='Webhook', ondelete='set null')
    posted_on = fields.Datetime(string='Fecha de envío')
    state = fields.Selection(
        [
            ('draft', 'Borrador'),
            ('sent', 'Enviado'),
            ('failed', 'Error'),
        ],
        string='Estado',
        default='draft',
        tracking=True,
    )
    error_message = fields.Text(string='Error')

    @api.depends('channel_id')
    def _compute_server_id(self):
        for record in self:
            record.server_id = record.channel_id.server_id

    def action_send(self):
        for record in self:
            if record.state != 'draft':
                record.error_message = 'El mensaje ya fue enviado o no está en estado borrador.'
                record.state = 'failed'
                continue
            if not record.webhook_id or not record.webhook_id.active:
                record.state = 'failed'
                record.error_message = 'Webhook no configurado o inactivo'
                continue
            record.posted_on = fields.Datetime.now()
            record.state = 'sent'
            record.error_message = False
            record.webhook_id.last_sent = record.posted_on
        return True

