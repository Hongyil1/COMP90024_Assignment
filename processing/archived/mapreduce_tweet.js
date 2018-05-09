{
  "_id": "_design/scenario",
  "_rev": "17-d0576b9e144e78b0e65322707de0d87a",
  "views": {
    "scenario1": {
      "reduce": "_sum",
      "map": "function (doc) {\n  var melbourne = ['south melbourne', 'brunswick west', 'carlton north', 'west melbourne', 'fitzroy north', 'south wharf', 'southbank', 'cremorne', 'williamstown', 'kensington', 'melbourne', 'south yarra', 'fitzroy', 'north melbourne', 'middle park', 'yarraville', 'flemington', 'albert park', 'spotswood', 'ascot vale', 'parkville', 'northcote', 'windsor', 'brunswick', 'richmond', 'footscray', 'clifton hill', 'carlton', 'prahran', 'east melbourne', 'newport', 'docklands', 'port melbourne', 'collingwood', 'seddon', 'maribyrnong', 'brunswick east', 'travancore', 'princes hill', 'abbotsford']\n  var sydney = ['bankstown', 'baulkham hills', 'blacktown', 'blue mountains', 'botany', 'camden', 'campbelltown', 'canterbury', 'burwood', 'cessnock', 'concord', 'fairfield', 'drummoyne', 'gosford', 'greater lithgow', 'hawkesbury', 'holroyd', 'hornsby', \"hunter's hill\", 'hurstville', 'kogarah', 'ku-ring-gai', 'lake macquarie', 'lane cove', 'leichhardt', 'liverpool', 'manly', 'marrickville', 'mosman', 'mudgee', 'mulwaree', 'norh sydney', 'oberon', 'parramatta', 'penrith', 'pittwater', 'rockdale', 'randwick', 'ryde', 'rylstone', 'singleton', 'south sydney', 'strathfield', 'sutherland shire', 'sydney', 'warringah', 'waverley', 'willoughby', 'wingecarribee', 'wollondilly', 'wollongong', 'woollahra', 'wyong', 'ashfield']\n    if(doc.lifestyle.length>0){\n      if(melbourne.indexOf(doc.location.suburb)!=-1||sydney.indexOf(doc.location.suburb)!=-1){\n        for(j=0; j<doc.lifestyle.length; j++){\n         emit([doc.sentiment,doc.lifestyle[j]],1)\n        }\n      }\n    }\n}"
    },
    "scenario2": {
      "reduce": "_sum",
      "map": "function (doc) {\n  var liquor_top_10_AURIN = ['melbourne', 'south yarra', 'carlton', 'south melbourne', 'north melbourne', 'docklands', 'southbank', 'carlton north', 'east melbourne', 'west melbourne'];\n  if(liquor_top_10_AURIN.indexOf(doc.location.suburb)!=-1&&doc.liquor){\n      emit([doc.sentiment,doc.location.suburb],1)\n  }\n}"
    },
    "scenario3": {
      "reduce": "_sum",
      "map": "function (doc) {\n  var melbourne = ['south melbourne', 'brunswick west', 'carlton north', 'west melbourne', 'fitzroy north', 'south wharf', 'southbank', 'cremorne', 'williamstown', 'kensington', 'melbourne', 'south yarra', 'fitzroy', 'north melbourne', 'middle park', 'yarraville', 'flemington', 'albert park', 'spotswood', 'ascot vale', 'parkville', 'northcote', 'windsor', 'brunswick', 'richmond', 'footscray', 'clifton hill', 'carlton', 'prahran', 'east melbourne', 'newport', 'docklands', 'port melbourne', 'collingwood', 'seddon', 'maribyrnong', 'brunswick east', 'travancore', 'princes hill', 'abbotsford']\n  if(melbourne.indexOf(doc.location.suburb)!=-1&&doc.crime){\n    emit(doc.location.suburb,1)\n  }\n}"
    },
    "scenario4": {
      "reduce": "_sum",
      "map": "function (doc) {\n  var melbourne=['south melbourne', 'brunswick west', 'carlton north', 'west melbourne', 'fitzroy north', 'south wharf', 'southbank', 'cremorne', 'williamstown', 'kensington', 'melbourne', 'south yarra', 'fitzroy', 'north melbourne', 'middle park', 'yarraville', 'flemington', 'albert park', 'spotswood', 'ascot vale', 'parkville', 'northcote', 'windsor', 'brunswick', 'richmond', 'footscray', 'clifton hill', 'carlton', 'prahran', 'east melbourne', 'newport', 'docklands', 'port melbourne', 'collingwood', 'seddon', 'maribyrnong', 'brunswick east', 'travancore', 'princes hill', 'abbotsford'];\n  if(melbourne.indexOf(doc.location.suburb)!=-1){\n    emit(doc.time.when,1)\n  }\n}"
    },
    "scenario5": {
      "reduce": "_sum",
      "map": "function (doc) {\n  if(doc.retweet.original_sentiment != null){\n  emit(doc.retweet.original_sentiment, 1);\n  }\n}"
    }
  },
  "language": "javascript"
}