from sqlalchemy import create_engine
import hashlib

engine = create_engine('postgresql://cmpe321:1234@localhost:5432/cmpe321-hw3')


def db_init():

    engine.execute(
        'CREATE TABLE IF NOT EXISTS Database_Managers (id serial, username text, password text, PRIMARY KEY(username), CONSTRAINT "cannot have more than 5 database managers, update one instead" CHECK(id <= 5 ));')

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Drugs (drugbank_id varchar(7), name text, description text, smiles text, PRIMARY KEY(drugbank_id));")

    engine.execute("CREATE TABLE IF NOT EXISTS Articles (doi text, authors text[], institution text, PRIMARY KEY(doi));")

    engine.execute("CREATE TABLE IF NOT EXISTS Side_Effects (umls_cui varchar(8), name text, PRIMARY KEY(umls_cui));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Proteins (uniprot_id varchar(6), sequence text, name text, PRIMARY KEY(uniprot_id));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Institutions (name text, members text[], points integer, PRIMARY KEY(name));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Users (name text, username text, institution text, password text, points integer, PRIMARY KEY(username, institution));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Causes (drugbank_id varchar(7) NOT NULL, umls_cui varchar(8), PRIMARY KEY(drugbank_id, umls_cui));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Interacts (drugbank_id_1 varchar(7), drugbank_id_2 varchar(7), PRIMARY KEY(drugbank_id_1, drugbank_id_2));")

    engine.execute(
        "CREATE TABLE IF NOT EXISTS Binds (drugbank_id varchar(7) NOT NULL, uniprot_id varchar(6), reaction_id integer, doi text NOT NULL, affinity_nM real, measure text, PRIMARY KEY(reaction_id));")

    engine.execute(
         "INSERT INTO Database_Managers (username, password) SELECT 'selen.parlar', \'%s\' WHERE NOT EXISTS (SELECT 1 FROM database_managers WHERE username = 'selen.parlar');" % hashlib.sha256('selen.parlar'.encode('utf-8')).hexdigest())

    engine.execute(
         "INSERT INTO Database_Managers (username, password) SELECT 'riza.ozcelik', \'%s\' WHERE NOT EXISTS (SELECT 1 FROM database_managers WHERE username = 'riza.ozcelik');" % hashlib.sha256('riza.ozcelik0'.encode('utf-8')).hexdigest())

    engine.execute(
         "INSERT INTO Database_Managers (username, password) SELECT 'arzucan_ozgur', \'%s\' WHERE NOT EXISTS (SELECT 1 FROM database_managers WHERE username = 'arzucan_ozgur');" % hashlib.sha256('arzucan_135'.encode('utf-8')).hexdigest())

    engine.execute(
        "create or replace function filterbyaff (minaff real, maxaff real, measurement text) returns table(drugbank_id varchar(7), drug_name text, description text, smiles text, drugbank_id2 varchar(7), uniprot_id varchar(6), reaction_id int, doi text, affinity_nm real, measure text, uniprot_id2 varchar(6), sequence text, prot_name text) language plpgsql as $$ begin return query select * from drugs inner join binds on drugs.drugbank_id = binds.drugbank_id inner join proteins on binds.uniprot_id = proteins.uniprot_id where binds.affinity_nm < maxaff and binds.affinity_nm > minaff and binds.measure = measurement; end;$$"
    )

    engine.execute(
        "create or replace function drug_deletion() returns trigger language plpgsql as $$ begin delete from binds where binds.drugbank_id = OLD.drugbank_id; delete from causes where causes.drugbank_id = OLD.drugbank_id; delete from interacts where interacts.drugbank_id_1 = OLD.drugbank_id or interacts.drugbank_id_2 = OLD.drugbank_id; return null; end; $$"
    )

    engine.execute(
        "create trigger drug_deletion after delete on drugs for each row execute procedure drug_deletion();"
    )

    engine.execute(
        "create or replace function prot_deletion() returns trigger language plpgsql as $$ begin delete from binds where binds.uniprot_id= OLD.uniprot_id; return null; end; $$"
    )

    engine.execute(
        "create trigger prot_deletion after delete on proteins for each row execute procedure prot_deletion();"
    )

    engine.execute(
        "create or replace function article_add() returns trigger language plpgsql as $$ begin update institutions set points = points+5+2*array_length(new.authors, 1) where institutions.name = new.institution; update users set points = points+2 where users.username = any(new.authors) and users.institution = new.institution; return null; end; $$"
    )

    engine.execute(
        "create trigger article_add after insert on articles for each row execute procedure article_add();"
    )


