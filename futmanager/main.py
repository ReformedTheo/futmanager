import argparse
from futmanager.interfaces.cli import run as run_cli
from futmanager.interfaces.gui import run_gui

def main():
    parser = argparse.ArgumentParser(
        description="Simule partidas de futebol: ou em texto (CLI) ou em janela (GUI)."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Rodar simulação texto-only (apenas uma partida)"
    )
    args = parser.parse_args()

    if args.cli:
        # chama seu run() atual, que faz a simulate e printa no terminal
        run_cli()
    else:
        # abre a janela Pygame com campo, camisas e painel de eventos
        run_gui()

if __name__ == "__main__":
    main()