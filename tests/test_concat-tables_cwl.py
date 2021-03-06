#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the paste-col.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'concat-tables.cwl')

class TestConcatTables(unittest.TestCase):
    def test_concat_two_tables(self):
        """
        Test that two files are concatenated correctly
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines1 = ["HEADER1", "foo1", "bar1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["HEADER2", "foo2", "bar2"]
            input_file2 = os.path.join(tmpdir, "input2.txt")
            with open(input_file2, "w") as fout:
                for line in input_lines2:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file1
                    },
                    {
                      "class": "File",
                      "path": input_file2
                    }
                    ],
                "output_filename": "output.txt"
                }

            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
            "cwl-runner",
            *CWL_ARGS,
            "--outdir", output_dir,
            "--tmpdir-prefix", tmp_dir,
            "--cachedir", cache_dir,
            cwl_file, input_json_file
            ]

            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            expected_lines = ['HEADER1\tHEADER2', 'foo1\tNA', 'bar1\tNA', 'NA\tfoo2', 'NA\tbar2']
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$d92a4e707cb5dad2ec557edfe976680dfffc5f3f',
                    'size': 53,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_one_tables(self):
        """
        Test that two files are concatenated correctly
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines1 = ["HEADER1", "foo1", "bar1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file1
                    },
                    ],
                "output_filename": "output.txt"
                }

            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
            "cwl-runner",
            *CWL_ARGS,
            "--outdir", output_dir,
            "--tmpdir-prefix", tmp_dir,
            "--cachedir", cache_dir,
            cwl_file, input_json_file
            ]

            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            expected_lines = ['HEADER1', 'foo1', 'bar1']
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$2274c54c24a98e8235e34d78b700d04cb95f48dd',
                    'size': 21,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
