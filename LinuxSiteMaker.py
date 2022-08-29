import os
import socket
from shutil import *
from OpenSSL import *
from createdb import new_db
from random import *

def getDomeinNaam():
    global domeinNaam
    domeinNaam = input("Voer uw gekozen domeinnaam in: ")
    if domeinNaam.endswith(".ikdoeict"):
        domeinNaam = domeinNaam
    else:
        domeinNaam = domeinNaam + ".ikdoeict"

    print("Gekozen domein: " + domeinNaam)


def controleerDomeinen():
    domeinDir = os.listdir("/var/www/html/vhosts/")
    if domeinNaam not in domeinDir:
        return True
    else:
        return False


def backUp():
    print("#### PERFORMING BACKUP #####")
    copyfile(f"/var/named/{domeinNaam}", f"/var/named/{domeinNaam}.copy")
    print("#### Backed-up zone #####")
    copytree(f"/var/www/html/vhosts/{domeinNaam}", f"/var/www/html/vhosts/{domeinNaam}.copy")
    print("#### Backed-up site #####")
    os.system(
        f"mysqldump -u root --password='dankmemes' {domeinNaam} > /var/www/html/vhosts/{domeinNaam}/{domeinNaam}.sql")
    print("#### Backed-up server #####")
    print("#### COMPLETE ####")


def maakZoneFile():
    f = open("/etc/named.conf", "a")
    f.write(f"\n\nzone \"{domeinNaam}\" IN " + "{"
            + "\n\ttype master;"
            + f"\n\tfile \"{domeinNaam}\";"
            + "\n};")

    f = open(f"/var/named/{domeinNaam}", "w")
    f.write("$TTL 3H"
            + f"\n@\tIN SOA {domeinNaam}. student.{domeinNaam}. ("
            + "\n0 ;\tserial"
            + "\n1D ;\trefresh"
            + "\n1H ;\tretry"
            + "\n1W ;\t expire"
            + "\n3H ) ;\t minimum"
            + "\n)"
            + "\n;Name Server info"
            + f"\n@ IN NS {domeinNaam}."
            + f"\n{domeinNaam}.\tIN\tA\t10.129.38.72"
            + f"\nwww\tIN\tCNAME\t{domeinNaam}.")
    print("#### ZONE FILE MADE ####")


def typeSite():
    typeSiteVar = input("HTTP of HTTPS: ")
    if typeSite.lower() == 'http':
        httpSite()
    elif typeSite.lower() == 'https':
        httpsSite()
    else:
        typeSite()


def httpsSite():
    os.system(f"sudo touch /var/log/httpd/vhosts/{domeinNaam}.log")
    f = open("/etc/httpd/conf.d/vhosts.conf", "a")
    createCertificates()
    f.write(f"\n<VirtualHost *:443>"
            + f"\n\tServerName www.{domainName}"
            + f"\n\tDocumentRoot \"/var/www/html/vhosts/{domainName}/\""
            + f"\n\tErrorLog \"/var/log/httpd/vhosts/{domainName}.log\""
            + f"\n\tSSLCertificateFile \"/etc/httpd/ssl/{domainName}/{domainName}.crt\""
            + f"\n\tSSLCertificateKeyFile \"/etc/httpd/ssl/{domainName}/{domainName}.key\""
            + "\n</VirtualHost>")
    f.close()


def createCertificates():
    print("#### Generating SSL certificates ####")
    os.system(f"sudo mkdir /etc/httpd/ssl/{domainName}")
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = "BE"
    cert.get_subject().ST = "Oost-Vlaanderen"
    cert.get_subject().L = "Gent"
    cert.get_subject().O = "Odisee"
    cert.get_subject().OU = "ICT"
    cert.get_subject().CN = socket.gethostname()
    cert.get_subject().emailAddress = "jens.marissens@student.odisee.be"
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.set_serial_number(randint(0, 1000))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
    cert.sign(k, 'sha512')
    with open(f"/etc/httpd/ssl/{domainName}/{domainName}.crt", "wt") as crt:
        crt.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(f"/etc/httpd/ssl/{domainName}/{domainName}.key", "wt") as key:
        key.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    print("\t-> Generated certificates")

def httpSite():
    os.system(f"sudo touch /var/log/httpd/vhosts/{domeinNaam}.log")
    f = open("/etc/httpd/conf.d/vhosts.conf", "a")
    f.write(f"\n<VirtualHost *:8888>"
            f"\n\tServerName\twww.{domeinNaam}"
            f"\n\tServerAlias\tmarissens.{domeinNaam}"
            f"\n\tDocumentRoot\t/var/www/html/vhosts/{domainName}/"
            f"\n\tErrorLog\t/var/log/httpd/vhosts/{domainName}.log"
            f"\n</VirtualHost>")
    f.close()


def databaseOrStatic():
    db = input("Wil je een database aanmaken (y/n): ")
    if db.lower() == 'y':
        wordPress()
    elif db.lower() == 'n':
        print("#### Statische website komt er aan. ####")
        copytree("/var/www/html/vhosts/klant1.ikdoeict", f"/var/www/html/vhosts/{domainName}")
    else:
        maakDatabase()

def wordPress():
    db = input("Wordt het een Wordpress database(y/n): ")
    if db.lower() == 'y':
        maakDatabase("wordpress")
        change_selinux()
    elif db.lower() == 'n':
        maakDatabase("todo")
    else:
        wordPress()


def maakDatabase(populate=" "):
    dbuser = input("Database username: ")
    userpass = input("Database user password: ")
    new_db(domainName[:-9], dbuser, userpass)
    if populate is not " ":
        populate_db(populate, domainName[:-9], dbuser, userpass)
    print("#### DATABASE AANGEMAAKT####")

def populate_db(dbsource, dbdestination, dbuser, userpass):
    os.system(f"mysqldump -u root --password='dankmemes' {dbsource} > {dbsource}.sql")
    os.system(f"mysql -u {dbuser} --password='{userpass}' {dbdestination} < {dbsource}.sql")

def restart():
    os.system("sudo systemctl restart httpd named")
    print("#### Services herstart ####")

def change_selinux():
    os.system(f"sudo chcon -h httpd_sys_rw_content_t /var/www/html/vhosts/{sitename}")


if __name__ == "__main__":
    getDomeinNaam()
    if controleerDomeinen():
        maakZoneFile()
        typeSite()
        databaseOrStatic()
        restart()
    else:
        backUp()
        print("#### BACKED UP. CLOSING... ####")
