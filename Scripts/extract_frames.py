import cv2  # still used to save images out
import os
import numpy as np
from decord import VideoReader
from decord import cpu, gpu
import sys


def extract_frames(video_path, frames_dir, overwrite=False, start=-1, end=-1, every=1):
    """
    Extract frames from a video using decord's VideoReader
    :param video_path: path of the video
    :param frames_dir: the directory to save the frames
    :param overwrite: to overwrite frames that already exist?
    :param start: start frame
    :param end: end frame
    :param every: frame spacing
    :return: count of images saved
    """

    # make the paths OS (Windows) compatible
    video_path = os.path.normpath(video_path)
    # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)

    # get the video path and filename from the path
    #video_dir, video_filename = os.path.split(video_path)

    assert os.path.exists(video_path)  # assert the video file exists

    # load the VideoReader
    # can set to cpu or gpu .. ctx=gpu(0)
    vr = VideoReader(video_path, ctx=cpu(0))

    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = len(vr)

    frames_list = list(range(start, end, every))
    saved_count = 0

    # this is faster for every > 25 frames and can fit in memory
    if every > 25 and len(frames_list) < 1000:
        frames = vr.get_batch(frames_list).asnumpy()

        # lets loop through the frames until the end
        for index, frame in zip(frames_list, frames):
            save_path = os.path.join(frames_dir, "{:010d}.jpg".format(
                index))  # create the save path
            # if it doesn't exist or we want to overwrite anyways
            if not os.path.exists(save_path) or overwrite:
                # save the extracted image
                cv2.imwrite(save_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                saved_count += 1  # increment our counter by one

    else:  # this is faster for every <25 and consumes small memory
        for index in range(start, end):  # lets loop through the frames until the end
            frame = vr[index]  # read an image from the capture

            if index % every == 0:  # if this is a frame we want to write out based on the 'every' argument
                save_path = os.path.join(frames_dir, "{:010d}.jpg".format(
                    index))  # create the save path
                # if it doesn't exist or we want to overwrite anyways
                if not os.path.exists(save_path) or overwrite:
                    # save the extracted image
                    cv2.imwrite(save_path, cv2.cvtColor(
                        frame.asnumpy(), cv2.COLOR_RGB2BGR))
                    saved_count += 1  # increment our counter by one

    return saved_count  # and return the count of the images we saved


def video_to_frames(video_path, frames_dir, overwrite=False, every=1):
    """
    Extracts the frames from a video
    :param video_path: path to the video
    :param frames_dir: directory to save the frames
    :param overwrite: overwrite frames if they exist?
    :param every: extract every this many frames
    :return: path to the directory where the frames were saved, or None if fails
    """

    # make the paths OS (Windows) compatible
    video_path = os.path.normpath(video_path)
    # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)

    # get the video path and filename from the path
    video_dir, video_filename = os.path.split(video_path)

    # make directory to save frames, its a sub dir in the frames_dir with the video name
    os.makedirs(os.path.join(frames_dir), exist_ok=True)

    print("Extracting frames from {}".format(video_filename))

    # let's now extract the frames
    extract_frames(video_path, frames_dir, every=every)

    # when done return the directory containing the frames
    return frames_dir


if __name__ == '__main__':
    # test it
    video_to_frames(video_path=sys.argv[1],
                    frames_dir=str(sys.argv[1]).split(".")[0], overwrite=False, every=5)
