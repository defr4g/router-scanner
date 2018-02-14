# router-scanner
**Versão atual: 1.0.2**

Um simples scanner para procurar e salvar roteadores em massa.

Usando um sistema de paralelismo com multiprocesso para ficar com uma grande velocidade.
# versão do python
**Utilize a versão 3!**
# instalações iniciais
    python -m pip install netaddr
    python -m pip install requests
# sintaxe de usagem
    python router-scanner.py primeiro_ip segundo_ip numero_de_tarefas
# exemplo de usagem
    python router-scanner.py 200.0.13.1 200.0.14.255 10
# atualizações
**1.0.0** - Bugs resolvidos

**1.0.1** - Supressão de erros adicionadas

**1.0.2** - Novos serviços adicionados
