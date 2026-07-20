"""Traducao de excecao do markitdown em frase acionavel em portugues.

PRODUCT.md lista "ferramenta de dev" como anti-referencia explicita, e o
publico-alvo e nao-tecnico. `FileNotFoundError: [WinError 2]` nao diz a essa
pessoa o que fazer a seguir — toda frase daqui termina numa acao que ela
consegue executar.

Sem Tk e sem importar markitdown: o casamento e por NOME de classe, subindo a
MRO. Assim o modulo e puro, o teste nao carrega a dependencia pesada, e uma
troca de biblioteca de conversao nao arrasta este arquivo junto.
"""
import os

# Detalhe tecnico e para anexar num pedido de suporte, nao para ler. Stack de
# parser passa facil de 10 mil chars e empurraria a frase util pra fora da tela.
DETAIL_LIMIT = 300

FALLBACK = ("O arquivo pode estar corrompido, incompleto ou num formato que "
            "não conseguimos ler. Tente abri-lo no programa de origem e "
            "salvá-lo de novo.")

# Nome da classe -> frase. Checado antes das heuristicas de mensagem.
BY_TYPE = {
    "FileNotFoundError": (
        "Não encontramos mais este arquivo. Ele pode ter sido movido, "
        "renomeado ou apagado depois de entrar na fila. Adicione-o de novo."),
    "PermissionError": (
        "O arquivo está aberto em outro programa, ou o Windows bloqueou o "
        "acesso. Feche o arquivo — e o .md já gerado, se estiver aberto — e "
        "converta de novo."),
    "IsADirectoryError": (
        "Isto é uma pasta, não um arquivo. Adicione os arquivos de dentro "
        "dela."),
    "UnsupportedFormatException": (
        "Este tipo de arquivo não é suportado. Confira a lista de formatos no "
        "botão “Selecionar arquivos…”."),
    "MissingDependencyException": (
        "Falta um componente para ler este formato nesta instalação. "
        "Reinstale o aplicativo para resolver."),
    "UnicodeDecodeError": (
        "O conteúdo do arquivo não está numa codificação que conseguimos ler. "
        "Se for um arquivo de texto, salve-o como UTF-8 e tente de novo."),
}

# Substring na mensagem (minuscula) -> frase. Ultimo recurso, porque depende do
# texto de bibliotecas de terceiros: uma atualizacao pode mudar a frase e cair
# no FALLBACK. Cair no FALLBACK e aceitavel; casar errado nao seria.
BY_MESSAGE = (
    (("password", "encrypted", "senha"),
     "Este PDF está protegido por senha. Remova a proteção no programa de "
     "origem e converta de novo."),
    (("no space left", "disk full", "espaço"),
     "O disco está sem espaço para gravar o resultado. Libere espaço e "
     "converta de novo."),
    (("timed out", "timeout", "connection", "network"),
     "A conversão precisou da internet e a conexão falhou. Verifique a rede e "
     "tente de novo."),
)


def friendly_error(exc):
    """Frase acionavel para `exc`. Nunca levanta: um erro aqui viraria erro
    dentro do tratamento de erro, e o usuario ficaria sem mensagem nenhuma."""
    try:
        for cls in type(exc).__mro__:
            if cls.__name__ in BY_TYPE:
                return BY_TYPE[cls.__name__]
        message = str(exc).lower()
        for needles, phrase in BY_MESSAGE:
            if any(n in message for n in needles):
                return phrase
    except Exception:  # noqa: BLE001 — exc exotico: melhor generico que nada
        pass
    return FALLBACK


def error_text(exc, path=""):
    """Bloco completo do preview: titulo, frase acionavel, detalhe tecnico por
    ultimo. O detalhe fica no fim de proposito — DESIGN.md marca texto de dev
    como Don't, e o backlog pede ele atras de um "detalhes", nunca como
    mensagem principal. Tk nao tem disclosure nativo barato; a posicao e o
    rotulo fazem o mesmo trabalho."""
    name = os.path.basename(path) if path else ""
    title = f"Não foi possível converter {name}" if name else \
        "Não foi possível converter este arquivo"
    detail = str(exc)
    if len(detail) > DETAIL_LIMIT:
        detail = detail[:DETAIL_LIMIT] + "…"
    return (f"{title}\n\n{friendly_error(exc)}\n\n\n"
            f"Detalhes técnicos (para suporte):\n{detail}")
