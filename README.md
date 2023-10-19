# cicfighters-py3
Jogo recriado pelo grupo de Python do Colégio Militar Dom Pedro II com base no "Cicfighters" - jogo criado por um grupo de alunos de ciências da computação da Universidade de Brasília (UNB) - para a feira do conhecimento de 2023 do Colégio Militar Dom Pedro II.

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

Apertar F11, coloca o jogo em tela inteira

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
