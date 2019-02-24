from unittest import TestCase, mock
from yapf_diff import (parseLine, parseUnifiedDiff, File, LineRange)

# common fixtures
diff1 = '''
# oddly padded
'''

diff2 = '''
# includes non-python files
'''


class TestDiffParsing(TestCase):
  @mock.patch('yapf_diff.File', spec=True)
  @mock.patch('yapf_diff.LineRange', spec=True)
  def test_file_line_parsing(self, mock_lineRange, mock_file):
    params = (
        ('+++ b/yapf_diff/__init__.py', mock_file, [mock_lineRange]),
        ('@@ -1,7 +1,7 @@            ', mock_lineRange, [mock_file]),
        ('+        },                ', None, [mock_file, mock_lineRange]),
        ('-        ],                ', None, [mock_file, mock_lineRange]),
        ('     "develop": {          ', None, [mock_file, mock_lineRange]),
    )
    for (line, to_call, uncalled) in params:
      [i.reset_mock() for i in (mock_file, mock_lineRange)]
      with self.subTest(line=line.rstrip(), to_call=to_call, uncalled=uncalled):
        parseLine(line)
        if to_call:
          to_call.assert_called_with(line)
        for i in uncalled:
          i.assert_not_called()


if __name__ == '__main__':
  TestCase.run()
