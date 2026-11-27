#!/usr/bin/env python3
"""Test dell'hook dei processi pesanti: python3 -m unittest test_blocca_pesanti, dalla cartella
tools/hooks."""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest import mock

import blocca_pesanti

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
UNITY = "/Applications/Unity/Hub/Editor/6000.5.3f1/Unity.app/Contents/MacOS/Unity"


def problems(command, cwd=ROOT):
    found = []
    blocca_pesanti.check(command, cwd, 2, set(), found)
    return found


def script(folder, name, text):
    path = os.path.join(folder, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


class Blocca(unittest.TestCase):
    def test_unity_in_batchmode(self):
        self.assertTrue(problems(f'"{UNITY}" -batchmode -runTests -projectPath .'))
        self.assertTrue(problems(f"{UNITY} -batchmode -quit -projectPath . -logFile -"))

    def test_unity_in_una_condizione(self):
        self.assertTrue(problems(f'if "{UNITY}" -batchmode -quit; then echo ok; fi'))
        self.assertTrue(problems(f"while ! {UNITY} -batchmode -quit; do sleep 1; done"))

    def test_unity_dentro_uno_script_shell(self):
        with tempfile.TemporaryDirectory() as folder:
            script(folder, "test.sh", f'#!/bin/bash\n# lancia i test\nUNITY="{UNITY}"\n"$UNITY" -batchmode -runTests\n')
            self.assertTrue(problems("bash test.sh", folder))
            self.assertTrue(problems("./test.sh", folder))

    def test_unity_dentro_uno_script_python(self):
        with tempfile.TemporaryDirectory() as folder:
            script(folder, "lancia.py", f'"""Lancia i test."""\nimport subprocess\n'
                                        f'subprocess.run(["{UNITY}", "-batchmode", "-runTests"])\n')
            self.assertTrue(problems("python3 lancia.py", folder))

    def test_due_livelli(self):
        with tempfile.TemporaryDirectory() as folder:
            script(folder, "dentro.sh", f"{UNITY} -batchmode -quit\n")
            script(folder, "fuori.sh", f"bash {folder}/dentro.sh\n")
            self.assertTrue(problems("bash fuori.sh", folder))

    def test_rifiuta_dal_json(self):
        data = {"tool_name": "Bash", "tool_input": {"command": f"{UNITY} -batchmode"}, "cwd": ROOT}
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(data))), redirect_stderr(io.StringIO()):
            self.assertEqual(blocca_pesanti.main(), 2)


class Lascia(unittest.TestCase):
    def test_con_pesante_sh(self):
        self.assertFalse(problems(f'tools/pesante.sh "{UNITY}" -batchmode -runTests'))

    def test_unity_check(self):
        # Lo script dei test e della compilazione nel worktree passa da pesante.sh.
        self.assertFalse(problems("tools/unity-check.sh"))
        self.assertFalse(problems('tools/unity-check.sh --filter "Game.Tests"'))
        self.assertFalse(problems("tools/unity-check.sh --compile-only"))

    def test_aprire_l_editor(self):
        # La procedura «Worktree e Editor» apre l'Editor con open, non in batchmode.
        self.assertFalse(problems("open -na /Applications/Unity/Hub/Editor/6000.5.3f1/Unity.app --args "
                                  "-projectPath /Users/antonio/workspaces/unity/progetto"))

    def test_engine_check(self):
        self.assertFalse(problems("dotnet run --project tools/engine-check"))

    def test_lettori(self):
        self.assertFalse(problems("cat tools/unity-check.sh && sed -n 1,40p tools/pesante.sh"))
        self.assertFalse(problems(f"grep -n batchmode tools/unity-check.sh; ps -Axo pid=,args= | grep {UNITY}"))
        self.assertFalse(problems("git log -3 -- tools/hooks/blocca_pesanti.py && cat tools/hooks/blocca_pesanti.py"))

    def test_docstring_e_commenti(self):
        with tempfile.TemporaryDirectory() as folder:
            script(folder, "nota.py", f'"""Si lancia con:\n    {UNITY} -batchmode -runTests\n"""\n'
                                      f"import os  # oppure {UNITY} -batchmode\n")
            script(folder, "giro.sh", f"#!/bin/bash\n# prima: {UNITY} -batchmode\necho fatto\n")
            self.assertFalse(problems("python3 nota.py", folder))
            self.assertFalse(problems("bash giro.sh", folder))

    def test_l_hook_e_i_suoi_test(self):
        self.assertFalse(problems("python3 tools/hooks/blocca_pesanti.py < /dev/null"))
        self.assertFalse(problems("python3 tools/hooks/test_blocca_pesanti.py"))

    def test_lascia_dal_json(self):
        data = {"tool_name": "Bash", "tool_input": {"command": "git status"}, "cwd": ROOT}
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(data))):
            self.assertEqual(blocca_pesanti.main(), 0)


if __name__ == "__main__":
    unittest.main()
