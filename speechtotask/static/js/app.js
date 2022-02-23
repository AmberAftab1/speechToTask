var gumStream;
//stream from getUserMedia()
var recorder;
//WebAudioRecorder object
var input;
//MediaStreamAudioSourceNode we'll be recording var encodingType;
//holds selected encoding for resulting audio (file)
var encodeAfterRecord = true;
// when to encode
var audioContext = new AudioContext;
//new audio context to help us record
var encodingTypeSelect = document.getElementById("encodingTypeSelect");

var blobVar;
var audioVar = new Audio("./synthesize.mp3");
var audioVar2 = new Audio("./confirm.mp3");


$("#recordButton").click(function (){
    startRecording();
});

$("#stopButton").click(function (){
    stopRecording();
});


$("#yesButton").click(function (){
    modifyChunk();
});

function sleep(miliseconds) {
   var currentTime = new Date().getTime();

   while (currentTime + miliseconds >= new Date().getTime()) {
   }
}



$("#submit-prompt").click(function (ev){
    ev.preventDefault();
    $(".buttonload").toggle();
    $("#submit-prompt").hide();
    $("#cancel-prompt").hide();
    $("#prompt").hide();
    $("#title-prompt").hide();
    var checkBox = document.getElementById("muteCheck");
    if (checkBox.checked == false){    
	audioVar2.play();
    }
	//sleep(5000);
    var blob = blobVar;
    var form = new FormData();
    form.append('audio', blob);
    //form.append('audioProcessing', True);
    const csrftoken = getCookie('csrftoken');
    var prompt = $("#prompt").val();
    var ajax_url = $("#submit-prompt").attr('data-ajax-url');
    var ajax_prompt_url = $("#submit-prompt").attr('data-ajax-prompt-url');
    //form.append('prompt', prompt);
         $.ajax({
                    url: ajax_url,
                    type: 'POST',
                    data: form,
                    dataType : "json",
                    processData: false,
                    contentType: false,
                    headers: {'X-CSRFToken': csrftoken},
                    success: function (data) {

                     var id = data.id;
	             var checkBox = document.getElementById("muteCheck");
                     if (checkBox.checked == false){
                     sleep(5000);
		     }
                     //alert(prompt);

                     $.ajax({
                    url: ajax_prompt_url,
                    type: 'POST',
                    data: {prompt: prompt, id: id},
                    dataType : "json",
                    //processData: false,
                    //contentType: false,
                    headers: {'X-CSRFToken': csrftoken},
                    success: function (data) {

                     var prompt = data.prompt;
                     //alert(prompt, "  success");
                     recordButton.disabled = false;
		     alert("Voice memo uploaded successfully");
	             //window.location.reload();
		     window.location.href = "/speechtotask/recordings";
                    },
                    error: function () {
                        //$(".buttonload").hide();
    			//$("#recordButton").toggle();
			//recordButton.disabled = false;
			//document.getElementById("display").innerHTML = 00:00:00
			//document.getElementById("recordingState").innerText = "Start Recording"
    			//$("#stopButton").toggle();
			//alert("Voice memo z " + prompt + "uploaded successfully");
                        window.location.reload();
                        //alert("Failed AJAX 2");
                    },
                    timeout: 500000
                    });

                    },
                    error: function () {
                        //alert("Failed AJAX 1");
                    },
                    timeout: 500000
                    });
});



function modifyChunk(){
        var ajax_url = $("#yesButton").attr('data-ajax-url');
        var chunkId = $("#yesButton").attr('data-chunkId');
        var id = $("#yesButton").attr('data-id');
        var lines = $("#yesButton").attr('data-lines');
        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                chunkId: chunkId,
                id: id

            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers:  {'X-CSRFToken': csrftoken},

            context: this


        })
          // Code to run if the request succeeds (is done);
          // The response is passed to the function
          .done(function( json ) {
               var chunk = json.chunk;
               var nextChunk = json.nextChunk;


                document.getElementById("transcript").innerText = document.getElementById("transcript").innerText + chunk


                // var toAdd = $(`<p id = "transcript" class="transcription"> ${chunk} </p>
                // <hr size="2" width="80%" margin-right="20px" margin-left="20px" color="#90ee90">`)
                //
                // var targetDiv = $("#chunks-to-summarize");
                // $(toAdd).appendTo(targetDiv);

                if (nextChunk === "") {
                    removeElement('task');
                    removeElement('yesButton');
                    removeElement('taskPrompt');
                    removeElement('chunkToProcess');
                    var prompt = $(`<p class = "promptQuestion"> You have reached the end of the text. Please proceed to the next task. </p>"`);

                    var targetElem = $("#taskDiv");
                    $(prompt).appendTo(targetElem);

                    document.getElementById('noButton').innerHTML = "Next task";

                } else{
                    document.getElementById("chunkToProcess").innerText = nextChunk;
                }
                

          })
          // Code to run if the request fails;
          .fail(function( xhr, status, errorThrown ) {
            // alert( "Sorry, there was a problem!" );
            console.log( "Error: " + errorThrown );
          })
          // Code to run regardless of success or failure;
          .always(function( xhr, status ) {
            // alert( "The request is complete!" );
          });
}

