import sqlalchemy as db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import xml.etree.ElementTree as ET

Base = declarative_base()
engine = db.create_engine('mysql+pymysql://root@127.0.0.1:3306/tp_python')
Session = sessionmaker(bind=engine)

class Commune(Base):
    __tablename__ = 'communes'

    id = Column(Integer, primary_key=True)
    code_dpt = Column(String(3), ForeignKey('departements.code_dpt'))
    code_arr = Column(Integer)
    code_canton = Column(Integer)
    code_commune = Column(Integer)
    nom_commune = Column(String(50))
    pop_municipale = Column(Integer)
    pop_a_part = Column(Integer)
    pop_tot = Column(Integer)

    departement = relationship("Departement", backref="communes")

    def __repr__(self):
        return "<Commune(code_dpt='%s', code_arr='%d'," \
               " code_canton='%d', code_commune='%d', nom_commune='%s', pop_municipale='%d'," \
               " pop_a_part='%d', pop_tot='%d')>" % (self.code_dpt,
                                                     self.code_arr, self.code_canton, self.code_commune,
                                                     self.nom_commune, self.pop_municipale, self.pop_a_part, self.pop_tot)

class Departement(Base):
    __tablename__ = 'departements'

    code_region = Column(Integer, ForeignKey('regions.code_region'))
    nom_region = Column(String(50))
    code_dpt = Column(String(3), primary_key=True)
    nom_dpt = Column(String(50))
    nb_arr = Column(Integer)
    nb_cantons = Column(Integer)
    nb_communes = Column(Integer)
    pop_municipale = Column(Integer)
    pop_tot = Column(Integer)

    region = relationship("Region", backref="departements")

    def __repr__(self):
        return "<Departement(code_region='%d', nom_region='%s', code_dpt='%s', nom_dpt='%s'," \
               " nb_arr='%d', nb_cantons='%d', nb_communes='%s', pop_municipale='%d', pop_tot='%d')>" % \
                                                    (self.code_region, self.nom_region, self.code_dpt,
                                                     self.nom_dpt, self.nb_arr, self.nb_cantons,
                                                     self.nb_communes, self.pop_municipale, self.pop_tot)

class Region(Base):
    __tablename__ = 'regions'

    code_region = Column(Integer, primary_key=True)
    nom_region = Column(String(50))
    nb_arr = Column(Integer)
    nb_cantons = Column(Integer)
    nb_communes = Column(Integer)
    pop_municipale = Column(Integer)
    pop_tot = Column(Integer)

    def __repr__(self):
        return "<Region(code_region='%d', nom_region='%s'," \
               " nb_arr='%d', nb_cantons='%d', nb_communes='%s', pop_municipale='%d', pop_tot='%d')>" % \
                                                    (self.code_region, self.nom_region,
                                                     self.nb_arr, self.nb_cantons,
                                                     self.nb_communes, self.pop_municipale, self.pop_tot)


def ParseAndPopulate():
    # Régions
    region_file = '../../data/regions.csv'
    with open(region_file, 'rt') as file:
        session = Session()
        ignore = 8 # Ignore 8 premières lignes
        current = 0
        for line in file:
            current += 1
            if current > ignore:
                str = line.split(';')
                if len(str) == 7:
                    if str[3] == "":
                        str[3] = "0"
                    new_region = Region(code_region=int(str[0]),
                                        nom_region=str[1],
                                        nb_arr=int(str[2]),
                                        nb_cantons=int(str[3]),
                                        nb_communes=int(str[4].replace(" ", "")),
                                        pop_municipale=int(str[5].replace(" ", "")),
                                        pop_tot=int(str[6].replace(" ", "")))
                    session.add(new_region)
        session.commit()
        print("Régions OK")

    # Départements
    dpt_file = '../../data/departements.csv'
    with open(dpt_file, 'rt') as file:
        session = Session()
        ignore = 8  # Ignore 8 premières lignes
        current = 0
        for line in file:
            current += 1
            if current > ignore:
                str = line.split(';')
                if str[5] == "":
                    str[5] = "0"
                new_dpt = Departement(code_region=int(str[0]),
                                    nom_region=str[1],
                                    code_dpt=str[2],
                                    nom_dpt=str[3],
                                    nb_arr=int(str[4]),
                                    nb_cantons=int(str[5]),
                                    nb_communes=int(str[6].replace(" ", "")),
                                    pop_municipale=int(str[7].replace(" ", "")),
                                    pop_tot=int(str[8].replace(" ", "")))
                region = session.query(Region).filter(Region.code_region == new_dpt.code_region).first()
                region.departements.append(new_dpt)
            session.commit()
        print("Départements OK")

    # Communes
    commune_file = '../../data/communes.csv'
    with open(commune_file, 'rt') as file:
        session = Session()
        ignore = 8  # Ignore 8 premières lignes
        current = 0
        for line in file:
            current += 1
            if current > ignore:
                str = line.split(';')
                if str[4] == "":
                    str[4] = "0"
                new_commune = Commune(
                                    code_dpt=str[2],
                                    code_arr=int(str[3]),
                                    code_canton=int(str[4]),
                                    code_commune=int(str[5]),
                                    nom_commune=str[6],
                                    pop_municipale=int(str[7].replace(" ", "")),
                                    pop_a_part=int(str[8].replace(" ", "")),
                                    pop_tot=int(str[9].replace(" ", "")))
                session.add(new_commune)
        session.commit()
        print("Communes OK")

