import os
import sys
import traceback
from io import StringIO
import warnings
import re

warnings.simplefilter("error")

from support import get_data_files
from support import TestData

from parser import TestParser


def runParserTest(input, expected, errors):
    warnings.resetwarnings()
    warnings.simplefilter("error")

    data = StringIO()
    parser = TestParser(dump=data, strict=False)

    try:
        parser.feed(input)
    except:
        errorMsg = "\n".join(["\n\nInput:", input, "\nExpected:", expected,
                              "\nTraceback:", traceback.format_exc()])
        assert False, errorMsg

    output = data.getvalue()

    errorMsg = "\n".join(["\n\nInput:", input, "\nExpected:", expected,
                          "\nReceived:", output])
    assert expected == output, errorMsg


def test_parser():
    files = get_data_files('tree-construction')

    for filename in files:
        testName = os.path.basename(filename).replace(".dat", "")
        if testName in ("template",):
            continue

        tests = TestData(filename, "data")

        for index, test in enumerate(tests):
            input, errors, innerHTML, expected = [test[key] for key in
                                                  ('data', 'errors',
                                                   'document-fragment',
                                                   'document')]
            if errors:
                errors = errors.split("\n")

            if innerHTML:
                # html.parser doesn't provide fragment parsing
                continue

            yield (runParserTest, input, expected, errors)
