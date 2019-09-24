var server = 'studenti';
var BOSH_SERVICE = 'http://127.0.0.1:7070/http-bind/';
var ROOM = 'prova@conference.' + server;
var ROOM_SERVICE = 'conference.' + server;
var connection = null;
var jid=null;
var sid=null;
var rid=null;
var ut=null;
var registered = null;

serverJ= null;
if(window.location.protocol === 'http:')
	serverJ = "http://" + window.location.hostname + ":8088/janus";
else
	serverJ = "https://" + window.location.hostname + ":8089/janus";

var janus = null;
var videocall = null;
var started = false;
var spinner = null;
var audioenabled = false;
var videoenabled = false;
var myusername = null;
var yourusername = null;
var jsepIncoming = null;

function log(msg) {
  $('#log').append('<div></div>').append(document.createTextNode(msg));
  console.log(msg);
}

function onConnect(status) {
  if (status == Strophe.Status.CONNECTING) {
    log('Strophe is connecting.');
  } else if (status == Strophe.Status.CONNFAIL) {
    log('Strophe failed to connect.');
  } else if (status == Strophe.Status.DISCONNECTING) {
    log('Strophe is disconnecting.');
  } else if (status == Strophe.Status.DISCONNECTED) {
    log('Strophe is disconnected.');
    let url = "index.html";
	window.location.href = url; //nel caso di una log out si ritorna al LogIn
  } else if (status == Strophe.Status.CONNECTED) {
    log('Strophe is connected.');
    connection.send($pres());
	connection.addHandler(onMessage, null, 'message', 'chat', null, null); //handle del messaggio one-to-one
	connection.addHandler(onMessageGroup, null, 'message','groupchat',null,null); //handle del messaggio di gruppo
  }else if(status == Strophe.Status.ATTACHED){
	log('Strophe is attached.');
	getRoster(); //PRENDO GLI UTENTI
	listRooms();
	connection.addHandler(onMessage, null, 'message', 'chat', null, null); //handle del messaggio one-to-one
	connection.addHandler(onMessageGroup, null, 'message','groupchat',null,null); //handle del messaggio di gruppo
	connection.addHandler(onSubscriptionRequest, null, "presence", "subscribe"); //richiesta 
    connection.addHandler(onPresence, null, "presence"); //presence
	connection.send($pres());
	//getRoster(); //PRENDO GLI UTENTI
	//listRooms(); 
  }
}

function onMessage(msg) {
	var to = msg.getAttribute('to');
	var from = msg.getAttribute('from');
	var type = msg.getAttribute('type');
	var elems = msg.getElementsByTagName('body');
	console.log("Sono in onMessage");
	if (type == "chat" && elems.length > 0) {
		var body = elems[0]; 
		var dest=Strophe.getNodeFromJid(from);  //pulisco la sorgente: mi serve solo il Node. 
		if ($('.contacts li:contains("' + dest + '")').length){
		/*se abbiamo già l'utente nella lista (quella mostrata dal panel), dobbiamo distinguere due cose
		1: l'utente è solo nella lista e non stiamo visualizzando la conversazione
		2: l'utente è proprio quello di cui visualizzo la conversazione. 
		*/
			if($('#dest').text() == dest)
				$('<li class="sent"> <p>'+Strophe.getText(body)+'</p></li>').appendTo($('.messages ul'));
		//se sto visualizzando la sua conversazione, si appende semplicemente il messaggio
			else
				document.getElementById(dest).style.color = "red"; 
		//la notifica di messaggio ricevuto consiste nel colorare l'utente di rosso.
		$(".messages").animate({ scrollTop: ($("#messaggilista li").height()*$("#messaggilista li").length) }, "fast");
	}else {
		$('<li class="contact" id="'+dest+'" tabindex="1">'+dest+'</li>').appendTo($('.contacts ul'));
		//$('<li class="contact" id ="'+dest+'"><div class="wrap"><span class="contact-status online"></span><img src="#" alt="" /><div class="meta"><p class="name">'+dest+'</p><p class="preview"><span>You:</span>'+dest+'</p></div></div></li>').appendTo('.contacts ul');
		document.getElementById(dest).style.color = "red";
		//se l'utente non è presente nella lista dei contatti, dobbiamo aggiungere quest'ultimo
		//in modo da poter continuare la conversazione
	}
  }
  return true;
}
function onMessageGroup(msg){	
	var to = msg.getAttribute('to');
	var from = msg.getAttribute('from');
	var type = msg.getAttribute('type');
	var elems = msg.getElementsByTagName('body');
	var body = elems[0]; 
	
	
	
	if(type == "groupchat" && elems.length > 0){	
		//dobbiamo sapere in quale gruppo è stato inviato un messaggio
		// e anche chi lo ha scritto
		var fromGroup = /(?<=\/)(.*?)(?=\@)/.exec(from);  //recupero il mittente
		var destGroup = from.split('@'); //recupero il gruppo.
		var toag= Strophe.getNodeFromJid(to);
		console.log(toag);
		console.log(fromGroup[0]);
		//console.log(fromGroup[0]);
		//bisogna controllare che chi ha scritto il messaggio non è l'utente della chat.
		console.log("Sono in onMessageGroup");
		//$('.contactsGroup li:contains("' + destGroup[0] + '")').length && fromGroup[0] != Strophe.getNodeFromJid(ut)
		if($('#dest').text() == destGroup[0]){//controllo se l'utente sta visualzzando la conversazione di gruppo. 
			if(toag==fromGroup[0]) 
				$('<li class="replies"> <p> You: '+Strophe.getText(body)+'</p></li>').appendTo($('.messages ul'));
			else 
				$('<li class="sent"> <p>'+fromGroup[0]+': '+Strophe.getText(body)+'</p></li>').appendTo($('.messages ul'));
			$(".messages").animate({ scrollTop: ($("#messaggilista li").height()*$("#messaggilista li").length) }, "fast");
		}else
			document.getElementById(destGroup[0]).style.color = "red";
			//motifica di messaggio nel gruppo
		
	}
	return true;
}

