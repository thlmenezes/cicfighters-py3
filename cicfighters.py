# /************************************************************/
# /*                                                          */
# /*    CIC Fighters:                                         */
# /*      Jogo de luta com os professores do CIC =)           */
# /*                                                          */
# /*    Uso: python cicfighter.py                             */
# /*    Ou para modo em tela cheia: python cicfighter.py -f   */
# /*                                                          */
# /*    Controles:                                            */
# /*    P1                                                    */
# /*    movimento: w, a, s, d                                 */
# /*    botoes: y - soco, u - chute, i - especial             */
# /*                                                          */
# /*    P2                                                    */
# /*    movimento: Cima, baixo, esquerda e direita            */
# /*    botoes: NUM7 - soco, NUM8 - chute, NUM9 - especial    */
# /*                                                          */
# /*    ESC para sair                                         */
# /*                                                          */
# /************************************************************/

import GameEngine


def get_usage_instructions():
    """Imprime informacoes de uso"""
    return """
        Uso: cicfighter.py

        Opções:
            -f | --fullscreen       : Modo em tela cheia
            -h | --help             : Esta tela
"""


if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], "fh", ["fullscreen", "help"])
    except getopt.GetoptError:
        print(get_usage_instructions())
        sys.exit(1)

    fullscreen = False
    for opt, arg in opts:
        if opt in ("-f", "--fullscreen"):
            fullscreen = True
        if opt in ("-h", "--help"):
            print(get_usage_instructions())
            sys.exit(1)

    Engine = GameEngine.GameEngine(fullscreen)
    Engine.run()
