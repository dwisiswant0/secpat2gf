# secpat2gf

convert secret patterns to gf compatible.

## Install

#### from PyPI

```console
$ pip3 install secpat2gf
```

#### from Source

```console
$ git clone https://github.com/dwisiswant0/secpat2gf
$ cd secpat2gf/
$ pip3 install -r requirements.txt
$ python3 -m build
$ pip3 install dist/secpat2gf-*.whl --force-reinstall
```

## Usage

```console
$ secpat2gf --help
usage: secpat2gf [-h] -r RULE_FILE [-e ENGINE] [-f FLAGS] [-s]

options:
  -h, --help            show this help message and exit
  -r RULE_FILE, --rule-file RULE_FILE
                        path to rule file/URL
  -e ENGINE, --engine ENGINE
                        set custom engine (default: grep)
  -f FLAGS, --flags FLAGS
                        grep flags (default: -aHnoPr)
  -s, --save            save to /home/dw1/.gf instead of stdout
```

### Example

Converting YAML-based rule URL to gf compatible

```console
$ secpat2gf -r https://github.com/mazen160/secrets-patterns-db/raw/master/datasets/generic.yml
[02/10/2023 08:56:55 AM] Slack Token pattern
{
  "flags": "-aHnPr",
  "pattern": "(xox[pborsa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})"
}
[02/10/2023 08:56:55 AM] test pattern
{
  "flags": "-aHnPr",
  "pattern": "test"
}
[02/10/2023 08:56:55 AM] generic password pattern
{
  "flags": "-aHnPr",
  "pattern": "password.+"
}
[02/10/2023 08:56:55 AM] Generic secret pattern
{
  "flags": "-aHnPr",
  "pattern": "secret.+"
}
...
```

Converting YAML-based rule file to gf & save the results

```console
$ secpat2gf --save -r generic.yaml
[02/10/2023 10:30:56 AM] directory '$HOME/.gf' created successfully
[02/10/2023 10:30:57 AM] Saving Slack Token pattern to $HOME/.gf/slack-token_secrets.json
[02/10/2023 10:30:57 AM] Saving test pattern to $HOME/.gf/test_secrets.json
[02/10/2023 10:30:57 AM] Saving generic password pattern to $HOME/.gf/generic-password_secrets.json
[02/10/2023 10:30:57 AM] Saving Generic secret pattern to $HOME/.gf/generic-secret_secrets.json
[02/10/2023 10:30:57 AM] Saving Generic token pattern to $HOME/.gf/generic-token_secrets.json
...
```

Then we can see that the pattern can be successfully compiled to gf:

```console
$ gf -list
admin-password_secrets
aws-client-id_secrets
aws-mws-id_secrets
aws-secret-key_secrets
basic-auth-credentials_secrets
basic-token_secrets
bearer-token_secrets
$ gf -dump admin-password_secrets # dump pattern
grep -aHnPr "(admin).+(secret|token|key).+" .
```

### Weaponizing

See [workaround](https://github.com/dwisiswant0/gf-secrets#workaround-recycle) from [gf-secrets](https://github.com/dwisiswant0/gf-secrets) to weaponize those patterns.

## Resources

- [secrets-patterns-db](https://github.com/mazen160/secrets-patterns-db) - Secrets Patterns DB: The largest open-source Database for detecting secrets, API keys, passwords, tokens, and more.
- [gf](https://github.com/tomnomnom/gf) - A wrapper around grep, to help you grep for things.
- [gfx](https://github.com/dwisiswant0/gfx) - Improved version of gf by @tomnomnom.
- [gf-secrets](https://github.com/dwisiswant0/gf-secrets) - Secret and/or credential patterns used for gf.

## License

`secpat2gf` is distributed under MIT. See `LICENSE` file.