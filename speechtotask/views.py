from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
import time
import boto3
import json
import requests
from django.core.files import File as DjangoFile
import os
from .models import Recording, Summary, SpeechtoTaskUser
import pandas as pd
import smtplib
import ssl
from pyquery import PyQuery
from django.contrib import messages
from shutil import copyfile
from random import seed
from random import randint

# Create your views here.
@login_required()
def home(request):
    if request.user.is_authenticated: 
        try:
            results = SpeechtoTaskUser.objects.get(user_id = request.user.id).summary_url            
            return render(request, "speechtotask/home/home.html", {"results": results})
        except:       
            return render(request, "speechtotask/home/home.html")
    else:
        return render(request, "speechtotask/index.html")
    # return render(request, "speechtotask/home/home.html")


#
# def google_login(request):
#     return render(request, "speechtotask/index.html")


@login_required()
def summary(request):
    if request.user.is_authenticated:
        return render(request, "speechtotask/summary/summary.html")
    else:
        return render(request, "speechtotask/index.html")


@login_required()
def recordings_list(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            recordings = Recording.objects.all().order_by('-date_posted')
        else:
            recordings = Recording.objects.filter(userObject = request.user).order_by('-date_posted')
        return render(request, "speechtotask/recordings/list.html", {"recordingsList": recordings})
    else:
        return render(request, "speechtotask/index.html")

@login_required()
def lame_encoder(request, id=0):
    filename = "speechtotask/static/js/Mp3LameEncoder.min.js.mem"
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="application/javascript")

@login_required()
def web_recorder(request):
    filename = "speechtotask/static/js/WebAudioRecorder.min.js"
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="application/javascript")

@login_required()
def web_recorder_mp3(request):
    filename = "speechtotask/static/js/WebAudioRecorderMp3.min.js"
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="application/javascript")


@login_required()
def delete_audio(request,id):
    try:
        recordingObject = Recording.objects.get(pk=id).delete()
    except Recording.DoesNotExist:
        return redirect('speechtotask:home')
    
    return redirect('speechtotask:recordings_list')

#
# def transcribe_audio(request, id):
#     audio_id = request.POST.get('audio_id')
#     try:
#         recordingObject = Recording.objects.get(pk=id)
#     except Recording.DoesNotExist:
#         return redirect('speechtotask:home')
#
#     if recordingObject.transcription_url:  # retrieves transcription if it already exists
#
#         # file = open(str(recordingObject.transcription), 'r')
#         # data = file.readlines()
#         # transcription = ""
#         # for elem in data:
#         #     transcription += elem
#
#         with open(str(recordingObject.transcription_url), encoding='utf-8') as data_file:
#             transcription_data = json.loads(data_file.read())
#
#         return render(request, "speechtotask/transcription/transcription.html",
#                       {"transcription": transcription_data, "recording": recordingObject})
#
#     transcribe = boto3.client('transcribe')
#     filename = str(audio_id).split("/")[-1]
#     now = datetime.now()
#     dt_string = now.strftime("%Y-%m-%d-%H-%M-%S-transcribe-job")
#
#     job_uri = "s3://speechtotask/" + filename + ".mp3"
#     transcribe.start_transcription_job(
#         TranscriptionJobName=dt_string,
#         Media={'MediaFileUri': job_uri},
#         MediaFormat='mp3',
#         LanguageCode='en-IN'
#     )
#     while True:
#         status = transcribe.get_transcription_job(TranscriptionJobName=dt_string)
#         if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
#             break
#         print("Not ready yet...")
#         time.sleep(5)
#     print("Job complete!")
#     data_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
#
#     ssl._create_default_https_context = ssl._create_unverified_context
#
#     data = pd.read_json(data_uri)
#
#     metaData = data['results']['items']
#
#     request_url = requests.get(data_uri).text
#     json_file = json.loads(request_url)
#     transcription = json_file['results']['transcripts'][0]['transcript']
#
#     file = open(filename + ".txt", 'w')
#     file.write(transcription)
#     file.close()
#     file = DjangoFile(open(filename + ".txt", mode='rb'), name=filename + ".txt")
#
#     transcription_data = []
#     startTime = metaData[0]['start_time']
#     stringChunk = ""
#     endTime = metaData[0]['end_time']
#     count = 0
#     for dict in metaData:
#         if dict['type'] == 'punctuation' and dict['alternatives'][0]['content'] == '.':
#             stringChunk += dict['alternatives'][0]['content'] + " "
#             dataChunk = {"id": count, "startTime": startTime, "endTime": endTime, "string": stringChunk}
#             count += 1
#             transcription_data.append(dataChunk)
#             stringChunk = ""
#             startTime = endTime
#         else:
#             stringChunk += dict['alternatives'][0]['content'] + " "
#             if dict['type'] != 'punctuation':
#                 endTime = dict['end_time']
#     dataChunk = {"id": count, "startTime": startTime, "endTime": endTime, "string": stringChunk}
#     transcription_data.append(dataChunk)
#
#     with open(filename + "_data.txt", 'w') as fout:
#         json.dump(transcription_data, fout)
#
#     file_data = DjangoFile(open(filename + "_data.txt", mode='rb'), name=filename + "_data.txt")
#
#     recordingObject.transcription = file
#     recordingObject.transcription_url = file_data
#     recordingObject.save()
#
#     file_path = filename + '.txt'
#     os.remove(file_path)
#     file_path = filename + "_data.txt"
#     os.remove(file_path)
#
#     return render(request, "speechtotask/transcription/transcription.html",
#                   {"transcription": transcription_data, "recording": recordingObject})


