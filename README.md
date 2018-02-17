# router-scanner
**Versão atual: 1.0.8**

Um simples scanner para procurar e salvar roteadores em massa

Usando um sistema de paralelismo com multiprocesso para ficar com uma grande velocidade
### características
- [x] Sistema de paralelismo com multitarefa/multiprocesso e filtro do scan
- [x] Scan com um alcance entre 2 endereços de ip
- [x] Scan com múltiplas portas e múltiplos roteadores e serviços
- [x] Correção e supressão de erros e bugs comuns
- [x] Cores no foreground
- [] Scan intensivo no servidor explorando diversas falhas
- [] Ataque de força bruta
- [] Verificação da tecnologia da máquina

### versão do python
**Utilize a versão 3!**
### instalações iniciais
    python -m pip install -U netaddr
    python -m pip install -U requests
    python -m pip install -U colorama
### sintaxe de usagem
    python router-scanner.py primeiro_ip segundo_ip numero_de_tarefas
    python router-scanner.py primeiro_ip segundo_ip numero_de_tarefas roteadores(opcional)
### exemplo de usagem
    python router-scanner.py 200.0.13.1 200.0.14.255 10
    python router-scanner.py 200.0.13.1 200.0.13.255 10 phpmyadmin
    python router-scanner.py 200.0.13.1 200.0.13.255 10 tp-link,routeros
### comandos de ajuda
    python router-scanner.py show_examples
    python router-scanner.py show_recommended
    python router-scanner.py show_routers
### atualizações
**1.0.0** - Bugs resolvidos ***Atualizado em 14/02/2018***

**1.0.1** - Supressão de erros adicionadas ***Atualizado em 14/02/2018***

**1.0.2** - Novos serviços adicionados (WebDAV, phpMyAdmin) ***Atualizado em 14/02/2018***

**1.0.3** - Bugs resolvidos e sistema de filtro adicionado ***Atualizado em 14/02/2018***

**1.0.4** - Novos serviços adicionados (WordPress, Joomla, Drupal) ***Atualizado em 14/02/2018***

**1.0.5** - Bugs resolvidos ***Atualizado em 14/02/2018***

**1.0.6** - Parar scan com Ctrl C e cores adicionads ***Atualizado em 14/02/2018***

**1.0.7** - Ignorando certificados SSL ***Atualizado em 14/02/2018***

**1.0.8** - Bugs resolvidos ***Atualizado em 14/02/2018***
