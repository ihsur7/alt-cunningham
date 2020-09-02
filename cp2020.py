import random as rm

def d110():
    return rm.randint(1,10)

class stats:
    def __init__(self, intel, ref, cl, tech, lk, att, ma, body, em):
        self.intel = intel
        self.ref = ref
        self.cl = cl
        self.tech = tech
        self.lk = lk
        self.att = att
        self.ma = ma
        self.ma_run = ma * 3
        self.ma_lift = self.ma_run / 4
        self.em = em
        self.hmty = em * 10
        self.body = body
        self.bdytype = None
        self.btm = None
        self.bt_lift = body * 10
        self.bt_dlift = body * 40
        if body <= 2:
            bdytype = 'Very Weak'
            btm = 0
        elif body == 3 or body == 4:
            bdytype = 'Weak'
            btm = -1
        elif body >= 5 and body == 7:
            bdytype = 'Average'
            btm = -2
        elif body == 8 or body == 9:
            bdytype = 'Strong'
            btm = -3
        else:
            bdytype = 'Very Strong'
            btm = -4
        print(bdytype, btm)
        self.savenum = body


class armour:
    def __init__(self, head, torso, rarm, larm, rleg, lleg):
        self.head = head
        self.torso = torso
        self.rarm = rarm
        self.larm = larm
        self.rleg = rleg
        self.lleg = lleg


class character:
    def __init__(self, handle, role):
        self.handle = handle
        self.role = role

class lifepath:
    clothes = ['Bike Leathers', 'Blue Jeans', 'Corporate Suits', 'Jumpsuits', 'Miniskirts', 'High Fashion', 'Cammos', 'Normal Clothes', 'Nude', 'Bag Lady Chick']
    hairstyle = ['Mohawk', 'Long & Ratty', 'Short & Spiked', 'Wild & all over', 'Bald', 'Striped', 'Tinted', 'Neat, short', 'Short, curly', 'Long, straight']
    affectations = ['Tattoos', 'Mirrorshades', 'Ritual Scars', 'Spiked Gloves', 'Nose Rings', 'Earrings', 'Long Fingernails', 'Spike heeled boots', 'Weird Contact Lenses', 'Fingerless gloves']
    ethnicbg = {'Anglo-American': ['English'],
                'African': ['Bantu', 'Fante', 'Kongo', 'Ashanti', 'Zulu', 'Swahili'],
                'Japanese': ['Japanese'],
                'Korean': ['Korean'],
                'Central European/Soviet': ['Bulgarian', 'Russian', 'Czech', 'Polish', 'Ukranian', 'Slovak'],
                'Pacific Islander': ['Microneasian', 'Tagalog', 'Polynesian', 'Malayan', 'Sudanese', 'Indonesian', 'Hawaiian'],
                'Chinese/Southeast Asian': ['Burmese', 'Cantonese', 'Mandarin', 'Thai', 'Tibetan', 'Vietnamese'],
                'Black American': ['English', 'Blackfolk'],
                'Hispanic American': ['Spanish', 'English'],
                'Central/South American': ['Spanish', 'Portuguese'],
                'European': ['French', 'German', 'English', 'Spanish', 'Italian', 'Greek', 'Danish', 'Dutch', 'Norwegian', 'Swedish', 'Finnish']
                }
    fambg = {'Family Ranking': ['Corporate Executive', 'Corporate Manager', 'Corporate Technician', 'Nomad Pack', 'Pirate Fleet', 'Gang Family', 'Crime Lord', 'Combat Zone Poor', 'Urban homeless', 'Arcology family'],
             'Parents': [{'1-6': 'Both parents are living. Go to FAMILY STATUS', '7-10': 'Something has happened to one or both parents. Go to SOMETHING HAPPENED TO YOUR PARENTS'}],
             'Family Status': [{'1-6': 'Family status in danger, and you risk losing everything (if you have not already. Go to FAMILY TRAJEDY', '7-10': 'Family status is OK, even if parents are missing or dead. Go to CHILDHOOD ENVIRONMENT'}],
             'Family Tragedy': ['Family lost everything through betrayal', 'Family lost everything through bad management', 'Family exiled or otherwise driven from their original home/nation/corporation',
                                'Family is imprisioned and you alone escaped', 'Family vanished. You are the only remaining member', 'Family was murdered/killed and you were the only survivor',
                                'Family is involved in a longterm conspiracy, organisation or association, such as a crime family or revolutionary group', 'Your family was scattered to the winds due to misfortune',
                                'Your family is cursed with a hereditary feud that has lasted for generations', 'You are the inheritor of a family debt; you must honor this debt before moving on with your life'],
             'Something happened to your parents': ['Your parent(s) died in warfare', 'Your parent(s) died in an accident', 'Your parent(s) were murdered', 'Your parent(s) have amnesia and do not remember you',
                                                    'You never knew your parent(s)', 'Your parent(s) are in hiding to protect you', 'You were left with relatives for safekeeping', 'You grew up on the Street and never had parents',
                                                    'Your parent(s) gave you up for adoption', 'Your parent(s) sold you for money'],
             'Childhood Environment': ['Spent on the Street, with no adult supervision', 'Spent in  a safe Corporate Suburbia', 'In a Nomad Pack moving from town to town', 'In a decaying, once upscale neighbourhood',
                                       'In a defended Corporate Zone in the central City', 'In the heart of the Combat Zone', 'In a small village or town far from the City', 'In a large arcology city', 'In an aquatic Pirate Pack',
                                       'On a Corporate controlled Farm or Research Facility'],
             'Siblings': []}
    # def __init__(self, playerclothes, playerhairstyles, playeraffectations, playerethnicbg, playerfambg):
    #     self.playerclothes = 


v = character('v', 'solo')
v = stats(10, 10, 10, 10, 10, 10, 10, 10, 10)