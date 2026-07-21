from errors import DETAIL_LIMIT, FALLBACK, error_text, friendly_error


class UnsupportedFormatException(Exception):
    """Dubles dos tipos do markitdown. O casamento em errors.py e por nome de
    classe, entao o teste nao precisa importar a dependencia pesada."""


class MissingDependencyException(Exception):
    pass


def test_por_tipo():
    assert "movido" in friendly_error(FileNotFoundError(2, "No such file"))
    assert "aberto em outro programa" in friendly_error(PermissionError())
    assert "não é suportado" in friendly_error(UnsupportedFormatException())
    assert "Reinstale" in friendly_error(MissingDependencyException())


def test_subclasse_casa_pela_mro():
    class ErroDoParser(FileNotFoundError):
        pass

    assert friendly_error(ErroDoParser()) == friendly_error(FileNotFoundError())


def test_por_mensagem():
    assert "senha" in friendly_error(Exception("PDF is password protected"))
    assert "espaço" in friendly_error(OSError("No space left on device"))


def test_tipo_ganha_da_mensagem():
    # PermissionError cuja mensagem contem "encrypted": o tipo e o sinal forte.
    assert "aberto em outro programa" in friendly_error(
        PermissionError("cannot open encrypted file"))


def test_desconhecido_cai_no_fallback():
    assert friendly_error(RuntimeError("segfault in libfoo 0x7f")) == FALLBACK
    assert friendly_error(None) == FALLBACK   # nunca levanta


def test_error_text():
    txt = error_text(FileNotFoundError(), r"C:\docs\relatorio.pdf")
    assert txt.startswith("Não foi possível converter relatorio.pdf")
    assert "movido" in txt
    # Texto de dev nunca e a mensagem principal: vem depois da frase util.
    assert txt.index("movido") < txt.index("Detalhes técnicos")


def test_detalhe_truncado():
    txt = error_text(RuntimeError("x" * 5000))
    assert "x" * DETAIL_LIMIT in txt
    assert "x" * (DETAIL_LIMIT + 1) not in txt


if __name__ == "__main__":
    test_por_tipo()
    test_subclasse_casa_pela_mro()
    test_por_mensagem()
    test_tipo_ganha_da_mensagem()
    test_desconhecido_cai_no_fallback()
    test_error_text()
    test_detalhe_truncado()
    print("ok")
