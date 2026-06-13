import streamlit as st
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Cromos - Mundial 2026",
    page_icon="🏆",
    layout="wide"
)

# ============================================================
# LISTADO DE CROMOS INTEGRADO (48 equipos + especiales)
# ============================================================

CROMOS_POR_EQUIPO = {
    # ========== GRUPO A ==========
    "México": [f"MEX {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Luis Malagón", "Johan Vásquez", "Jorge Sánchez", "César Montes",
        "Jesús Gallardo", "Israel Reyes", "Diego Lainez", "Carlos Rodríguez", "Edson Álvarez",
        "Orbelin Pineda", "Marcel Ruiz", "Foto Equipo", "Érick Sánchez", "Hirving Lozano",
        "Santiago Giménez", "Raúl Jiménez", "Alexis Vega", "Roberto Alvarado", "César Huerta"
    ], start=1)],
    
    "Sudáfrica": [f"RSA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Ronwen Williams", "Sipho Chaine", "Aubrey Modiba", "Samukele Kabini",
        "Khuliso Mudau", "Khulumani Ndamane", "Siyabonga Ngezana", "Nkosinathi Sibisi",
        "Teboho Mokoena", "Thalente Mbatha", "Foto Equipo", "Bathusi Aubaas", "Yaya Sithole",
        "Sipho Mbule", "Lyle Foster", "Iqraam Rayners", "Mohau Nkota", "Oswin Appollis"
    ], start=1)],
    
    "Corea del Sur": [f"KOR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Hyeonwoo Jo", "Seunggyu Kim", "Minjae Kim", "Yumin Cho", "Youngwoo Seol",
        "Hanbeom Lee", "Taeseok Lee", "Myungjae Lee", "Jaesung Lee", "Inbeom Hwang",
        "Kangin Lee", "Foto Equipo", "Seungho Paik", "Jens Castrop", "Donggyeong Lee",
        "Guesung Cho", "Heungmin Son", "Heechan Hwang", "Hyeongyu Oh"
    ], start=1)],
    
    "República Checa": [f"CZE {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Matěj Kovář", "Jindřich Staněk", "Ladislav Krejčí", "Vladimír Coufal",
        "Jaroslav Zelený", "Tomáš Holeš", "David Zima", "Michal Sadílek", "Lukáš Provod",
        "Lukáš Červ", "Tomáš Souček", "Foto Equipo", "Pavel Šulc", "Matěj Vydra",
        "Vasil Kušej", "Tomáš Chorý", "Václav Černý", "Adam Hložek", "Patrik Schick"
    ], start=1)],
    
    # ========== GRUPO B ==========
    "Canadá": [f"CAN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Dayne St. Clair", "Alphonso Davies", "Alistair Johnston", "Samuel Adekugbe",
        "Samuel Richie Larvea", "Derek Cornelius", "Moïse Bombito", "Kamal Miller",
        "Stephen Eustáquio", "Ismaël Koné", "Jonathan Osorio", "Foto Equipo",
        "Jacob Shaffelburg", "Mathieu Choinière", "Niko Sigur", "Tajon Buchanan",
        "Liam Millar", "Dyle Larin", "Jonathan David"
    ], start=1)],
    
    "Bosnia-Herzegovina": [f"BIH {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Nikola Vasilj", "Amar Dedić", "Sead Kolašinac", "Tarik Muharemović",
        "Nihad Mujakić", "Nikola Katić", "Amir Hadžiahmetović", "Benjamin Tahirović",
        "Armin Gigović", "Ivan Šunjić", "Ivan Bašić", "Foto Equipo", "Dženis Burnić",
        "Esmir Bajraktarevic", "Amar Memić", "Ermedin Demirović", "Edin Džeko",
        "Samed Baždar", "Haris Tabaković"
    ], start=1)],
    
    "Qatar": [f"QAT {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Meshaal Barsham", "Sultan Albrake", "Lucas Mendes", "Homam Ahmed",
        "Boualem Khoukhi", "Pedro Miguel", "Tarek Salman", "Mohammed Mannai", "Karim Boudiaf",
        "Assim Madibo", "Hamed Fatehi", "Foto Equipo", "Mohammed Waad", "Abdulaziz Hatem",
        "Hassan Al-Haydos", "Edmilson Junior", "Akram Hassan Afif", "Ahmed Al-Ganehi", "Almoez Ali"
    ], start=1)],
    
    "Suiza": [f"SUI {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Gregor Kobel", "Yvon Mvogo", "Manuel Akanji", "Ricardo Rodríguez",
        "Nico Elvedi", "Aurèle Amenda", "Silvan Widmer", "Granit Xhaka", "Denis Zakaria",
        "Remo Freuler", "Fabian Rieder", "Foto Equipo", "Ardon Jashari", "Johan Manzambi",
        "Michel Aebischer", "Breel Embolo", "Rubén Vatgas", "Dan Ndoye", "Zeki Amdouni"
    ], start=1)],
    
    # ========== GRUPO C ==========
    "Brasil": [f"BRA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Alisson", "Bento", "Marquinhos", "Éder Militão", "Gabriel Magalhães",
        "Danilo", "Wesley", "Lucas Paquetá", "Casemiro", "Bruno Guimarães", "Luiz Henrique",
        "Foto Equipo", "Vinicius Júnior", "Rodrygo", "João Pedro", "Matheus Cunha",
        "Gabriel Martinelli", "Raphinha", "Estêvão"
    ], start=1)],
    
    "Marruecos": [f"MAR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Yassine Bounou", "Munir El Kajoui", "Achraf Hakimi", "Noussair Mazraoui",
        "Nayef Aguerd", "Romain Saïss", "Jawad El Yamiq", "Adam Masina", "Sofyan Amrabat",
        "Azzedine Ounahi", "Eliesse Ben Seghir", "Foto Equipo", "Bilal El Khannouss",
        "Ismael Saibari", "Youssef En-Nesyri", "Abde Ezzalzouli", "Soufiane Rahimi",
        "Brahim Díaz", "Ayoub El Kaabi"
    ], start=1)],
    
    "Haití": [f"HAI {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Johny Placide", "Carlens Arcus", "Martin Expérience", "Jean-Kévin Duverne",
        "Ricardo Adé", "Duke Lacroix", "Garven Metusala", "Hannes Delcroix", "Leverton Pierre",
        "Danley Jean Jacques", "Jean-Ricner Bellegarde", "Foto Equipo", "Christopher Attys",
        "Derrick Etienne Jr.", "Josué Casimir", "Ruben Providence", "Duckens Nazon",
        "Louicius Deedson", "Frantzdy Pierrot"
    ], start=1)],
    
    "Escocia": [f"SCO {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Angus Gunn", "Jack Hendry", "Kieran Tierney", "Aaron Hickey",
        "Andrew Robertson", "Scott McKenna", "John Souttar", "Anthony Ralston", "Grant Hanley",
        "Scott McTominay", "Billy Gilmour", "Foto equipo", "Lewis Ferguson", "Ryan Christie",
        "Kenny McLean", "John McGinn", "Lyndon Dykes", "Ché Adams", "Ben Gannon-Doak"
    ], start=1)],
    
    # ========== GRUPO D ==========
    "USA": [f"USA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Matt Freese", "Chris Richards", "Tim Ream", "Mark McKenzie", "Alex Freeman",
        "Antonee Robinson", "Tyler Adams", "Tanner Tessmann", "Weston McKenny",
        "Christian Roldan", "Timothy Weah", "Foto Equipo", "Diego Luna", "Malik Tillman",
        "Christian Pulisic", "Brenden Aaronson", "Ricardo Pepi", "Haji Wright", "Folarin Balogun"
    ], start=1)],
    
    "Paraguay": [f"PAR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Roberto Fernández", "Orlando Gill", "Diego Gómez", "Fabián Balbuena",
        "Juan José Cáceres", "Omar Alderete", "Júnior Alonso", "Mathías Villasanti",
        "Diego Gómez", "Damián Bobadilla", "Andrés Cubas", "Foto Equipo", "Matías Galarza Fonda",
        "Julio Enciso", "Alejandro Romero Gamarra", "Miguel Almirón", "Ramón Sosa",
        "Ángel Romero", "Antonio Sanabria"
    ], start=1)],
    
    "Australia": [f"AUS {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Mathew Ryan", "Joe Gauci", "Harry Souttar", "Alessandro Circati",
        "Jordan Bos", "Aziz Behich", "Cameron Burgess", "Lewis Miller", "Milos Degenek",
        "Jackson Irvine", "Riley McGree", "Team Photo", "Aiden O'Neill", "Connor Metcalfe",
        "Patrick Yazbek", "Craig Goodwin", "Kusini Yengi", "Nestory Irankunda", "Mohamed Touré"
    ], start=1)],
    
    "Turquía": [f"TUR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Uğurcan Çakır", "Mert Müldür", "Zeki Çelik", "Abdülkereím Bardakgi",
        "Çağlar Söyüncü", "Merih Demiral", "Ferdi Kadıoğlu", "Kaan Ayhan", "Ismail Yüksek",
        "Hakan Çalhanoğlu", "Orkun Kökçü", "Foto Equipo", "Arda Güler", "Irfan Can Kahveci",
        "Yunus Akgün", "Can Uzun", "Barış Alper Yılmaz", "Kerem Aktürkoğlu", "Kenan Yildiz"
    ], start=1)],
    
    # ========== GRUPO E ==========
    "Alemania": [f"GER {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Marc-André ter Stegen", "Jonathan Tah", "David Raum", "Nico Schlotterbeck",
        "Antonio Rüdiger", "Waldemar Anton", "Ridle Baku", "Maximilian Mittelstadt",
        "Joshua Kimmich", "Florian Wirtz", "Felix Nmecha", "Foto Equipo", "Leon Goretzka",
        "Jamal Musiala", "Serge Gnabry", "Kai Havertz", "Leroy Sané", "Karim Adeyemi",
        "Nick Woltemade"
    ], start=1)],
    
    "Curaçao": [f"CUW {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Eloy Room", "Armando Obispo", "Sherel Floranus", "Jurien Gaari",
        "Joshua Bremet", "Roshon Van Eijma", "Shurandy Sambo", "Livano Comenencia",
        "Godfried Roemeratoe", "Juninho Bacuna", "Leandro Bacuna", "Foto Equipo", "Tahith Chong",
        "Kenji Gorré", "Jearl Margaritha", "Jürgen Locadia", "Jeremy Antonisse",
        "Gervane Kastaneer", "Sontje Hansen"
    ], start=1)],
    
    "Costa de Marfil": [f"CIV {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Yahia Fofana", "Ghislain Konan", "Wilfried Singo", "Odilon Kossounou",
        "Evan Ndicka", "Willy Boly", "Emmanuel Agbadou", "Ousmane Diomande", "Franck Kessié",
        "Seko Fofana", "Ibrahim Sangaré", "Foto Equipo", "Jean-Philippe Gbamin", "Amad Diallo",
        "Sébastien Haller", "Simon Adingra", "Yan Diomande", "Evann Guessand", "Oumar Diakité"
    ], start=1)],
    
    "Ecuador": [f"ECU {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Hernán Galíndez", "Gonzalo Valle", "Piero Hincapié", "Pervis Estupiñán",
        "Willian Pacho", "Ángelo Preciado", "Joel Ordóñez", "Moisés Caicedo", "Alan Franco",
        "Kendry Páez", "Pedro Vite", "Foto Equipo", "John Yeboah", "Leonardo Campana",
        "Gonzalo Plata", "Nilson Angulo", "Alan Minda", "Kevin Rodríguez", "Enner Valencia"
    ], start=1)],
    
    # ========== GRUPO F ==========
    "Países Bajos": [f"NED {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Bart Verbruggen", "Virgil van Dijk", "Micky van de Ven", "Jurien Timber",
        "Denzel Dumfries", "Nathan Aké", "Jeremie Frimpong", "Jan Paul van Hecke",
        "Tijjani Reijnders", "Ryan Gravenberch", "Teun Koopmeiners", "Foto Equipo",
        "Frenkie de Jong", "Xavi Simons", "Justin Kluivert", "Memphis Depay", "Donyel Malen",
        "Wout Weghorst", "Cody Gakpo"
    ], start=1)],
    
    "Japón": [f"JPN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Zion Suzuki", "Henry Heroki Mochizuki", "Ayumu Seko", "Junnosuke Suzuki",
        "Shogo Taniguchi", "Tsuyoshi Watanabe", "Kaishu Sano", "Yuki Soma", "Ao Tanaka",
        "Daichi Kamada", "Takefusa Kubo", "Foto Equipo", "Ritsu Doan", "Keito Nakamura",
        "Takumi Minamino", "Shuto Machino", "Junya Ito", "Koki Ogawa", "Ayase Ueda"
    ], start=1)],
    
    "Suecia": [f"SWE {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Viktor Johansson", "Isak Hien", "Gabriel Dudmundsson", "Emil Holm",
        "Voctor Nilsson Lindelöf", "Gustaf Lagerbielke", "Lucas Bergvall", "Hugo Larsson",
        "Jesper Karlström", "Yasin Ayari", "Mattias Svanberg", "Foto Equipo", "Daniel Svensson",
        "Ken Sema", "Roony Bardghji", "Dejan Kulusevski", "Anthony Elanga", "Alexander Isak",
        "Viktor Gvökeres"
    ], start=1)],
    
    "Túnez": [f"TUN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Bechir Ben Saïd", "Aymen Dahmen", "Van Valery", "Montassar Talbi",
        "Yassine Meriah", "Ali Abdi", "Dylan Bronn", "Ellyes Skhiri", "Aïssa Laïdouni",
        "Ferjani Sassi", "Mohamed Ali Ben Romdhane", "Foto Equipo", "Hannibal Mejbri",
        "Elias Achouri", "Elias Saad", "Hazem Mastouri", "Ismaël Gharbi", "Sayfallah Ltaief",
        "Naïm Sliti"
    ], start=1)],
    
    # ========== GRUPO G ==========
    "Bélgica": [f"BEL {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Thibaut Courtois", "Arthur Theate", "Timothy Castagne", "Zeno Debast",
        "Bradon Mechele", "Maxim De Cuyper", "Thomas Meunier", "Youri Tieleman", "Amadou Onana",
        "Nicolas Raskin", "Alexis Saelemaekers", "Foto Equipo", "Hans Vanaken", "Kevin De Bruyne",
        "Jërërmy Doku", "Charles de Ketelaere", "Leandro Trossard", "Loïs Openda", "Romelu Lukaku"
    ], start=1)],
    
    "Egipto": [f"EGY {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Mohamed Elshenawy", "Mohamed Hany", "Mohamed Hamdy", "Yasser Ibrahim",
        "Khaled Sobhi", "Ramy Rabia", "Hossam Abdelmaguid", "Ahmes Fatouh", "Marwan Attia",
        "Zizo", "Hamdy Fathy", "Foto Equipo", "Mohanad Lasheen", "Emam Ashour", "Osama Faisal",
        "Mohamed Salah", "Mostafa Mohamed", "Trezeguet", "Omar Marsmoush"
    ], start=1)],
    
    "Irán": [f"IRN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Alireza Beiranvand", "Morteza Pouraliganji", "Ehsan Hajsafi", "Milad Mohammadi",
        "Shojae Khalilzadeh", "Ramin Rezaeian", "Hossein Kanaani", "Sadegh Moharrami",
        "Saleh Hardani", "Saeed Ezatolahi", "Saman Ghoddos", "Foto Equipo", "Omid Noorafkan",
        "Roozbeh Cheshmi", "Mohammad Mohebi", "Sardar Azmoun", "Mehdi Taremi",
        "Alireza Jahanbakhsh", "Ali Gholizadeh"
    ], start=1)],
    
    "Nueva Zelanda": [f"NZL {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Max Crocombe", "Alex Paulsen", "Michael Boxall", "Liberato Cacace",
        "Tim Payne", "Tyler Bindon", "Francis de Vries", "Finn Surman", "Joe Bell",
        "Sarpreet Singh", "Ryan Thomas", "Team Photo", "Matthew Garbett", "Marko Stamenić",
        "Ben Old", "Chris Wood", "Elijah Just", "Callum McCowatt", "Kosta Barbarouses"
    ], start=1)],
    
    # ========== GRUPO H ==========
    "España": [f"ESP {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Unai Simón", "Robin Le Normand", "Aymeric Laporte", "Dean Huijsen",
        "Pedro Porro", "Dani Carvajal", "Marc Cucurella", "Martín Zubimendi", "Rodri",
        "Pedri", "Fabián Ruiz", "Foto Equipo", "Mikel Merino", "Lamine Yamal", "Dani Olmo",
        "Nico Williams", "Ferran Torres", "Álvaro Morata", "Mikel Oyarzabal"
    ], start=1)],
    
    "Cabo Verde": [f"CPV {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Vozinha", "Logan Costa", "Pico", "Dinev", "Steven Moreira", "Wagner Pina",
        "João Paulo", "Yannick Semedo", "Kevin Pina", "Patrick Andrade", "Jamiro Monteiro",
        "Foto Equipo", "Deroy Duarte", "Garry Rodrigues", "Jovane Cabral", "Ryan Mendes",
        "Dailon Livramento", "Willy Semedo", "Beb"
    ], start=1)],
    
    "Arabia Saudí": [f"KSA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Nawaf Alaqidi", "Andulrahman Alsanbi", "Saud Abdulhamid", "Nawaf Bouwashl",
        "Jehad Thikri", "Moteb AlHarbi", "Hassan Altambakti", "Musab Aljuwayr", "Ziyad Aljohani",
        "Abdullah Alkhaibari", "Nasser Aldawsari", "Foto Equipo", "Saleh Abu Alshamat",
        "Marwan Alsahafi", "Salem Aldawsari", "Abdulrahman Alobud", "Feras Albrikan",
        "Saleh Alshehri", "Abdullah Alhamdan"
    ], start=1)],
    
    "Uruguay": [f"URU {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Sergio Rochet", "Santiago Mele", "Ronald Araújo", "José María Giménez",
        "Sebastián Cáceres", "Mathias Olivera", "Guillermo Varela", "Nhitam Nández",
        "Federico Valverde", "Giorgian de Arrascaeta", "Rodrigo Bentancur", "Foto Equipo",
        "Manuel Ugarte", "Nicolás de la Cruz", "Maxi Araújo", "Darwin Núñez", "Federico Viñas",
        "Rodrigo Aguirre", "Facundo Pellistri"
    ], start=1)],
    
    # ========== GRUPO I ==========
    "Francia": [f"FRA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Mike Maignan", "Theo Hernández", "William Saliba", "Jules Koundé",
        "Ibrahima Konaté", "Dayot Upamecano", "Lucas Digne", "Aurélien Tchouaméni",
        "Eduardo Camavinga", "Manu Koné", "Adrien Rabiot", "Foto Equipo", "Michael Olise",
        "Ousmane Dembélé", "Bradley Barcola", "Désiré Doué", "Kingsley Coman", "Hugo Ekitiké",
        "Kylian Mbappé"
    ], start=1)],
    
    "Senegal": [f"SEN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Eduardo Mendy", "Yehvann Diouf", "Moussa Niakhaté", "Abdoulaye Sec",
        "Ismail Jakobs", "El Hadji Malick Diouf", "Kalidou Koulibaly", "Idrissa Gana Gueye",
        "Pape Marar Sarr", "Pape Gueye", "Habib Diarra", "Foto Equipo", "Lamine Camara",
        "Sadio Mané", "Ismaïla Sarr", "Boulaye Dia", "Iliman Ndiaye", "Nicolas Jackson",
        "Krépin Diatta"
    ], start=1)],
    
    "Irak": [f"IRQ {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Jalal Hassan", "Rebin Sulaka", "Hussein Ali", "Akam Hashem", "Merchas Doski",
        "Zaid Tahseen", "Manaf Younis", "Zidane Iqbal", "Amir Al-Ammari", "Ibrahim Bavesh",
        "Ali Jasim", "Foto Equipo", "Youssef Amyn", "Aimar Sher", "Marko Farji", "Osama Rashid",
        "Ali Al-Hamadi", "Aymen Hussein", "Mohanad Ali"
    ], start=1)],
    
    "Noruega": [f"NOR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Ørjan Nyland", "Julian Ryerson", "Leo Østigård", "Kristoffer Vassbakk Ajer",
        "Marcus Holmgren Pedersen", "David Møller Wolfe", "Torbjørn Heggem", "Morten Thorsby",
        "Martin Ødegaard", "Sander Berge", "Andreas Schjelderup", "Foto Equipo", "Patrick Berg",
        "Erling Haaland", "Alexander Sørloth", "Aron Dønnum", "Jørgen Strand Larsen",
        "Antonio Musa", "Oscar Bobb"
    ], start=1)],
    
    # ========== GRUPO J ==========
    "Argentina": [f"ARG {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Emiliano Martínez", "Nahuel Molina", "Cristian Romero", "Nicolás Otamendi",
        "Nicolás Tagliafico", "Leonardo Balerdi", "Enzo Fernández", "Alexis Mac Allister",
        "Rodrigo de Paul", "Exequiel Palacios", "Leandro Paredes", "Foto Equipo", "Nico Paz",
        "Franco Mastantuono", "Nico González", "Lionel Messi", "Lautaro Martínez",
        "Julián Álvarez", "Giuliano Simeone"
    ], start=1)],
    
    "Argelia": [f"ALG {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Alexis Guendouz", "Ramy Bensebaini", "Youcef Atal", "Rayan Aït-Nouri",
        "Mohamed Amine Tougai", "Aïssa Mandi", "Ismaél Bennacer", "Houssem Aouar",
        "Hicham Boudaoui", "Ramiz Zerrouki", "Nabil Bentaleb", "Foto Equipo", "Farès Chaïbi",
        "Riyad Mahrez", "Saïd Benrahma", "Anis Hadj Moussa", "Amine Gouiri",
        "Baghdad Bounedjah", "Mohammed Amoura"
    ], start=1)],
    
    "Austria": [f"AUT {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Alexander Schlager", "Patrick Pentz", "David Alaba", "Kevin Danso",
        "Philipp Lienhart", "Stefan Bosch", "Phillipp Mwene", "Alexander Prass", "Xaver Schlager",
        "Marcel Sabitzer", "Konrad Laimer", "Foto Equipo", "Florian Grillitsch",
        "Nicolas Seiwald", "Romano Schmid", "Patrick Wimmer", "Christoph Baumgartner",
        "Michael Gregoritsch", "Marko Arnautović"
    ], start=1)],
    
    "Jordania": [f"JOR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Yazeed Abulaila", "Ihsan Haddad", "Mohammad Abu Hashish", "Yazan Al-Arab",
        "Abdullah Nasib", "Saleem Obaid", "Mohammad Abualnadi", "Ibrahim Saadeh",
        "Nizar Al-Rashdan", "Noor Al-Rawabder", "Mohannad Abu Taha", "Foto Equipo",
        "Amer Jamous", "Mousa Al-Taamari", "Yazan Al-Naimat", "Mahmoud Al-Mardi", "Ali Olwan",
        "Mohammad Abu Zrayq", "Ibrahim Sabra"
    ], start=1)],
    
    # ========== GRUPO K ==========
    "Portugal": [f"POR {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Diogo Costa", "José Sá", "Rubén Dias", "João Cancelo", "Diogo Dalot",
        "Nuno Mendes", "Gonçalo Inácio", "Bernado Silva", "Bruno Fernandes", "Rubén Neves",
        "Vitinha", "Foto Equipo", "João Neves", "Cristiano Ronaldo", "Francisco Trincão",
        "João Felix", "Gonçalo Ramos", "Pedro Neto", "Rafael Leão"
    ], start=1)],
    
    "Congo DR": [f"COD {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Lionel Mpasi", "Aaron Wan-Bissaka", "Axel Tuanzebe", "Arthur Masuaku",
        "Chancel Mbemba", "Joris Kavembe", "Charles Pickel", "Ngal'ayel Mukau", "Edo Kavembe",
        "Samuel Moutoussamy", "Noah Sadiki", "Foto Equipo", "Théo Bongonda", "Meschack Elia",
        "Yoane Wissa", "Brian Cipenga", "Fiston Mavele", "Cédric Bakambu", "Nathanaél Mbuku"
    ], start=1)],
    
    "Uzbekistán": [f"UZB {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Utkir Yusupov", "Farrukh Sayfiev", "Sherzod Nasrullaev", "Umar Eshmurodov",
        "Husniddin Aliqulov", "Rustam Ashurmatov", "Khojiakbar Alijonov", "Abdukodir Khusanov",
        "Odiljon Hamrobekov", "Otabek Shukurov", "Jamshid Iskanderov", "Foto Equipo",
        "Azizbek Turgunboev", "Khojimat Erkinov", "Eldor Shomurodov", "Oston Urunov",
        "Jalolidoin Masharipov", "Igor Sergeev"
    ], start=1)],
    
    "Colombia": [f"COL {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Camilo Vargas", "David Ospina", "Dávinson Sánchez", "Yerry Mina",
        "Daniel Muñoz", "Johan Mojica", "Jhon Lucumí", "Santiago Arias", "Jefferson Lerma",
        "Kevin Castaño", "Richard Ríos", "Foto Equipo", "James Rodríguez",
        "Juan Fernando Quintero", "Jorge Carrascal", "Jhon Arias", "Jhon Córdova",
        "Luis Suárez", "Luis Díaz"
    ], start=1)],
    
    # ========== GRUPO L ==========
    "Inglaterra": [f"ENG {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Jordan Pickford", "John Stones", "Marc Guéhi", "Ezri Konsa",
        "Trent Alexander-Arnold", "Reece James", "Dan Burn", "Jordan Henderson", "Declan Rice",
        "Jude Bellingham", "Cole Palmer", "Foto Equipo", "Morgan Rogers", "Anthony Gordon",
        "Phil Foden", "Bukayo Saka", "Harry Kane", "Marcus Rashford", "Ollie Watkins"
    ], start=1)],
    
    "Croacia": [f"CRO {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Dominik Livaković", "Duje Caleta-Car", "Joško Gvardiol", "Josip Stanišić",
        "Luka Vušković", "Josip Šutalo", "Kristijan Jakić", "Luka Modrić", "Mateo Kovacic",
        "Martin Baturina", "Lovro Majer", "Foto Equipo", "Mario Pašalić", "Petar Sučić",
        "Ivan Perišić", "Marco Pašalić", "Ante Budimir", "Andrej Kramarić", "Franjo Ivanović"
    ], start=1)],
    
    "Ghana": [f"GHA {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Lawrence Ati Zigi", "Tariq Lamptey", "Mohammed Salisu", "Alidu Seidu",
        "Alexander Djiku", "Gideon Mensah", "Caleb Yirenkyi", "Abdul Issahaku Fatawu",
        "Thomas Partey", "Salis Abdul Samed", "Kamaldeen Sulemana", "Foto Equipo",
        "Mohammed Kudus", "Iñaki Williams", "Jordan Ayew", "André Ayew", "Joseph Paintsil",
        "Osman Bukari", "Antoine Semenyo"
    ], start=1)],
    
    "Panamá": [f"PAN {i} - {nombre}" for i, nombre in enumerate([
        "Escudo", "Orlando Mosquera", "Luis Mejía", "Fidel Escobar", "Andrés Andrade",
        "Michael Amir Murillo", "Eric Davies", "José Córdoba", "César Blackman", "Cristian Martín",
        "Anibal Godoy", "Adalberto Carrasquilla", "Foto Equipo", "Édgar Bárcenas",
        "Carlos Harvey", "Ismael Díaz", "José Fajardo", "Cecilio Waterman", "José Luis Rodríguez",
        "Alberto Quintero"
    ], start=1)],
    
    # ========== SECCIONES ESPECIALES ==========
    "🏆 FIFA World Cup History": [
        "FWC 1 - Logo Mundial - Parte Superior",
        "FWC 2 - Logo Mundial - Parte Inferior", 
        "FWC 3 - Official Mascots",
        "FWC 4 - Official Slogan",
        "FWC 5 - Official Ball",
        "FWC 6 - Canadá - Host Country Emblem",
        "FWC 7 - México - Host Country Emblem",
        "FWC 8 - USA - Host Country Emblem",
        "FWC 9 - Italia - Mundial Italia 1934",
        "FWC 10 - Uruguay - Mundial Brasil 1950",
        "FWC 11 - Alemania - Mundial Suiza 1964",
        "FWC 12 - Brasil - Mundial Chile 1962",
        "FWC 13 - Alemania - Mundial Alemania 1974",
        "FWC 14 - Argentina - Mundial México 1986",
        "FWC 15 - Brasil - Mundial USA 1994",
        "FWC 16 - Brasil - Mundial Corea - Japón 2002",
        "FWC 17 - Italia - Mundial Alemania 2006",
        "FWC 18 - Alemania - Mundial Brasil 2014",
        "FWC 19 - Argentina - Mundial Catar 2022"
    ],
    
    "⭐ Extra Stickers": [
        "EXT 1 - Lionel Messi - Argentina",
        "EXT 2 - Jérémy Doku - Bélgica",
        "EXT 3 - Vinicius Júnior - Brasil",
        "EXT 4 - Alphonso Davies - Canadá",
        "EXT 5 - Luis Díaz - Colombia",
        "EXT 6 - Luka Modrić - Croacia",
        "EXT 7 - Moisés Caicedo - Ecuador",
        "EXT 8 - Mohamed Salah - Egipto",
        "EXT 9 - Jude Bellingham - Inglaterra",
        "EXT 10 - Kylian Mbappé - Francia",
        "EXT 11 - Florian Wirtz - Alemania",
        "EXT 12 - Raúl Jiménez - México",
        "EXT 13 - Achraf Hakimi - Marruecos",
        "EXT 14 - Cody Gakpo - Países Bajos",
        "EXT 15 - Erling Haaland - Noruega",
        "EXT 16 - Cristiano Ronaldo - Portugal",
        "EXT 17 - Heung-min Son - Corea del Sur",
        "EXT 18 - Lamine Yamal - España",
        "EXT 19 - Christian Pulisic - Estados Unidos",
        "EXT 20 - Federico Valverde - Uruguay"
    ],
    
    "🥤 Coca Cola - Edición España": [
        "CC1 - Lamine Yamal - España",
        "CC2 - Joshua Kimmich - Alemania",
        "CC3 - Eduardo Camavinga - Francia",
        "CC4 - Joško Gvardiol - Croacia",
        "CC5 - Federico Valverde - Uruguay",
        "CC6 - Virgil van Dijk - Países Bajos",
        "CC7 - Alphonso Davies - Canadá",
        "CC8 - Raúl Jiménez - México",
        "CC9 - William Saliba - Francia",
        "CC10 - Lautaro Martínez - Argentina",
        "CC11 - Harry Kane - Inglaterra",
        "CC12 - Antonee Robinson - Estados Unidos"
    ]
}

