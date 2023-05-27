# cicfighters-py3
Atualização do jogo CiCfighters https://github.com/DaniloT/cicfighters para python 3 e pygame 2.4.0

# Como instalar?
Utilize a aba Releases para fazer download dos assets e executável de acordo com o seu sistema operacional

AVISO: Os assets precisam estar na mesma pasta do executavél para que o jogo inicialize sem erros, dessa forma

```txt
assets/
cicfigthers.exe
```

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
