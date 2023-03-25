from moviepy.editor import *
import moviepy
import random
import os
<<<<<<< HEAD
import utils.speak
#from utils.Scalegif import scale_vid
=======
from utils.Scalegif import scale_vid
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def GetDaySuffix(day):
    if day == 1 or day == 21 or day == 31:
        return "st"
    elif day == 2 or day == 22:
        return "nd"
    elif day == 3 or day == 23:
        return "rd"
    else:
        return "th"

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
music_path = os.path.join(dir_path, "Music/")

def add_return_comment(comment):
    need_return = 30
    new_comment = ""
    return_added = 0
    return_added += comment.count('\n')
    for i, letter in enumerate(comment):
        if i > need_return and letter == " ":
            letter = "\n"
            need_return += 30
            return_added += 1
        new_comment += letter
    return new_comment, return_added
        

class CreateMovie():

    @classmethod
    def CreateMP4(cls, post_data):

        clips = []
        for post in post_data:
            print(post['image_path'])
            #if "gif" not in post['image_path']:
             #   clip = ImageSequenceClip([post['image_path']], durations=[12])
              #  clips.append(clip)
            #else:
            clip = VideoFileClip(post['image_path'])
            #clip_lengthener = [clip] * 60
            #clip = concatenate_videoclips(clip_lengthener)
            #clip = clip.subclip(0,12)
            clips.append(clip)
        
        # After we have out clip.
        clip:VideoFileClip= clips[0]
        duration = clip.duration
<<<<<<< HEAD
        maxDur = 59
        if duration > maxDur:
            clip = clip.subclip(0,maxDur)
            duration = maxDur

        clip2 = clip.subclip(0,duration-3)
        clip2 = clip2.set_duration(duration-3)

        clip1 = clip.subclip(duration-3,duration)
        clip1 = clip1.set_duration(3)

        clip = concatenate_videoclips([clip1,clip2])
        clip = clip.set_duration(duration)

        width, height = clip.size
        #audio = clip.audio
        # voice:int=1
        # speakClip:AudioFileClip = utils.speak.audioClip(post['Best_comment'],voice)
        # speakClip = speakClip.set_start(3)

=======
        maxDur = 60
        if duration > maxDur:
            clip = clip.subclip(0,maxDur)
            duration = maxDur

        clip2 = clip.subclip(0,duration-3)
        clip2 = clip2.set_duration(duration-3)

        clip1 = clip.subclip(duration-3,duration)
        clip1 = clip1.set_duration(3)

        clip = concatenate_videoclips([clip1,clip2])
        clip = clip.set_duration(duration)
        audio = clip.audio
        
        # clip = concatenate_videoclips(clips)

        # Hack to fix getting extra frame errors??
        #clip = clip.subclip(0,60)

>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
        # colors = ['yellow', 'LightGreen', 'LightSkyBlue', 'LightPink4', 'SkyBlue2', 'MintCream','LimeGreen', 'WhiteSmoke', 'HotPink4']
        # colors = colors + ['PeachPuff3', 'OrangeRed3', 'silver']
        # random.shuffle(colors)
        # text_clips = []
<<<<<<< HEAD

        # #for i, post in enumerate(post_data):
        # return_comment, return_count = add_return_comment(post['Best_comment'])
        # txt = TextClip(return_comment, font='Courier',
        #             fontsize=28, color=colors.pop(), bg_color='black')
        
        # txtWidth, txtHeight = txt.size
        # txt = txt.on_color(col_opacity=.3)
        # txt = txt.set_position(int(width/2)-int(txtWidth/2),int(height*.8))
        # txt = txt.set_start((0, 3 + 12)) # (min, s)
        # txt = txt.set_duration(7)
        # txt = txt.crossfadein(0.5)
        # txt = txt.crossfadeout(0.5)
        # text_clips.append(txt)
            # return_comment, _ = add_return_comment(post['best_reply'])
            # txt = TextClip(return_comment, font='Courier',
            # fontsize=38, color=colors.pop(), bg_color='black')
            # txt = txt.on_color(col_opacity=.3)
            # txt = txt.set_position((15,585 + (return_count * 50)))
            # txt = txt.set_start((0, 5 + (i * 12))) # (min, s)
            # txt = txt.set_duration(7)
            # txt = txt.crossfadein(0.5)
            # txt = txt.crossfadeout(0.5)
            # text_clips.append(txt)

                
        #     notification_sounds = []
        #     notification = AudioFileClip(os.path.join(music_path, f"notification.mp3"))
        #     notification = notification.set_start((0, 3 + (i * 12)))
        #     notification_sounds.append(notification)
        #     notification = AudioFileClip(os.path.join(music_path, f"notification.mp3"))
        #     notification = notification.set_start((0, 5 + (i * 12)))
        #     notification_sounds.append(notification)
        
        # music_file = os.path.join(music_path, f"music{random.randint(0,4)}.mp3")
        # music = AudioFileClip(music_file)
        # music = music.set_start((0,0))
        # music = music.volumex(.1)
        # music = music.set_duration(59)

        #new_audioclip = CompositeAudioClip([speakClip])
        #clip.write_videofile(f"video_clips.mp4", fps = 24)

        #clip = VideoFileClip("video_clips.mp4",audio=True) #audio=false
        
