<h1 align="center">Projeto - Estrutura de Dados e Algoritmos</h1>
<h2 align="center">ANÁLISE COMPARATIVA DA ESTRUTURA DE DADOS SKIPLIST</h2>

<h2 align="center">Tecnologias Utilizadas:</h2>

<div align="center">

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
![Conda](https://img.shields.io/badge/conda-342B029.svg?&style=for-the-badge&logo=anaconda&logoColor=white)

</div>


<h2 align="center">Sobre o projeto:</h2>

<p>Os objetivos gerais incluem em realizar comparação experimental direta entre a SkipList, LinkedList, AVL e Árvore Rubro-Negra, em cenários com um grande volume de dados, comparando desempenho nas operações de inserção, busca e remoção de dados, a fim de, identificar a aplicabilidade e uso real da SkipList. Em paralelo aos testes de desempenho, será conduzida uma análise aprofundada da eficiência assintótica da SkipList, permitindo confrontar os resultados empíricos com as análises de eficiência.
	Os objetivos específicos incluem realizar experimentos controlados, com diferentes volumes de dados, registrar o comportamento das estruturas em cada cenário, observar o desempenho da SkipList com amostras de dados ordenados e aleatórios, avaliar escalabilidade 
</p>


<h2 align="center">Executando o projeto:</h2>

<h3>Rodando localmente:</h3>
<p><b>*Certifique se de ter instalado em sua máquina o Python. Os comandos abaixo são válidos para um dispositivo Windows.</b></p>
<p>•Clone esse repositório em sua máquina:</p>

```bash
  git clone https://github.com/samubbrando/projeto-leda.git
```

<p>•Acesse a pasta do projeto:</p>

```bash
  cd projeto-leda
```

<p>•Ative o ambiente virtual:</p>

```bash
.\config\.venv\Scripts\Activate.ps1
```

<p>•Defina as variáveis de ambiente:</p>

```bash
$env:SAMPLE_SIZES="1000 2500 5000 7500 10000 20000 40000 60000 80000 100000"
$env:SAMPLE_RELATIVE_PATH="src/samples"
```

<p>•Gere as amostras:</p>

```bash
python -m src.scripts.util.generate_sample
```
