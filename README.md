# Simulador Petri Nets

Este simulador permite ao usuário montar uma rede de Petri a partir da leitura de um arquivo XML do tipo ".pflow" ou também por um script python, criando um objeto do tipo PetriNet e chamando os métodos correspondentes para adicionar lugares, transições e conectá-los através de arcos. 

Os objetos relacionados à execução da rede de Petri estão no arquivo _graph\_objects.py_ e o desserializador de XML que monta a rede está no arquivo _XMLParser.py_. O arquivo _run\_petri\_net\_for\_file.py_ permite montar e executar a rede a partir de um XML e recebe o nome do arquivo e o número de execuções por parâmetro. Os arquivos _exemplo1\_petri\_net\_simples.py_ mostra como criar a rede por um script python e o arquivo _exemplo1\_ra\_real.py_ mostra como alterar as marcas da rede durante a execução. 

Para executar o simulador: 

Lendo de um arquivo: 
```
python run_petri_net_for_file.py NOME_DO_ARQUIVO.pflow 10
```

Executando os exemplos:
```
python exemplo1_petri_net_simples.py
python exemplo2_ra_real.py
```