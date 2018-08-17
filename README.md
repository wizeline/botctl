# botctl
Command line tools for the Wizeline bots platform, by now it works for a local
instance of bots platform only.

## Commands included

### botctl

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

### mkbot
Usage:
```sh
$ mkbot bot-for-testing
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
$ botmod update-conversation BOT_NAME < conversation-script.json
```
