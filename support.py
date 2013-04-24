import os
import sys
import codecs
import glob

base_path = os.path.split(__file__)[0]

test_dir = os.path.join(base_path, 'testdata')

def get_data_files(subdirectory, files='*.dat'):
    return glob.glob(os.path.join(test_dir, subdirectory, files))


class DefaultDict(dict):
    def __init__(self, default, *args, **kwargs):
        self.default = default
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        return dict.get(self, key, self.default)


class TestData(object):
    def __init__(self, filename, newTestHeading="data", encoding="utf8"):
        if encoding == None:
            self.f = open(filename, mode="rb")
        else:
            self.f = codecs.open(filename, encoding=encoding)
        self.encoding = encoding
        self.newTestHeading = newTestHeading

    def __del__(self):
        self.f.close()

    def __iter__(self):
        data = DefaultDict(None)
        key = None
        for line in self.f:
            heading = self.isSectionHeading(line)
            if heading:
                if data and heading == self.newTestHeading:
                    # Remove trailing newline
                    data[key] = data[key][:-1]
                    yield self.normaliseOutput(data)
                    data = DefaultDict(None)
                key = heading
                data[key] = "" if self.encoding else b""
            elif key is not None:
                data[key] += line
        if data:
            yield self.normaliseOutput(data)

    def isSectionHeading(self, line):
        """If the current heading is a test section heading return the heading,
        otherwise return False"""
        # print(line)
        if line.startswith("#" if self.encoding else b"#"):
            return line[1:].strip()
        else:
            return False

    def normaliseOutput(self, data):
        # Remove trailing newlines
        for key, value in data.items():
            if value.endswith("\n" if self.encoding else b"\n"):
                data[key] = value[:-1]
        return data

