Some scripts for ad-hoc tests.

transfer_docs_to_xsd.py:

Copies documentation from the XML Component definition files and adds it to the XSD file.
For best results, run xmllint on the XSD file before running the script, and then run xmllint on the resulting file too.
That ensures that the git diff shows the only relevant changes (without any formatting bits).

verify-schema-lems-defs.sh:

Checks the XML and XSD files and generates a report of what entities are not present in both.
