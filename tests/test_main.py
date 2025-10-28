import io
import sys
import importlib
import konvigius.__main__


def test_main_output(monkeypatch, capsys):
    """
    Test that konvigius.__main__.main() prints the expected version header
    and some expected key phrases.
    """

    # --- Arrange ---
    # Patch __version__ so the output is predictable
    monkeypatch.setattr(konvigius.__main__, "__version__", "9.9.9")

    # --- Act ---
    konvigius.__main__.main()
    out = capsys.readouterr().out

    # --- Assert ---
    assert "Konvigius v9.9.9" in out
    assert "configuration utilities" in out
    assert "examples directory" in out
    assert "manual()" in out
    assert "python -c" in out


