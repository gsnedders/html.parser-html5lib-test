from html.parser import HTMLParser
from html.entities import html5 as entities

class TestParser(HTMLParser):
    def __init__(self, dump, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.depth = 0
        self.dump = dump
        self.curtext = []

    def feed(self, *args, **kwargs):
        super().feed(*args, **kwargs)
        self.dumpcurtext()

    def formatdump(self, s):
        self.dump.write("".join(["| ", "  " * self.depth, s, "\n"]))

    def dumpcurtext(self):
        if len(self.curtext):
            self.formatdump("".join(['"'] + self.curtext + ['"']))
            self.curtext = []

    def handle_starttag(self, tag, attrs):
        self.dumpcurtext()
        self.formatdump("<%s>" % tag)
        self.depth += 1
        for attr in sorted(attrs, key=lambda x: x[0]):
            self.formatdump('%s="%s"' % attr)

    def handle_endtag(self, tag):
        self.dumpcurtext()
        self.depth -= 1

    def handle_data(self, data):
        self.curtext.append(data)

    def handle_entityref(self, name):
        if name in entities:
            self.curtext.append(entities[name])
        else:
            self.curtext.append("&")
            self.curtext.append(name)

    def handle_charref(self, name):
        if name[0] == "x":
            value = int(name[1:], 16)
        else:
            value = int(name, 10)
        self.curtext.append(chr(value))

    def handle_comment(self, data):
        self.dumpcurtext()
        self.formatdump("<!-- %s -->" % data)

    def handle_decl(self, decl):
        self.dumpcurtext()
        self.formatdump("<!%s>" % decl)

    def handle_pi(self, data):
        self.dumpcurtext()
        self.formatdump("<?%s>" % data)

    def unknown_decl(self, data):
        assert False, "No other declarations exist in HTML"


if __name__ == "__main__":
    from io import StringIO
    import sys

    if len(sys.argv) == 1:
        print("Pass HTML as first argument or pass - to read from stdin")
        sys.exit(1)

    if sys.argv[1] == "-":
        data = "".join(sys.stdin)
    else:
        data = sys.argv[1]

    dumper = StringIO()
    parser = TestParser(dumper, strict=False)
    parser.feed(data)
    print(dumper.getvalue())
