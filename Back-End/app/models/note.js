const mongoose = require('mongoose');

const NoteSchema = mongoose.Schema({
    id:String,
    fullName: String,
    email:String,
    comment: String
}, {
    timestamps: true
});

module.exports = mongoose.model('Note', NoteSchema);