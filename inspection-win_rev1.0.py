from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import time
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import cv2
from pathlib import Path
import shutil
import numpy as np

root = Tk() # root 메인 창
root.title("원시 데이터 이미지 검수 및 파일명 변경 저장")
root.geometry('1480x770+20+20') 
root.resizable(False, False) 

current_path = os.getcwd()

def add_file():
    files = filedialog.askopenfilenames(title = '이미지 파일을 선택하세요.', \
        filetypes = (('JPG 파일', '*.jpg'), ('모든 파일', '*.*')), \
        initialdir = current_path)

    for file in files:
        list_file.insert(END, file)

    list_file.selection_set(0)

    preview_image(list_file.get(0))

def del_file():
    # sel_files = sorted(list_file.curselection(), reverse = True)
    if list_file.get(0) == '':
        msgbox.showwarning('경고', '이미지 파일이 추가되지 않았습니다.')
    else:
        for file in reversed(list_file.curselection()):
            list_file.delete(file)

def preview_image(path):
    img_width = 780
    img_height = 500

    image = Image.open(path)
    width, height = image.size[0], image.size[1]
    img_info(path, width, height)

    if width >= height:
        pre_width, pre_height = img_width, int(height * img_width / width)
    else:
        pre_width, pre_height = int(width * img_height / height), img_height

    resized_img = image.resize((pre_width, pre_height))
   
    photo = ImageTk.PhotoImage(resized_img)
    photo_frame.configure(image = photo)
    photo_frame.image_names = photo

def img_view():
    img_width = 600
    img_height = 900

    sel_path = list_file.curselection()
    path = list_file.get(sel_path)
    img_name = path.strip().split('/')[-1]
    src = cv2.imread(path)
    width, height, channel = src.shape

    if width >= height:
        pre_width, pre_height = img_width, int(height * img_width / width)
    else:
        pre_width, pre_height = int(width * img_height / height), img_height

    dst = cv2.resize(src, dsize = (pre_height, pre_width), interpolation = cv2.INTER_AREA)
    x1, y1 = 0, int(pre_height / 3)
    x2, y2 = pre_width, int(pre_height / 3)
    x3, y3 = 0, int(pre_height * 2 / 3)
    x4, y4 = pre_width, int(pre_height * 2 / 3)
    x5, y5 = int(pre_width / 3), 0
    x6, y6 = int(pre_width / 3), pre_height
    x7, y7 = int(pre_width * 2 / 3), 0
    x8, y8 = int(pre_width * 2/ 3), pre_height
    # np.zeros(dst.shape, dtype = np.uint8)
    cv2.line(dst, (y1, x1), (y2, x2), (255, 255, 255), 1)
    cv2.line(dst, (y3, x3), (y4, x4), (255, 255, 255), 1)
    cv2.line(dst, (y5, x5), (y6, x6), (255, 255, 255), 1)
    cv2.line(dst, (y7, x7), (y8, x8), (255, 255, 255), 1)

    # photo = cv2.add(dst, dst5)

    cv2.imshow('{}'.format(img_name), dst)
    cv2.waitKey()
    cv2.destroyWindow('{}'.format(img_name))

def empty_image():
    photo = PhotoImage()
    photo_frame.configure(image = photo)
    photo_frame.image_names = photo

def get_exif(path):
    ret = {}
    i = Image.open(path)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def img_info(path, width, height):
    img_width.config(text = '현재 이미지 가로 : {}'.format(width))
    img_height.config(text = '현재 이미지 세로 : {}'.format(height))

def change_img(event):
    change_path = list_file.curselection()

    preview_image(list_file.get(change_path))

count = 0

def img_fairing():
    img_qy = int(fair_combo.get()[0])
    global count

    if img_qy <= list_file.size():
        if count < img_qy:
            if count ==0:
                for i in range(1, 5):
                    list_file.selection_clear(i)
            path = list_file.get(count)
            preview_image(path)
            list_file.selection_clear(count -1)
            list_file.selection_set(count)
            count += 1
        else:
            count = 0

    else:
        if list_file.get(0) == '':
            msgbox.showwarning('경고', '이미지 파일이 추가되지 않았습니다.')
        else:
            msgbox.showwarning('경고', '등록된 이미지 파일이 페어링 대상 이미지 장수와 맞지 않습니다.')

def next_img():
    next_path = list_file.curselection()[0] + 1

    path = list_file.get(next_path)
    preview_image(path)

    list_file.selection_clear(next_path - 1)
    list_file.selection_set(next_path)

