import argparse


class CommonArgumentParse(object):
    """
    Common argument parser class, which can be inherited in any downloader and used for argument parsing and executing
    the download
    """
    @classmethod
    def parse_args(cls, args):
        parser = argparse.ArgumentParser()
        return parser.parse_args(args)

    @classmethod
    def create_object_from_args(cls, args):
        return cls()

    @classmethod
    def main(cls, clargs=None):
        parser = cls.parse_args(clargs)
        processor = cls.create_object_from_args(parser)
        processor.execute()

    def execute(self):
        """
        Do the work
        :return:
        """
        pass