# ============================================================
# ICONOS PARA EQUIPOS
# ============================================================
ICONOS_EQUIPOS = {
    "España": "🇪🇸", "Argentina": "🇦🇷", "Brasil": "🇧🇷", "Francia": "🇫🇷",
    "Alemania": "🇩🇪", "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Portugal": "🇵🇹", "México": "🇲🇽",
    "USA": "🇺🇸", "Canadá": "🇨🇦", "Uruguay": "🇺🇾", "Países Bajos": "🇳🇱",
    "Bélgica": "🇧🇪", "Croacia": "🇭🇷", "Colombia": "🇨🇴", "Japón": "🇯🇵",
    "Corea del Sur": "🇰🇷", "Marruecos": "🇲🇦", "Senegal": "🇸🇳", "Egipto": "🇪🇬",
    "Suiza": "🇨🇭", "Australia": "🇦🇺", "Irán": "🇮🇷", "Arabia Saudí": "🇸🇦",
    "Sudáfrica": "🇿🇦", "Nueva Zelanda": "🇳🇿", "Turquía": "🇹🇷", "Austria": "🇦🇹",
    "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Noruega": "🇳🇴", "Suecia": "🇸🇪", "Irak": "🇮🇶",
    "Jordania": "🇯🇴", "Qatar": "🇶🇦", "Haití": "🇭🇹", "Curaçao": "🇨🇼",
    "Paraguay": "🇵🇾", "Argelia": "🇩🇿", "República Checa": "🇨🇿",
    "Bosnia-Herzegovina": "🇧🇦", "Cabo Verde": "🇨🇻", "Congo DR": "🇨🇩",
    "Costa de Marfil": "🇨🇮", "Ecuador": "🇪🇨", "Túnez": "🇹🇳", "Ghana": "🇬🇭",
    "Panamá": "🇵🇦", "Uzbekistán": "🇺🇿"
}