function sendMessage(msg) {
//invio di un messaggio
	//messaggio one-to-one
	if($('#type').text() == 'User'){
		$('<li class="replies"> <p>'+msg+'</p></li>').appendTo($('.messages ul'));   
		$(".messages").animate({ scrollTop: ($("#messaggilista li").height()*$("#messaggilista li").length) }, "fast");
		 var m = $msg({
			to: $('#dest').text()+'@'+server,
			from: $('#utente').val(),
			type: 'chat'
		  }).c("body").t(msg);
		  connection.send(m);
	}else{
	//messaggio di gruppo
		//$('<li class="replies"> <p>'+'You: '+msg+'</p></li>').appendTo($('.messages ul'));   

		 var m = $msg({
			to: $('#dest').text()+'@'+ROOM_SERVICE,
			from: $('#utente').val(),
			type: 'groupchat'
		  }).c("body").t(msg);
		  connection.send(m);
	}
}


function subscribePresence(jid) {
	//vogliamo aggiungere l'utente alla lista "preferiti" 
	// per essere notificati al suo cambiamento di stato.
  log('subscribePresence: ' + jid);
  connection.send($pres({
    to: jid+'@'+server,
    type: "subscribe"
  }));
  //getRoster();
  if (($('#'+jid).text()=="")){
		
		$('<li class="contact" id='+jid+' tabindex="1">'+jid+'</li>').appendTo($('.contacts ul'));
		//$('<li class="contact" id ="'+jid+'"><div class="wrap"><span class="contact-status online"></span><img src="#" alt="" /><div class="meta"><p class="name">'+jid+'</p><p class="preview"><span>You:</span>'+jid+'</p></div></div></li>').appendTo('.contacts ul');
	}
}

function getRoster() {
	//ritorna tutti gli utenti a cui siamo sottoscritti
  var iq = $iq({
    type: 'get'
  }).c('query', {
    xmlns: 'jabber:iq:roster'
  });
  connection.sendIQ(iq, rosterCallback);
}

function rosterCallback(iq) {
  log('rosterCallback:');
  $(iq).find('item').each(function() {
  var jid = Strophe.getNodeFromJid($(this).attr('jid'));
  var type = $(this).attr('subscription');
	if (($('#'+jid).text()=="") && type != 'from'){
		
		$('<li class="contact" id='+jid+' tabindex="1">'+jid+'</li>').appendTo($('.contacts ul'));
		//$('<li class="contact" id ="'+jid+'"><div class="wrap"><span class="contact-status online"></span><img src="#" alt="" /><div class="meta"><p class="name">'+jid+'</p><p class="preview"><span>You:</span>'+jid+'</p></div></div></li>').appendTo('.contacts ul');
	}
	log('	>' + jid);
  });
}