# def verify_transcription(request, id):
#     text = request.POST.get('entire-transcript')
#     pq = PyQuery(text)
#     l_id = [item.text() for item in pq.items('p#id')]
#     l_timings = [item.text() for item in pq.items('p#timings')]
#     l_transcript = [item.text() for item in pq.items('p#transcript')]
#     transcript = pq('p#transcript').text()
#
#     combined = []
#     for i in range(len(l_id)):
#         combined.append((l_id[i], l_timings[i], l_transcript[i]))
#
#     result = []
#     for item in combined:
#         time = item[1].split("-")
#         startTime = time[0].strip(' s')
#         endTime = time[1].strip(' s')
#         d = {"id": item[0], "startTime": startTime, "endTime": endTime, "string": item[2]}
#         result.append(d)
#
#     recording = Recording.objects.get(pk=id)
#     filename = str(recording.transcription_url)
#
#     with open(filename, 'w') as f:
#         json.dump(result, f)
#
#     filename = str(recording.transcription)
#     with open(filename, 'w') as f:
#         f.write(transcript)
#
#     return redirect('speechtotask:transcribe_audio', id=id)
#
#
# def summarise_audio(request, id, chunkId):
#     try:
#         recordingObject = Recording.objects.get(pk=id)
#     except Recording.DoesNotExist:
#         return redirect('speechtotask:home')
#
#     with open(str(recordingObject.transcription_url), encoding='utf-8') as data_file:
#         transcription_data = json.loads(data_file.read())
#
#     nextChunk = ""
#     lines = ""
#
#     for data in transcription_data:
#         if recordingObject.startId <= int(data['id']) <= chunkId:
#             lines += data['string']
#         elif int(data['id']) == chunkId + 1:
#             nextChunk = data['string']
#             break
#
#     summaries = Summary.objects.filter(recordingId=recordingObject)
#
#     return render(request, "speechtotask/summary/summarization.html",
#                   {"summaries": summaries, "lines": lines, "chunkId": recordingObject.chunkId,
#                    "startId": recordingObject.startId,
#                    "id": recordingObject.id,
#                    "nextChunk": nextChunk})
#
#
# def summarise_chunk(request, id):
#     try:
#         recordingObject = Recording.objects.get(pk=id)
#     except Recording.DoesNotExist:
#         return redirect('speechtotask:home')
#
#     startId = recordingObject.startId
#     chunkId = recordingObject.chunkId
#
#     with open(str(recordingObject.transcription_url), encoding='utf-8') as data_file:
#         transcription_data = json.loads(data_file.read())
#
#     lines = ""
#     for data in transcription_data:
#         if startId <= int(data['id']) <= chunkId:
#             lines+=data['string']
#         elif int(data['id']) > chunkId:
#             break
#
#     return render(request, "speechtotask/summary/chunkSummarization.html",
#                   {"lines": lines, "id": id})
#
#
# def update_summary(request, id):
#     try:
#         recordingObject = Recording.objects.get(pk=id)
#     except Recording.DoesNotExist:
#         return redirect('speechtotask:home')
#
#     startId = recordingObject.startId
#     chunkId = recordingObject.chunkId
#
#     userSummary = request.POST.get('chunkSummary')
#
#     summary = Summary(
#         recordingId=recordingObject,
#         startId=startId,
#         chunkId=chunkId,
#         summaryChunk=userSummary,
#     )
#     summary.save()
#     recordingObject.startId = chunkId + 1
#     recordingObject.chunkId = chunkId + 1
#     recordingObject.save()
#     chunkId = recordingObject.startId
#     if not recordingObject.processed:
#         return redirect('speechtotask:summarise_audio', id=id, chunkId=chunkId)
#     else:
#         return redirect('speechtotask:recordings_list')
#
#
# def modify_chunk(request):
#     is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
#     if is_ajax and request.method == 'POST':
#         chunkId = request.POST.get('chunkId')
#         id = request.POST.get('id')
#
#         try:
#             recording = Recording.objects.get(pk=id)
#             recording.chunkId = recording.chunkId + 1
#             recording.save()
#
#             with open(str(recording.transcription_url), encoding='utf-8') as data_file:
#                 transcription_data = json.loads(data_file.read())
#
#             chunkToAdd = ""
#             nextChunk = ""
#             found = False
#             for data in transcription_data:
#                 if int(data['id']) == recording.chunkId:
#                     chunkToAdd = data['string']
#                 elif int(data['id']) == recording.chunkId + 1:
#                     nextChunk = data['string']
#                     found = True
#                     break
#             if found == False:
#                 recording.processed = True
#                 recording.save()
#                 return JsonResponse({'success': 'success', 'chunk': chunkToAdd, 'nextChunk': ""}, status=200)
#
#             return JsonResponse({'success': 'success', 'chunk': chunkToAdd, 'nextChunk': nextChunk}, status=200)
#         except Recording.DoesNotExist:
#             return JsonResponse({'error': 'No recording found with that ID.'}, status=200)
#
#     else:
#         return JsonResponse({'error': 'Invalid Ajax  request.'}, status=400)

