# sPyCat
This repo contains the json files, light curves, and finders for the pulsars in sPyCat.

Each spider has a JSON file within the JSON folder, and a corresponding folder within the spiders directory.

## Editing known spiders
If you wish to propose any changes to the JSON files, or want to update finders/light curves for any spider, please create a new branch,
edit the corresponding information, and then submit a pull request with the updated information. This will then be reviewed
by our team to ensure the format of the updates is correct, and to ensure references for any targets are correct.

## Adding a new spider
If you wish to add a new spider to sPyCat, please create a new branch, create a JSON file which follows the format for other spiders, create a new folder
within spiders with the new objects name, and add any light curves to it. Finders are also welcome, but not required as these can be
created on the fly when recompiling the website.


## The JSON files
Each spider has a JSON file which specifies the parameters of that system. A given field can have up to sub fields: value, error, reference, flag.

Value: This is the value required for the field.
Error: This is the numerical value of the error on the parameter.
Reference: This should be the bibcode of the paper from which the value comes from
Flag: This is an internal parameter used to compare the values in these files to those in ATNF. It can be set to 1.

Example 1: The ID field has a single subfield: "ID": {"Value": "PSR J1959+2048"}.
Example 2: The RA field has 4 subfields: "RAJ": {"Value": "19:59:36.76988", "Error": "5.00e-05", "Ref": "1994ApJ...426L..85A", "Flag": "0"}. This tells us the RA value, it's error, the paper this value comes from, and the flag value.
