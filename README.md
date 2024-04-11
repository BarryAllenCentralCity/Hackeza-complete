# Database Structure

# Table: USER_DETAIL

Fields:
email (String, Primary Key, Unique, Not Null): The email address of the user.  
It serves as the primary key and must be unique and not null.  
roles (String, Not Null): Represents the roles associated with the user.  

# Table: JOURNALS
Fields:  
j_email (String, Not Null): Email address associated with the journal entry.  
j_dop (String, Not Null): Date of publication.  
j_nat_inat (String, Not Null): Nature of the journal entry (e.g., international, national).  
j_ranking (Integer, Not Null): Ranking of the journal.  
j_broad_area (String, Not Null): Broad area to which the journal entry belongs.  
j_con_name (String): Name of the conference associated with the journal entry (if applicable).  
j_impf (String, Not Null): Impact factor of the journal.  
j_pap_tit (String, Not Null): Title of the paper.  
j_doi (String, Primary Key, Not Null): Digital Object Identifier (DOI) of the journal entry. It serves as the primary key and must be not null.  
j_authors (String, Not Null): Authors of the paper.  
j_volume (String, Not Null): Volume number.  
j_issue (String, Not Null): Issue number.  
j_page_n (String, Not Null): Page numbers.  
j_publisher (String, Not Null): Publisher of the journal.  
j_con_loc (String, Not Null): Location of the conference associated with the journal entry (if applicable).  

# Table: CONFERENCE  
Fields:  
c_email (String, Not Null): Email address associated with the conference entry.  
c_date (Integer, Not Null): Date of the conference.  
c_nat (String, Not Null): Nature of the conference (e.g., international, national).  
c_corerank (Integer, Not Null): Core ranking of the conference.  
c_pap_tit (String, Not Null): Title of the paper presented at the conference.  
c_short_name (String, Not Null): Short name of the conference.  
c_con_location (String, Not Null): Location of the conference.  
c_full_name (String, Not Null): Full name of the conference.  
c_url (String, Primary Key, Not Null): URL of the conference. It serves as the primary key and must be not null.  
c_authors (String, Not Null): Authors of the paper presented at the conference.  
c_volume (String, Not Null): Volume number.  
c_issue (String, Not Null): Issue number.  
c_page_n (String, Not Null): Page numbers.  
c_publisher (String, Not Null): Publisher of the conference proceedings.  
  
# USER_DETAILS Table  

![image](https://github.com/BarryAllenCentralCity/Hackeza-complete/assets/93136153/e21caea2-e57a-45bd-a7a3-71078bd1bb90)

