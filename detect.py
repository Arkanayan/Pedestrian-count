from imutils.object_detection import non_max_suppression
import numpy as np
import numpy
import imutils
import cv2
import subprocess as sp
import threading

import rx



def count_peoples(frame):
    """ Count number of people in the frame given """
    import cv2
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    print("Enter processing")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = imutils.resize(gray )

    (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4),
            padding=(8, 8), scale=1.05)
    
    # for (x, y, w, h) in rects:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
    print("Peoples: {}".format(len(pick)))
    return len(pick)

def count_people_observable(frame):
    """ Reactivate version of counting people
        Returns an observable that returns number of peoples
     """
    def subscribe(observer):
        num_peoples = count_peoples(frame)
        observer.on_next(num_peoples)
        observer.on_completed()
        return lambda: None
    return rx.Observable.create(subscribe)

def get_time_in_video(total_frames, frame_rate, curr_frame):
    """Calculate current time of video"""
    # return (total_frames * frame_rate) / curr_frame
    return curr_frame / frame_rate

def plot_people_count(fig, num_of_people=0, time=0):
    """Plot num of people in the plot given in fig"""
    # print("Peoples: ", num_of_people)
    fig.bar(time, num_of_people, 1/1.5)
    fig.draw()
    return True

def update_plot(frame, plt, time):
    count_peoples = count_peoples(frame)
    plot_people_count(plt, num_of_people, time)

# Specify path of the video here
cap = cv2.VideoCapture('samples/random_people_walk.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

index = 0
frameRate = cap.get(cv2.CAP_PROP_FPS)
print("Frame rate: ", frameRate)

success, image = cap.read()

### Setup parameters #####
## Number of seconds to skip
seconds = 1
fps = cap.get(cv2.CAP_PROP_FPS)
multiplier = fps * seconds

# Make plot interactive, so it can be updated while running the script
import matplotlib.pyplot as plt
plt.ion()

# Allocate threads
import multiprocessing
from threading import current_thread
from rx.concurrency import ThreadPoolScheduler

# calculate number of CPU's, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

while success:
    curr_frame = cap.get(1)
    print("frame: ", curr_frame)

    success, frame = cap.read()

    frameId = int(round(cap.get(1)))
    # print("Res: ", frameId % multiplier)
    if int(frameId % multiplier) == 0:
        curr_time = get_time_in_video(total_frames, fps, curr_frame)

        # here Rx is used to compute num of peoples on different thread and
        # Also we are passing current time in zip operator for plotting purposes
        rx.Observable.zip(count_people_observable(frame.copy()), rx.Observable.from_([curr_time]), lambda peoples, time: (peoples, time)) \
            .subscribe_on(pool_scheduler) \
            .subscribe(on_next=lambda people_and_time: (plt.pause(0.05), plot_people_count(plt, people_and_time[0], people_and_time[1])))
    
    cv2.imshow('orig', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

plt.show()
cap.release()
cv2.destroyAllWindows()

