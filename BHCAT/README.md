# Dormant black holes catalogue
This repo contains the json files, finders, and python code for building the dormant black hole catalogue.

Each dormant black hole has a JSON file within the JSON folder, and a corresponding folder within the sources directory.

## Editing known dormant black holes
If you wish to propose any changes to the JSON files, or want to update finders for any dormant black hole, please create a new branch,
edit the corresponding information, and then submit a pull request with the updated information. This will then be reviewed
by our team to ensure the format of the updates is correct, and to ensure references for any targets are correct.

## Adding a new system
If you wish to add a new dormant black hole system to the catalgoue, please create a new branch, create a JSON file which follows the format for other systems. Then submit a pull request with the updated information. This will then be reviewed by our team to ensure the format of the updates is correct, and to ensure references for any targets are correct.

## The JSON files
Each system has a JSON file which specifies the parameters of that system. A given field can have up to sub fields: value, error, reference, flag.

Value: This is the value required for the field.
Error: This is the numerical value of the error on the parameter.
Reference: This should be the bibcode of the paper from which the value comes from

Example 1: The ID field has a single subfield: "ID": {"Value": "GAIA BH1"}.
Example 2: The RA field has 3 subfields: "RAJ": {"Value": "262.17120816", "Error": "1e-8", "Ref": "2023MNRAS.518.1057E"}. This tells us the RA value, it's error, and the paper this value comes from.