function onSubscriptionRequest(stanza) {
  if (stanza.getAttribute("type") == "subscribe") {
    var from = $(stanza).attr('from');
    log('onSubscriptionRequest: from=' + from);
    // Invio di una notifica 'subscribed'
	alert(from + ' added you to his favorites.')
    connection.send($pres({
      to: from,
      type: "subscribed"
    }));
  }
  return true;
}

function onPresence(presence) {
  log('onPresence:');
  var presence_type = $(presence).attr('type'); 
  var from = Strophe.getNodeFromJid($(presence).attr('from')); 
  var selezione=$(presence).attr('from'); //mi serve per sapere cosa fare.
  
  if(selezione.includes('@'+ROOM_SERVICE)){
	  log("**********"+selezione);
	  
  }else{
	if (!presence_type){ 
		presence_type = "online";
	  
	}
	log('	>' + from + ' --> ' + presence_type);
	if (presence_type != 'error') {
		if (presence_type === 'unavailable') {
		// Gestire account offline
		$("#"+from).css("background","transparent");
		} else {
		var show = $(presence).find("show").text(); 
		if (show === 'chat' || show === '') {
			// Gestire account online
			$("#"+from).css("background","green");
		
		} else {
			// etc...
		}
		}
	}
	}
  return true;
}

function listRooms() {
  connection.muc.listRooms(ROOM_SERVICE, function(msg) {
	$(msg).find('item').each(function() {
		var jid = $(this).attr('jid'),
        name = $(this).attr('name');
		$('<li class="contact" id='+name+' tabindex="1">'+name+'</li>').appendTo($('.contactsGroup ul'));				
    });
  }, function(err) {
    log("listRooms - error: " + err);
  });
}

function enterRoom(room) {
  log("enterRoom: " + room);
  connection.muc.init(connection);
  connection.muc.join(room+'@'+ROOM_SERVICE, Strophe.getBareJidFromJid(ut), room_msg_handler,  room_pres_handler);
}

function room_pres_handler(a,b,c) {
	log('MUC: room_pres_handler');
	return true;
}

function room_msg_handler(msg, b, c) {
  return true;
}

function exitRoom(room) {
  log("exitRoom: " + room);
}

function rawInput(data) {
  console.log('RECV: ' + data);
  var url = window.location.href;
  var oldrid = window.location.href.substr(url.indexOf("rid=")+4);
  var newrid = parseInt(oldrid)+1;
  var query = window.location.search;
  query = query.substr(0,query.indexOf("rid=")+4)+newrid;
  window.history.pushState('chat.html','title','/Chat/chat.html'+query);
  
}

function rawOutput(data) {
  console.log('SENT: ' + data);
}

function createNewChat(testo){
	//caricamento del nome nella chatArea
	$('.contact-profile').empty();
	$('.messages ul').empty();
	$('<p id="dest">'+testo+'</p>').appendTo($('.contact-profile'));
	$('<p id="type" hidden>User</p>').appendTo($('.contact-profile'));
	//caricamento dei messaggi che abbiamo con il contatto selezionato
	connection.mam.query(Strophe.getBareJidFromJid(ut), {
		with: testo+'@'+server,
		onMessage: function(message) {
		var sorg=$(message).find("forwarded message").attr("from");
		var dest=$(message).find("forwarded message").attr("to");
		var type=$(message).find("forwarded message").attr("type");
		console.log("Sono in CreateNewChat");
		if(type=='chat'){
			if (Strophe.getNodeFromJid(sorg)==testo){
				$('<li class="sent"> <p>'+$(message).find("forwarded message body").text()+'</p></li>').appendTo($('.messages ul'));
			}else{
				$('<li class="replies"> <p>'+$(message).find("forwarded message body").text()+'</p></li>').appendTo($('.messages ul'));
			}
			
		}
		$(".messages").animate({ scrollTop: ($("#messaggilista li").height()*$("#messaggilista li").length) }, "fast");
		return true;
		},
		onComplete: function(response) {

			//console.log("Got all the messages");
			//console.log(response);
	}
	});
	
}

