function(doc){
    if(doc.type !== "session") return;

    emit(doc._id, null);
}
