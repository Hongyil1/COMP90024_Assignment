{
  "_id": "_design/scenario",
  "_rev": "15-90354924a8342831d722b67f4be28b18",
  "views": {
    "scenario4": {
      "reduce": "_sum",
      "map": "function (doc) {\n    emit([doc.created_time,doc.suburb],1)\n}"
    }
  },
  "language": "javascript"
}