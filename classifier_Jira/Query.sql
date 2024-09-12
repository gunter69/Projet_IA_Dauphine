#Script SQL pour l'analyse / mise en forme des datas#

#ci-dessous differentes requetes pour faire un état des lieux sur les données manquantes dans la table issue
select * from issue i 


select count(*) from issue i 
where Description =''
or Description is null

select count(*) from issue i 
where `Type` ='' or `Type` is null

select distinct Status from issue i 

select Status, count(*) from issue i 
group by Status 

select distinct Resolution from issue i 

select Resolution, count(*) from issue i 
group by Resolution 


#cette requete permet le calcule du nombre de mots dans les descriptions + les mois des dates pour gagner du temps par rapport à la librairie python
DROP TABLE IF EXISTS data_cleaned;

create table data_cleaned2 
select 
*,
month(iss.Creation_Date) as created_month,
month(iss.Last_Updated) as lastUpdated_month,
(LENGTH(iss.Description) - LENGTH(REPLACE(iss.Description, ' ', '')) + 1) as description_wordcount
from tawos_cleaned.issue iss


# pour la suite analyse sur la table de change log qui permet d'avoir plus d'information sur les issues durant leur vie

select tt, nb from
(select distinct(To_String) as tt , count(*) as nb from change_log cl 
where Field  = 'status'
group by To_String
union 
select distinct(From_String) as tt , count(*) as nb from change_log cl 
where Field  = 'status'
group by From_String
)as r1
order by 1 desc
