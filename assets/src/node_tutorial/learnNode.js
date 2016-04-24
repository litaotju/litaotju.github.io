var events = require('events');
var emitter = new events.EventEmitter();
emitter.on('some_event', function(){
    console.log('some_event happended');
});
var i = 0;
do {
    setTimeout( function(){emitter.emit('some_event')}, 1000);
    i++;
}while(i < 5)
    
var count = events.EventEmitter.listenerCount(emitter, 'some_event');
console.log("emitter has "+count+" listener");