"""
Micro-Hotspots — Street & Suburb Level Crime Data
====================================================
Breaks police stations into sub-areas with specific:
- Suburbs / Sections / Zones
- Known dangerous streets and intersections
- Venue types (taverns, shebeens, taxi ranks, malls)
- Specific coordinates for street-level mapping
- Crime type dominant at that micro-location

Sources: SAPS crime scene data, news reports (News24, IOL, Daily Maverick,
GroundUp, Cape Argus), CPF reports, LEAP deployment reports, GI-TOC gang monitor
"""

MICRO_HOTSPOTS = [
    # ============================================================
    #  WESTERN CAPE — CAPE FLATS (Street-level)
    # ============================================================

    # --- KHAYELITSHA ---
    {"n":"Site B Supermarket","lat":-34.0445,"lng":18.6758,"parent":"Khayelitsha","p":"WC","suburb":"Site B",
     "street":"Ntlazane Rd","type":"venue","venue":"Supermarket",
     "crimes":[{"type":"shooting","desc":"4 killed in supermarket shooting","date":"Jan 2026","src":"News24","url":"https://www.news24.com/news24/southafrica"},{"type":"murder","desc":"Armed robbery turned fatal","date":"Dec 2025","src":"GroundUp","url":"https://www.groundup.org.za"}],
     "dominant":"shooting","risk":9,"note":"Jan 2026 mass shooting. 4 dead."},
    {"n":"Harare Section","lat":-34.0550,"lng":18.6830,"parent":"Khayelitsha","p":"WC","suburb":"Harare",
     "street":"Mew Way / Harare Square","type":"section","venue":"Residential",
     "crimes":[{"type":"shooting","desc":"3 men shot dead in Harare","date":"Jul 2025","src":"News24","url":"https://www.news24.com/news24/southafrica"},{"type":"murder","desc":"Gang-related killing","date":"Oct 2025","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"}],
     "dominant":"murder","risk":9,"note":"Multiple mass shootings 2025."},
    {"n":"Site C Taxi Rank","lat":-34.0380,"lng":18.6810,"parent":"Khayelitsha","p":"WC","suburb":"Site C",
     "street":"Spine Rd / Lwandle Rd","type":"venue","venue":"Taxi Rank",
     "crimes":[{"type":"robbery","desc":"Armed muggings at taxi rank","date":"Nov 2025","src":"Cape Argus","url":"https://www.iol.co.za/capeargus"},{"type":"carjack","desc":"Minibus taxi hijacked","date":"Sep 2025","src":"EWN","url":"https://ewn.co.za"}],
     "dominant":"robbery","risk":8,"note":"Peak crime: 5-7pm commuter hours."},
    {"n":"Makhaza","lat":-34.0350,"lng":18.7050,"parent":"Khayelitsha","p":"WC","suburb":"Makhaza",
     "street":"Steve Biko Rd","type":"section","venue":"Residential",
     "crimes":[{"type":"assault","desc":"Tavern brawl escalated to stabbing","date":"Dec 2025","src":"GroundUp","url":"https://www.groundup.org.za"}],
     "dominant":"assault","risk":7,"note":"Alcohol-fuelled violence dominant."},
    {"n":"Khayelitsha Mall Area","lat":-34.0405,"lng":18.6715,"parent":"Khayelitsha","p":"WC","suburb":"Site B",
     "street":"Ntlazane Rd / Khayelitsha CBD","type":"venue","venue":"Mall/Shopping",
     "crimes":[{"type":"robbery","desc":"Armed robbery at mall entrance","date":"Oct 2025","src":"IOL","url":"https://www.iol.co.za"},{"type":"kidnapping","desc":"Express kidnapping in parking lot","date":"Nov 2025","src":"News24","url":"https://www.news24.com"}],
     "dominant":"robbery","risk":8,"note":"Parking lot & ATM hotspot."},
    {"n":"Endlovini Informal","lat":-34.0520,"lng":18.6650,"parent":"Khayelitsha","p":"WC","suburb":"Endlovini",
     "street":"Off Mew Way","type":"settlement","venue":"Informal Settlement",
     "crimes":[{"type":"murder","desc":"Body found in informal area","date":"Jan 2026","src":"SABC","url":"https://www.sabcnews.com"}],
     "dominant":"murder","risk":9,"note":"Limited police access. No street lights."},

    # --- NYANGA ---
    {"n":"Borcherd's Quarry Rd","lat":-33.9830,"lng":18.5610,"parent":"Nyanga","p":"WC","suburb":"Nyanga",
     "street":"Borcherd's Quarry Rd","type":"street","venue":"Road",
     "crimes":[{"type":"carjack","desc":"Tourist shot following GPS through area","date":"2023","src":"News24","url":"https://www.news24.com"},{"type":"robbery","desc":"Multiple armed robberies on this road","date":"2025","src":"CPF Report","url":"https://www.saps.gov.za"}],
     "dominant":"carjack","risk":10,"note":"UK govt specifically warns against. Google removed route."},
    {"n":"Nyanga Junction (Terminus)","lat":-33.9875,"lng":18.5655,"parent":"Nyanga","p":"WC","suburb":"Nyanga",
     "street":"Klipfontein Rd / Lansdowne Rd","type":"venue","venue":"Taxi Rank/Terminus",
     "crimes":[{"type":"robbery","desc":"Daily muggings at terminus","date":"Ongoing","src":"CPF","url":"https://www.saps.gov.za"},{"type":"stabbing","desc":"Knife attacks near rank","date":"Dec 2025","src":"Cape Argus","url":"https://www.iol.co.za/capeargus"}],
     "dominant":"robbery","risk":9,"note":"#1 mugging hotspot in WC."},
    {"n":"Lusaka Section","lat":-33.9810,"lng":18.5700,"parent":"Nyanga","p":"WC","suburb":"Lusaka",
     "street":"NY1 / NY3","type":"section","venue":"Residential",
     "crimes":[{"type":"murder","desc":"Gang shooting in Lusaka","date":"Nov 2025","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"}],
     "dominant":"murder","risk":9,"note":"Gang territory. Firearms dominant."},
    {"n":"NY78 Shebeens","lat":-33.9850,"lng":18.5680,"parent":"Nyanga","p":"WC","suburb":"Nyanga East",
     "street":"NY78","type":"venue","venue":"Shebeen cluster",
     "crimes":[{"type":"assault","desc":"Weekend stabbings outside shebeens","date":"Ongoing","src":"SAPS","url":"https://www.saps.gov.za"},{"type":"murder","desc":"Fatal stabbing after drinking","date":"Jan 2026","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"assault","risk":8,"note":"Weekend peak: Fri-Sun midnight-4am."},

    # --- MITCHELLS PLAIN ---
    {"n":"Tafelsig","lat":-34.0620,"lng":18.6050,"parent":"Mitchells Plain","p":"WC","suburb":"Tafelsig",
     "street":"AZ Berman Dr / Spine Rd","type":"section","venue":"Residential",
     "crimes":[{"type":"shooting","desc":"50+ shootings in one week","date":"2025","src":"GI-TOC","url":"https://globalinitiative.net"},{"type":"gang","desc":"Fancy Boys vs Terrible Josters territory","date":"Ongoing","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"}],
     "dominant":"shooting","risk":10,"note":"Worst gang violence in SA. 50+ shootings/week 2025."},
    {"n":"Beacon Valley","lat":-34.0550,"lng":18.6150,"parent":"Mitchells Plain","p":"WC","suburb":"Beacon Valley",
     "street":"Beacon Valley Rd","type":"section","venue":"Residential",
     "crimes":[{"type":"shooting","desc":"Drive-by shooting","date":"Nov 2025","src":"News24","url":"https://www.news24.com"}],
     "dominant":"shooting","risk":9,"note":"Gang crossfire zone."},
    {"n":"Eastridge","lat":-34.0480,"lng":18.6180,"parent":"Mitchells Plain","p":"WC","suburb":"Eastridge",
     "street":"Merrydale Ave","type":"section","venue":"Residential",
     "crimes":[{"type":"drugs","desc":"Tik lab bust","date":"Oct 2025","src":"SAPS","url":"https://www.saps.gov.za"},{"type":"gang","desc":"Drug distribution hub","date":"Ongoing","src":"GI-TOC","url":"https://globalinitiative.net"}],
     "dominant":"drugs","risk":8,"note":"Methamphetamine (tik) hub."},
    {"n":"Promenade Mall Area","lat":-34.0500,"lng":18.6100,"parent":"Mitchells Plain","p":"WC","suburb":"Town Centre",
     "street":"AZ Berman Dr","type":"venue","venue":"Shopping Centre",
     "crimes":[{"type":"robbery","desc":"Armed robbery at mall parking","date":"Dec 2025","src":"IOL","url":"https://www.iol.co.za"},{"type":"carjack","desc":"Hijacking in parking lot","date":"Nov 2025","src":"Cape Argus","url":"https://www.iol.co.za/capeargus"}],
     "dominant":"robbery","risk":7,"note":"Parking lot crime hotspot."},

    # --- BONTEHEUWEL ---
    {"n":"Jakkalsvlei Ave / Jakes Gerwel Dr","lat":-33.9540,"lng":18.5420,"parent":"Bonteheuwel","p":"WC","suburb":"Bonteheuwel",
     "street":"Jakkalsvlei Ave & Jakes Gerwel Dr","type":"intersection","venue":"Traffic Light",
     "crimes":[{"type":"murder","desc":"Tourist Karin van Aardt stabbed to death at traffic light","date":"6 Dec 2024","src":"News24","url":"https://www.news24.com/news24/southafrica/news/camps-bay-tourist-stabbed-bonteheuwel"},{"type":"carjack","desc":"Multiple smash-and-grabs at intersection","date":"Ongoing","src":"CPF","url":"https://www.saps.gov.za"}],
     "dominant":"murder","risk":10,"note":"Tourist murdered Dec 2024. GPS routes through here from airport."},

    # ============================================================
    #  GAUTENG (Street-level)
    # ============================================================

    # --- HILLBROW ---
    {"n":"Twist St / Pretoria St","lat":-26.1940,"lng":28.0480,"parent":"Hillbrow","p":"GP","suburb":"Hillbrow",
     "street":"Twist St & Pretoria St","type":"intersection","venue":"Street",
     "crimes":[{"type":"robbery","desc":"Phone snatching and muggings daily","date":"Ongoing","src":"TimesLIVE","url":"https://www.timeslive.co.za"},{"type":"drugs","desc":"Open drug dealing","date":"Ongoing","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"}],
     "dominant":"robbery","risk":9,"note":"Don't walk with phone visible."},
    {"n":"Ponte City Tower","lat":-26.1975,"lng":28.0530,"parent":"Hillbrow","p":"GP","suburb":"Berea/Hillbrow",
     "street":"Lily Ave / Saratoga Ave","type":"venue","venue":"Residential Tower",
     "crimes":[{"type":"robbery","desc":"Muggings around Ponte base","date":"Ongoing","src":"News24","url":"https://www.news24.com"},{"type":"drugs","desc":"Drug dealing in building surrounds","date":"2025","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"robbery","risk":8,"note":"Iconic building but surrounds dangerous."},
    {"n":"Hillbrow Police Station Area","lat":-26.1965,"lng":18.0490,"parent":"Hillbrow","p":"GP","suburb":"Hillbrow",
     "street":"Kotze St","type":"area","venue":"Mixed commercial",
     "crimes":[{"type":"sexual","desc":"GBV incidents reported","date":"Ongoing","src":"SAPS","url":"https://www.saps.gov.za"}],
     "dominant":"sexual","risk":8,"note":"High GBV area. Overcrowded buildings."},

    # --- ALEXANDRA ---
    {"n":"London Rd / Far East Bank","lat":-26.1020,"lng":28.1080,"parent":"Alexandra","p":"GP","suburb":"Far East Bank",
     "street":"London Rd","type":"street","venue":"Commercial strip",
     "crimes":[{"type":"robbery","desc":"Business robberies on London Rd","date":"Dec 2025","src":"News24","url":"https://www.news24.com"},{"type":"kidnapping","desc":"Express kidnapping from spaza shop","date":"Nov 2025","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"robbery","risk":9,"note":"Main commercial strip. Heavy foot traffic."},
    {"n":"Madala Hostel Area","lat":-26.1050,"lng":28.0950,"parent":"Alexandra","p":"GP","suburb":"Alexandra Central",
     "street":"2nd Ave / 4th Ave","type":"area","venue":"Hostel/Residential",
     "crimes":[{"type":"murder","desc":"Stabbing near hostel","date":"Oct 2025","src":"TimesLIVE","url":"https://www.timeslive.co.za"}],
     "dominant":"murder","risk":9,"note":"Hostel tensions. Weapon violence."},
    {"n":"Pan Africa Taxi Rank","lat":-26.1070,"lng":28.0990,"parent":"Alexandra","p":"GP","suburb":"Alexandra",
     "street":"Pan Africa Dr","type":"venue","venue":"Taxi Rank",
     "crimes":[{"type":"robbery","desc":"Armed robberies at taxi rank","date":"Ongoing","src":"Citizen","url":"https://www.citizen.co.za"},{"type":"assault","desc":"Fight at taxi rank","date":"Dec 2025","src":"EWN","url":"https://ewn.co.za"}],
     "dominant":"robbery","risk":8,"note":"Rush hour danger zone 5-7pm."},

    # --- SOWETO ---
    {"n":"Vilakazi St / Orlando West","lat":-26.2368,"lng":27.9065,"parent":"Soweto - Orlando","p":"GP","suburb":"Orlando West",
     "street":"Vilakazi St","type":"street","venue":"Tourist/Commercial",
     "crimes":[{"type":"robbery","desc":"Tourist phone snatching","date":"Dec 2025","src":"News24","url":"https://www.news24.com"},{"type":"carjack","desc":"Attempted hijacking near Mandela House","date":"Sep 2025","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"robbery","risk":6,"note":"Tourist area but phone theft rampant."},
    {"n":"Jabulani Mall","lat":-26.2350,"lng":27.8550,"parent":"Soweto - Dobsonville","p":"GP","suburb":"Jabulani",
     "street":"Bolani Rd / Koma Rd","type":"venue","venue":"Mall",
     "crimes":[{"type":"robbery","desc":"Armed robbery in parking lot","date":"Nov 2025","src":"TimesLIVE","url":"https://www.timeslive.co.za"},{"type":"carjack","desc":"Vehicle hijacked leaving mall","date":"Oct 2025","src":"Citizen","url":"https://www.citizen.co.za"}],
     "dominant":"carjack","risk":7,"note":"Mall parking lot hotspot."},
    {"n":"Chris Hani Baragwanath Hospital Area","lat":-26.2640,"lng":27.9380,"parent":"Soweto - Diepkloof","p":"GP","suburb":"Diepkloof",
     "street":"Chris Hani Rd / Old Potch Rd","type":"area","venue":"Hospital vicinity",
     "crimes":[{"type":"robbery","desc":"Muggings near hospital entrance","date":"Ongoing","src":"News24","url":"https://www.news24.com"}],
     "dominant":"robbery","risk":6,"note":"Targeting hospital visitors."},

    # --- JHB CBD ---
    {"n":"Bree St Taxi Rank","lat":-26.2020,"lng":28.0400,"parent":"Johannesburg Central","p":"GP","suburb":"JHB CBD",
     "street":"Bree St / Sauer St","type":"venue","venue":"Taxi Rank",
     "crimes":[{"type":"robbery","desc":"Phone snatching and bag grabs","date":"Daily","src":"News24","url":"https://www.news24.com"},{"type":"assault","desc":"Muggings escalating to assault","date":"Ongoing","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"robbery","risk":9,"note":"Busiest taxi rank in SA. Peak danger."},
    {"n":"Jeppestown / Denver","lat":-26.2100,"lng":28.0600,"parent":"Johannesburg Central","p":"GP","suburb":"Jeppestown",
     "street":"Main Reef Rd / Jules St","type":"section","venue":"Mixed residential",
     "crimes":[{"type":"extortion","desc":"Construction mafia extortion","date":"2025","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"},{"type":"kidnapping","desc":"Business owner kidnapped","date":"Oct 2025","src":"News24","url":"https://www.news24.com"}],
     "dominant":"extortion","risk":8,"note":"Extortion capital. Construction mafia."},
    {"n":"Carlton Centre / Ghandi Square","lat":-26.2060,"lng":28.0480,"parent":"Johannesburg Central","p":"GP","suburb":"JHB CBD",
     "street":"Commissioner St / Von Wielligh St","type":"venue","venue":"Commercial",
     "crimes":[{"type":"robbery","desc":"Smash and grab near Carlton","date":"Dec 2025","src":"Citizen","url":"https://www.citizen.co.za"}],
     "dominant":"robbery","risk":7,"note":"Daytime pickpocketing. Night: avoid."},

    # --- SANDTON ---
    {"n":"Grayston Dr Off-Ramp","lat":-26.1050,"lng":28.0570,"parent":"Sandton","p":"GP","suburb":"Sandton",
     "street":"Grayston Dr / M1 off-ramp","type":"intersection","venue":"Highway Off-ramp",
     "crimes":[{"type":"carjack","desc":"Window smash hijacking at red light","date":"Nov 2025","src":"News24","url":"https://www.news24.com"},{"type":"robbery","desc":"Smash and grab targeting luxury vehicles","date":"Ongoing","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"carjack","risk":7,"note":"Peak: 6-8pm. Target luxury vehicles."},
    {"n":"Marlboro Taxi Rank","lat":-26.0900,"lng":28.1050,"parent":"Sandton","p":"GP","suburb":"Marlboro",
     "street":"Marlboro Dr","type":"venue","venue":"Taxi Rank",
     "crimes":[{"type":"robbery","desc":"Commuter muggings","date":"Ongoing","src":"TimesLIVE","url":"https://www.timeslive.co.za"}],
     "dominant":"robbery","risk":7,"note":"Contrast: affluent Sandton, dangerous rank."},

    # --- DIEPSLOOT ---
    {"n":"Diepsloot Extension 1","lat":-25.9280,"lng":28.0120,"parent":"Diepsloot","p":"GP","suburb":"Extension 1",
     "street":"R511 / Diepsloot Main","type":"settlement","venue":"Informal Settlement",
     "crimes":[{"type":"murder","desc":"Body found in open field","date":"Dec 2025","src":"News24","url":"https://www.news24.com"},{"type":"sexual","desc":"GBV incident reported","date":"Nov 2025","src":"SABC","url":"https://www.sabcnews.com"}],
     "dominant":"murder","risk":9,"note":"Mob justice incidents common."},

    # ============================================================
    #  KZN (Street-level)
    # ============================================================

    # --- INANDA ---
    {"n":"Amaoti Section","lat":-29.6680,"lng":30.8800,"parent":"Inanda","p":"KZN","suburb":"Amaoti",
     "street":"Amaoti Rd","type":"section","venue":"Residential",
     "crimes":[{"type":"murder","desc":"Multiple stabbings reported","date":"Dec 2025","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"murder","risk":9,"note":"Knife violence dominant."},
    {"n":"Bhambayi","lat":-29.6750,"lng":30.8650,"parent":"Inanda","p":"KZN","suburb":"Bhambayi",
     "street":"Bhambayi Rd","type":"settlement","venue":"Informal",
     "crimes":[{"type":"sexual","desc":"#1 nationally for rape","date":"Q3 2025","src":"SAPS","url":"https://www.saps.gov.za"},{"type":"assault","desc":"Domestic violence cluster","date":"Ongoing","src":"GroundUp","url":"https://www.groundup.org.za"}],
     "dominant":"sexual","risk":10,"note":"#1 rape station nationally. GBV crisis."},

    # --- DURBAN CBD ---
    {"n":"Point Rd / Victoria Embankment","lat":-29.8620,"lng":31.0250,"parent":"Durban Central","p":"KZN","suburb":"Point",
     "street":"Point Rd / Mahatma Gandhi Rd","type":"street","venue":"Entertainment district",
     "crimes":[{"type":"robbery","desc":"Muggings targeting tourists","date":"Ongoing","src":"News24","url":"https://www.news24.com"},{"type":"drugs","desc":"Open drug trade","date":"Ongoing","src":"IOL","url":"https://www.iol.co.za"}],
     "dominant":"robbery","risk":8,"note":"Night-time danger zone. Don't walk alone."},
    {"n":"Warwick Junction","lat":-29.8560,"lng":31.0150,"parent":"Durban Central","p":"KZN","suburb":"Warwick",
     "street":"Warwick Ave / Brook St","type":"venue","venue":"Transport Hub/Market",
     "crimes":[{"type":"robbery","desc":"Pickpocketing and bag snatching daily","date":"Ongoing","src":"TimesLIVE","url":"https://www.timeslive.co.za"},{"type":"assault","desc":"Trader disputes escalating","date":"2025","src":"Daily Maverick","url":"https://www.dailymaverick.co.za"}],
     "dominant":"robbery","risk":8,"note":"Busiest transport hub in KZN."},

    # ============================================================
    #  EASTERN CAPE (Street-level)
    # ============================================================
    {"n":"Govan Mbeki Ave / Central","lat":-33.9610,"lng":25.6000,"parent":"Gqeberha Central","p":"EC","suburb":"Central",
     "street":"Govan Mbeki Ave","type":"street","venue":"Commercial",
     "crimes":[{"type":"robbery","desc":"Daylight muggings","date":"Ongoing","src":"Herald","url":"https://www.heraldlive.co.za"}],
     "dominant":"robbery","risk":7,"note":"Main commercial strip."},
    {"n":"KwaZakhele Taverns","lat":-33.8775,"lng":25.6250,"parent":"KwaZakele","p":"EC","suburb":"KwaZakhele",
     "street":"Stanford Rd area","type":"venue","venue":"Tavern cluster",
     "crimes":[{"type":"assault","desc":"Weekend stabbings outside taverns","date":"Ongoing","src":"SAPS","url":"https://www.saps.gov.za"},{"type":"murder","desc":"Fatal stabbing after drinking","date":"Nov 2025","src":"Herald","url":"https://www.heraldlive.co.za"}],
     "dominant":"assault","risk":8,"note":"Fri-Sun peak. Alcohol-fuelled."},
]


def get_hotspots_for_station(station_name: str):
    """Get all micro-hotspots within a station's jurisdiction"""
    return [h for h in MICRO_HOTSPOTS if h['parent'] == station_name]


def get_hotspots_by_province(province: str):
    """Get all micro-hotspots in a province"""
    return [h for h in MICRO_HOTSPOTS if h['p'] == province]


def get_hotspots_by_risk(min_risk: int = 8):
    """Get highest-risk micro-hotspots"""
    return sorted([h for h in MICRO_HOTSPOTS if h['risk'] >= min_risk], 
                  key=lambda x: x['risk'], reverse=True)


if __name__ == '__main__':
    print(f"Total micro-hotspots: {len(MICRO_HOTSPOTS)}")
    print(f"\nTop 10 most dangerous specific locations:")
    for h in get_hotspots_by_risk(9)[:10]:
        print(f"  [{h['risk']}/10] {h['n']} ({h['suburb']}, {h['parent']})")
        print(f"          Street: {h['street']} | Type: {h['dominant']}")
        if h['crimes']:
            print(f"          Latest: {h['crimes'][0]['desc']} — {h['crimes'][0]['src']}")