def pre_img():
    pre_path = list_file.curselection()[0] - 1

    path = list_file.get(pre_path)
    preview_image(path)

    list_file.selection_clear(pre_path + 1)
    list_file.selection_set(pre_path)

ok_flag = 0

def chk_list():
    chk_var = [chkvar1, chkvar2, chkvar3, chkvar4, chkvar5, chkvar6, chkvar7, chkvar8, chkvar9, chkvar10, \
               chkvar11, chkvar12, chkvar13, chkvar14, chkvar15]
    chk_stat = []
    global ok_flag

    for i in chk_var:
        if i.get() == 1:
            chk_stat.append(chk_var.index(i) + 1)
    
    if len(chk_stat) > 0:
        if list_file.get(0) == '':
            msgbox.showwarning('경고', '이미지 파일이 추가되지 않았습니다.')
        else:
            ng_log(chk_stat)
            ng_ok_delete()
            chkbox_clear()
            msgbox.showwarning('경고', '이미지 검수 결과 NG 발생하여 리스트에서 삭제합니다.\n해당 이미지 세트는 재촬영 후 다시 진행해 주세요.')
    else:
        if list_file.get(0) == '':
            msgbox.showwarning('경고', '이미지 파일이 추가되지 않았습니다.')
        else:
            ok_log()
            ok_flag = 1
            msgbox.showinfo('알림', '검수가 완료되었습니다. \n해당 이미지 세트를 아래에서 저장해 주세요.')

def ng_ok_delete():
    img_qy = int(fair_combo.get()[0])
    if img_qy > list_file.size():
        msgbox.showwarning('경고', '남아있는 이미지 파일 수가 페어링 이미지 수 보다 작습니다.')
    else:
        for i in range(img_qy - 1, -1,  -1):
            list_file.delete(i)
    
        if list_file.get(0) != '':
            list_file.selection_set(0)
            preview_image(list_file.get(0))
        else:
            empty_image()

def chkbox_clear():
    chk_var = [chkvar1, chkvar2, chkvar3, chkvar4, chkvar5, chkvar6, chkvar7, chkvar8, chkvar9, chkvar10, \
               chkvar11, chkvar12, chkvar13, chkvar14, chkvar15]

    for i in chk_var:
        i.set(0)
        
def ng_log(chk_list):
    img_qy = int(fair_combo.get()[0])
    cur_time = time.localtime()
    cur_date = time.strftime('%y%m%d', cur_time)

    cur_path = Path(list_file.get(0)).parent.absolute()

    if not os.path.isfile('{}/ng_{}.log'.format(cur_path, cur_date)):
        file = open('{}/ng_{}.log'.format(cur_path, cur_date), 'w')
        file.writelines('1|재촬영 이미지 : {}|재촬영 사유 : {}\n'.format([list_file.get(i) for i in range(img_qy)], chk_list))
        file.close()
    else:
        file = open('{}/ng_{}.log'.format(cur_path, cur_date), 'r')
        file_line = len(file.readlines()) + 1
        file.close()
        file = open('{}/ng_{}.log'.format(cur_path, cur_date), 'at')
        file.writelines('{}|재촬영 이미지 : {}|재촬영 사유 : {}\n'.format(file_line, [list_file.get(i) for i in range(img_qy)], chk_list))
        file.close()

def ok_log():
    img_qy = int(fair_combo.get()[0])
    cur_time = time.localtime()
    cur_date = time.strftime('%y%m%d', cur_time)

    cur_path = Path(list_file.get(0)).parent.absolute()

    if not os.path.isfile('{}/ok_{}.log'.format(cur_path, cur_date)):
        file = open('{}/ok_{}.log'.format(cur_path, cur_date), 'w')
        file.writelines('1|검수 통과 이미지 : {}\n'.format([list_file.get(i) for i in range(img_qy)]))
        file.close()
    else:
        file = open('{}/ok_{}.log'.format(cur_path, cur_date), 'r')
        file_line = len(file.readlines()) + 1
        file.close()
        file = open('{}/ok_{}.log'.format(cur_path, cur_date), 'at')
        file.writelines('{}|검수 통과 이미지 : {}\n'.format(file_line, [list_file.get(i) for i in range(img_qy)]))
        file.close()

def make_direction():
    direction_values = ['01', '02', '03', '04']
    direction_no3.configure(value = direction_values)

def clear_direction():
    direction_values_reset = ['']
    direction_no3.configure(value = direction_values_reset)

