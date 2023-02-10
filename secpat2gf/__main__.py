import argparse
import errno
import logging
import os
from secpat2gf.secpat2gf import secpat2gf

def main():
    logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    gf_dir = os.path.join(os.environ.get("HOME"), ".gf")
    gf_flags = "-aHnPr"

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rule-file", required=True, type=str, help="path to rule file/URL")
    parser.add_argument("-f", "--flags", default=gf_flags, type=str, help="grep flags (default: %s)" % gf_flags)
    parser.add_argument("-s", "--save", action="store_true", help="save to %s instead of stdout" % gf_dir)

    args = parser.parse_args()

    if args.save == False:
        secpat2gf(args)

    if not os.path.exists(gf_dir):
        try:
            os.makedirs(gf_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                logging.error("error creating directory %s: %s", gf_dir, str(e))
        else:
            logging.info("directory '%s' created successfully", gf_dir)

    secpat2gf(args)

if __name__ == "__main__":
    main()