function seekAudio(time){
    event.preventDefault();
    var audio = document.getElementById("audioClip");
    audio.currentTime = time
    audio.play();
}


function startRecording() {
        var constraints = {
            audio: true,
            video: false
        }
	var checkBox = document.getElementById("muteCheck");
	if (checkBox.checked == false){
	audioVar.play();
	}
        document.getElementById('recordIndicator').style.fill = "#FF0000";


         $("#display").toggle();
	//var audioElement = document.createElement("audio"); 
	//audioElement.src = "../../synthesize.mp3";
	//audioElement.play();
        startTime = Date.now();
        setInterval(function printTime() {
            elapsedTime = Date.now() - startTime;
            document.getElementById("display").innerHTML = timeToString(elapsedTime);
             }, 1000);

        document.getElementById("recordingState").innerText = "Recording...";




        /* We're using the standard promise based getUserMedia() https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */
        navigator.mediaDevices.getUserMedia(constraints).then(
            function (stream) {
                // __log("getUserMedia() success, stream created, initializing WebAudioRecorder...");
                //assign to gumStream for later use
                gumStream = stream;
                /* use the stream */
                audioContext = new AudioContext();
                input = audioContext.createMediaStreamSource(stream);
                //stop the input from playing back through the speakers
                //input.connect(audioContext.destination)
                //get the encoding
                encodingType = "mp3";
                //disable the encoding selector
                recorder = new WebAudioRecorder(input, {
                    workerDir: "static/js/",
                    encoding: encodingType,
                });

                recorder.onComplete = function (recorder, blob) {

                    console.log("start sending binary data...");
                    blobVar = blob
                }
                recorder.setOptions({
                    timeLimit: 300,
                    encodeAfterRecord: encodeAfterRecord,
                    ogg: {
                        quality: 0.5
                    },
                    mp3: {
                        bitRate: 160
                    }
                });
                //start the recording process
                recorder.startRecording();
                // __log("Recording started");
            }).catch(function (err) { //enable the record button if getUSerMedia() fails
            console.log("failed");
            recordButton.disabled = false;
            stopButton.disabled = true;
        });
        //disable the record button
        // recordButton.disabled = true;
        recordButton.disabled = true;
        stopButton.disabled = false;
}

function stopRecording() {
    console.log("stopRecording() called");
    document.getElementById('recordIndicator').style.fill = "#ffffff";

    elapsedTime = 0;
    $("#display").hide();
    $("#recordButton").hide();
    $("#stopButton").hide();
    $("#results").hide();
    //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //disable the stop button
    stopButton.disabled = true;
    recordButton.disabled = true;
    //tell the recorder to finish the recording (stop recording + encode the recorded audio)

    recorder.finishRecording();

      $("#hiddenForm").toggle();
      document.getElementById("recordingState").innerText = "Upload Recording";
      // $("#recordingState").textContent = "Upload Recording:";

    // __log('Recording stopped');
}




function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(cookieValue);
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function copyContent () {
    document.getElementById("hidden-input").value =
        document.getElementById("verified-transcript").innerHTML;
    return true;
}

function removeElement(id) {
    var elem = document.getElementById(id);
    return elem.parentNode.removeChild(elem);
}


function timeToString(time) {
  let diffInHrs = time / 3600000;
  let hh = Math.floor(diffInHrs);

  let diffInMin = (diffInHrs - hh) * 60;
  let mm = Math.floor(diffInMin);

  let diffInSec = (diffInMin - mm) * 60;
  let ss = Math.floor(diffInSec);

  let formattedHH = hh.toString().padStart(2, "0");
  let formattedMM = mm.toString().padStart(2, "0");
  let formattedSS = ss.toString().padStart(2, "0");

  return `${formattedHH}:${formattedMM}:${formattedSS}`;
}

// setInterval(function printTime() {
//   let elapsedTime = Date.now() - startTime;
// }, 1000);

