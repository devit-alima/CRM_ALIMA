# -*- coding: utf-8 -*-
from array import *
from datetime import datetime, date

from odoo import models, api, fields
TYPE_DON=[
    ('adhesion', 'Adhésion'),
    ('don', 'Don')
]
TYPE_CB=[
    ('Master Card', 'Master Card'),
    ('Visa', 'Visa'),
]
PLATEFORME=[
    ('iRaiser', 'iRaiser'),
    ('PayPal','PayPal'),
    ('Paybox','Paybox'),
    ('Netprelevement', 'Netprélèvement'),
    ('Alvarum', 'Alvarum'),
    ('Partenariat', 'Partenariat'),
    ('Autres','Autres'),
]

FORME_DON=[
    ('Compte bancaire', 'Compte bancaire'),
    ('Carte Bancaire', 'Carte Bancaire'),
    ('Cheque', 'Chèque'),
    ('Especes', 'Espèces'),
    ('Prelevement Salaire', 'Prélèvement Salaire'),
    ('Don manuel', 'Don manuel'),
]

MOYEN_PAIEMENT=[
                ('Abandon de creance','Abandon de Créance'),
                ('Especes','Espèces'),
                ('Cheque','Chèque'),
                ('Virement bancaire','Virement bancaire'),
                ('Prelevement','Prélèvement salaire'),
                ('Carte bancaire','Carte bancaire'),
                ('Compte bancaire','Compte bancaire'),
                ('SMS','SMS'),
                ('Autres','Autre(s)'),
                ]
MODE_VERSEMENT=[
    ('avec prelevement','avec prélèvement automatique'),
    ('sans prelevement','sans prélèvement automatique'),
]
FORME_DON_RECU=[
    ('Acte authentique', 'Acte authentique'),
    ('acte sous seing prive', 'Acte sous Seing privé'),
    ('declaration de don manuel', 'Déclaration de don manuel'),
    ('Don manuel', 'Don manuel'),
    ('Autres','Autres'),
]
TYPE_PRELEVEMENT=[
    ('Iraiser', 'Iraiser'),
    ('Netprelevement', 'Netprelevement')
]
DEVISE=[
    ('EUR', 'EUR'),
    ('XOF', 'XOF'),
    ('USD', 'USD'),
    ('GNF', 'GNF'),
    ('XAF', 'XAF'),
    ('Autre', 'Autre'),
]
TYPE_ENVOI=[
    ('Email', 'Email'),
    ('Courrier', 'Courrier')
]
NATURE_DON=[
    ('Numeraire', 'Numeraire'),
    ('Titres de Societes Cotees', 'Titres de Sociétés Côtées'),
    ('Autres', 'Autres'),
]
DROIT_REDUCTION_IMPOT=[
    ('200 du CGI IRP', '200 du CGI IRPP'),
    ('238 bis du CGI IS', '238 bis du CGI IS'),
    ('885-0 V bis A du CGI ISF', '885-0 V bis A du CGI ISF'),
]
OUIOUNON= [
    ('OUI','OUI'),
    ('NON','NON'),
]
TYPE_CB=[
    ('CB','CB'),
    ('VISA','VISA'),
    ('MasterCard','MasterCard'),
    ('AMEX','AMEX'),
]
LIBERALITE=[
    ('Don','Don'),
    ('Donation','Donation'),
    ('Legs','Legs'),
    ('Assurance-vie','Assurance-vie'),
]
RF=[
    ('R','R'),
    ('A','A'),
    ('N','N'),
]
SENS=[
    ('Eortant','Sortant'),
    ('Entrant','Entrant'),
]
schu=["","UN ","DEUX ","TROIS ","QUATRE ","CINQ ","SIX ","SEPT ","HUIT ","NEUF "]
schud=["DIX ","ONZE ","DOUZE ","TREIZE ","QUATORZE ","QUINZE ","SEIZE ","DIX SEPT ","DIX HUIT ","DIX NEUF "]
schd=["","DIX ","VINGT ","TRENTE ","QUARANTE ","CINQUANTE ","SOIXANTE ","SOIXANTE ","QUATRE VINGT ","QUATRE VINGT "]