def make_occluded():
    occluded_values = ['None', 'SemiTransparent', 'WireDense', 'WireMedium', 'WireLoose']
    occluded_no3.configure(value = occluded_values)

def clear_occluded():
    occluded_values_reset = ['']
    occluded_no3.configure(value = occluded_values_reset)

direc = 0
def save():
    img_qy = int(fair_combo.get()[0])
    cur_path = Path(list_file.get(0)).parent.absolute()
    dir_list = ['01', '02', '03', '04']
    occluded_list = ['None', 'SemiTransparent', 'WireDense', 'WireMedium', 'WireLoose']
    global direc, ok_flag

    if list_file.get(0) == '':
        msgbox.showwarning('경고', '저장할 이미지가 없습니다.')
    elif worker_id2.get() == '':
        msgbox.showwarning('경고', '촬영자 ID가 선택되지 않았습니다.')
    elif class_name2.get() == '':
        msgbox.showwarning('경고', 'Class 명이 선택되지 않았습니다.')
    elif class_name4.get() == '':
        msgbox.showwarning('경고', '객체 ID가 선택되지 않았습니다.')

    if direction_no2.get()  == 2 and direction_no3.get()  == '':
        msgbox.showwarning('경고', '방향 No. 수동 입력이 선택되어 방향 No.를 선택해야 합니다.')
    elif direction_no2.get()  == 2 and direction_no3.get() != '':
        sel_dir = direction_no3.get()
    else:
        sel_dir = list_file.size() / img_qy

    if occluded_no2.get()  == 2 and occluded_no3.get()  == '':
        msgbox.showwarning('경고', '가림막명 수동 입력이 선택되어 가림막을 선택해야 합니다.')
    elif occluded_no2.get()  == 2 and occluded_no3.get() != '':
        sel_occlueded = occluded_no3.get()
    else:
        sel_occlueded = 5
    class_name = class_name2.get()
    insta_id = class_name4.get()
    if list_file.get(0) != '' and worker_id2.get() != '':
        cur_path = Path(list_file.get(0)).parent.absolute()
        img_files = os.listdir(cur_path)

        if save_method.get() == 1 and ok_flag == 1:
            if direction_no2.get()  == 1 and occluded_no2.get()  == 1:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_list[i])
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 1 and occluded_no2.get()  == 2:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_no3.get())
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 1:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_list[i])
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 2:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_no3.get())
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
        elif save_method.get() == 2 and ok_flag == 1:
            if direction_no2.get()  == 1 and occluded_no2.get()  == 1:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_list[i])
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        shutil.copyfile(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 1 and occluded_no2.get()  == 2:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_no3.get())
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        shutil.copyfile(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 1:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_list[i])
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    shutil.copyfile(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 2:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_no3.get())
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    shutil.copyfile(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
        elif save_method.get() == 3 :
            if direction_no2.get()  == 1 and occluded_no2.get()  == 1:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_list[i])
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 1 and occluded_no2.get()  == 2:
                if direc < sel_dir:
                    for i in range(img_qy):
                        save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, dir_list[direc], occluded_no3.get())
                        if save_name in img_files:
                            msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                            direc -= 1
                            break
                        os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                    ng_ok_delete()
                    ok_flag = 0
                    direc += 1
                else:
                    direc = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 1:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_list[i])
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
            elif direction_no2.get()  == 2 and occluded_no2.get()  == 2:
                for i in range(img_qy):
                    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_name, worker_id2.get(), insta_id, direction_no3.get(), occluded_no3.get())
                    if save_name in img_files:
                        msgbox.showwarning('경고', '{} 파일명이 존재합니다. 확인 후 다시 진행해 주세요'.format(save_name))
                        break
                    os.rename(list_file.get(i), '{}/{}'.format(cur_path, save_name))
                ng_ok_delete()
                ok_flag = 0
        else:
            msgbox.showwarning('경고', '검수를 진행하지 않았습니다.')

# top 프레임
frame_top = Frame(root, relief = 'solid', bd = 1, width = 1480)
frame_top.pack(side = 'top', fill = 'both', expand = True)

# top_left 이미지 검수 프레임
frame_image = LabelFrame(frame_top, text = '원시 데이타 이미지 검수', width = 800)
frame_image.pack(side = 'left', expand = True)

# top_left add/del 프레임
frame_add_del = Frame(frame_image)
frame_add_del.pack(side = 'top', fill = 'both', expand = True)

