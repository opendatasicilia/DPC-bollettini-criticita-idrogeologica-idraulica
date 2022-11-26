# CSV Bollettini Protezione Civile 
## Criticità nazionale, rischio idrogeologico, rischio temporali, rischio idraulico 

A partire dal primo semestre del 2021, i bollettini della protezione civile relativi alle criticità comunicate dai centri funzionali decentrati di tutte le regioni e province autonome sono stati resi disponibili, oltre che sul sito, anche sul [repository github](https://github.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica) ufficiale della Protezione Civile.

Con questo nuovo sistema di pubblicazione, però, non è stato più pubblicato il formato più semplice da usare e più utilizzato, cioè il formato **CSV**. Nonostante le diverse [issues](https://github.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/issues) aperte sul repo ufficiale della Protezione Civile, tale mancanza non è mai stata sanata.


Questo progetto nasce sia per superare questo ostacolo sia per fornire informazioni più dettagliate sulle allerte della protezione civile a livello comunale.


## Struttura dei dati
Di seguito viene descritta la struttura dei file .csv

data_pubblicazione,data_validita_inizio,data_validita_fine,zona_codice,avviso_criticita,avviso_idrogeologico,avviso_temporali,avviso_idraulico


### YYYYMMDD-bollettino-[oggi|domani]-zone.csv

Bollettini `criticità nazionale`, `rischio idrogeologico`, `idraulico` e `temporali` per zona. 

Nome campo | Descrizione | Formato | Esempio |
-- | -- | -- | --
**data_pubblicazione**| Data e ora di pubblicazione del bollettino|Data formato ISO8601|2022-11-26T15:10:59+01:00|
**data_validita_inizio**| Data e ora di inizio validità del bollettino|Data formato ISO8601|2022-11-26T15:10:59+01:00
**data_validita_fine**| Data e ora di fine validità del bollettino|Data formato|2022-11-26T23:59:59+01:00
**zona_codice**|Codice della zona|codice|Testo|Abru-A
**avviso_criticita**|Avviso rischio criticità|Testo|Ordinaria per rischio temporali / ALLERTA GIALLA
**avviso_idrogeologico**|Avviso rischio idrogeologico|Testo|Ordinaria / ALLERTA GIALLA
**avviso_temporali**|Avviso rischio temporali|Testo|Ordinaria / ALLERTA GIALLA
**avviso_idraulico**|Avviso rischio idraulico|Testo|Assenza di fenomeni significativi prevedibili / NESSUNA ALLERTA

### bollettino-[oggi|domani]-zone-latest.csv

Questo file rappresenta il `permalink` del bollettino `zone` più recente e ha la stessa struttura di` YYYYMMDD-bollettino-[oggi|domani]-zone.csv`


### YYYYMMDD-bollettino-[oggi|domani]-comuni.csv
Bollettini `criticità nazionale`, `rischio idrogeologico`, `idraulico` e `temporali` per **comune**. 

Nome campo | Descrizione | Formato | Esempio |
-- | -- | -- | --
**data_pubblicazione**| Data e ora di pubblicazione del bollettino|Data formato ISO8601|2022-11-26T15:10:59+01:00|
**data_validita_inizio**| Data e ora di inizio validità del bollettino|Data formato ISO8601|2022-11-26T15:10:59+01:00
**data_validita_fine**| Data e ora di fine validità del bollettino|Data formato|2022-11-26T23:59:59+01:00
**pro_com_t**|Codice ISTAT del comune|Testo|001001	
**comune_nome**|Nome del comune|Testo|Agliè
**provincia_nome**|Provincia|Testo|Torino
**regione_nome**|Regione|Testo|Piemonte
**zona_codice**|Codice della zona|codice|Testo|Piem-L
**avviso_criticita**|Avviso rischio criticità|Testo|Ordinaria per rischio temporali / ALLERTA GIALLA
**avviso_idrogeologico**|Avviso rischio idrogeologico|Testo|Ordinaria / ALLERTA GIALLA
**avviso_temporali**|Avviso rischio temporali|Testo|Ordinaria / ALLERTA GIALLA
**avviso_idraulico**|Avviso rischio idraulico|Testo|Assenza di fenomeni significativi prevedibili / NESSUNA ALLERTA

### bollettino-[oggi|domani]-comuni-latest.csv

Questo file rappresenta il `permalink` del bollettino per `comune` più recente e ha la stessa struttura di` YYYYMMDD-bollettino-[oggi|domani]-comuni.csv`


### zone.csv

Elenco delle zone monitorate dalla Protezione Civile

Nome campo | Descrizione | Formato | Esempio |
-- | -- | -- | --
**zona_codice**| Codice zona  | Testo   |         Abru-A          
**zona_nome**  | Nome della zona| Testo   | Bacini Tordino Vomano  

### zone_comuni.csv
Elenco comuni italiani con indicazione della zona 

Nome campo | Descrizione | Formato | Esempio |
-- | -- | -- | --
**pro_com_t** | Codice ISTAT del comune |Testo |001001
**comune_nome** | Nome del comune | Testo |Agliè
**provincia_nome** | Provincia |Testo |Torino
**provincia_sigla** | Sigla provincia |Testo |TO
**regione_nome** | Nome regione |Testo  |Piemonte
**zona_codice** | Codice zona |Testo|Piem-L
**zona_nome** | Nome zona |Testo|Pianura Torinese e Colline

## Fonte Dati
- [Bollettini allerta criticità nazionale, rischio idrogeologico, idraulico, temporali - Dipartimento Protezione Civile](https://github.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica)
- [Comuni Italiani - progetto Open Data Sicilia](https://github.com/opendatasicilia/comuni-italiani)

## Licenza
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.it) - [Visualizza licenza](https://github.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/blob/main/LICENSE)

## Note
Il Dipartimento della Protezione Civile (DPC) rilascia il bollettino delle allerte di criticità nazionale, rischio idrogeologico, idraulico, temporali **una volta al giorno** poco prima delle ore **16.00**. Nel caso di variazioni e/o aggiornamenti il DPC può pubblicare ulteriori bollettini; per questo motivo questo progetto verificherà ogni `4 ore` gli eventuali bollettini di aggiornamento.

