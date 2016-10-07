class FakeBoto3(object):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def describe_spot_price_history(*args, **kwargs):
        pass


class FakeOnDemand(object):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get_js_file():
        with open("tests/cost/linux-od.min.js") as js_file:
            js = js_file.read()

        return js