btn_add_file = Button(frame_add_del, width = 12, text = '파일 추가', command = add_file)
btn_add_file.pack(side = 'left', fill = 'x', padx = 5, pady = 3)

btn_del_file = Button(frame_add_del, width = 12, text = '선택 삭제', command = del_file)
btn_del_file.pack(side = 'right', fill = 'x', padx = 5, pady = 3)

# 선택 이미지 리스트 프레임
list_frame = Frame(frame_image, width = 800)
list_frame.pack(fill = 'both')

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = 'right', fill = 'both', padx = 5, pady = 5)

list_file = Listbox(list_frame, selectmode = 'single', width = 112, height = 10, yscrollcommand = scrollbar.set)
list_file.pack(side = 'left', expand = True, padx = 5, pady = 5)

scrollbar.config(command = list_file.yview)

list_file.bind("<Double-Button-1>", change_img) # 디스플레이된 리스트 중 하나 선택하면 이미지 변경

# 이미지 preview 프레임
photo = PhotoImage()
photo_frame = Label(frame_image, width = 800, height = 500, bg = 'white', image = photo)
photo_frame.pack(expand = 1, anchor = 'center')

# preview select 프레임
frame_preview = Frame(frame_image)
frame_preview.pack(fill = 'both', expand = True)

fair_label = Label(frame_preview, text = '페어링 대상 이미지 장수 선택')
fair_label.pack(side = 'left', padx = 5, pady = 5)

fair_values = [str(i) + '장' for i in range(1, 6)]
fair_combo = ttk.Combobox(frame_preview, height = 5, value = fair_values, state = 'readonly')
fair_combo.current(4)
fair_combo.pack(side = 'left', padx = 5, pady = 5)

btn_fairing = Button(frame_preview, padx = 5, pady = 5, width = 12, text = '페어링 확인', command = img_fairing, repeatdelay = 500, repeatinterval = 100)
btn_fairing.pack(side = 'left', padx = 5, pady = 5)

btn_fairing_label = Label(frame_preview, text = '버튼을 계속 눌러주세요.')
btn_fairing_label.pack(side ='left')

btn_next = Button(frame_preview, padx = 5, pady = 5, width = 12, text = '다 음', command = next_img)
btn_next.pack(side = 'right', padx = 5, pady = 5)

btn_previous = Button(frame_preview, padx = 5, pady = 5, width = 12, text = '이 전', command = pre_img)
btn_previous.pack(side = 'right', padx = 5, pady = 5)

# top_right 이미지 검수 체크리스트 / 저장 프레임
frame_check_save = LabelFrame(frame_top, text = '이미지 검수 체크 및 저장', width = 680)
frame_check_save.pack(side = 'right', fill = 'both', expand = True)

# top_right 이미지 검수 체크리스트 프레임
frame_check = LabelFrame(frame_check_save, text = '이미지 검수 체크 리스트', width = 660)
frame_check.pack(fill = 'both', expand = True, pady = 5)

chkvar1 = IntVar()
chkbox = Checkbutton(frame_check, text = '1. 가림막 객체(5장) 페이링 N.G.', variable = chkvar1)
chkbox.pack(anchor = 'w')

chkvar2 = IntVar()
chkbox = Checkbutton(frame_check, text = '2. 객체 및 가림막 Focus N.G.', variable = chkvar2)
chkbox.pack(anchor = 'w')

chkvar3 = IntVar()
chkbox = Checkbutton(frame_check, text = '3. 객체 이미지 잘림 N.G.', variable = chkvar3)
chkbox.pack(anchor = 'w')

chkvar4 = IntVar()
chkbox = Checkbutton(frame_check, text = '4. 객체 및 가림막 그림자 N.G.', variable = chkvar4)
chkbox.pack(anchor = 'w')

chkvar5 = IntVar()
chkbox = Checkbutton(frame_check, text = '5. 객체, 가림막 및 배경 빛반사 N.G.', variable = chkvar5)
chkbox.pack(anchor = 'w')

chkvar6 = IntVar()
chkbox = Checkbutton(frame_check, text = '6. 객체의 4방향 특징 위주 촬영 N.G.', variable = chkvar6)
chkbox.pack(anchor = 'w')

chkvar7 = IntVar()
chkbox = Checkbutton(frame_check, text = '7. 객체의 모습 그대로 촬영 N.G.', variable = chkvar7)
chkbox.pack(anchor = 'w', ipady = 3)

