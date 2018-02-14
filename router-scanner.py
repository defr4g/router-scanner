# Autor: João (@hackerftsg)
# Versão: 1.0.2
# Cópia não comédia

from sys import modules, argv
from re import match, findall
from multiprocessing import cpu_count

try:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from functools import reduce
    from requests import session
    from requests.exceptions import ConnectionError, ReadTimeout
    from netaddr import IPRange
    from netaddr.core import AddrFormatError
except ImportError as err:
    exit("Erro: não encontramos o pacote %s" % err.__str__().split(" ")[-1])

global this, ports, routers, found_routers, selected_routers, do_filter
this = modules[__name__]
ports = [80, 8080, 8081, 8181]
routers = [
    ("TP-LINK", r"TP-LINK Technologies|Roteador Wireless N", ("/")),
    ("pfSense", r"Rubicon Communications", ("/")),
    ("RouterOS", r"RouterOS router configuration page", ("/")),
    ("Cisco", r"copyright\.js|Cisco SPA Configuration", ("/")),
    ("WebDAV", r"WebDAV testpage", ("/webdav")),
    ("phpMyAdmin", r"Donate to phpMyAdmin|phpMyAdmin.+setup", ("/phpmyadmin/scripts/setup.php"))
]
found_routers = {}
selected_routers = []
do_filter = True


class Banner(object):
    def __init__(self, author, version):
        self.author, self.version = author, version

    def __str__(self):
        return ("• Ferramenta     - Router Scanner\n"
                "• Autor          - {author}\n"
                "• Funcionando em - {values}\n"
                "• Versão         - {version}".format(
                author=self.author,
                values=", ".join([x[0] for x in routers]),
                version=self.version))


class IPAddress(object):
    def __init__(self, ip):
        self.ip = ip

    def __bool__(self):
        return bool(match(r"^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$", self.ip))


class Router(object):
    def __init__(self, router):
        self.router = router.lower()

    def __bool__(self):
        if "," in self.router:
            self.router = self.router.strip(",").split(",")
            for router in self.router:
                if router in [x[0].lower() for x in routers]:
                    selected_routers.append(router)
        if self.router in [x[0].lower() for x in routers]:
            selected_routers.append(self.router)
        return True if len(selected_routers) > 0 else False


def scanner(url):
    try:
        s = session()
        s.trust_env = False
        s.max_redirects = 1
        r = s.get(url, timeout=2)
        for x, y, z in routers:
            if x.lower() in selected_routers:
                if len(z[0]) > 1:
                    for a in z:
                        r = s.get(url + a, timeout=2)
                if len(findall(y, r.text)) > 0:
                    found_routers[url] = x
                    return {True: x}
        return {False: ""}
    except (ConnectionError, ReadTimeout):
        return {False: ""}


if __name__ == "__main__":
    setattr(this, "__author__", "João (@hackerftsg)")
    setattr(this, "__version__", "1.0.3")
    setattr(this, "__usage__", "• Usagem: python %s primeiro_ip segundo_ip tarefas roteadores(opcional)\n\n"
                               "• Use o argumento 'show_examples' para ver os exemplos\n"
                               "• Use o argumento 'show_recommended para ver as recomendações\n"
                               "• Use o argumento 'show_routers' para ver todos roteadores disponíveis\n\n"
                               "• LEIA! Você não precisa usar o argumento 'roteadores' se não quiser filtrar o scan." % argv[0])
    setattr(this, "__examples__", "• Exemplo do argumento  'roteadores': tp-link,pfsense\n"
                                  "• Exemplo do argumento  'roteadores': phpmyadmin\n"
                                  "• Exemplo do argumento     'tarefas': 16\n"
                                  "• Exemplo do argumento 'primeiro_ip': 192.168.0.1\n"
                                  "• Exemplo do argumento  'segundo_ip': 192.168.0.120")
    setattr(this, "__recommended__", "• Número de tarefas recomendadas para seu PC: %d\n"
                                     "• Nunca use muitas tarefas caso seu PC for fraco" % cpu_count() ** 2)
    setattr(this, "__routers__", "".join(["• Roteador: '" + x[0].lower() + "'\n" for x in routers]).rstrip("\n"))
    setattr(this, "__msg__", "• Roteador encontrado: {link}        \tModelo: {model}")

    print(Banner(__author__, __version__), end="\n\n")

    if "show_examples" in argv:
        exit(__examples__)
    elif "show_recommended" in argv:
        exit(__recommended__)
    elif "show_routers" in argv:
        exit(__routers__)

    if len(argv) == 4:
        [selected_routers.append(x[0].lower()) for x in routers]
        do_filter = False
    elif len(argv) != 5:
        exit(__usage__)

    if not IPAddress(argv[1]) or not IPAddress(argv[2]):
        exit(__examples__)

    if not argv[3].lstrip("0").isdigit():
        exit(__examples__)

    if int(argv[3]) > cpu_count() ** 4:
        exit(__recommended__)

    if do_filter:
        if not Router(argv[4]):
            exit(__routers__)

    urls = []

    try:
        for x in ports:
            for y in IPRange(argv[1], argv[2]):
                urls.append("http://" + str(y) + ":" + str(x))
    except AddrFormatError:
        exit(__usage__)

    with ThreadPoolExecutor(max_workers=int(argv[3])) as executor:
        workers = {executor.submit(scanner, x): x for x in urls}
        for worker in as_completed(workers):
            data = list(reduce(lambda x, y: x + y, worker.result().items()))
            if data[0]:
                print(__msg__.format(link=workers[worker],
                                     model=data[1]))

    for x, y in found_routers.items():
        print("%s: %s" % (y, x), file=open("found_routers.txt", "a"))

    if len(found_routers) == 0:
        print("• Nenhum roteador foi encontrado")