function createNewChatGroup(testo){
	//caricamento del nome nella chatArea
	$('.contact-profile').empty();
	$('.messages ul').empty();
	$('<p id="dest">'+testo+'</p>').appendTo($('.contact-profile'));
	$('<p id="type" hidden>Group</p>').appendTo($('.contact-profile'));
	//caricamento dei messaggi che abbiamo con il gruppo selezionato
	//Strophe.getBareJidFromJid(ut)
	connection.mam.query(Strophe.getBareJidFromJid(ut), {
		with: testo+'@'+ ROOM_SERVICE,
		onMessage: function(message) {
		console.log("Sono in CreateNewChatGroup");
		/*var sorg=$(message).find("forwarded message").attr("from");
		console.log(sorg);
		var dest=$(message).find("forwarded message").attr("to");
		console.log("************************************************************");
		var sorgente = /(?<=\/)(.*?)(?=\@)/.exec(sorg); //chi ha scritto il messaggio	
		if (sorgente[0]!=Strophe.getNodeFromJid(ut)){
			$('<li class="sent"> <p>'+sorgente[0]+': '+$(message).find("forwarded message body").text()+'</p></li>').appendTo($('.messages ul'));
		}else{
			$('<li class="replies"> <p>'+'You: '+$(message).find("forwarded message body").text()+'</p></li>').appendTo($('.messages ul'));
		}*/
		return true;
		},
		onComplete: function(response) {

			//console.log("Got all the messages");
			//console.log(response);
		}
	});
}

//Funzione di registrazione utente
function registerUsername() {
	// Try a registration
	var username = Strophe.getNodeFromJid(ut);
	if(username === "") {
		bootbox.alert("Insert a username to register (e.g., pippo)");
		return;
	}
	if(/[^a-zA-Z0-9]/.test(username)) {
		bootbox.alert('Input is not alphanumeric');
		return;
	}
	var register = { "request": "register", "username": username };
	videocall.send({"message": register});
}


//Funzione per call
function doCall() {
	// Call someone
	var username = $('#dest').text();
	if(username === "") {
		bootbox.alert("Select a user to call (e.g., pluto chat)");
		
		return;
	}
	if(/[^a-zA-Z0-9]/.test(username)) {
		bootbox.alert('Input is not alphanumeric');
		
		return;
	}
	$('#call').attr('disabled', true);
	$('#videos').removeClass('hide').show();
	$('#ring').removeClass('hide').show();
	$('#accept').hide();
	//Chiamata all'utente selezionato
	videocall.createOffer(
		{
			// By default, it's sendrecv for audio and video...
			//media: { data: false },	// ... let's negotiate data channels as well
			success: function(jsep) {
				Janus.debug("Got SDP!");
				Janus.debug(jsep);
				var body = { "request": "call", "username": $('#dest').text() };
				console.log('INVIATO'+body);
				videocall.send({"message": body, "jsep": jsep});
			},
			error: function(error) {
				Janus.error("WebRTC error...", error);
				bootbox.alert("WebRTC error... " + error);
			}
		});
}


