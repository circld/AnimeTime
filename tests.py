import unittest as ut
import animetime as at
import argparse as ap
import sys
from cStringIO import StringIO
from contextlib import contextmanager


class ArgumentParsing(ut.TestCase):

    def setUp(self):
        self.parser = at.create_parser()

    def test_create_parser_creates_name_and_episode_args(self):
        args = self.parser.parse_args(['some_name', 'some_episode'])

        self.assertIn('name', args)
        self.assertIn('episode', args)

    def test_passing_no_arguments_raises_error(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])
