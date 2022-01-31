# DTBank
A unified drug-target database with a web-based user interface.

DTBank contains the following information:

1. **User** includes the following attributes; username, institute name, and password. There exists only one
user with a specific username and institute. There can be an unlimited number of users. Passwords are
 encrypted using the SHA256 algorithm and stored in the database accordingly.
2. **Database manager** consists of the following attributes: username and password. There exists only
one database manager with a specific username. There can be at most 5 database managers registered
to the system. Passwords are encrypted using the SHA256 algorithm and stored in the database
accordingly.
3. **DrugBank** includes DrugBank ID, drug name, description, and interaction with other drugs. By definition, each DrugBank ID is unique.
4. **SIDER** includes UMLS CUI (side effect IDs), DrugBank ID, and side effect name. By definition, each
UMLS CUI is unique.
5. **BindingDB** includes Reaction ID, DrugBank ID, UniProt ID, target (protein) name, SMILES (chemical
notation of drug), affinity in nM (the strength of the binding interaction between drugs and targets), the
measure of the interaction (Ki, Kd, IC50), DOI (link on the web to identify the article or document that
mentions the drug-target interaction. E.g., https://doi.org/10.1093/bioinformatics/bty593), authors of the article or document, usernames of the corresponding authors, and institutions of the authors. Authors
are considered as contributors. Each contribution makes an impact on the institute. By definition, each
Reaction ID is unique and contributors are users of DTBank.
6. UniProt includes UniProt ID and amino acid sequence of the corresponding protein. By definition, each
UniProt ID is unique.

Two types of people can use DTBank: users and database managers. Both types can log
in to the system. Users are able to perform only the operations that are defined for their roles. DTBank users
can be contributors to the papers/documents stored in BindingDB. Each institute has a score based
on the number of publications and number of the contributors to these publications. Institutes get 5 points for
each publication and get 2 points for each contributor of the corresponding publication.

The UI supports the following operations:

1. Database managers are able to log in to the system with their credentials.
2. Database managers are able to add new users to the system.
3. Database managers are able to update affinity values of drugs using Reaction IDs and delete drugs
using DrugBank IDs.
4. Database managers are able to delete proteins using UniProt IDs.
5. Database managers are able to update contributors of papers=documents using Reaction IDs.
6. Database managers are able to separately view all drugs listed in DrugBank, all proteins listed in
UniProt, all side effects listed in SIDER, all drug-target interactions, all papers and their contributors
listed in BindingDB, and all users in DTBank.
7. Users are able to log in to the system with their credentials.
8. Users are able to separately view the names, DrugBank IDs, SMILES strings, descriptions, target
names, and side effect names of all drugs.
9. Users are able to view all interactions of a specific drug.
10. Users are able to view all side effects of a specific drug.
11. Users are able to view all interacting targets of a specific drug.
12. Users are able to view interacting drugs of a specific protein.
13. Users are able to view drugs that affect the same protein.
14. Users are able to view proteins that bind the same drug.
15. Users are able to view drugs that have a specific side effect.
16. Users are able to search a keyword and view the drugs that contain this keyword in their descriptions.
17. Users are able to view the drug(s) with the least amount of side effects that interact with a specific
protein.
18. Users are able to view the DOI of papers and contributors of the corresponding paper.
19. Users are able to rank institutes according to their total scores (Decreasing order).
20. Users are able to filter interacting targets of a specific drug considering the selected measurement
type and the range of the affinity values.
21. The system has three triggers:

* When a drug is deleted, it is removed from the the list of the interacting drugs of other drugs,
and its corresponding entries from SIDER and BindingDB.

* When a protein is deleted, its corresponding entries from BindingDB are removed.

* When a new publication is added to the system, the corresponding institute gets 5 points for a
new publication and gets 2 points for each individual who contributed to it. Also, when there is
an update on the publication that changes the number of contributors, update the corresponding
institute's score accordingly.