chkvar8 = IntVar()
chkbox = Checkbutton(frame_check, text = '8. 식별 가능한 개인 정보 또는 저작권 침해 N.G.', variable = chkvar8)
chkbox.pack(anchor = 'w')

chkvar9 = IntVar()
chkbox = Checkbutton(frame_check, text = '9. 대형 객체(1m x 1m)의 경우, 가림막이 60% 이상 가림 N.G.', variable = chkvar9)
chkbox.pack(anchor = 'w')

chkvar10_frame = Frame(frame_check)
chkvar10_frame.pack(fill = 'x')

chkvar10 = IntVar()
chkbox = Checkbutton(chkvar10_frame, text = \
                        '10. 객체 최소 이미지 크기 300 x 300 px 이상 또는 전체 이미지 9등분 중 가운데 한 구역 이상 차지 N.G.', variable = chkvar10)
chkbox.pack(side = 'left')

chkvar10_view = Button(chkvar10_frame, text = '보기', command = img_view)
chkvar10_view.pack(side = 'left', padx = 5)

chkvar11 = IntVar()
chkbox = Checkbutton(frame_check, text = '11. 이미지 크기가 1980 x 1080 px 이상 / 4032 x 3024 이하 N.G.', variable = chkvar11)
chkbox.pack(anchor = 'w')

# 현재 이미지 가로 세로 크기
img_width_height = Frame(frame_check)
img_width_height.pack(fill = 'x')

img_width = Label(img_width_height, text = '현재 이미지 가로 : ')
img_width.pack(side = 'left', padx = 23)

img_height = Label(img_width_height, text = '현재 이미지 세로 : ')
img_height.pack(side = 'left', padx = 5)

chkvar12 = IntVar()
chkbox = Checkbutton(frame_check, text = '12. 촬영 밝기에 따른 객체 이미지 손상 N.G.', variable = chkvar12)
chkbox.pack(anchor = 'w')

chkvar13 = IntVar()
chkbox = Checkbutton(frame_check, text = '13. 가림막 오염(머리카락, 손, 접힘 자국 등) N.G.', variable = chkvar13)
chkbox.pack(anchor = 'w')

chkvar14 = IntVar()
chkbox = Checkbutton(frame_check, text = '14. 군집 촬영(한송이는 가능) N.G.', variable = chkvar14)
chkbox.pack(anchor = 'w')

chkvar15 = IntVar()
chkbox = Checkbutton(frame_check, text = '15. 객체가 가림막에 가려짐 N.G.', variable = chkvar15)
chkbox.pack(anchor = 'w')

# check_button Frame

check_button = Frame(frame_check)
check_button.pack(fill = 'x')

btn = Button(check_button, text = '확인', command = chk_list)
btn.pack(side = 'right', padx = 5)

btn_cmd = Label(check_button, text ='페어링 이미지 세트에 대한 검수 및 체크리스트 체크 완료 후 확인 누르세요.')
btn_cmd.pack(side = 'right', padx = 5)

# bottom 파일명 변경 저장 프레임
frame_save = LabelFrame(frame_check_save, text = '파일명 변경하여 저장', width = 660)
frame_save.pack(fill = 'both', expand = True, pady = 5)

# # 저장경로 프레임
# path_frame = LabelFrame(frame_save, text = '저장경로', width = 780)
# path_frame.pack(pady = 5, fill = 'x')

# txt_dest_path = Entry(path_frame, width = 80)
# txt_dest_path.pack(side = 'left', fill = 'x', expand = True, padx = 5, pady = 5, ipady = 5) # ipady : entry 높이 조정

# btn_dest_path = Button(path_frame, text = '찾아보기', width = 10, command = save_path)
# btn_dest_path.pack(side = 'right', padx = 5, pady = 5)

# 저장방법 프레임
path_frame = LabelFrame(frame_save, text = '저장방법', width = 660)
path_frame.pack(pady = 5, fill = 'x')

save_method = IntVar()
save_method1 = Radiobutton(path_frame, text = '파일 이름 변경', value = 1, variable = save_method)
save_method1.select()
save_method2 = Radiobutton(path_frame, text = '다른 이름으로 저장', value = 2, variable = save_method)
save_method3 = Radiobutton(path_frame, text = '검수없이 파일 이름 변경', value = 3, variable = save_method)

save_method1.pack(side = 'left', padx = 5, pady = 5) 
save_method2.pack(side = 'left', padx = 5, pady = 5) 
save_method3.pack(side = 'left', padx = 5, pady = 5) 

