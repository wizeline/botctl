import json
import sys

from datetime import datetime

from botctl.errors import BotNotFound
from botctl.gateway import BotCMSGateway, BotIntegrationsGateway
from botctl.types import BotControlCommand


class BotClient:
    def __init__(self, gateway):
        self._gateway = gateway

    def get_bots(self):
        response = self._gateway.get('/bots')
        return response.json()

    def get_by_name(self, bot_name):
        bots = self.get_bots()
        for bot in bots:
            if bot.get('name') == bot_name:
                users = self.get_bot_users_by_id(bot['id'])
                if users:
                    bot.update({'users': users})

                return bot

        raise BotNotFound(bot_name)

    def make_admin(self, bot_id, user_id):
        self.set_user_role(bot_id, user_id, 'admin')

    def remove_admin(self, bot_id, user_id):
        self.set_user_role(bot_id, user_id, 'customer')

    def set_user_role(self, bot_id, user_id, role):
        url = f'/bots/{bot_id}/users/{user_id}'
        self._gateway.put(url, json={'role': role})

    def make_bot(self, bot_name):
        self._gateway.post('/bots', json={'name': bot_name})

    def destroy_bot(self, bot_name):
        bot = self.get_by_name(bot_name)
        bot_id = bot.get('id')

        url = f'/bots/{bot_id}'
        self._gateway.delete(url)

    def get_bot_users_by_id(self, bot_id):
        url = f'/bots/{bot_id}/users'
        return self._gateway.get(url).json()

    def invite_user(self, bot_name, user_email):
        bot = self.get_by_name(bot_name)
        bot_id = bot.get('id')
        url = f'/bots/{bot_id}/invite'
        self._gateway.post(url, json={'email': user_email})

    def uninvite_user(self, bot_id, user_id):
        url = f'/bots/{bot_id}/users/{user_id}'
        self._gateway.delete(url)

    def post_conversation(self, bot_name, conversation):
        bot = self.get_by_name(bot_name)
        bot_id = bot.get('id')

        url = f'/bots/{bot_id}/conversations'
        response = self._gateway.post(url, data=conversation, fail=False)
        if not response.ok:
            # Now de platform expects the name of the script file
            time_stamp = datetime.utcnow().timestamp()
            body = {
                'name': f'{time_stamp}-{bot_name}-script.json',
                'script': json.dumps(conversation)
            }
            response = self._gateway.post(url, json=body)

    def install_bot_integration(self,
                                bot_name,
                                integration_name,
                                integration_config):

        bot = self.get_by_name(bot_name)
        bot_id = bot.get('id')

        url = f'/bots/{bot_id}/integrations/{integration_name}/install'
        response = self._gateway.post(url, json=integration_config, fail=False)

        if response.status_code == 409:
            url = f'/bots/{bot_id}/integrations/{integration_name}'
            response = self._gateway.put(url, json=integration_config)

        if not response.ok:
            sys.stderr.write((f'Could not install {integration_name} '
                              f'integration on bot {bot_name}\n'))

    def install_nlp(self, bot_name, nlp_config):
        bot = self.get_by_name(bot_name)
        bot_id = bot.get('id')

        url = f'/bots/{bot_id}/nlp_provider/luis'
        response = self._gateway.post(url, json=nlp_config)
        if not response.ok:
            print(response.status_code, response.text)

    def get_bot_integrations(self, bot):
        bot_id = bot.get('id')
        url = f'/bots/{bot_id}/integrations'
        return self._gateway.get(url)


class BotClientCommand(BotControlCommand):
    def set_up(self):
        self.client = BotClient(BotCMSGateway(self.config))

    def dump_bot_name(self, bot):
        print(bot.get('name'))

    def get_users_table(self, bot):
        user_format = '{:40}  {}'
        header = user_format.format('EMAIL', 'ROLE') + '\n' + \
            user_format.format(40 * '-', 10 * '-')
        users = map(
            lambda u: user_format.format(u['email'], u['role']),
            bot.get('users', [])
        )

        return header + '\n' + '\n'.join(users)

    def get_integrations_table(self, bot):
        integrations = map(
            lambda i: i['name'], self.client.get_bot_integrations(bot).json()
        )
        return '\n'.join(integrations)

    def dump_bot(self, bot):
        name = bot['name']
        bot_id = bot['id']
        print(f'Bot: {name} (ID: {bot_id})\n')
        print(f'INTEGRATIONS\n{self.get_integrations_table(bot)}\n')
        print(f'USERS\n{self.get_users_table(bot)}')


class IntegrationClient:
    def __init__(self, gateway):
        self._gateway = gateway

    def deploy_integration(self, integration_name):
        return self._gateway.post(
            '/integrations/install',
            json={'integration_name': integration_name}
        )

    def get_integration(self, integration_name):
        return self._gateway.get(
            f'/integrations/{integration_name}'
        ).json()

    def get_integrations(self):
        return self._gateway.get(
            '/integrations'
        ).json()

    def get_function(self, integration_name, function_name):
        return self._gateway.get(
            f'/integrations/{integration_name}/functions/{function_name}'
        ).json()

    def call_function(
            self,
            integration_name,
            function_name,
            payload
    ):
        return self._gateway.post(
            f'/integrations/{integration_name}/functions/{function_name}',
            json=payload
        ).json()


class IntegrationClientCommand(BotControlCommand):
    def set_up(self):
        self.client = IntegrationClient(BotIntegrationsGateway(self.config))

    def _dump_config_options(self, integration_spec):
        options = integration_spec.get('configuration_options')
        if not options:
            return

        print('CONFIGURATION OPTIONS')
        for option, spec in options.items():
            print(f'{option:25}  {spec["description"]}')

    def _dump_function_names(self, integration_spec):
        functions = integration_spec.get('functions')
        if not functions:
            return

        print('\nFUNCTIONS AVAILABLE')
        for function_name in sorted(functions.keys()):
            print(function_name)

    def dump_integration(self, integration_spec):
        self._dump_config_options(integration_spec)
        self._dump_function_names(integration_spec)

    def dump_function(self, integration_name, function_name, function_spec):
        params = function_spec['params']

        line_format = '{name:20}  {param_type:5} {required:^8}  {desc}'
        print(f'FUNCTION: {integration_name}.{function_name}()\n')
        print(line_format.format(
            name='PARAMETER',
            param_type='TYPE',
            required='REQUIRED',
            desc='DESCRIPTION'
        ))
        for name, value in params.items():
            str_required = '*' if value['is_required'] else ' '
            print(line_format.format(
                name=name,
                param_type=value['type'],
                required=str_required,
                desc=value['description']
            ))
