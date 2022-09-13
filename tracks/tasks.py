from celery import shared_task
from .models import Track
from .utils import generate_waveform, parse_metadata, process_track


@shared_task
def discover_unprocessed_tracks():
    tracks = Track.objects.filter(celery_upload_status=0).order_by('created')[:20]  # 20 tracks per minute

    # set status 'processing' before actual processing
    # for track in tracks:
    #     track.celery_upload_status = 1
    #     track.save()
    #
    # for track in tracks:
    #     process_track(track)
