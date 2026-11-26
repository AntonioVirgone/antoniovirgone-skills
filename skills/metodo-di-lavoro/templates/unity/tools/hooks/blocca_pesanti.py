#!/usr/bin/env python3
"""Hook PreToolUse sul Bash: Unity in batchmode (test, compilazione, build) parte solo da tools/pesante.sh,
che tiene il tetto di 6 processi pesanti per tutto il Mac (viene da age-of-dinos, dove un controllo
statico ne ha lanciati 200 insieme). Rifiuta il comando se un suo pezzo lancia Unity senza passare da
pesante.sh, anche dentro uno script che il comando esegue (i file che nomina, fino a due livelli, con le
variabili assegnate nel comando stesso sostituite). Non segue i file nominati da chi li legge soltanto (sed,
cat, grep…), e nei file che segue salta i commenti e, negli script Python, i docstring: lì si citano i
comandi, non si lanciano. Legge il JSON dell'hook su stdin; esce con 2 per rifiutare, 0 per lasciare.
I test: python3 -m unittest test_blocca_pesanti, dalla cartella tools/hooks."""

import io
import json
import os
import re
import sys
import tokenize

# Un pezzo di comando lancia qualcosa di pesante se contiene uno di questi.
HEAVY = re.compile(
    r"MacOS/Unity\b"
    r"|(?<![\w-])-(?:batchmode|runTests|executeMethod)\b"
)
WRAPPER = "pesante.sh"
# La cartella dell'hook: l'hook e i suoi test citano i comandi pesanti nelle stringhe, non li lanciano.
HERE = os.path.dirname(os.path.realpath(__file__))
# I comandi che leggono o cercano e non lanciano niente.
READERS = {
    "grep", "egrep", "rg", "sed", "awk", "cat", "head", "tail", "less", "more", "echo", "printf", "wc",
    "sort", "uniq", "cut", "tr", "diff", "ls", "find", "pgrep", "pkill", "kill", "ps", "git", "gh",
    "file", "stat", "du", "cp", "mv", "rm", "mkdir", "touch", "ln", "chmod", "test", "[", "[[",
    "jq", "nl", "column", "tee", "xxd", "strings", "lsof", "which", "type", "command",
}
# I prefissi che non sono il comando vero.
# Anche le parole chiave della shell che aprono una condizione: il comando vero viene dopo.
PREFIXES = {"nice", "nohup", "time", "exec", "env", "caffeinate", "sudo", "xargs", "if", "elif", "while", "until", "!"}
SEGMENT = re.compile(r"\n|;|&&|\|\||\||&|\$\(|`|\(|\)|\{|\}|\bthen\b|\bdo\b|\belse\b")
ASSIGN = re.compile(r"(?:^|[\s;&|(])([A-Za-z_]\w*)=(\"[^\"]*\"|'[^']*'|[^\s;&|()]+)")
MAX_FILE = 1_000_000


def expand(text, values):
    def repl(match):
        name = match.group(1) or match.group(2)
        return values.get(name, match.group(0))
    return re.sub(r"\$\{(\w+)\}|\$(\w+)", repl, text)


def assignments(text):
    values = {}
    for name, value in ASSIGN.findall(text):
        values[name] = expand(value.strip("\"'"), values)
    return values


def first_word(segment):
    words = segment.strip().split()
    while words and (re.fullmatch(r"[A-Za-z_]\w*=\S*", words[0]) or words[0] in PREFIXES
                     or (words[0].startswith("-") and len(words) > 1)):
        words = words[1:]
    return os.path.basename(words[0]) if words else ""


def segments(text):
    """I pezzi del testo, ognuno un comando a sé."""
    for line in text.splitlines():
        # Un array assegnato (args=(-batchmode ...)) non lancia niente: le sue parentesi non vanno spezzate.
        line = re.sub(r"\b[A-Za-z_]\w*=\([^)]*\)", "ARRAY=", line)
        for segment in SEGMENT.split(line):
            yield segment.strip()


def is_heavy(segment):
    return HEAVY.search(segment) is not None