$(document).ready(function() {
	
	
	
	
	
	//funzione per prendere i parametri dalla queryString
	function getUrlVars(requestedKey) {
	var vars = [], hash;
	var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

	for (var i = 0; i < hashes.length; i++) {
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	if (typeof requestedKey == 'undefined') {
		return vars;
	} else {
		return vars[requestedKey];
	}
	}


	ut=decodeURIComponent(getUrlVars("user"));
	$("#utente").val(Strophe.getNodeFromJid(ut));
	sid=getUrlVars('sid');
	rid=getUrlVars('rid');
	
	//Gestione connessione con openfire
    var url = BOSH_SERVICE;
    connection = new Strophe.Connection(url);
    connection.rawInput = rawInput;
    connection.rawOutput = rawOutput;
    connection.attach(ut, sid, rid,onConnect); 
   
	// Initialize the library (console debug enabled)
	Janus.init({debug: true, callback: function() {
			// Make sure the browser supports WebRTC
			if(!Janus.isWebrtcSupported()) {
				bootbox.alert("No WebRTC support... ");
				return;
			}
			// Create session
			janus = new Janus(
				{
					server: serverJ,
					success: function() {
						// Attach to videocall plugin
						janus.attach(
							{
								plugin: "janus.plugin.videocall",
								success: function(pluginHandle) {
									videocall = pluginHandle;
									if(!registered){
										registerUsername();
									}
									Janus.log("Plugin attached! (" + videocall.getPlugin() + ", id=" + videocall.getId() + ")");
								},
								error: function(error) {
									Janus.error("  -- Error attaching plugin...", error);
									bootbox.alert("  -- Error attaching plugin... " + error);
								},
								consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");
									if(on) {
										// Darken screen and show hint
										$.blockUI({ 
											message: '',
											css: {
												border: 'none',
												padding: '15px',
												backgroundColor: 'transparent',
												color: '#aaa',
												top: '10px',
												left: (navigator.mozGetUserMedia ? '-100px' : '300px')
											} });
									} else {
										// Restore screen
										$.unblockUI();
									}
								},
								mediaState: function(medium, on) {
									Janus.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium);
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#videoleft").parent().unblock();
								},
								onmessage: function(msg, jsep) {
									Janus.debug(" ::: Got a message :::");
									Janus.debug(JSON.stringify(msg));
									var result = msg["result"];
									if(result !== null && result !== undefined) {
										if(result["list"] !== undefined && result["list"] !== null) {
											var list = result["list"];
											Janus.debug("Got a list of registered peers:");
											Janus.debug(list);
											for(var mp in list) {
												Janus.debug("  >> [" + list[mp] + "]");
											}
										} else if(result["event"] !== undefined && result["event"] !== null) {
											var event = result["event"];
											if(event === 'registered') {
												myusername = result["username"];
												Janus.log("Successfully registered as " + myusername + "!");
												registered =true;
											} else if(event === 'calling') {
												Janus.log("Waiting for the peer to answer...");
												// TODO Any ringtone?
											} else if(event === 'incomingcall') {
												$('#ring').removeClass('hide').show();
												Janus.log("Incoming call from " + result["username"] + "!");
												jsepIncoming = jsep;
												yourusername = result["username"];
												
											} else if(event === 'accepted') {
												var peer = result["username"];
												if(peer === null || peer === undefined) {
													Janus.log("Call started!");
												} else {
													Janus.log(peer + " accepted the call!");
													yourusername = peer;
												}
												// TODO Video call can start
												if(jsep !== null && jsep !== undefined)
													videocall.handleRemoteJsep({jsep: jsep});
											} else if(event === 'hangup') {
												Janus.log("Call hung up by " + result["username"] + " (" + result["reason"] + ")!");
												// TODO Reset status
												videocall.hangup();
												$('#accept').removeClass('hide').show();
												$('#ring').hide();
												if(spinner !== null && spinner !== undefined)
													spinner.stop();
												$('#waitingvideo').remove();
												$('#videos').hide();
												$('#call').attr('disabled', false);
												$('#toggleaudio').attr('disabled', true);
												$('#togglevideo').attr('disabled', true);
											
											}
										}
									} else {
										// FIXME Error?
										var error = msg["error"];
										bootbox.alert(error);
										if(error.indexOf("already taken") > 0) {
											// FIXME Use status codes...
											$('#username').removeAttr('disabled').val("");
											$('#register').removeAttr('disabled').unbind('click').click(registerUsername);
										}
										// TODO Reset status
										videocall.hangup();
										if(spinner !== null && spinner !== undefined)
											spinner.stop();
										$('#waitingvideo').remove();
										$('#videos').hide();
										$('#call').attr('disabled', false);
										$('#toggleaudio').attr('disabled', true);
										$('#togglevideo').attr('disabled', true);
										
									}
								},
								onlocalstream: function(stream) {
									Janus.debug(" ::: Got a local stream :::");
									Janus.debug(JSON.stringify(stream));
									$('#videos').removeClass('hide').show();
									if($('#myvideo').length === 0)
										$('#videoleft').append('<video class="rounded centered" id="myvideo" width=320 height=240 autoplay muted="muted"/>');
									attachMediaStream($('#myvideo').get(0), stream);
									$("#myvideo").get(0).muted = "muted";
									$("#videoleft").parent().block({
										message: '<b>Publishing...</b>',
										css: {
											border: 'none',
											backgroundColor: 'transparent',
											color: 'white'
										}
									});
									// No remote video yet
									$('#videoright').append('<video class="rounded centered" id="waitingvideo" width=320 height=240 />');
									if(spinner == null) {
										var target = document.getElementById('videoright');
										spinner = new Spinner({top:100}).spin(target);
									} else {
										spinner.spin();
									}
									var videoTracks = stream.getVideoTracks();
									if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
										// No webcam
										$('#myvideo').hide();
										$('#videoleft').append(
											'<div class="no-video-container">' +
												'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
												'<span class="no-video-text">No webcam available</span>' +
											'</div>');
									}
								},
								onremotestream: function(stream) {
									Janus.debug(" ::: Got a remote stream :::");
									Janus.debug(JSON.stringify(stream));
									if($('#remotevideo').length === 0)
										$('#videoright').append('<video class="rounded centered hide" id="remotevideo" width=320 height=240 autoplay/>');
									// Show the video, hide the spinner and show the resolution when we get a playing event
									$("#remotevideo").bind("playing", function () {
										$('#waitingvideo').remove();
										$('#remotevideo').removeClass('hide');
										if(spinner !== null && spinner !== undefined)
											spinner.stop();
										spinner = null;
										var width = this.videoWidth;
										var height = this.videoHeight;
										
										if(webrtcDetectedBrowser == "firefox") {
											// Firefox Stable has a bug: width and height are not immediately available after a playing
											setTimeout(function() {
												var width = $("#remotevideo").get(0).videoWidth;
												var height = $("#remotevideo").get(0).videoHeight;
												
											}, 2000);
										}
									});
									attachMediaStream($('#remotevideo').get(0), stream);
									var videoTracks = stream.getVideoTracks();
									if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0 || videoTracks[0].muted) {
										// No remote video
										$('#remotevideo').hide();
										$('#videoright').append(
											'<div class="no-video-container">' +
												'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
												'<span class="no-video-text">No remote video available</span>' +
											'</div>');
									}
									$('#callee').removeClass('hide').html(yourusername).show();
									// Enable audio/video buttons and bitrate limiter
									audioenabled = true;
									videoenabled = true;
									$('#toggleaudio').html("Disable audio").removeClass("btn-success").addClass("btn-danger")
											.unbind('click').removeAttr('disabled').click(
										function() {
											audioenabled = !audioenabled;
											if(audioenabled)
												$('#toggleaudio').html("Disable audio").removeClass("btn-success").addClass("btn-danger");
											else
												$('#toggleaudio').html("Enable audio").removeClass("btn-danger").addClass("btn-success");
											videocall.send({"message": { "request": "set", "audio": audioenabled }});
										});
									$('#togglevideo').html("Disable video").removeClass("btn-success").addClass("btn-danger")
											.unbind('click').removeAttr('disabled').click(
										function() {
											videoenabled = !videoenabled;
											if(videoenabled)
												$('#togglevideo').html("Disable video").removeClass("btn-success").addClass("btn-danger");
											else
												$('#togglevideo').html("Enable video").removeClass("btn-danger").addClass("btn-success");
											videocall.send({"message": { "request": "set", "video": videoenabled }});
										});
									$('#toggleaudio').parent().removeClass('hide').show();
									
								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification :::");
									$('#myvideo').remove();
									$('#remotevideo').remove();
									$("#videoleft").parent().unblock();
									$('#callee').empty().hide();
									yourusername = null;
									$('#videos').hide();
									$('#toggleaudio').attr('disabled', true);
									$('#togglevideo').attr('disabled', true);
									$('#waitingvideo').remove();
									$('#videos').hide();
									$('#accept').removeClass('hide').show();
									$('#ring').hide();
									$('#call').attr('disabled', false);
								}
								
							});				//FINE ATTACH
					},
					error: function(error) {
						Janus.error(error);
						bootbox.alert(error, function() {
							window.location.reload();
						});
					},
					destroyed: function() {
						window.location.reload();
					}
				});
	}});
	
	
	
	$('#send').attr('disabled',true); 
	//all'inizio il bottone di send è disabilitato.
	//si deve abilitare solo quando scriviamo qualcosa. Ovviamente 
	//è possibile inviare il messaggio solo se il destinatario è specificato.
	
	
	$('.message-input input').on('keyup',function(){
        if($('.message-input input').val() !=''){
			log("abilito send");
            $('#send').attr('disabled', false);
        }else{
			$('#send').attr('disabled',true);
		}
    });
	
	
	$('#send').bind('click', function() {
	 //aggiungere che se non ho selezionato un user non posso mandare proprio nulla
		var msg = $(".message-input input").val();
		if( $('#dest').text()!=""){
			sendMessage(msg);
			$(".message-input input").val('');
		}else{
			log("non lo invio");
		}
  });
	
	$(window).on('keydown', function(e) {
	 if (e.which == 13) {
		var msg = $(".message-input input").val();
		if( $('#dest').text()!=""){
			sendMessage(msg);
			$(".message-input input").val('');
		}else{
			log("non lo invio");
		}
		return false;
	}
  });
	
	
	$('#subscribe').attr('disabled',true);
	

	$('.contacts ul').on('click','li.contact',function() {
		console.log($(this).text()); // gets text contents of clicked li
		document.getElementById($(this).text()).style.color = "white";
		createNewChat($(this).text());
		if(registered)
			$('#call').attr('disabled',false);
    });
	
	$('.contactsGroup ul').on('click','li.contact',function() {
		console.log($(this).text()); // stampa il contenuto dell'elemento della lista cliccato
		document.getElementById($(this).text()).style.color = "white";
		$('#call').attr('disabled',true);
		enterRoom($(this).text());
		createNewChatGroup($(this).text());
    });
	
	$('#newMessage').attr('disabled',true);
	
    $('#ricercaus').on('keyup',function(){
        if($('#ricercaus').val() !=''){
            $('#newMessage').attr('disabled', false);
			$('#subscribe').attr('disabled', false);
        }else{
			$('#newMessage').attr('disabled',true);
			$('#subscribe').attr('disabled', true);
		}
    });


	$('#subscribe').bind('click', function() {
		var user = $('#ricercaus').val();
		if(user != Strophe.getNodeFromJid(ut))
		subscribePresence(user);
  });
  
	
	$('#newMessage').bind('click', function() {
		let utente = $('#ricercaus').val();
		if ($('#'+utente).text()=="") {
			$('<li class="contact" id='+$('#ricercaus').val()+' tabindex="1">'+$('#ricercaus').val()+'</li>').appendTo($('.contacts ul'));	
			//$('<li class="contact" id ="'+$('#ricercaus').val()+'"><div class="wrap"><span class="contact-status online"></span><img src="#" alt="" /><div class="meta"><p class="name">'+$('#ricercaus').val()+'</p><p class="preview"><span>You:</span>'+$('#ricercaus').val()+'</p></div></div></li>').appendTo('.contacts ul');
		}
		createNewChat($('#ricercaus').val())
		$('#ricercaus').val('');
		$('#newMessage').attr('disabled',true);
	});
			
	$('#btnLogout').on('click',function(){
		connection.disconnect();	
	});

	$('#call').on('click',doCall);
	
	$('#accept').on('click',function(){
		$('#accept').hide();
		$('#call').attr('disabled', false);
		videocall.createAnswer(
													{
														jsep: jsepIncoming,
														// No media provided: by default, it's sendrecv for audio and video
														//media: { data: true },	// Let's negotiate data channels as well
														success: function(jsep) {
															Janus.debug("Got SDP!");
															Janus.debug(jsep);
															var body = { "request": "accept" };
															videocall.send({"message": body, "jsep": jsep});
														},
														error: function(error) {
															Janus.error("WebRTC error:", error);
															bootbox.alert("WebRTC error... " + JSON.stringify(error));
														}
													});
	});
	
	$('#decline').on('click', function(){
		$('#accept').removeClass('hide').show();
		$('#ring').hide();
		$('#call').attr('disabled', false);
		if(spinner !== null && spinner !== undefined)
			spinner.stop();
		$('#waitingvideo').remove();
		$('#videos').hide();							
		$('#toggleaudio').attr('disabled', true);
		$('#togglevideo').attr('disabled', true);
		var hangup = { "request": "hangup" };
		videocall.send({"message": hangup});
		videocall.hangup();
		yourusername=null;
	});
	
	

	
});