def CreerBase():
    # Création du schéma
    Commune.__table__.drop(engine)
    Departement.__table__.drop(engine)
    Region.__table__.drop(engine)
    Base.metadata.create_all(engine)

    # Parsing et Remplissage
    ParseAndPopulate()

# Calcul populations
def ComparePop():
    session = Session()
    regions = session.query(Region).all()
    erreurReg = ""
    erreurDpt = ""
    for region in regions:
        popReg = 0
        for departement in region.departements:
            popDpt = 0
            for commune in departement.communes:
                popDpt += commune.pop_tot
            print("Dpt : ", departement.nom_dpt, " : ", popDpt, " calculé  |  ", departement.pop_tot, " fichier")
            if popDpt != departement.pop_tot:
                erreurDpt += departement.nom_dpt + " "
            popReg += popDpt
        print("### Reg : ", region.nom_region, " : ", popReg, " calculé  |  ", region.pop_tot, " fichier")
        if popReg != region.pop_tot:
            erreurReg += region.nom_region + " "
    print("Populations régionales erronées : ", erreurReg)
    print("Populations départementales erronées : ", erreurDpt)

def CommunesDoublon():
    session = Session()
    regions = session.query(Region).all()
    communesFaites = []
    for region in regions:
        for departement in region.departements:
            for commune in departement.communes:
                if commune.nom_commune not in communesFaites:
                    communesFaites.append(commune.nom_commune)
                    dpts = session.query(Commune).filter(Commune.nom_commune == commune.nom_commune).all()
                    if(len(dpts) > 1):
                        str = "Doublon : " + commune.nom_commune + " : "
                        for doublon in dpts:
                            str += doublon.code_dpt + " "
                        print(str)

# taken from http://effbot.org/zone/element-lib.htm#prettyprint
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def SauvXML():
    session = Session()
    regions = session.query(Region).all()
    regionsET = ET.Element("regions")
    tree = ET.ElementTree(regionsET)
    for region in regions:
        regionET = ET.SubElement(regionsET, "region")
        regionET.set("code_region", str(region.code_region))
        regionET.set("nom_region", str(region.nom_region))
        regionET.set("nb_arr", str(region.nb_arr))
        regionET.set("nb_cantons", str(region.nb_cantons))
        regionET.set("nb_communes", str(region.nb_communes))
        regionET.set("pop_municipale", str(region.pop_municipale))
        regionET.set("pop_tot", str(region.pop_tot))
        for departement in region.departements:
            departementET = ET.SubElement(regionET, "departement")
            departementET.set("code_region", str(departement.code_region))
            departementET.set("nom_region", str(departement.nom_region))
            departementET.set("code_dpt", str(departement.code_dpt))
            departementET.set("nom_dpt", str(departement.nom_dpt))
            departementET.set("nb_arr", str(departement.nb_arr))
            departementET.set("nb_cantons", str(departement.nb_cantons))
            departementET.set("nb_communes", str(departement.nb_communes))
            departementET.set("pop_municipale", str(departement.pop_municipale))
            departementET.set("pop_tot", str(departement.pop_tot))
            for commune in departement.communes:
                communeET = ET.SubElement(departementET, "commune")
                communeET.set("code_dpt", str(commune.code_dpt))
                communeET.set("code_arr", str(commune.code_arr))
                communeET.set("code_canton", str(commune.code_canton))
                communeET.set("code_commune", str(commune.code_commune))
                communeET.set("nom_commune", str(commune.nom_commune))
                communeET.set("pop_municipale", str(commune.pop_municipale))
                communeET.set("pop_a_part", str(commune.pop_a_part))
                communeET.set("pop_tot", str(commune.pop_tot))
    indent(regionsET)
    tree.write("save.xml", encoding="UTF-8")

def ChargXML():
    session = Session()
    tree = ET.parse('save.xml')
    root = tree.getroot()
    for regionET in root:
        region = Region()
        region.code_region = regionET.attrib["code_region"]
        region.nom_region = regionET.attrib["nom_region"]
        region.nb_arr = regionET.attrib["nb_arr"]
        region.nb_cantons = regionET.attrib["nb_cantons"]
        region.nb_communes = regionET.attrib["nb_communes"]
        region.pop_municipale = regionET.attrib["pop_municipale"]
        region.pop_tot = regionET.attrib["pop_tot"]
        session.add(region)
        for departementET in regionET:
            departement = Departement()
            departement.code_dpt = departementET.attrib["code_dpt"]
            departement.code_region = departementET.attrib["code_region"]
            departement.nom_region = departementET.attrib["nom_region"]
            departement.nom_dpt = departementET.attrib["nom_dpt"]
            departement.nb_arr = departementET.attrib["nb_arr"]
            departement.nb_cantons = departementET.attrib["nb_cantons"]
            departement.nb_communes = departementET.attrib["nb_communes"]
            departement.pop_municipale = departementET.attrib["pop_municipale"]
            departement.pop_tot = departementET.attrib["pop_tot"]
            session.add(departement)
            for communeET in departementET:
                commune = Commune()
                commune.code_dpt = communeET.attrib["code_dpt"]
                commune.code_arr = communeET.attrib["code_arr"]
                commune.code_canton = communeET.attrib["code_canton"]
                commune.code_commune = communeET.attrib["code_commune"]
                commune.nom_commune = communeET.attrib["nom_commune"]
                commune.pop_municipale = communeET.attrib["pop_municipale"]
                commune.pop_a_part = communeET.attrib["pop_a_part"]
                commune.pop_tot = communeET.attrib["pop_tot"]
                session.add(commune)
    session.commit()
ChargXML()
