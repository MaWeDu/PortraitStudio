"""Editable portrait suggestions and plain-language selection labels."""
from portrait_core import QUESTIONS

DESCRIPTIONS = {
    'Bewerbung und LinkedIn': 'für Bewerbungsunterlagen und berufliches Profil',
    'Bewerbungsfoto': 'für Lebenslauf und Bewerbung', 'LinkedIn': 'für dein berufliches Onlineprofil',
    'Business-Porträt': 'für Website, Teamseite oder berufliche Vorstellung',
    'Business Casual': 'gepflegt und entspannt, z. B. Hemd oder Bluse ohne Krawatte',
    'Klassisch formell': 'z. B. Anzug oder Kostüm, auf Wunsch mit Krawatte',
    'Modern Business': 'klarer Business-Look, z. B. Sakko oder Blazer mit schlichtem Oberteil',
    'Smart Casual': 'gehobener Freizeitlook, z. B. Feinstrick oder Polo',
    'Wie auf den Referenzfotos': 'vorhandene Kleidung beibehalten',
    'Eigene Vorgabe': 'deinen Wunsch im Detailfeld beschreiben',
    'Neutrales Fotostudio': 'ruhige einfarbige Fläche ohne Ablenkung',
    'Dezentes modernes Büro': 'zurückhaltende, leicht unscharfe Arbeitsumgebung',
    'Helle Architektur': 'helle Wände oder klare Gebäudelinien im Hintergrund',
    'Warmer dezenter Hintergrund': 'sanfte warme Farbtöne und ruhige Umgebung',
    'Freundlich und natürlich': 'entspannter Ausdruck, ungezwungen und offen',
    'Ruhig und souverän': 'gelassener Blick und aufrechte Haltung',
    'Leicht lächelnd': 'kleines, dezentes Lächeln',
    'Seriös und konzentriert': 'aufmerksamer Blick und zurückhaltende Mimik',
    'Kopf und Schultern, leicht gedreht': 'enger Ausschnitt mit etwas seitlich gedrehtem Oberkörper',
    'Kopf und Schultern, frontal': 'enger Ausschnitt, Oberkörper gerade zur Kamera',
    'Bis zur Brustmitte, leicht gedreht': 'mehr Kleidung sichtbar, Oberkörper etwas seitlich',
    'Weiteres Halbporträt': 'mehr vom Oberkörper und der Umgebung sichtbar',
    'Minimal; Hautstruktur erhalten': 'nur sehr dezente Korrekturen, Poren bleiben sichtbar',
    'Leicht; nur vorübergehende Hautunreinheiten': 'z. B. einzelne Pickel korrigieren, dauerhafte Merkmale erhalten',
    'Keine Retusche': 'Haut und persönliche Merkmale unverändert lassen',
    'Unverändert wie auf den Referenzfotos': 'Frisur und Styling beibehalten',
    'Haare und Kleidung leicht ordnen': 'abstehende Haare oder Falten dezent richten',
    '1': 'ein Porträt', '3': 'drei Varianten', '5': 'fünf Varianten',
    'Zeitlos und klassisch': 'ruhige Farben und traditionelle Porträtgestaltung',
    'Dezent modern': 'klare Gestaltung und frische, zurückhaltende Farben',
    'Direkt in die Kamera': 'direkter Blickkontakt', 'Leicht versetzt': 'knapp an der Linse vorbeischauen',
    'Dezent seitlich': 'Blick etwas zur Seite',
    '4:5 und 1:1': 'Hochformat und quadratisch', '4:5': 'kompaktes Hochformat',
    '3:4': 'etwas längeres Hochformat', '1:1': 'quadratisch, z. B. für Profilbilder',
}

def option_label(value):
    return f'{value} ({DESCRIPTIONS[value]})'

# These are starting points for a photographic style, not rules about people.
JOB_PRESETS = {
    'IT / Softwareentwicklung': ('Softwareentwicklung / IT', 'Smart Casual', 'Dezentes modernes Büro', 'Freundlich und natürlich', 'Dezent modern'),
    'Data Analyst / Data Science': ('Data Analyst / Data Science', 'Business Casual', 'Dezentes modernes Büro', 'Ruhig und souverän', 'Dezent modern'),
    'Büro / Verwaltung': ('Büro / Verwaltung', 'Business Casual', 'Neutrales Fotostudio', 'Freundlich und natürlich', 'Zeitlos und klassisch'),
    'Finanzen / Bank / Versicherung': ('Finanzen / Bank / Versicherung', 'Klassisch formell', 'Neutrales Fotostudio', 'Ruhig und souverän', 'Zeitlos und klassisch'),
    'Beratung / Projektmanagement': ('Beratung / Projektmanagement', 'Modern Business', 'Helle Architektur', 'Ruhig und souverän', 'Dezent modern'),
    'Vertrieb / Kundenservice': ('Vertrieb / Kundenservice', 'Business Casual', 'Warmer dezenter Hintergrund', 'Leicht lächelnd', 'Zeitlos und klassisch'),
    'Marketing / Kommunikation': ('Marketing / Kommunikation', 'Modern Business', 'Helle Architektur', 'Freundlich und natürlich', 'Dezent modern'),
    'Design / Kreativberufe': ('Design / Kreativberufe', 'Smart Casual', 'Warmer dezenter Hintergrund', 'Freundlich und natürlich', 'Dezent modern'),
    'Gesundheit / Pflege / Therapie': ('Gesundheit / Pflege / Therapie', 'Business Casual', 'Neutrales Fotostudio', 'Freundlich und natürlich', 'Zeitlos und klassisch'),
    'Bildung / Soziales': ('Bildung / Soziales', 'Smart Casual', 'Warmer dezenter Hintergrund', 'Freundlich und natürlich', 'Zeitlos und klassisch'),
    'Ingenieurwesen / Technik': ('Ingenieurwesen / Technik', 'Business Casual', 'Neutrales Fotostudio', 'Ruhig und souverän', 'Zeitlos und klassisch'),
    'Handwerk / Produktion / Logistik': ('Handwerk / Produktion / Logistik', 'Smart Casual', 'Neutrales Fotostudio', 'Freundlich und natürlich', 'Zeitlos und klassisch'),
    'Führung / Management': ('Führung / Management', 'Modern Business', 'Dezentes modernes Büro', 'Ruhig und souverän', 'Zeitlos und klassisch'),
    'Ausbildung / Studium / Berufseinstieg': ('Ausbildung / Studium / Berufseinstieg', 'Business Casual', 'Neutrales Fotostudio', 'Freundlich und natürlich', 'Zeitlos und klassisch'),
}

def preset_answers(job):
    context, outfit, background, expression, style = JOB_PRESETS[job]
    result = {key: options[0] if options else '' for key, _, options in QUESTIONS}
    result.update(context=context, outfit=outfit, background=background, expression=expression, style=style,
                  market='', gaze='Direkt in die Kamera', formats='4:5 und 1:1', notes='')
    for key, _, options in QUESTIONS:
        if options:
            result[key + '_detail'] = ''
    return result
