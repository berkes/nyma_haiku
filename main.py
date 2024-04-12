from itertools import cycle
import os
import random
import re
import time

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from rich import print
from rich.progress import track

model = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template( """
    You are a Gerbrand Adriaensz. Bredero, A seventeenth century Dutch poet
    that writes poems about people, entrepeneurs and companies.

    Write a sonnet about the company \"{company}\" in Dutch.

    Explain in the sonnet that this company is part of NYMA.
    The NYMA is an incubator for creative, innovative, companies and crafstmen.
    Write in twentiest century Dutch, but use some words from romanticism.

    Mention the name of the company only once. Mention NYMA only once.
    """)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

companies = [
    "10KB",
    "Aha!Lab",
    "ALBA Booking + Management",
    "All You Can Stream",
    "ANDC",
    "Anna Treurniet",
    "ARK Rewilding Nederland",
    "Atelier Herbestemming",
    "Atelier Joost Seegers",
    "Bartswerk",
    "Be Grace Coaching",
    "Boeijenjong Architecten",
    "Bokmans Maatwerk",
    "Boks Fabriek",
    "Bottendaalgroep",
    "Bureau in cc",
    "Bureau Stroom",
    "Busy Bike",
    "Christine Bornfeld",
    "Club Goud",
    "COURAGE Betekent",
    "Created, grafisch ontwerp studio",
    "Cultuur Academy",
    "De Achtertuin",
    "de Haarsmit",
    "De Markies Nijmegen BV",
    "De MoesApp",
    "De Schoenfabriek",
    "De Smeltkroes BV",
    "De Winkel van Winkel",
    "deMessenslijper",
    "DONKA",
    "Dorris Vooijs",
    "DUALarchitects",
    "Duncan de Fey fotografie",
    "Eendenverhuur NYMA",
    "Eventure Nederland BV",
    "Fleuranova – The Bubbly Brand Studio",
    "Flowra",
    "Fotobolwerk",
    "Fysiokracht",
    "Galloway Recording Studio",
    "Gloed tegelkachels",
    "Go Cameo",
    "Grafische Werkplaats Nijmegen",
    "Groenewas",
    "Gustavson",
    "HAN Civil Society Lab",
    "HAN university of Applied Sciences",
    "Hein Rutjes App & Software development",
    "Hella +Elke",
    "Hello Tuesday ",
    "Het Derde Beeld",
    "Het Inktlokaal",
    "Huting.net",
    "IDKR8",
    "illustratiesenzo of gewoon Doesjka Bramlage",
    "Infolearn",
    "Ingeving",
    "J Ontwerp",
    "Jonge Helden Academie",
    "JORDAN ARTISAN",
    "Karen Vermeer",
    "Klerkx project- en procesmanagement",
    "Marcelle Hilgers",
    "Matia Studio",
    "Meet Me There Management, Music & Publishing",
    "Moiety Film",
    "More or Less Design",
    "Movus",
    "My Dear Beer",
    "Ollie",
    "Onwijs Lekker IJs; De IJsprofessor",
    "Pain du Souterrain",
    "Patrick Feijen Script-ed…",
    "Pittig Bakkie",
    "Positive Impact Design",
    "Praktijk Sentio",
    "Precies Piet",
    "RDM Architecten",
    "ReVisie Design",
    "RH Beeld en Geluid, Music Wiriting Place",
    "Robbins Metaalwerkerij",
    "Rowan van Vreede",
    "ROX Escape Experience",
    "Rupsdesign",
    "Sandra Mesman – Betekenisvolle Communicatie",
    "Sara Donkers Fotografie",
    "Schitteren in je werk",
    "School voor Humor & Authenticiteit",
    "Simone Luijckx – Branding voor veranderaars",
    "SJAAN.lens.based.artist.",
    "Staalstudio Nimma",
    "Stefan van Hulten – Creative Storytelling",
    "Stichting 2cv4u",
    "Stichting Architectuurcentrum Nijmegen",
    "Studio Antonius",
    "Studio Do",
    "Studio Flix",
    "Studio Hartebeest",
    "Studio HOEK",
    "StudioBont",
    "StudioMIK",
    "Studio Waalplein",
    "Suzan Doornbos",
    "Team F",
    "Teken- en schilderschool TINT- Nijmegen",
    "Telpa Telecom en Marc Hoekstra Voice-over en stemacteur",
    "The Bike Media",
    "TIG Academy",
    "TMO",
    "Trafo",
    "Traject Tuin",
    "Tussen de Lijnen",
    "Upbeatles",
    "Vasim Circus Space",
    "Vasim Events",
    "Veel Soeps",
    "Verschilmakers Groep B.V.",
    "VideoExpress",
    "Viquel Automation",
    "VR Lab",
    "Waalkraft",
    "We Do",
    "What Els",
    "WP Wolf",
    "YUNGS",
]
random.shuffle(companies)
companies = cycle(companies)

rainbow = cycle([
    "green1",
    "spring_green2",
    "spring_green1",
    "medium_spring_green",
    "cyan2",
    "cyan1",
    "cyan2",
    "medium_spring_green",
    "spring_green1",
    "spring_green2",
    "green1",
])

def run_chain():
    # Clear the terminal
    os.system("clear")

    company = next(companies)
    company_re = re.compile(re.escape(company), re.IGNORECASE)
    nyma_re = re.compile(r"NYMA", re.IGNORECASE)


    first_chunk = True
    print(f"[bold cyan]{company}[/bold cyan] zit ook in de [bold]NYMA[/bold].\n\t")
    for chunk in chain.stream({"company": company}):
        # Start the first chunk with a tab
        if first_chunk:
            first_chunk = False
            print("\t", end="", flush=True)

        # if the chunk contains a newline, print a newline and a tab
        color = next(rainbow)
        chunk = chunk.replace("\n", "\n\t")
        # replace the company name with a bold version
        chunk = company_re.sub("[bold]"+company+"[/bold]", chunk)
        # replace NYMA with a bold version
        chunk = nyma_re.sub("[bold]NYMA[/bold]", chunk)

        print(f"[{color}]{chunk}[/{color}]", end="", flush=True)

    print("\n")
    print("Dit gedicht, een sonnet, is geschreven door AI.")
    print("Een experimentje van [bold]Bèr Kessels[/bold].")
    print("Meer weten over AI of deze matige dichter? Mail of app me: ber@berk.es, 06-29075065")

if __name__ == "__main__":
    wait = os.environ.get("WAIT")
    if wait:
        wait = int(wait)
    else:
        wait = 0

    while True:
        run_chain()
        for i in track(range(wait), description="Volgend gedicht wordt geschreven..."):
           time.sleep(1)