@login_required()
@csrf_exempt
def upload(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    # if is_ajax and request.method == 'POST':
    if request.method == 'POST':
        #if request.POST.get("audioProcessing")==True:
            #audio_data = request.POST.get('audio')
        try:
            audio_data = request.FILES['audio']
        except MultiValueDictKeyError:
            audio_data = False
            #audio_data = request.FILES['audio']
        #prompt = request.POST.get("prompt")
        now = datetime.now()
        random_num = now.strftime("%m-%d-%Y-%H-%M-%S")
        audio_data.name = audio_data.name +  "-" + random_num +"-" +  request.user.username 
        record = Recording(
            filename=random_num,
            prompt=request.user.username + "-" + random_num,
            userObject= request.user,
            voice_record=audio_data,
        )
        record.save()
        #f = open('mail-google.txt')
        #email_info = json.load(f)
        EMAIL_ADDRESS = 'amber19@vt.edu'
        EMAIL_PASSWORD = 'khcvxylvaaowzzjl'
        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            subject = 'ALERT! Voice memo uploaded!'
            body = 'User ' + request.user.username + ' has uploaded a new voice memo!'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
        os.system("cp "+str(record.voice_record)+" /audiodata/")

        # filename = str(record.voice_record).split("/")[-1]
        # s3 = boto3.resource('s3')
        # s3.meta.client.upload_file(str(record.voice_record), 'speechtotask', filename + ".mp3")
        # print("Uploaded FILE!!!!!")
        return JsonResponse({'success': 'success', 'id': record.id}, status=200)
    return redirect('speechtotask:home')

@login_required()
@csrf_exempt
def prompt(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    # if is_ajax and request.method == 'POST':
    if request.method == 'POST':
        prompt = request.POST.get("prompt")
        id = request.POST.get("id")
        #print("Prompt: ", prompt, " ID: ", id)
        recording = Recording.objects.get(pk=id)
        if prompt != "":
            recording.prompt = prompt
            recording.save()
        return JsonResponse({'success': 'success', 'prompt': recording.prompt}, status=200)
    return redirect('speechtotask:home')


@login_required()
@csrf_exempt
def synthesize(request):
    filename = "/app/speechtotask/hi.mp3"
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="audio/mp3")


@login_required()
@csrf_exempt
def confirm(request):
    filename = "/app/speechtotask/thanks.mp3"
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="audio/mp3")


@login_required()
@csrf_exempt
def get_blob(request):
    filename = request.get_full_path()[1:]
    filename = "/audiodata/"+request.get_full_path().split("/")[-1]
    data = open(filename, "rb").read()
    return HttpResponse(data, content_type="audio/mp3")