=======
        # notification_sounds = []
        # for i, post in enumerate(post_data):
        #     return_comment, return_count = add_return_comment(post['Best_comment'])
        #     txt = TextClip(return_comment, font='Courier',
        #                 fontsize=38, color=colors.pop(), bg_color='black')
        #     txt = txt.on_color(col_opacity=.3)
        #     txt = txt.set_position((5,500))
        #     txt = txt.set_start((0, 3 + (i * 12))) # (min, s)
        #     txt = txt.set_duration(7)
        #     txt = txt.crossfadein(0.5)
        #     txt = txt.crossfadeout(0.5)
        #     text_clips.append(txt)
        #     return_comment, _ = add_return_comment(post['best_reply'])
        #     txt = TextClip(return_comment, font='Courier',
        #     fontsize=38, color=colors.pop(), bg_color='black')
        #     txt = txt.on_color(col_opacity=.3)
        #     txt = txt.set_position((15,585 + (return_count * 50)))
        #     txt = txt.set_start((0, 5 + (i * 12))) # (min, s)
        #     txt = txt.set_duration(7)
        #     txt = txt.crossfadein(0.5)
        #     txt = txt.crossfadeout(0.5)
        #     text_clips.append(txt)

        #     notification = AudioFileClip(os.path.join(music_path, f"notification.mp3"))
        #     notification = notification.set_start((0, 3 + (i * 12)))
        #     notification_sounds.append(notification)
        #     notification = AudioFileClip(os.path.join(music_path, f"notification.mp3"))
        #     notification = notification.set_start((0, 5 + (i * 12)))
        #     notification_sounds.append(notification)
        
        #music_file = os.path.join(music_path, f"music{random.randint(0,4)}.mp3")
        #music = AudioFileClip(music_file)
        #music = music.set_start((0,0))
        #music = music.volumex(.4)
        #music = music.set_duration(59)

        #xnew_audioclip = CompositeAudioClip([music]+notification_sounds)
        #clip.write_videofile(f"video_clips.mp4", fps = 24)

        #clip = VideoFileClip("video_clips.mp4",audio=True) #audio=false
        #clip = CompositeVideoClip([clip] + text_clips)

        width, height = clip.size
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
        ratio = width/height
        if ratio > 1:
            print("Resizing video")
            bg = moviepy.video.VideoClip.ImageClip("img\\black_bg_1080x1920.png")
            clip = CompositeVideoClip([bg,clip.set_duration(duration).set_position("center")])
<<<<<<< HEAD
        #clip = CompositeVideoClip([clip] + text_clips)
        clip = clip.set_duration(duration)
        #clip.set_audio(audio)
        #clip.audio = new_audioclip
        clip.write_videofile("video.mp4", fps = 24,codec='libx264',threads=2,preset='ultrafast')
=======

        clip = clip.set_duration(duration)
        clip.set_audio(audio)
        # clip.audio = new_audioclip
        clip.write_videofile("video.mp4")#, fps = 24,codec='libx264',threads=2,preset='ultrafast')
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

        
        if os.path.exists(os.path.join(dir_path, "video_clips.mp4")):
            os.remove(os.path.join(dir_path, "video_clips.mp4"))
        else:
            print(os.path.join(dir_path, "video_clips.mp4"))

if __name__ == '__main__':
    print(TextClip.list('color'))