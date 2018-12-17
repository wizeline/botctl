# botctl
Command line tools for the Wizeline bots platform, by now it works for a local
instance of bots platform only.

## Commands included

### botctl
```
Usage:
        $ botctl [COMMAND] [OPTIONS]

Commands available:
        * set
        * get
        * del
        * chenv
For help:
        $ botctl help [COMMAND]
```

Usage:
```sh
$ botctl set token YOUR_PLATFORM_ACCESS_TOKEN
```
```sh
$ botctl get token
```
```sh
$ botctl del token
```

Other platform variables are:

- cms
- operations
- integrations
- analytics

And they set the URL for each platform component

```sh
$ botctl chenv local
```
```sh
$ botctl chenv development
```
```sh
$ botctl chenv production
```

### mkbot
Usage:
```sh
$ mkbot bot-for-testing
```

### rmbot
Usage:
```sh
$ rmbot bot-for-testing
```

### lsbot
Usage:
```sh
$ lsbot
```

### showbot
Usage:
```sh
$ showbot BOT_NAME
```

### botmod

Usage:
```sh
$ botmod install-integration BOT_NAME INTEGRATION_NAME < integration-config.json
```
```sh
$ botmod install-conversation BOT_NAME < conversation-script.json
```
```sh
$ botmod install-nlp BOT_NAME < nlp-configuration.json
```
nlp-configuration.json looks like:
```javascript
{
  "region": "string",
  "version": "string",
  "app_id": "string",
  "subscription_key": "string",
  "env": "string"
}
```

### botusr

```
$ botusr invite BOT_NAME USER_EMAIL
```
```
$ botusr uninvite BOT_NAME USER_EMAIL
```

### integration

Configure an integration to use it from the command line
```
$ integration config ${INTEGRATION_NAME} < ${INTEGRATION_CONFIG}
```

List the integrations available
```
$ integration list
```

Deploy the latest changes from an integration
```
$ integration deploy ${INTEGRATION_NAME}
```

Display details of an integration
```
$ integration show ${INTEGRATION_NAME}
```

Display details of an integration's function
```
$ integration show ${INTEGRATION_NAME}.${FUNCTION_NAME}
```

Call an integration's function
```
$ integration call ${INTEGRATION_NAME}.${INTEGRATION_FUNCTION} < ${ARGUMENTS}
```