def obtener_icono(nombre):
    if nombre in ["🏆 FIFA World Cup History", "⭐ Extra Stickers", "🥤 Coca Cola - Edición España"]:
        return nombre[0]
    for key, icono in ICONOS_EQUIPOS.items():
        if key.lower() in nombre.lower() or nombre.lower() in key.lower():
            return icono
    return "⚽"

# ============================================================
# INICIALIZACIÓN
# ============================================================
if 'datos' not in st.session_state:
    st.session_state.datos = {}
if 'equipo_actual' not in st.session_state:
    st.session_state.equipo_actual = None
if 'json_cargado' not in st.session_state:
    st.session_state.json_cargado = False

# Cargar datos iniciales si están vacíos
if not st.session_state.datos:
    for equipo in CROMOS_POR_EQUIPO:
        st.session_state.datos[equipo] = {"faltas": [], "repes": []}

# ============================================================
# INTERFAZ
# ============================================================

st.title("🏆 GESTOR DE CROMOS - MUNDIAL 2026 🏆")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("💾 Guardar/Cargar progreso")
    
    # Guardar progreso
    if st.button("💾 Guardar progreso", use_container_width=True):
        json_str = json.dumps(st.session_state.datos, indent=4, ensure_ascii=False)
        st.download_button(
            label="📥 Descargar JSON",
            data=json_str,
            file_name=f"mi_coleccion_cromos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Cargar progreso
    uploaded_json = st.file_uploader(
        "Cargar progreso guardado (JSON)",
        type=['json'],
        key="json_upload"
    )
    
    if uploaded_json is not None:
        try:
            datos_json = json.load(uploaded_json)
            for equipo in CROMOS_POR_EQUIPO:
                if equipo not in datos_json:
                    datos_json[equipo] = {"faltas": [], "repes": []}
            st.session_state.datos = datos_json
            st.session_state.json_cargado = True
            st.success("✅ Progreso cargado")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    st.header("📊 Estadísticas")
    
    total_faltas = sum(len(d.get("faltas", [])) for d in st.session_state.datos.values())
    total_repes = sum(len(d.get("repes", [])) for d in st.session_state.datos.values())
    total_cromos = sum(len(c) for c in CROMOS_POR_EQUIPO.values())
    
    st.metric("📋 Equipos", len(CROMOS_POR_EQUIPO))
    st.metric("🎴 Cromos totales", total_cromos)
    st.metric("❌ Faltas totales", total_faltas)
    st.metric("🔄 Repes totales", total_repes)
    
    st.markdown("---")
    st.header("📥 Exportar")
    
    if st.button("📥 Exportar faltas y repes (CSV)", use_container_width=True):
        datos_exp = []
        for equipo, contenido in st.session_state.datos.items():
            for cromo in contenido.get("faltas", []):
                datos_exp.append({"Equipo": equipo, "Cromo": cromo, "Estado": "FALTA ❌"})
            for cromo in contenido.get("repes", []):
                datos_exp.append({"Equipo": equipo, "Cromo": cromo, "Estado": "REPETIDO 🔄"})
        
        if datos_exp:
            import pandas as pd
            df_exp = pd.DataFrame(datos_exp)
            csv = df_exp.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Descargar CSV",
                csv,
                f"faltas_repes_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.warning("No hay datos")

# ============================================================
# CONTENIDO PRINCIPAL
# ============================================================

# Selección de equipo
col_equipos, col_cromos = st.columns([1, 2])

with col_equipos:
    st.subheader("📋 Equipos")
    
    busqueda = st.text_input("🔍 Buscar", placeholder="Nombre del equipo...")
    
    # Separar especiales de normales
    equipos_especiales = ["🏆 FIFA World Cup History", "⭐ Extra Stickers", "🥤 Coca Cola - Edición España"]
    equipos_normales = [e for e in CROMOS_POR_EQUIPO.keys() if e not in equipos_especiales]
    
    equipos_filtrados = []
    if busqueda:
        for e in equipos_normales + equipos_especiales:
            if busqueda.lower() in e.lower():
                equipos_filtrados.append(e)
    else:
        equipos_filtrados = equipos_especiales + equipos_normales
    
    for equipo in equipos_filtrados:
        faltas_eq = len(st.session_state.datos.get(equipo, {}).get("faltas", []))
        total_eq = len(CROMOS_POR_EQUIPO.get(equipo, []))
        porcentaje = int(((total_eq - faltas_eq) / total_eq) * 100) if total_eq > 0 else 0
        
        icono = obtener_icono(equipo)
        
        if st.button(
            f"{icono} {equipo}",
            key=f"btn_{equipo}",
            use_container_width=True,
            type="secondary" if st.session_state.equipo_actual != equipo else "primary"
        ):
            st.session_state.equipo_actual = equipo
            st.rerun()
        
        # Mostrar barra de progreso
        st.progress(porcentaje / 100, text=f"{porcentaje}%")

with col_cromos:
    if st.session_state.equipo_actual:
        equipo = st.session_state.equipo_actual
        cromos = CROMOS_POR_EQUIPO.get(equipo, [])
        
        if not cromos:
            st.error("Equipo no encontrado")
        else:
            if equipo not in st.session_state.datos:
                st.session_state.datos[equipo] = {"faltas": [], "repes": []}
            
            icono = obtener_icono(equipo)
            st.subheader(f"{icono} {equipo}")
            
            faltas = set(st.session_state.datos[equipo].get("faltas", []))
            repes = set(st.session_state.datos[equipo].get("repes", []))
            
            total_eq = len(cromos)
            conseguidos = total_eq - len(faltas)
            porcentaje = int((conseguidos / total_eq) * 100) if total_eq > 0 else 0
            
            st.progress(porcentaje / 100)
            st.caption(f"📊 {conseguidos}/{total_eq} ({porcentaje}%) | 🔄 Repes: {len(repes)}")
            
            st.markdown("---")
            
            # Botones rápidos
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Todo conseguido", use_container_width=True):
                    st.session_state.datos[equipo]["faltas"] = []
                    st.session_state.datos[equipo]["repes"] = []
                    st.rerun()
            with col_b:
                if st.button("❌ Todo faltas", use_container_width=True):
                    st.session_state.datos[equipo]["faltas"] = cromos.copy()
                    st.session_state.datos[equipo]["repes"] = []
                    st.rerun()
            
            st.markdown("---")
            st.subheader("🎴 Listado de cromos")
            
            # Mostrar cromos (en grid de 2 columnas para mejor rendimiento)
            for idx in range(0, len(cromos), 2):
                col1, col2 = st.columns(2)
                
                # Cromo 1
                cromo1 = cromos[idx]
                conseguido1 = cromo1 not in faltas
                repetido1 = cromo1 in repes
                
                with col1:
                    with st.container(border=True):
                        st.markdown(f"**{cromo1}**")
                        nuevo_cons1 = st.checkbox("✅", value=conseguido1, key=f"c1_{equipo}_{idx}")
                        nuevo_rep1 = st.checkbox("🔄", value=repetido1, key=f"r1_{equipo}_{idx}", disabled=not nuevo_cons1)
                        
                        if nuevo_cons1 != conseguido1:
                            if nuevo_cons1:
                                faltas.discard(cromo1)
                            else:
                                faltas.add(cromo1)
                                repes.discard(cromo1)
                            st.session_state.datos[equipo]["faltas"] = list(faltas)
                            st.session_state.datos[equipo]["repes"] = list(repes)
                            st.rerun()
                        
                        if nuevo_rep1 != repetido1 and nuevo_cons1:
                            if nuevo_rep1:
                                repes.add(cromo1)
                            else:
                                repes.discard(cromo1)
                            st.session_state.datos[equipo]["repes"] = list(repes)
                            st.rerun()
                
                # Cromo 2 (si existe)
                if idx + 1 < len(cromos):
                    cromo2 = cromos[idx + 1]
                    conseguido2 = cromo2 not in faltas
                    repetido2 = cromo2 in repes
                    
                    with col2:
                        with st.container(border=True):
                            st.markdown(f"**{cromo2}**")
                            nuevo_cons2 = st.checkbox("✅", value=conseguido2, key=f"c2_{equipo}_{idx}")
                            nuevo_rep2 = st.checkbox("🔄", value=repetido2, key=f"r2_{equipo}_{idx}", disabled=not nuevo_cons2)
                            
                            if nuevo_cons2 != conseguido2:
                                if nuevo_cons2:
                                    faltas.discard(cromo2)
                                else:
                                    faltas.add(cromo2)
                                    repes.discard(cromo2)
                                st.session_state.datos[equipo]["faltas"] = list(faltas)
                                st.session_state.datos[equipo]["repes"] = list(repes)
                                st.rerun()
                            
                            if nuevo_rep2 != repetido2 and nuevo_cons2:
                                if nuevo_rep2:
                                    repes.add(cromo2)
                                else:
                                    repes.discard(cromo2)
                                st.session_state.datos[equipo]["repes"] = list(repes)
                                st.rerun()
    else:
        st.info("👈 Selecciona un equipo de la lista")

st.markdown("---")
st.caption("🏆 Gestor de Cromos - Mundial 2026 | 48 equipos + Historia + Extra Stickers + Coca Cola")