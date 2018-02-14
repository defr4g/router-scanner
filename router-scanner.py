# Autor: João (@hackerftsg)
# Versão: 1.0.2
# Cópia não comédia

from sys import modules, argv
from re import match, findall
from multiprocessing import cpu_count

try:
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from functools import reduce
    from requests import get as rget
    from requests.exceptions import ConnectionError, ReadTimeout
    from netaddr import IPRange
    from netaddr.core import AddrFormatError
except ImportError as err:
    exit("Erro: não encontramos o pacote %s" % err.__str__().split(" ")[-1])

global this, ports, routers, found_routers
this = modules[__name__]
ports = [80, 8080, 8081, 8181]
routers = [
    ("TP-LINK", r"TP-LINK Technologies|Roteador Wireless N", "/"),
    ("pfSense", r"Rubicon Communications", "/"),
    ("RouterOS", r"RouterOS router configuration page", "/"),
    ("Cisco", r"copyright\.js|Cisco SPA Configuration", "/"),
    ("WebDAV", r"WebDAV testpage", "/webdav"),
    ("phpMyAdmin", r"Donate to phpMyAdmin|phpMyAdmin.+setup", "/phpmyadmin/scripts/setup.php")
]
found_routers = {}


class Banner(object):
    def __init__(self, author, version):
        self.author, self.version = author, version

    def __str__(self):
        return ("• KL DNS     - Router Scanner\n"
                "• Autor      - {author}\n"
                "• Working on - {values}\n"
                "• Versão     - {version}".format(
                author=self.author,
                values=", ".join([x[0] for x in routers]),
                version=self.version))


class IPAddress(object):
    def __init__(self, ip):
        self.ip = ip

    def __bool__(self):
        return bool(match(r"^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$", self.ip))


def scanner(url):
    try:
        req = rget(url, timeout=2)
        for x, y, z in routers:
            if z != "/":
                req = rget(url + z, timeout=2)
            if len(findall(y, req.text)) > 0:
                found_routers[url] = x
                return {True: x}
        return {False: ""}
    except (ConnectionError, ReadTimeout):
        return {False: ""}


if __name__ == "__main__":
    setattr(this, "__author__", "João (@hackerftsg)")
    setattr(this, "__version__", "1.0.2")
    setattr(this, "__usage__", "• Usagem: python %s primeiro_ip segundo_ip tarefas\n"
                               "• Número de tarefas recomendadas para seu PC: %d" % (argv[0], cpu_count() ** 2))
    setattr(this, "__msg__", "• Roteador encontrado: {link}    \tModelo: {model}")

    print(Banner(__author__, __version__), end="\n\n")

    if len(argv) != 4:
        exit(__usage__)

    if not IPAddress(argv[1]) or not IPAddress(argv[2]):
        exit(__usage__)

    if not argv[3].lstrip("0").isdigit():
        exit(__usage__)

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