class Don(models.Model):
    _name = 'crm.alima.don'
    _description = 'Dons'

    codeMedia=fields.Many2one('crm.alima.code.media', string='code media', ondelete='restrict')
    adhesion= fields.Selection(OUIOUNON, string="Adhesion")
    date=fields.Date(string="Date du don", required=True)
    forme_don=fields.Selection(FORME_DON_RECU, index=True, string='forme du don')
    nature_don=fields.Selection(NATURE_DON, string="Nature du don")
    liberalite=fields.Selection(LIBERALITE, string='Liberalite')
    moyen_paiment=fields.Selection(MOYEN_PAIEMENT, string="Moyen de paiement")
    mode_versement=fields.Selection(MODE_VERSEMENT, string="Mode de versement")
    commentaire=fields.Text(string="Commentaire")
    date_recep=fields.Date(string='Date de récéption du chèque')
    date_signature=fields.Date(string='Date de signature du chèque')
    date_remise=fields.Date(string='Date de remise du chèque')
    date_encais=fields.Date(string='Date d\'encaissement du chèque')
    montantEur=fields.Float(string="Montant du don en Euro")
    montantLettre=fields.Char(string="Montant en toutes lettres en euro", compute='convNombre2lettres', store=True)
    devis_origine=fields.Selection(DEVISE, string='Devis d\'origine')
    montant_dans_devise=fields.Float(string='montant dans la devise d\'origine', compute='tauxChange')
    taux_change=fields.Float(string='taux de change à la date du don', default=1)
    nom_banque=fields.Char(string='Non banque')
    numCheque=fields.Char(string='Numero cheque')
    remise_globale=fields.Boolean(string="remise globale")
    montant_remise_globale=fields.Float(string="montant remise globale")
    plateforme_paiement=fields.Selection(PLATEFORME, string='plateforme de paiement')
    parametreRF=fields.Selection(RF, string='RF')
    NumRecuFiscal=fields.Char(string="numero reçu fiscal")
    dateEdition=fields.Date(string='date édition RF')
    dateEnvoi=fields.Date(string='Date envoi RF')
    prelevement_en_cours=fields.Boolean(string='Prelevement en cours')
    commentaire_autre=fields.Text(string="Commentaire")
    donateur = fields.Many2one('crm.alima.donateur', string='donateur', required=True)
    montantEurSave=fields.Float(string='Montant du don en Euro sauvegarder')
    valide =fields.Boolean(dafault=False, string='Validation creation')
    id_intersa = fields.Char(string='ID Intersa')
    url_intersa = fields.Char(compute='_get_url_intersa', string="Url Intersa")
    datetime_import = fields.Datetime(readonly=True, string="Date Import")

    @api.multi
    def copy(self, default):
        self.ensure_one()
        self.donateur.nombreDons += 1
        return super(Don, self).copy(default)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res= super(Don, self).create(vals)
        res.montantEurSave= res.montantEur
        rec = res.donateur
        if not rec.datePremierDon:
            rec.datePremierDon =  res.date
            rec.montantPremierDon=res.montantEur
            rec.codemediaPremierDon=res.codeMedia
            rec.dateDernierDon= res.date
            rec.montantDernierDon= res.montantEur
            rec.codemediaDernierDon= res.codeMedia
            rec.cumulDonTotal=res.montantEur
            rec.nombreDons=1
            rec.don_moy=rec.cumulDonTotal
            rec.idpremierdon=res.id
            rec.iddernierdon=res.id
        else:
            if datetime.strptime(res.date,'%Y-%m-%d') > datetime.strptime(rec.dateDernierDon,'%Y-%m-%d'):
                rec.dateDernierDon= res.date
                rec.montantDernierDon=res.montantEur
                rec.codemediaDernierDon=res.codeMedia
                rec.cumulDonTotal=rec.cumulDonTotal + res.montantEur
                rec.nombreDons = rec.nombreDons + 1
                rec.don_moy = rec.cumulDonTotal/rec.nombreDons
                rec.iddernierdon = res.id
            if datetime.strptime(res.date,'%Y-%m-%d') < datetime.strptime(rec.datePremierDon,'%Y-%m-%d'):
                rec.datePremierDon = res.date
                rec.montantPremierDon = res.montantEur
                rec.codemediaPremierDon = res.codeMedia
                rec.cumulDonTotal = rec.cumulDonTotal + res.montantEur
                rec.nombreDons = rec.nombreDons + 1
                rec.don_moy = rec.cumulDonTotal/rec.nombreDons
                rec.idpremierdon = res.id
        if not rec.datePremierDonHPA and res.mode_versement !='avec prelevement':
            rec.datePremierDonHPA= res.date
            rec.montantPremierDonHPA=res.montantEur
            rec.codemediaPremierDonHPA=res.codeMedia
            rec.dateDernierDonHPA= res.date
            rec.montantDernierDonHPA= res.montantEur
            rec.codemediaDernierDonHPA= res.codeMedia
            rec.cumulDonHPA=res.montantEur
            rec.nombreDonsHPA=1
            rec.don_moyHPA=rec.cumulDonHPA
            rec.idpremierdonHPA=res.id
            rec.iddernierdonsHPA = res.id
        elif res.mode_versement !='avec prelevement':
            if datetime.strptime(res.date,'%Y-%m-%d') > datetime.strptime(rec.dateDernierDonHPA,'%Y-%m-%d'):
                rec.dateDernierDonHPA = res.date
                rec.montantDernierDonHPA = res.montantEur
                rec.codemediaDernierDonHPA = res.codeMedia
                rec.cumulDonHPA = rec.cumulDonHPA + res.montantEur
                rec.nombreDonsHPA = rec.nombreDonsHPA +1
                rec.don_moyHPA = rec.cumulDonHPA/rec.nombreDonsHPA
                rec.iddernierdonsHPA = res.id
            if datetime.strptime(res.date,'%Y-%m-%d') < datetime.strptime(rec.datePremierDonHPA,'%Y-%m-%d'):
                rec.datePremierDonHPA= res.date
                rec.montantPremierDonHPA=res.montantEur
                rec.codemediaPremierDonHPA=res.codeMedia
                rec.cumulDonHPA=rec.cumulDonHPA + res.montantEur
                rec.nombreDonsHPA = rec.nombreDonsHPA +1
                rec.don_moyHPA=rec.cumulDonHPA/rec.nombreDonsHPA
                rec.idpremierdonHPA = res.id
        if rec.nombreDons ==0:
                rec.freq_communication='Prospect'
        elif rec.nombreDons ==1:
                rec.freq_communication='Nouveau'
        if rec.nombreDons > 1:
                rec.freq_communication='Consolide'
        if rec.cumulDonTotal < 1000:
            rec.montant='Donor'
        elif rec.cumulDonTotal >= 1000 and rec.cumulDonTotal <= 5000:
            rec.montant='Middle donor'
        elif rec.cumulDonTotal > 5000 and rec.cumulDonTotal <= 50000:
            rec.montant='Global Leader'
        elif rec.cumulDonTotal > 50000:
            rec.montant='Investisseur Fondateur'
        return res

    @api.multi
    def unlink(self):
        my_array = array('i', [])
        for dons in self:
            test = bool()
            for idd in my_array:
                if idd == dons.donateur.id:
                    test = bool(1)
            if not test:
              my_array.append(dons.donateur.id)
        rep = super(Don, self).unlink()
        for iddonateur in my_array:
            rec = self.env['crm.alima.donateur'].search([('id', '=', iddonateur)])
            rec.datePremierDon=""
            rec.montantPremierDon=0
            rec.codemediaPremierDon=""
            rec.dateDernierDon=""
            rec.montantDernierDon=0
            rec.codemediaDernierDon=""
            rec.cumulDonTotal=0
            rec.nombreDons=0
            rec.don_moy=0
            rec.idpremierdon=0
            rec.iddernierdon=0
            rec.datePremierDonHPA=""
            rec.montantPremierDonHPA=0
            rec.codemediaPremierDonHPA=""
            rec.dateDernierDonHPA=""
            rec.montantDernierDonHPA=0
            rec.codemediaDernierDonHPA=0
            rec.cumulDonHPA=0
            rec.nombreDonsHPA=0
            rec.don_moyHPA=0
            rec.idpremierdonHPA=0
            rec.iddernierdonsHPA=0
            for res in rec.dons:
                rec = res.donateur
                if not rec.datePremierDon:
                    rec.datePremierDon =  res.date
                    rec.montantPremierDon=res.montantEur
                    rec.codemediaPremierDon=res.codeMedia
                    rec.dateDernierDon= res.date
                    rec.montantDernierDon= res.montantEur
                    rec.codemediaDernierDon= res.codeMedia
                    rec.cumulDonTotal=res.montantEur
                    rec.nombreDons=1
                    rec.don_moy=rec.cumulDonTotal
                    rec.idpremierdon=res.id
                    rec.iddernierdon=res.id
                else:
                    rec.dateDernierDon= res.date
                    rec.montantDernierDon=res.montantEur
                    rec.codemediaDernierDon=res.codeMedia
                    rec.cumulDonTotal=rec.cumulDonTotal + res.montantEur
                    rec.nombreDons=rec.nombreDons + 1
                    rec.don_moy=rec.cumulDonTotal/rec.nombreDons
                    rec.iddernierdon=res.id
                if not rec.datePremierDonHPA and res.mode_versement !='avec prelevement':
                    rec.datePremierDonHPA= res.date
                    rec.montantPremierDonHPA=res.montantEur
                    rec.codemediaPremierDonHPA=res.codeMedia
                    rec.dateDernierDonHPA= res.date
                    rec.montantDernierDonHPA= res.montantEur
                    rec.codemediaDernierDonHPA= res.codeMedia
                    rec.cumulDonHPA=res.montantEur
                    rec.nombreDonsHPA=1
                    rec.don_moyHPA=rec.cumulDonHPA
                    rec.idpremierdonHPA=res.id
                    rec.iddernierdonsHPA = res.id
                elif res.mode_versement !='avec prelevement':
                    rec.dateDernierDonHPA= res.date
                    rec.montantDernierDonHPA=res.montantEur
                    rec.codemediaDernierDonHPA=res.codeMedia
                    rec.cumulDonHPA=rec.cumulDonHPA + res.montantEur
                    rec.nombreDonsHPA = rec.nombreDonsHPA +1
                    rec.don_moyHPA=rec.cumulDonHPA/rec.nombreDonsHPA
                    rec.iddernierdonsHPA = res.id
            if rec.nombreDons ==0:
                    rec.freq_communication='Prospect'
            elif rec.nombreDons ==1:
                    rec.freq_communication='Nouveau'
            if rec.nombreDons > 1:
                    rec.freq_communication='Consolide'
            if rec.cumulDonTotal < 1000:
                rec.montant='Donor'
            elif rec.cumulDonTotal >= 1000 and rec.cumulDonTotal <= 5000:
                rec.montant='Middle donor'
            elif rec.cumulDonTotal > 5000 and rec.cumulDonTotal <= 50000:
                rec.montant='Global Leader'
            elif rec.cumulDonTotal > 50000:
                rec.montant='Investisseur Fondateur'
        return rep

    @api.multi
    def write(self, vals):
        montantEurSave = self.montantEur
        rep  =  super(Don, self).write(vals)
        res = self
        rec = res.donateur
        if str(rec.idpremierdon) == str(res.id):
            rec.datePremierDon =  res.date
            rec.montantPremierDon = res.montantEur
            rec.codemediaPremierDon = res.codeMedia

        if str(rec.iddernierdon) == str(res.id):
            rec.dateDernierDon= res.date
            rec.montantDernierDon=res.montantEur
            rec.codemediaDernierDon=res.codeMedia

        if str(rec.idpremierdon) == str(res.id) or str(rec.iddernierdon) == str(res.id):
            rec.cumulDonTotal = rec.cumulDonTotal - montantEurSave + res.montantEur
            rec.don_moy = rec.cumulDonTotal / rec.nombreDons

        if str(rec.idpremierdonHPA) == str(res.id):
            rec.datePremierDonHPA= res.date
            rec.montantPremierDonHPA=res.montantEur
            rec.codemediaPremierDonHPA=res.codeMedia

        if str(rec.iddernierdonsHPA) == str(res.id):
            rec.dateDernierDonHPA= res.date
            rec.montantDernierDonHPA=res.montantEur
            rec.codemediaDernierDonHPA=res.codeMedia

        if str(rec.idpremierdonHPA) == str(res.id) or str(rec.iddernierdonsHPA) == str(res.id):
            rec.cumulDonHPA = rec.cumulDonHPA - montantEurSave + res.montantEur
            rec.don_moyHPA = rec.cumulDonHPA/rec.nombreDonsHPA

        if rec.cumulDonTotal < 1000:
            rec.montant='Donor'
        elif rec.cumulDonTotal >= 1000 and rec.cumulDonTotal <= 5000:
            rec.montant='Middle donor'
        elif rec.cumulDonTotal > 5000 and rec.cumulDonTotal <= 50000:
            rec.montant='Global Leader'
        elif rec.cumulDonTotal > 50000:
            rec.montant='Investisseur Fondateur'

        return rep


    @api.depends('montantEur')
    def convNombre2lettres(self):
        for rec in self:
            nombre = rec.montantEur
            rec.montantLettre= rec.convNombre(int(nombre))

    @api.depends('taux_change', 'montantEur')
    def tauxChange(self):
        for rec in self:
            rec.montant_dans_devise= rec.taux_change * rec.montantEur

    @api.depends('id_intersa')
    def _get_url_intersa(self):
        for rec in self:
            if rec.id_intersa:
                rec.url_intersa = 'https://www.intersa.fr/imagesAlima/INT_' + rec.id_intersa


    def convNombre(self, nombre):
        s=''
        reste=nombre
        i=1000000000
        while i>0:
            y=reste/i
            if y!=0:
                centaine=y/100
                dizaine=(y - centaine*100)/10
                unite=y-centaine*100-dizaine*10
                if centaine==1:
                    s+="CENT "
                elif centaine!=0:
                    s+=schu[centaine]+"CENT "
                    if dizaine==0 and unite==0: s=s[:-1]+"S "
                if dizaine not in [0,1]: s+=schd[dizaine]
                if unite==0:
                    if dizaine in [1,7,9]: s+="DIX "
                    elif dizaine==8: s=s[:-1]+"S "
                elif unite==1:
                    if dizaine in [1,9]: s+="ONZE "
                    elif dizaine==7: s+="ET ONZE "
                    elif dizaine in [2,3,4,5,6]: s+="ET UN "
                    elif dizaine in [0,8]: s+="UN "
                elif unite in [2,3,4,5,6,7,8,9]:
                    if dizaine in [1,7,9]: s+=schud[unite]
                    else: s+=schu[unite]
                if i==1000000000:
                    if y>1: s+="MILLIARDS "
                    else: s+="MILLIARD "
                if i==1000000:
                    if y>1: s+="MILLIONS "
                    else: s+="MILLIONS "
                if i==1000:
                    s+="MILLE "
                if i==1000 and s=='UN MILLE ':
                    s="MILLE "
            #end if y!=0
            reste -= y*i
            dix=False
            i/=1000;
        #end while
        if len(s)==0: s+="ZERO "
        return s

    @api.multi
    def reset_reconsiliation_don(self):
        all_don = self.env['crm.alima.don'].search([])
        for don in all_don:
            don.write({'NumRecuFiscal':False}) 
    
    @api.multi
    def correction_historique_don(self):
        id_donateur_a_traiter = [
            5202,247,8508,3958,1069,
            3632,5559,2155,3736,6975,
            4731,4074,1467,4097,3222,
            2253,1394,4220,6855,3669,
            273,5213,5420,4926,6139,
            413,701,378,2252,4687,
            465,4553,2594,503,3838,
            3969,1336,4085,594,5029,
            5422,
        ]
        donateur_a_traiter = self.env['crm.alima.donateur'].browse(id_donateur_a_traiter)
        for donateur in donateur_a_traiter:
            for don in donateur.dons:
                if datetime.strptime(don.date,'%Y-%m-%d') > datetime.strptime(donateur.dateDernierDon,'%Y-%m-%d'):
                    donateur.dateDernierDon = don.date
                    donateur.montantDernierDon = don.montantEur
                    donateur.codemediaDernierDon = don.codeMedia
                    donateur.iddernierdon = don.id
                if datetime.strptime(don.date,'%Y-%m-%d') < datetime.strptime(donateur.datePremierDon,'%Y-%m-%d'):
                    donateur.datePremierDon = don.date
                    donateur.montantPremierDon = don.montantEur
                    donateur.codemediaPremierDon = don.codeMedia
                    donateur.idpremierdon = don.id
                if don.mode_versement != 'avec prelevement':
                    if datetime.strptime(don.date,'%Y-%m-%d') > datetime.strptime(donateur.dateDernierDonHPA,'%Y-%m-%d'):
                        donateur.dateDernierDonHPA = don.date
                        donateur.montantDernierDonHPA = don.montantEur
                        donateur.codemediaDernierDonHPA = don.codeMedia
                        donateur.iddernierdonsHPA = don.id
                    if datetime.strptime(don.date,'%Y-%m-%d') < datetime.strptime(donateur.datePremierDonHPA,'%Y-%m-%d'):
                        donateur.datePremierDonHPA = don.date
                        donateur.montantPremierDonHPA = don.montantEur
                        donateur.codemediaPremierDonHPA = don.codeMedia
                        donateur.idpremierdonHPA = don.id

class codeMedia(models.Model):
    _name='crm.alima.code.media'
    _description='Code media'

    #Codes media	Nom campagne	Canal	Sens	Année	programme	Pays
    #MKT4546	Urgence Ebola	Mailing	sortant	2017	Ebola	Nigeria
    name=fields.Char(string="Code media")
    nomcampagne=fields.Char(string="Nom campagne")
    canal=fields.Char(string="Canal")
    sens= fields.Selection(SENS, string="sens")
    annees= fields.Float(digits=(5, 0), string='Annee')
    programme= fields.Char(string="Programme")
    pays = fields.Char(string='Pays')



