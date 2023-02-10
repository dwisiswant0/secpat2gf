import json
import logging
import os
import re
import requests
import yaml

class secpat2gf:
    def __init__(self, args):
        self.gf_dir = os.path.join(os.environ.get("HOME"), ".gf")
        self.file = args.rule_file
        self.flags = args.flags
        self.save = args.save
        self.main()

    def main(self):
        if re.search("^https?://.*\\.ya?ml", self.file):
            content = requests.get(self.file).text
        else:
            with open(self.file, "r") as f:
                content = f.read()

        try:
            rule = yaml.load(content, Loader=yaml.FullLoader)
        except Exception as e:
            logging.error("error unmarshaling YAML: %s", str(e))
            return

        if rule['patterns'] is None:
            return

        for p in rule['patterns']:
            if p['pattern'] is None:
                name = p['name']
                regex = p['regex']
            else: # handle inconsistent indentation (see https://github.com/mazen160/secrets-patterns-db/issues/5)
                name = p['pattern']['name']
                regex = p['pattern']['regex']

            if not self.save:
                logging.info("%s pattern" % name)
                print(self.toGF(regex))
            else:
                self.toFile(name, regex)

    def toGF(self, pattern):
        data = {
            "flags": self.flags,
            "pattern": pattern
        }
        return json.dumps(data, indent=2)

    def _slugify(self, value):
        value = str(value).lower().replace(" ", "-")
        value = re.sub(r"[^\w-]+", "", value)
        value = re.sub(r"[-_]+", "-", value)
        return value

    def toFile(self, name, pattern):
        target = os.path.join(self.gf_dir, self._slugify(name) + "_secrets.json")
        logging.info("Saving %s pattern to %s" % (name, target))
        with open(target, "w") as file:
            file.write(self.toGF(pattern))
