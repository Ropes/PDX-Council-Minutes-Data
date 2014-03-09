Luigi-ETL-Demo
==============

Demonstration project for using Luigi process framework to run ETL jobs.

###Extract
Using scrapy, pull web assets and parse the html data for subject data. 

TODO: Pull up page of Multnomah county or Portland board meeting page
[Multnoma Board Records](http://multnomah.granicus.com/ViewPublisher.php?view_id=3)
[Portland Council Records](http://www.portlandonline.com/auditor/index.cfm?c=56674)
 * Construct list of available Minutes documents
 * Pull all Minute documents not previously processed
    * Each Minutes doc is it's own directory/Task which is delimited by a UID

###Transform
Sanitize example, clean/process/stem/nlp extracted data to record.
 * Each Minutes file is a pdf which needs to be parsed to extract headers and content data.
    * Use PDFMiner or PyPDF to extract necessary data.

###Loading/Save
 * Index data to Elasticsearch 
    * Have alternative for simple filesystem storage
 * Feed interesting data to D3.

##Setup
> pip install -r requirements.txt
TODO: Luigi config file
TODO: luigid daemon
TODO: Elasticsearch from docker image
TODO: Learn D3 for setup :/

##Running
TODO: Running scheduler
TODO: Running Elasticsearch docker image
TODO: Kickoff end task