def insert_data():

    engine.execute(
        "INSERT INTO Institutions VALUES ('Amgen Inc',ARRAY['morgan', 'vanstaden', 'chen', 'kalyanaraman'], 0);"
    )

    engine.execute(
        "INSERT INTO Institutions VALUES ('Human BioMolecular Research Institute',ARRAY['ghirmai', 'azar', 'cashman'], 0);"
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Morgan, RE','morgan','Amgen Inc', \'%s\', 0);" % hashlib.sha256('morgan00'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('van Staden, CJ','vanstaden','Amgen Inc', \'%s\', 0);" % hashlib.sha256('vanstaden01'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Chen, Y','chen','Amgen Inc', \'%s\', 0);" % hashlib.sha256('chen02'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Kalyanaraman','kalyanaraman','Amgen Inc', \'%s\',0 );" % hashlib.sha256('kalyanaraman03'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Ghirmai, S','ghirmai','Human BioMolecular Research Institute', \'%s\', 0);" % hashlib.sha256('ghirmai100'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Azar, MR','azar','Human BioMolecular Research Institute', \'%s\', 0);" % hashlib.sha256('azar101'.encode('utf-8')).hexdigest()
    )

    engine.execute(
        "INSERT INTO Users VALUES ('Cashman, JR','cashman','Human BioMolecular Research Institute', \'%s\', 0);" % hashlib.sha256('cashman102'.encode('utf-8')).hexdigest()
    )
    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00136','Calcitriol','\"Calcitriol is an active metabolite of vitamin D with 3 hydroxyl (OH) groups and is commonly referred to as 1,25-dihydroxycholecalciferol, or 1alpha,25-dihydroxyvitamin D<sub>3</sub>, 1,25-dihydroxyvitamin D<sub>3</sub>. It is produced in the body after series of conversion steps of 7-dehydrocholesterol from exposure to UV light. 7-dehydrocholesterol is converted to [DB00169] (vitamin D3) in the skin, which is then converted to [DB00146] in the liver and kidneys. [DB00146] undergoes hydroxylation to form calcitriol via 1α-hydroxylase (CYP27B1) activity [A26353]. Calcitriol is considered to be the most potent metabolite of vitamin D in humans [A3366]. Renal production of calcitriol is stimulated in response to PTH, low calcium and low phosphate [A26353]. Calcitriol plays a role in plasma calcium regulation in concert with parathyroid hormone (PTH) by enhancing absorption of dietary calcium and phosphate from the gastrointestinal tract, promoting renal tubular reabsorption of calcium in the kidneys, and stimulating the release of calcium stores from the skeletal system. In addition to promoting fatty acid synthesis and inhibiting lipolysis, calcitriol has been demonstrated to increase energy efficiency by suppressing UCP2 expression, which is modulated by signaling pathways of classical nuclear receptors (nVDR), where calcitriol acts as a natural ligand [A175615]. There is also evidence that calcitriol modulates the action of cytokines and may regulate immune and inflammatory response, cell turnover, cell differentiation [A26353]. Administered orally and intravenously, calcitriol is commonly used as a medication in the treatment of secondary hyperparathyroidism and resultant metabolic bone disease, hypocalcemia in patients undergoing chronic renal dialysis, and osteoporosis. It is also available in topical form for the treatment of mild to moderate plaque psoriasis in adults. Calcitriol is marketed under various trade names including Rocaltrol (Roche), Calcijex (Abbott) and Decostriol (Mibe, Jesalis).\"', 'C[C@H](CCCC(C)(C)O)[C@H]1CC[C@H]2\C(CCC[C@]12C)=C\C=C1\C[C@@H](O)C[C@H](O)C1=C');"
    )

    engine.execute(
        "INSERT INTO Drugs (drugbank_id, name, description) VALUES ('DB00152','Thiamine','\"Thiamine or thiamin, also known as vitamin B1, is a colorless compound with the chemical formula C12H17N4OS. It is soluble in water and insoluble in alcohol. Thiamine decomposes if heated. Thiamine was first discovered by Umetaro Suzuki in Japan when researching how rice bran cured patients of Beriberi. Thiamine plays a key role in intracellular glucose metabolism and it is thought that thiamine inhibits the effect of glucose and insulin on arterial smooth muscle cell proliferation. Thiamine plays an important role in helping the body convert carbohydrates and fat into energy. It is essential for normal growth and development and helps to maintain proper functioning of the heart and the nervous and digestive systems. Thiamine cannot be stored in the body, however, once absorbed, the vitamin is concentrated in muscle tissue.\"');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00271','Diatrizoate','A commonly used x-ray contrast medium. As diatrizoate meglumine and as Diatrizoate sodium, it is used for gastrointestinal studies, angiography, and urography.','CC(=O)Nc1c(I)c(NC(C)=O)c(I)c(C(O)=O)c1I');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00485','Dicloxacillin','One of the penicillins which is resistant to penicillinase.','Cc1onc(c1C(=O)N[C@H]1[C@H]2SC(C)(C)[C@@H](N2C1=O)C(O)=O)-c1c(Cl)cccc1Cl');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00649','Stavudine','A dideoxynucleoside analog that inhibits reverse transcriptase and has in vitro activity against HIV.','Cc1cn([C@@H]2O[C@H](CO)C=C2)c(=O)[nH]c1=O');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00704','Naltrexone','Derivative of noroxymorphone that is the N-cyclopropylmethyl congener of naloxone. It is a narcotic antagonist that is effective orally, longer lasting and more potent than naloxone, and has been proposed for the treatment of heroin addiction. The FDA has approved naltrexone for the treatment of alcohol dependence.','Oc1ccc2C[C@H]3N(CC4CC4)CC[C@@]45[C@@H](Oc1c24)C(=O)CC[C@@]35O');"
    )

    engine.execute(
        "INSERT INTO Drugs (drugbank_id, name, description) VALUES ('DB00842','Oxazepam','Oxazepam is an intermediate-acting, 3-hydroxybenzodiazepine used in the treatment of alcohol withdrawal and anxiety disorders. Oxazepam, like related 3-hydroxybenzodiazepine [lorazepam], is considered less susceptible to pharmacokinetic variability based on patient-specific factors (e.g. age, liver disease) - this feature is advantageous as compared to other benzodiazepines, and is likely owing in part to oxazepams relatively simple metabolism.[A203516] It is an active metabolite of both [diazepam] and [temazepam][A39486] and undergoes very little biotransformation following absorption, making it unlikely to participate in pharmacokinetic interactions.[L13895]');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00879','Emtricitabine','\"Emtricitabine is a nucleoside reverse transcriptase inhibitor (NRTI) indicated for the treatment of HIV infection in adults[L9019] or combined with [tenofovir alafenamide] for the prevention of HIV-1 infection in high risk adolescents and adults.[L9010] Emtricitabine is a cytidine analogue.[L9019] The drug works by inhibiting HIV reverse transcriptase, preventing transcription of HIV RNA to DNA.[L9019] Emtricitabine was granted FDA approval on 2 July 2003.[L9019]\"','Nc1nc(=O)n(cc1F)[C@@H]1CS[C@H](CO)O1');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB00990','Exemestane','Exemestane is an oral steroidal aromatase inhibitor used in the adjuvant treatment of hormonally-responsive (also called hormone-receptor-positive, estrogen-responsive) breast cancer in postmenopausal women. It irreversibly binds to the active site of the enzyme resulting in permanent inhibition.','C[C@]12CC[C@H]3[C@@H](CC(=C)C4=CC(=O)C=C[C@]34C)[C@@H]1CCC2=O');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB01132','Pioglitazone','\"Pioglitazone is an antihyperglycemic used as an adjunct to diet, exercise, and other antidiabetic medications to manage type 2 diabetes mellitus.[L11416,L11419,L11422,L11425] It is administered as a racemic mixture, though there is no pharmacologic difference between the enantiomers and they appear to interconvert _in vivo_ with little consequence.[L11416] The thiazolidinedione class of medications, which also includes [rosiglitazone] and [troglitazone], exerts its pharmacological effect primarily by promoting insulin sensitivity and the improved uptake of blood glucose[L11416] via agonism at the peroxisome proliferator-activated receptor-gamma (PPARγ).[A19757] PPARs are ligand-activated transcription factors that are involved in the expression of more than 100 genes and affect numerous metabolic processes, most notably lipid and glucose homeostasis.[A19759] Thiazolidinediones, including pioglitazone, have fallen out of favor in recent years due to the presence of multiple adverse effects and warnings regarding their use (e.g. congestive heart failure, bladder cancer) and the availability of safer and more effective alternatives for patients with type 2 diabetes mellitus.[L11461]\"','CCc1ccc(CCOc2ccc(CC3SC(=O)NC3=O)cc2)nc1');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB01220','Rifaximin','\"Rifaximin is a semisynthetic, rifamycin-based non-systemic antibiotic, meaning that the drug will not pass the gastrointestinal wall into the circulation as is common for other types of orally administered antibiotics. It has multiple indications and is used in treatment of travellers diarrhea caused by E. coli, reduction in risk of overt hepatic encephalopathy recurrence, as well as diarrhea-predominant irritable bowel syndrome (IBS-D) in adult women and men. It is marketed under the brand name Xifaxan by Salix Pharmaceuticals.\"','CO[C@H]1\C=C\O[C@@]2(C)Oc3c(C2=O)c2c4nc5cc(C)ccn5c4c(NC(=O)\C(C)=C/C=C/[C@H](C)[C@H](O)[C@@H](C)[C@@H](O)[C@@H](C)[C@H](OC(C)=O)[C@@H]1C)c(O)c2c(O)c3C');"
    )

    engine.execute(
        "INSERT INTO Drugs VALUES ('DB06335','Saxagliptin','Saxagliptin (rINN) is an orally active hypoglycemic (anti-diabetic drug) of the new dipeptidyl peptidase-4 (DPP-4) inhibitor class of drugs. FDA approved on July 31, 2009.','N[C@H](C(=O)N1[C@H]2C[C@H]2C[C@H]1C#N)C12CC3CC(CC(O)(C3)C1)C2');"
    )

    engine.execute(
        "INSERT INTO Proteins (uniprot_id, sequence) VALUES ('O15244','MPTTVDDVLEHGGEFHFFQKQMFFLLALLSATFAPIYVGIVFLGFTPDHRCRSPGVAELSLRCGWSPAEELNYTVPGPGPAGEASPRQCRRYEVDWNQSTFDCVDPLASLDTNRSRLPLGPCRDGWVYETPGSSIVTEFNLVCANSWMLDLFQSSVNVGFFIGSMSIGYIADRFGRKLCLLTTVLINAAAGVLMAISPTYTWMLIFRLIQGLVSKAGWLIGYILITEFVGRRYRRTVGIFYQVAYTVGLLVLAGVAYALPHWRWLQFTVSLPNFFFLLYYWCIPESPRWLISQNKNAEAMRIIKHIAKKNGKSLPASLQRLRLEEETGKKLNPSFLDLVRTPQIRKHTMILMYNWFTSSVLYQGLIMHMGLAGDNIYLDFFYSALVEFPAAFMIILTIDRIGRRYPWAASNMVAGAACLASVFIPGDLQWLKIIISCLGRMGITMAYEIVCLVNAELYPTFIRNLGVHICSSMCDIGGIITPFLVYRLTNIWLELPLMVFGVLGLVAGGLVLLLPETKGKALPETIEEAENMQRPRKNKEKMIYLQVQKLDIPLN');"
    )

    engine.execute(
        "INSERT INTO Proteins (uniprot_id, sequence) VALUES ('O15245','MPTVDDILEQVGESGWFQKQAFLILCLLSAAFAPICVGIVFLGFTPDHHCQSPGVAELSQRCGWSPAEELNYTVPGLGPAGEAFLGQCRRYEVDWNQSALSCVDPLASLATNRSHLPLGPCQDGWVYDTPGSSIVTEFNLVCADSWKLDLFQSCLNAGFLFGSLGVGYFADRFGRKLCLLGTVLVNAVSGVLMAFSPNYMSMLLFRLLQGLVSKGNWMAGYTLITEFVGSGSRRTVAIMYQMAFTVGLVALTGLAYALPHWRWLQLAVSLPTFLFLLYYWCVPESPRWLLSQKRNTEAIKIMDHIAQKNGKLPPADLKMLSLEEDVTEKLSPSFADLFRTPRLRKRTFILMYLWFTDSVLYQGLILHMGATSGNLYLDFLYSALVEIPGAFIALITIDRVGRIYPMAMSNLLAGAACLVMIFISPDLHWLNIIIMCVGRMGITIAIQMICLVNAELYPTFVRNLGVMVCSSLCDIGGIITPFIVFRLREVWQALPLILFAVLGLLAAGVTLLLPETKGVALPETMKDAENLGRKAKPKENTIYLKVQTSEPSGT');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('O15438','MDALCGSGELGSKFWDSNLSVHTENPDLTPCFQNSLLAWVPCIYLWVALPCYLLYLRHHCRGYIILSHLSKLKMVLGVLLWCVSWADLFYSFHGLVHGRAPAPVFFVTPLVVGVTMLLATLLIQYERLQGVQSSGVLIIFWFLCVVCAIVPFRSKILLAKAEGEISDPFRFTTFYIHFALVLSALILACFREKPPFFSAKNVDPNPYPETSAGFLSRLFFWWFTKMAIYGYRHPLEEKDLWSLKEEDRSQMVVQQLLEAWRKQEKQTARHKASAAPGKNASGEDEVLLGARPRPRKPSFLKALLATFGSSFLISACFKLIQDLLSFINPQLLSILIRFISNPMAPSWWGFLVAGLMFLCSMMQSLILQHYYHYIFVTGVKFRTGIMGVIYRKALVITNSVKRASTVGEIVNLMSVDAQRFMDLAPFLNLLWSAPLQIILAIYFLWQNLGPSVLAGVAFMVLLIPLNGAVAVKMRAFQVKQMKLKDSRIKLMSEILNGIKVLKLYAWEPSFLKQVEGIRQGELQLLRTAAYLHTTTTFTWMCSPFLVTLITLWVYVYVDPNNVLDAEKAFVSVSLFNILRLPLNMLPQLISNLTQASVSLKRIQQFLSQEELDPQSVERKTISPGYAITIHSGTFTWAQDLPPTLHSLDIQVPKGALVAVVGPVGCGKSSLVSALLGEMEKLEGKVHMKGSVAYVPQQAWIQNCTLQENVLFGKALNPKRYQQTLEACALLADLEMLPGGDQTEIGEKGINLSGGQRQRVSLARAVYSDADIFLLDDPLSAVDSHVAKHIFDHVIGPEGVLAGKTRVLVTHGISFLPQTDFIIVLADGQVSEMGPYPALLQRNGSFANFLCNYAPDEDQGHLEDSWTALEGAEDKEALLIEDTLSNHTDLTDNDPVTYVVQKQFMRQLSALSSDGEGQGRPVPRRHLGPSEKVQVTEAKADGALTQEEKAAIGTVELSVFWDYAKAVGLCTTLAICLLYVGQSAAAIGANVWLSAWTNDAMADSRQNNTSLRLGVYAALGILQGFLVMLAAMAMAAGGIQAARVLHQALLHNKIRSPQSFFDTTPSGRILNCFSKDIYVVDEVLAPVILMLLNSFFNAISTLVVIMASTPLFTVVILPLAVLYTLVQRFYAATSRQLKRLESVSRSPIYSHFSETVTGASVIRAYNRSRDFEIISDTKVDANQRSCYPYIISNRWLSIGVEFVGNCVVLFAALFAVIGRSSLNPGLVGLSVSYSLQVTFALNWMIRMMSDLESNIVAVERVKEYSKTETEAPWVVEGSRPPEGWPPRGEVEFRNYSVRYRPGLDLVLRDLSLHVHGGEKVGIVGRTGAGKSSMTLCLFRILEAAKGEIRIDGLNVADIGLHDLRSQLTIIPQDPILFSGTLRMNLDPFGSYSEEDIWWALELSHLHTFVSSQPAGLDFQCSEGGENLSVGQRQLVCLARALLRKSRILVLDEATAAIDLETDNLIQATIRTQFDTCTVLTIAHRLNTIMDYTRVLVLDKGVVAEFDSPANLIAARGIFYGMARDAGLA','Canalicular multispecific organic anion transporter 2');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('O15439','MLPVYQEVKPNPLQDANLCSRVFFWWLNPLFKIGHKRRLEEDDMYSVLPEDRSQHLGEELQGFWDKEVLRAENDAQKPSLTRAIIKCYWKSYLVLGIFTLIEESAKVIQPIFLGKIINYFENYDPMDSVALNTAYAYATVLTFCTLILAILHHLYFYHVQCAGMRLRVAMCHMIYRKALRLSNMAMGKTTTGQIVNLLSNDVNKFDQVTVFLHFLWAGPLQAIAVTALLWMEIGISCLAGMAVLIILLPLQSCFGKLFSSLRSKTATFTDARIRTMNEVITGIRIIKMYAWEKSFSNLITNLRKKEISKILRSSCLRGMNLASFFSASKIIVFVTFTTYVLLGSVITASRVFVAVTLYGAVRLTVTLFFPSAIERVSEAIVSIRRIQTFLLLDEISQRNRQLPSDGKKMVHVQDFTAFWDKASETPTLQGLSFTVRPGELLAVVGPVGAGKSSLLSAVLGELAPSHGLVSVHGRIAYVSQQPWVFSGTLRSNILFGKKYEKERYEKVIKACALKKDLQLLEDGDLTVIGDRGTTLSGGQKARVNLARAVYQDADIYLLDDPLSAVDAEVSRHLFELCICQILHEKITILVTHQLQYLKAASQILILKDGKMVQKGTYTEFLKSGIDFGSLLKKDNEESEQPPVPGTPTLRNRTFSESSVWSQQSSRPSLKDGALESQDTENVPVTLSEENRSEGKVGFQAYKNYFRAGAHWIVFIFLILLNTAAQVAYVLQDWWLSYWANKQSMLNVTVNGGGNVTEKLDLNWYLGIYSGLTVATVLFGIARSLLVFYVLVNSSQTLHNKMFESILKAPVLFFDRNPIGRILNRFSKDIGHLDDLLPLTFLDFIQTLLQVVGVVSVAVAVIPWIAIPLVPLGIIFIFLRRYFLETSRDVKRLESTTRSPVFSHLSSSLQGLWTIRAYKAEERCQELFDAHQDLHSEAWFLFLTTSRWFAVRLDAICAMFVIIVAFGSLILAKTLDAGQVGLALSYALTLMGMFQWCVRQSAEVENMMISVERVIEYTDLEKEAPWEYQKRPPPAWPHEGVIIFDNVNFMYSPGGPLVLKHLTALIKSQEKVGIVGRTGAGKSSLISALFRLSEPEGKIWIDKILTTEIGLHDLRKKMSIIPQEPVLFTGTMRKNLDPFNEHTDEELWNALQEVQLKETIEDLPGKMDTELAESGSNFSVGQRQLVCLARAILRKNQILIIDEATANVDPRTDELIQKKIREKFAHCTVLTIAHRLNTIIDSDKIMVLDSGRLKEYDEPYVLLQNKESLFYKMVQQLGKAEAAALTETAKQVYFKRNYPHIGHTDHMVTNTSNGQPSTLTIFETAL','Multidrug resistance-associated protein 4');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('O95342','MSDSVILRSIKKFGEENDGFESDKSYNNDKKSRLQDEKKGDGVRVGFFQLFRFSSSTDIWLMFVGSLCAFLHGIAQPGVLLIFGTMTDVFIDYDVELQELQIPGKACVNNTIVWTNSSLNQNMTNGTRCGLLNIESEMIKFASYYAGIAVAVLITGYIQICFWVIAAARQIQKMRKFYFRRIMRMEIGWFDCNSVGELNTRFSDDINKINDAIADQMALFIQRMTSTICGFLLGFFRGWKLTLVIISVSPLIGIGAATIGLSVSKFTDYELKAYAKAGVVADEVISSMRTVAAFGGEKREVERYEKNLVFAQRWGIRKGIVMGFFTGFVWCLIFLCYALAFWYGSTLVLDEGEYTPGTLVQIFLSVIVGALNLGNASPCLEAFATGRAAATSIFETIDRKPIIDCMSEDGYKLDRIKGEIEFHNVTFHYPSRPEVKILNDLNMVIKPGEMTALVGPSGAGKSTALQLIQRFYDPCEGMVTVDGHDIRSLNIQWLRDQIGIVEQEPVLFSTTIAENIRYGREDATMEDIVQAAKEANAYNFIMDLPQQFDTLVGEGGGQMSGGQKQRVAIARALIRNPKILLLDMATSALDNESEAMVQEVLSKIQHGHTIISVAHRLSTVRAADTIIGFEHGTAVERGTHEELLERKGVYFTLVTLQSQGNQALNEEDIKDATEDDMLARTFSRGSYQDSLRASIRQRSKSQLSYLVHEPPLAVVDHKSTYEEDRKDKDIPVQEEVEPAPVRRILKFSAPEWPYMLVGSVGAAVNGTVTPLYAFLFSQILGTFSIPDKEEQRSQINGVCLLFVAMGCVSLFTQFLQGYAFAKSGELLTKRLRKFGFRAMLGQDIAWFDDLRNSPGALTTRLATDASQVQGAAGSQIGMIVNSFTNVTVAMIIAFSFSWKLSLVILCFFPFLALSGATQTRMLTGFASRDKQALEMVGQITNEALSNIRTVAGIGKERRFIEALETELEKPFKTAIQKANIYGFCFAFAQCIMFIANSASYRYGGYLISNEGLHFSYVFRVISAVVLSATALGRAFSYTPSYAKAKISAARFFQLLDRQPPISVYNTAGEKWDNFQGKIDFVDCKFTYPSRPDSQVLNGLSVSISPGQTLAFVGSSGCGKSTSIQLLERFYDPDQGKVMIDGHDSKKVNVQFLRSNIGIVSQEPVLFACSIMDNIKYGDNTKEIPMERVIAAAKQAQLHDFVMSLPEKYETNVGSQGSQLSRGEKQRIAIARAIVRDPKILLLDEATSALDTESEKTVQVALDKAREGRTCIVIAHRLSTIQNADIIAVMAQGVVIEKGTHEELMAQKGAYYKLVTTGSPIS','Bile salt export pump');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('P35372','MDSSAAPTNASNCTDALAYSSCSPAPSPGSWVNLSHLDGNLSDPCGPNRTDLGGRDSLCPPTGSPSMITAITIMALYSIVCVVGLFGNFLVMYVIVRYTKMKTATNIYIFNLALADALATSTLPFQSVNYLMGTWPFGTILCKIVISIDYYNMFTSIFTLCTMSVDRYIAVCHPVKALDFRTPRNAKIINVCNWILSSAIGLPVMFMATTKYRQGSIDCTLTFSHPTWYWENLLKICVFIFAFIMPVLIITVCYGLMILRLKSVRMLSGSKEKDRNLRRITRMVLVVVAVFIVCWTPIHIYVIIKALVTIPETTFQTVSWHFCIALGYTNSCLNPVLYAFLDENFKRCFREFCIPTSSNIEQQNSTRIRQNTRDHPSTANTVDRTNHQLENLEAETAPLP','Cannabinoid receptor 1/Mu-type opioid receptor');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('P41143','MEPAPSAGAELQPPLFANASDAYPSACPSAGANASGPPGARSASSLALAIAITALYSAVCAVGLLGNVLVMFGIVRYTKMKTATNIYIFNLALADALATSTLPFQSAKYLMETWPFGELLCKAVLSIDYYNMFTSIFTLTMMSVDRYIAVCHPVKALDFRTPAKAKLINICIWVLASGVGVPIMVMAVTRPRDGAVVCMLQFPSPSWYWDTVTKICVFLFAFVVPILIITVCYGLMLLRLRSVRLLSGSKEKDRSLRRITRMVLVVVGAFVVCWAPIHIFVIVWTLVDIDRRDPLVVAALHLCIALGYANSSLNPVLYAFLDENFKRCFRQLCRKPCGRPDPSSFSRAREATARERVTACTPSDGPGGGAAA','\"Opioid receptors, mu/kappa/delta\"');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('P41145','MDSPIQIFRGEPGPTCAPSACLPPNSSAWFPGWAEPDSNGSAGSEDAQLEPAHISPAIPVIITAVYSVVFVVGLVGNSLVMFVIIRYTKMKTATNIYIFNLALADALVTTTMPFQSTVYLMNSWPFGDVLCKIVISIDYYNMFTSIFTLTMMSVDRYIAVCHPVKALDFRTPLKAKIINICIWLLSSSVGISAIVLGGTKVREDVDVIECSLQFPDDDYSWWDLFMKICVFIFAFVIPVLIIIVCYTLMILRLKSVRLLSGSREKDRNLRRITRLVLVVVAVFVVCWTPIHIFILVEALGSTSHSTAALSSYYFCIALGYTNSSLNPILYAFLDENFKRCFRDFCFPLKMRMERQSTSRVRNTVQDPAYLRDIDGMNKPV','Kappa-type opioid receptor');"
    )

    engine.execute(
        "INSERT INTO Proteins VALUES ('P41146','MEPLFPAPFWEVIYGSHLQGNLSLLSPNHSLLPPHLLLNASHGAFLPLGLKVTIVGLYLAVCVGGLLGNCLVMYVILRHTKMKTATNIYIFNLALADTLVLLTLPFQGTDILLGFWPFGNALCKTVIAIDYYNMFTSTFTLTAMSVDRYVAICHPIRALDVRTSSKAQAVNVAIWALASVVGVPVAIMGSAQVEDEEIECLVEIPTPQDYWGPVFAICIFLFSFIVPVLVISVCYSLMIRRLRGVRLLSGSREKDRNLRRITRLVLVVVAVFVGCWTPVQVFVLAQGLGVQPSSETAVAILRFCTALGYVNSCLNPILYAFLDENFKACFRKFCCASALRRDVQVSDRVRSIAKDVALACKTSETVPRPA','Nociceptin receptor');"
    )
    engine.execute(
        "INSERT INTO Articles VALUES ('10.1093/toxsci/kft176', ARRAY['morgan', 'vanstaden', 'chen', 'kalyanaraman'], 'Amgen Inc');"
    )

    engine.execute(
        "INSERT INTO Articles VALUES ('10.1016/j.bmc.2009.07.069', ARRAY['ghirmai', 'azar', 'cashman'], 'Human BioMolecular Research Institute');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704',	'P41146',	51013875,	'10.1016/j.bmc.2009.07.069',	10001, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P41145',50213047,'10.1016/j.bmc.2009.07.069', 0.81, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P41145',50213049,'10.1016/j.bmc.2009.07.069',42, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P41143',50213055,'10.1016/j.bmc.2009.07.069',16, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P41143',50213005,'10.1016/j.bmc.2009.07.069',67, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P35372',50213007,'10.1016/j.bmc.2009.07.069',0.3, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00704','P35372',50213052,'10.1016/j.bmc.2009.07.069', 3.6, 'Ki');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB06335','O95342',50773845,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00136','O15439',50772235,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00485','O15439',50775426,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00649','O15439',50775755,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00990','O15439',50775303,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00271','O15438',50772745,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00879','O15438',50776877,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB00990','O15438',50775691,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB01132','O15438',50774584,'10.1093/toxsci/kft176',133000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Binds VALUES ('DB01220','O15438',50775188,'10.1093/toxsci/kft176',65000, 'IC50');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0000729','Abdominal cramps');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0000737','Abdominal pain');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0001925','Albuminuria');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0002792','Anaphylactic shock');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0003123','Anorexia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0002994','Angioedema');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0004093','Asthenia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0010520','Cyanosis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0019080','Haemorrhage');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0020458','Hyperhidrosis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0020517','Hypersensitivity');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0002622','Amnesia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0002871','Anaemia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0036572','Convulsion');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0027707','Nephritis interstitial');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0027947','Neutropenia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0030193','Pain');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0030312','Pancytopenia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0031542','Phlebitis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0033687','Proteinuria');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0033774','Pruritus');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0035078','Renal failure');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0036830','Serum sickness');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0036974','Shock');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0037383','Sneezing');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018939','Blood disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018378','Guillain-Barre syndrome');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018418','Gynaecomastia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018965','Haematuria');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018681','Headache');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0019158','Hepatitis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0019163','Hepatitis B');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018799','Cardiac disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0018802','Cardiac failure congestive');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0687713','Gastrointestinal pain');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C2830004','Somnolence');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0003467','Anxiety');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0003862','Arthralgia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0004364','Autoimmune disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0853034','Blood creatine phosphokinase increased');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0853692','Blood triglycerides increased');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0860801','Glucose low');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0917801','Insomnia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0001125','Lactic acidosis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0877192','Lipodystrophy acquired');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0948594','Musculoskeletal discomfort');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0948586','Protein urine present');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0020580','Hypoaesthesia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0021053','Immune system disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0023530','Leukopenia');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0023895','Liver disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0037763','Muscle spasms');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0035243','Respiratory tract infection');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0037199','Sinusitis');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0037274','Skin disorder');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0600142','Hot flush');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0851341','Infestation NOS');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0549373','Laryngeal pain');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0555724','Lip dry');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0858259','Nasal discomfort');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0853254','Nasal passage irritation');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0858635','Pharyngolaryngeal pain');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0700590','Sweating increased');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C0750016','Generalized urticaria');"
    )

    engine.execute(
        "INSERT INTO Side_Effects VALUES ('C1384353','Infestation');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00271','DB00842');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00271','DB06335');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00271','DB00879');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00649','DB00704');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00704','DB00649');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00704','DB00842');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00842','DB00271');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00842','DB06335');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00842','DB00879');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00842','DB00704');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00879','DB00271');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00879','DB00842');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00879','DB06335');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB00990','DB01220');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB01132','DB06335');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB01132','DB01220');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB01220','DB00990');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB01220','DB01132');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB06335','DB00271');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB06335','DB00842');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB06335','DB00879');"
    )

    engine.execute(
        "INSERT INTO Interacts VALUES ('DB06335','DB01132');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00136','C0000729');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00136','C0000737');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00136','C0001925');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00136','C0002792');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00136','C0003123');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0002792');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0002994');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0004093');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0010520');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0019080');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0020458');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00152','C0020517');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00271','C0002622');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00271','C0002871');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00271','C0002792');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0036572');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0027707');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0027947');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0030193');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0030312');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0031542');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0033687');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0033774');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0035078');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0036830');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0036974');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00485','C0037383');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0018939');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0018378');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0018418');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0018965');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0018681');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0019158');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00649','C0019163');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00704','C0018799');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00704','C0018802');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00704','C0018681');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00842','C0687713');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00842','C2830004');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0000737');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0002871');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0002994');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0003467');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0003862');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0004093');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0004364');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0853034');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0853692');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0860801');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0917801');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0001125');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0877192');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0948594');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00879','C0948586');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00990','C0020580');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00990','C0021053');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00990','C0023530');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB00990','C0023895');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01132','C0037763');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01132','C0035243');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01132','C0037199');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01132','C0037274');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0687713');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0600142');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0851341');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0549373');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0555724');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0858259');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0853254');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0858635');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB01220','C0700590');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0853034');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0853692');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0687713');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0750016');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C1384353');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0851341');"
    )

    engine.execute(
        "INSERT INTO Causes VALUES ('DB06335','C0948594');"
    )

db_init()
insert_data()