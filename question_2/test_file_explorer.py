import unittest

from file_explorer import FileExplorer


class TestExampleSession(unittest.TestCase):

    def test_example(self):
        fe = FileExplorer()
        steps = [
            ("cwd", "/", "/"),
            ("ls", "", "/"),
            ("mkdir usr", None, "/"),
            ("cd random", "random not found.", "/"),
            ("cd usr", None, "/usr"),
            ("touch readme.md", None, "/usr"),
            ("mkdir share", None, "/usr"),
            ("ls", "readme.md share", "/usr"),
            ("cd readme.md", "readme.md is not a directory.", "/usr"),
            ("cd share", None, "/usr/share"),
            ("cwd", "/usr/share", "/usr/share"),
            ("cd ..", None, "/usr"),
            ("cd /usr/share", None, "/usr/share"),
        ]
        for command, expected_output, expected_cwd in steps:
            with self.subTest(command=command):
                self.assertEqual(fe.execute(command), expected_output)
                self.assertEqual(fe.cwd(), expected_cwd)


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.fe = FileExplorer()
        for cmd in ["mkdir usr", "cd usr", "mkdir share", "touch readme.md", "cd /"]:
            self.fe.execute(cmd)

    def test_cd_parent_at_root(self):
        self.assertEqual(self.fe.execute("cd .."), "currently at root.")
        self.assertEqual(self.fe.cwd(), "/")

    def test_cd_root(self):
        self.fe.execute("cd usr/share")
        self.assertIsNone(self.fe.execute("cd /"))
        self.assertEqual(self.fe.cwd(), "/")

    def test_relative_combination(self):
        self.fe.execute("cd usr/share")
        self.fe.execute("cd /")
        self.fe.execute("mkdir etc")
        self.fe.execute("cd usr/share")
        self.assertIsNone(self.fe.execute("cd ../../etc"))
        self.assertEqual(self.fe.cwd(), "/etc")

    def test_failed_cd_does_not_move(self):
        self.assertEqual(self.fe.execute("cd usr/nope"), "nope not found.")
        self.assertEqual(self.fe.cwd(), "/")

    def test_file_in_middle_of_path(self):
        self.assertEqual(
            self.fe.execute("cd usr/readme.md/x"), "usr/readme.md/x is not a directory."
        )
        self.assertEqual(self.fe.cwd(), "/")

    def test_too_many_parents(self):
        self.assertEqual(self.fe.execute("cd usr/../.."), "currently at root.")
        self.assertEqual(self.fe.cwd(), "/")

    def test_mkdir_already_exists(self):
        self.assertEqual(self.fe.execute("mkdir usr"), "usr already exists.")

    def test_touch_already_exists(self):
        self.fe.execute("cd usr")
        self.assertEqual(self.fe.execute("touch readme.md"), "readme.md already exists.")

    def test_ls_is_alphabetical(self):
        for name in ["zeta", "alpha", "Mid"]:
            self.fe.execute(f"touch {name}")
        self.assertEqual(self.fe.execute("ls"), "Mid alpha usr zeta")


if __name__ == "__main__":
    unittest.main()
