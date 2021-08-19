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
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");


recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);


function startRecording() {
    var constraints = {
        audio: true,
        video: false
    }
    // document.getElementById('recordIndicator').style.fill = "#FF0000";
    console.log("Recording started....");


    /* We're using the standard promise based getUserMedia() https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia */
    navigator.mediaDevices.getUserMedia(constraints).then(
        function(stream) {
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
            // encodingTypeSelect.disabled = true;
            recorder = new WebAudioRecorder(input, {
                workerDir: "static/js/",
                encoding: encodingType,
                onEncoderLoading: function(recorder, encoding) {
                    // show "loading encoder..." display
                    // __log("Loading " + encoding + " encoder...");
                },
                onEncoderLoaded: function(recorder, encoding) {
                    // hide "loading encoder..." display
                    // __log(encoding + " encoder loaded");
                }
            });

            recorder.onComplete = function(recorder, blob) {
                debugger;
                // __log("Encoding complete");
                createDownloadLink(blob, recorder.encoding);
                var filename = new Date().toISOString();
                console.log(filename);


                // console.log("start sending binary data...");
                // var form = new FormData();
                // form.append('audio', blob);
                // console.log("blob: ", blob);
                //
                // $.ajax({
                //      url: 'http://localhost:8000/speechtotask/upload',
                //         type: 'POST',
                //         data: form,
                //         processData: false,
                //         contentType: false,
                //         success: function (data) {
                //             console.log('response' + JSON.stringify(data));
                //         },
                //         error: function () {
                //            // handle error case here
                //         }
                //     });


                var xhr = new XMLHttpRequest();
                // xhr.open("POST", 'speechtotask:upload', true);
                // xhr.setRequestHeader('Content-Type', 'application/json');
                // xhr.send(JSON.stringify({
                //     value: blob
                // // }));
                // xhr.onload = function(e) {
                //     // if (this.readyState === 4) {
                //     //     // console.log("Server returned: ", e.target.responseText);
                //     // }
                // };
                var fd = new FormData();
                fd.append("audio_data", blob, filename);
                xhr.open("POST", "upload.php", true);
                xhr.send(fd);
            }
            recorder.setOptions({
                timeLimit: 120,
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
        }).catch(function(err) { //enable the record button if getUSerMedia() fails
        recordButton.disabled = false;
        stopButton.disabled = true;
    });
    //disable the record button
    recordButton.disabled = true;
    stopButton.disabled = false;
}

function stopRecording() {
    console.log("stopRecording() called");
    document.getElementById('recordIndicator').style.fill = "#ffffff";
    //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //disable the stop button
    stopButton.disabled = true;
    recordButton.disabled = false;
    //tell the recorder to finish the recording (stop recording + encode the recorded audio)
    recorder.finishRecording();
    // __log('Recording stopped');
}

function createDownloadLink(blob) {

	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//save to disk link
	link.href = url;
	link.download = filename+encodingType; //download forces the browser to donwload the file using the  filename
	link.innerHTML = "Download";

	//add the new audio element to li
	li.appendChild(au);

	//add the filename to the li
	li.appendChild(document.createTextNode(filename+encodingType))
	//add the save to disk link to li
	li.appendChild(link);

	//remove link
   var remove = document.createElement('a');
    remove.href = "#";
    remove.innerHTML = "Delete";
    remove.addEventListener("click", function(event) {

    })
li.appendChild(document.createTextNode(" ")) //add a space in between
li.appendChild(remove) //add the upload link to li


	//add the li element to the ol
    recordingsList.appendChild(li);
}


//
// function __log(e, data) {
// 	log.innerHTML += "\n" + e + " " + (data || '');
// }


