[DB_ID] data/spider/database/academic/academic.sqlite

[Schema]
# Table: author
(aid:INTEGER, Primary Key, the aid of the author)
(homepage:TEXT, the homepage of the author)
(name:TEXT, the name of the author)
(oid:INTEGER, the oid of the author)

# Table: cite
(cited:INTEGER, the cited of the cite, Maps to publication(pid))
(citing:INTEGER, the citing of the cite, Maps to publication(pid))

# Table: conference
(cid:INTEGER, Primary Key, the cid of the conference)
(homepage:TEXT, the homepage of the conference)
(name:TEXT, the name of the conference)

# Table: domain
(did:INTEGER, Primary Key, the did of the domain)
(name:TEXT, the name of the domain)

# Table: domain_author
(aid:INTEGER, Primary Key, the aid of the domain_author, Maps to author(aid))
(did:INTEGER, Primary Key, the did of the domain_author, Maps to domain(did))

# Table: domain_conference
(cid:INTEGER, Primary Key, the cid of the domain_conference, Maps to conference(cid))
(did:INTEGER, Primary Key, the did of the domain_conference, Maps to domain(did))

# Table: domain_journal
(did:INTEGER, Primary Key, the did of the domain_journal, Maps to domain(did))
(jid:INTEGER, Primary Key, the jid of the domain_journal, Maps to journal(jid))

# Table: domain_keyword
(did:INTEGER, Primary Key, the did of the domain_keyword, Maps to domain(did))
(kid:INTEGER, Primary Key, the kid of the domain_keyword, Maps to keyword(kid))

# Table: domain_publication
(did:INTEGER, Primary Key, the did of the domain_publication, Maps to domain(did))
(pid:INTEGER, Primary Key, the pid of the domain_publication, Maps to publication(pid))

# Table: journal
(homepage:TEXT, the homepage of the journal)
(jid:INTEGER, Primary Key, the jid of the journal)
(name:TEXT, the name of the journal)

# Table: keyword
(keyword:TEXT, the keyword of the keyword)
(kid:INTEGER, Primary Key, the kid of the keyword)

# Table: organization
(continent:TEXT, the continent of the organization)
(homepage:TEXT, the homepage of the organization)
(name:TEXT, the name of the organization)
(oid:INTEGER, Primary Key, the oid of the organization)

# Table: publication
(abstract:TEXT, the abstract of the publication)
(cid:TEXT, the cid of the publication, Maps to conference(cid))
(citation_num:INTEGER, the citation num of the publication)
(jid:INTEGER, the jid of the publication, Maps to journal(jid))
(pid:INTEGER, Primary Key, the pid of the publication)
(reference_num:INTEGER, the reference num of the publication)
(title:TEXT, the title of the publication)
(year:INTEGER, the year of the publication)

# Table: publication_keyword
(pid:INTEGER, Primary Key, the pid of the publication_keyword, Maps to publication(pid))
(kid:INTEGER, Primary Key, the kid of the publication_keyword, Maps to keyword(kid))

# Table: writes
(aid:INTEGER, Primary Key, the aid of the writes, Maps to author(aid))
(pid:INTEGER, Primary Key, the pid of the writes, Maps to publication(pid))

[Foreign keys]
cite.cited = publication.pid
cite.citing = publication.pid
domain_author.aid = author.aid
domain_author.did = domain.did
domain_conference.cid = conference.cid
domain_conference.did = domain.did
domain_journal.did = domain.did
domain_journal.jid = journal.jid
domain_keyword.did = domain.did
domain_keyword.kid = keyword.kid
domain_publication.did = domain.did
domain_publication.pid = publication.pid
publication.cid = conference.cid
publication.jid = journal.jid
publication_keyword.pid = publication.pid
publication_keyword.kid = keyword.kid
writes.aid = author.aid
writes.pid = publication.pid