# 이미지 파일 정보 프레임'
img_info_frame = LabelFrame(frame_save, text = '파일명 정보')
img_info_frame.pack(fill = 'both')

workers_id = Frame(img_info_frame)
workers_id.pack(side = 'top', fill = 'x')

worker_id1 = Label(workers_id, text = '촬영자 worker ID :')
worker_id1.pack(side = 'left', padx = 5, pady = 5)

values_workerid = ['{0:03d}'.format(i) for i in range(1, 101)]
worker_id2 = ttk.Combobox(workers_id, width = 5, value = values_workerid, state = 'readonly')
worker_id2.pack(side = 'left')

class_name = Frame(img_info_frame)
class_name.pack(side = 'top', fill = 'x')

class_name1 = Label(class_name, text = 'Class 명 : ')
class_name1.pack(side = 'left', padx = 5, pady = 5)

class_dict = {}
with open('setting/class_list.txt', 'rt', encoding = 'utf-8') as tmp_file:
    while True:
        tmp_line1 = tmp_file.readline().strip()
        if not tmp_line1:
            break
        tmp_line2 = tmp_line1.split('|')
        class_dict[tmp_line2[0]] = tmp_line2[1]
        
class_key_lists = list(sorted(class_dict.keys()))

class_name2 = ttk.Combobox(class_name, width = 30, height = 5, value = class_key_lists, state = 'readonly')
class_name2.pack(side = 'left', padx = 5, pady = 5)

class_name3 = Label(class_name, text = '객체 ID : ')
class_name3.pack(side = 'left', padx = 5, pady = 5)

values_insid = ['{0:03d}'.format(i) for i in range(1, 101)]
class_name4 = ttk.Combobox(class_name, width = 5, value = values_insid, state = 'readonly')
class_name4.pack(side = 'left', padx = 5, pady = 5)

direction_no = Frame(img_info_frame)
direction_no.pack(side = 'top', fill = 'x')

direction_no1 = Label(direction_no, text = '방향 No. :')
direction_no1.pack(side = 'left', padx = 5, pady = 5)

direction_no2 = IntVar()
btn_direction1 = Radiobutton(direction_no, text = '자동 입력', value = 1, variable = direction_no2, command = clear_direction)
btn_direction1.select()
btn_direction2 = Radiobutton(direction_no, text = '수동 입력', value = 2, variable = direction_no2, command = make_direction)

btn_direction1.pack(side = 'left', pady = 5)
btn_direction2.pack(side = 'left', padx = 5, pady = 5)

direction_values = ['']
direction_no3 = ttk.Combobox(direction_no, height = 5, value = direction_values, state = 'readonly')
direction_no3.pack(side = 'left')

# direction_values = ['', '01', '02', '03', '04']
# direction_no3 = ttk.Combobox(direction_no, height = 5, value = direction_values, state = 'readonly')
# direction_no3.pack(side = 'left')

occluded_no = Frame(img_info_frame)
occluded_no.pack(side = 'top', fill = 'x')

occluded_no1 = Label(occluded_no, text = '가림막 명 :')
occluded_no1.pack(side = 'left', padx = 5, pady = 5)

occluded_no2 = IntVar()
btn_occluded1 = Radiobutton(occluded_no, text = '자동 입력', value = 1, variable = occluded_no2, command = clear_occluded)
btn_occluded1.select()
btn_occluded2 = Radiobutton(occluded_no, text = '수동 입력', value = 2, variable = occluded_no2, command = make_occluded)

btn_occluded1.pack(side = 'left', pady = 5)
btn_occluded2.pack(side = 'left', padx = 5, pady = 5)

occluded_values = ['']
occluded_no3 = ttk.Combobox(occluded_no, height = 5, value = occluded_values, state = 'readonly')
occluded_no3.pack(side = 'left')

# occluded_values = ['', 'None', 'SemiTransparent', 'WireDense', 'WireMedium', 'WireLoose']
# occluded_no3 = ttk.Combobox(occluded_no, height = 5, value = occluded_values, state = 'readonly')
# occluded_no3.pack(side = 'left')

# 저장/닫기 프레임
save_close_frame = Frame(frame_save)
save_close_frame.pack(fill = 'both', pady = 5)

btn_close = Button(save_close_frame, text = '닫기', width = 10, command = root.quit)
btn_close.pack(side = 'right', padx = 5, pady = 5)

btn_save = Button(save_close_frame, text = '저장', width = 10, command = save)
btn_save.pack(side = 'right', padx = 5, pady = 5)

root.mainloop()