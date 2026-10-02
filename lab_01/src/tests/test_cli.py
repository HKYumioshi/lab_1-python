import subprocess


def test_cli_calc():

    result = subprocess.run(
        ['python', '-m', 'toolkit', 'calc', '2+2'],
        capture_output = True,
        text = True,
        check = False
    )
    assert result.returncode == 0
    assert "4.0" in result.stdout

def test_cli_conv():

    result = subprocess.run(
            ['python', '-m', 'toolkit', 'convert', '1000', '--from', 'g', '--to', 'kg'],
            capture_output = True,
            text = True,
            check = False
        )
    assert result.returncode == 0
    assert "1.0" in result.stdout