def heavy_segments(text):
    """I pezzi del testo che lanciano qualcosa di pesante senza pesante.sh."""
    found = []
    for segment in segments(text):
        if not is_heavy(segment) or WRAPPER in segment:
            continue
        # Un'assegnazione di variabile o di array non lancia niente.
        if re.fullmatch(r"[A-Za-z_]\w*=\(.*", segment) or re.fullmatch(r"[A-Za-z_]\w*=\S*", segment):
            continue
        if first_word(segment) in READERS:
            continue
        found.append(segment)
    return found


def files_named(text, cwd):
    """I file di testo che il comando nomina fuori dai comandi che leggono soltanto: gli script che può
    eseguire."""
    names = set()
    for segment in segments(text):
        if first_word(segment) in READERS:
            continue
        for token in re.findall(r"[^\s;&|()<>\"'`=]+", segment):
            path = os.path.expanduser(token)
            if not os.path.isabs(path):
                path = os.path.join(cwd, path)
            if os.path.isfile(path) and os.path.getsize(path) < MAX_FILE and not path.endswith((".log", ".xml", ".json", ".txt", ".md", ".cs", ".asset", ".png", ".unity", ".prefab", ".meta")):
                names.add(os.path.realpath(path))
    return names


def is_python(path, content):
    first = content.split("\n", 1)[0]
    return path.endswith(".py") or (first.startswith("#!") and "python" in first)


def code_only(path, content):
    """Il testo di uno script senza i commenti e, se è Python, senza i docstring (le stringhe che sono
    un'istruzione da sole): quello che resta è ciò che lo script esegue. Le righe restano al loro posto."""
    if not is_python(path, content):
        return "\n".join("" if line.lstrip().startswith("#") else line for line in content.split("\n"))
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return content
    lines = content.split("\n")
    skip = (tokenize.NL, tokenize.COMMENT)
    drop = []
    for i, token in enumerate(tokens):
        if token.type == tokenize.COMMENT:
            drop.append(token)
        elif token.type == tokenize.STRING:
            before = next((t for t in reversed(tokens[:i]) if t.type not in skip), None)
            after = next((t for t in tokens[i + 1:] if t.type not in skip), None)
            starts = before is None or before.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)
            ends = after is None or after.type in (tokenize.NEWLINE, tokenize.ENDMARKER)
            if starts and ends:
                drop.append(token)
    for token in reversed(drop):
        (row, col), (end_row, end_col) = token.start, token.end
        if row == end_row:
            line = lines[row - 1]
            lines[row - 1] = line[:col] + line[end_col:]
        else:
            lines[row - 1] = lines[row - 1][:col]
            for r in range(row, end_row - 1):
                lines[r] = ""
            lines[end_row - 1] = lines[end_row - 1][end_col:]
    return "\n".join(lines)


def check(text, cwd, depth, seen, problems):
    values = assignments(text)
    text = expand(text, values)
    for segment in heavy_segments(text):
        problems.append(segment)
    if depth == 0:
        return
    for path in files_named(text, cwd):
        if path in seen or path.endswith(WRAPPER) or os.path.dirname(path) == HERE:
            continue
        seen.add(path)
        try:
            with open(path, encoding="utf-8") as handle:
                content = code_only(path, handle.read())
        except (OSError, UnicodeDecodeError):
            continue
        before = len(problems)
        check(content, os.path.dirname(path), depth - 1, seen, problems)
        for i in range(before, len(problems)):
            problems[i] = f"{path}: {problems[i]}"


def main():
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        return 0
    command = (data.get("tool_input") or {}).get("command", "")
    cwd = data.get("cwd") or os.getcwd()
    problems = []
    check(command, cwd, 2, set(), problems)
    if not problems:
        return 0
    shown = "\n".join(f"  - {problem[:200]}" for problem in problems[:5])
    sys.stderr.write(
        "Bloccato: questo comando lancia Unity senza tools/pesante.sh, che tiene al massimo 6 processi "
        "pesanti su tutto il Mac (metodo-di-lavoro, UNITY.md, «Worktree e Editor»).\n"
        f"{shown}\n"
        "Rilancia ogni processo pesante come `tools/pesante.sh <comando>`; per tanti in parallelo "
        "`xargs -P 6 ... tools/pesante.sh ...`. Non aggirare il blocco: se serve davvero altro, chiedi all'utente.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
