from django.utils import timezone


# ==========================================
# LESSON STATUS
# ==========================================

def publish_lesson(lesson):
    lesson.status = "PUBLISHED"
    lesson.save()


def draft_lesson(lesson):
    lesson.status = "DRAFT"
    lesson.save()


# ==========================================
# LIVE LESSON SERVICES
# ==========================================

def schedule_live_lesson(
    lesson,
    meet_link,
    start_time,
    end_time,
):
    """
    Schedule a live lesson.
    """

    lesson.is_live = True
    lesson.meeting_link = meet_link
    lesson.live_start = start_time
    lesson.live_end = end_time
    lesson.save()

    return lesson


def cancel_live_lesson(lesson):
    """
    Cancel a scheduled live lesson.
    """

    lesson.is_live = False
    lesson.meeting_link = ""
    lesson.live_start = None
    lesson.live_end = None
    lesson.live_status = "NOT_STARTED"
    lesson.save()

    return lesson


def start_live_lesson(lesson):
    """
    Mark lesson as live.
    """

    lesson.live_status = "LIVE"
    lesson.save()

    return lesson


def end_live_lesson(lesson):
    """
    Mark lesson as finished.
    """

    lesson.live_status = "ENDED"
    lesson.save()

    return lesson


# ==========================================
# LIVE STATUS CHECKER
# ==========================================

def update_live_status(lesson):
    """
    Automatically update lesson status depending
    on the current time.
    """

    if not lesson.is_live:
        return lesson

    now = timezone.now()

    if lesson.live_start and lesson.live_end:

        if now < lesson.live_start:
            lesson.live_status = "NOT_STARTED"

        elif lesson.live_start <= now <= lesson.live_end:
            lesson.live_status = "LIVE"

        elif now > lesson.live_end:
            lesson.live_status = "ENDED"

        lesson.save()

    return lesson


# ==========================================
# RECORDING
# ==========================================

def attach_recording(lesson, recording_url):
    """
    Save the recording link after class ends.
    """

    lesson.recording_url = recording_url
    lesson.save()

    return lesson


# ==========================================
# UTILITIES
# ==========================================

def lesson_has_started(lesson):

    if not lesson.live_start:
        return False

    return timezone.now() >= lesson.live_start


def lesson_has_ended(lesson):

    if not lesson.live_end:
        return False

    return timezone.now() > lesson.live_end


def lesson_is_live(lesson):

    if not lesson.is_live:
        return False

    now = timezone.now()

    if lesson.live_start and lesson.live_end:
        return lesson.live_start <= now <= lesson.live_end

    return False