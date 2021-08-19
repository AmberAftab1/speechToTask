from django.contrib.auth.views import LogoutView
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from . import views

app_name = 'speechtotask'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('recordings',views.recordings_list, name = 'recordings_list'),
    path('upload',views.upload, name='upload'),
    # path('modify-chunk', views.modify_chunk, name='modify_chunk'),
    # path('transcribe/<int:id>', views.transcribe_audio, name='transcribe_audio'),
    # path('summarise/<int:id>/<int:chunkId>', views.summarise_audio, name = 'summarise_audio'),
    # path('summarise-chunk/<int:id>', views.summarise_chunk, name = 'summarise_chunk'),
    # path('update-summary/<int:id>', views.update_summary, name='update_summary'),
    # path('transcribe/Mp3LameEncoder.min.js.mem', views.lame_encoder, name='lame_encoder'),
    # path('summarise/<int:id>/Mp3LameEncoder.min.js.mem', views.lame_encoder, name='lame_encoder'),
    # path('verify/<int:id>', views.verify_transcription, name = 'verify_transcription'),
    # path('Mp3LameEncoder.min.js.mem', views.lame_encoder, name='lame_encoder'),
    path('static/js/Mp3LameEncoder.min.js.mem', views.lame_encoder, name='lame_encoder'),
    path('static/js/WebAudioRecorder.min.js', views.web_recorder, name='web_recorder'),
    path('static/js/WebAudioRecorderMp3.min.js', views.web_recorder_mp3, name='web_recorder_mp3'),
    re_path(r'^audio/blob*', views.get_blob, name="get_blob"),
]