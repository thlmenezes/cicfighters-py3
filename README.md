# cicfighters-py3
Atualização do jogo CiCfighters https://github.com/DaniloT/cicfighters para python 3 e pygame 2.4.0

# Como instalar?
Utilize a aba Releases para fazer download dos assets e executável de acordo com o seu sistema operacional

AVISO: Os assets precisam estar na mesma pasta do executavél para que o jogo inicialize sem erros, dessa forma

```txt
assets/
cicfigthers.exe
```

# Como jogar?

Jogador 1 utiliza, por padrão:
- WASD para se movimentar
- Y para socar
- U para chutar
- I para especial

Os controles do Jogador 1 podem ser customizados clicando em F1 e seguindo as instruções em tela

Jogador 2 utiliza, por padrão:
- ⬆️⬅️⬇️➡️ para se movimentar
- 7 para socar
- 8 para chutar
- 9 para especial

Os controles do Jogador 2 podem ser customizados clicando em F2 e seguindo as instruções em tela

Apertar Enter, coloca o jogo em tela inteira

Apertar ESC, retorna a tela anterior (fechando o jogo caso esteja no Menu)

# Contribuindo

Instalar dependências

```bash
pip install -r requirements.txt
```

# Criando build local

```bash
pip install Nuitka
python -m nuitka --follow-imports cicfighters.py
```
