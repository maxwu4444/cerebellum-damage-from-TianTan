from psychopy import visual, core, event, data, gui
import os, glob, random

# -----------------------------
# 1. 被试信息及数据文件设置
# -----------------------------
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title='视觉感知实验')
if not dlg.OK:
    core.quit()  # 如果取消，则退出实验

# 创建数据保存文件夹（若不存在则创建）
#if not os.path.isdir('data'):
#    os.makedirs('data')
# 数据文件名（CSV 格式）
filename = 'E:/@小脑损伤/case1_TianTan20250228/视觉感知/加工时间/results/test.csv'
dataFile = open(filename, 'w')
dataFile.write('trial,stim_duration,draw_response_time,image_file\n')
# -----------------------------
# 2. 窗口和刺激对象的设置
# -----------------------------
# 创建实验窗口（单位为像素）
win = visual.Window(size=(1024, 768), fullscr=False, color='grey', units='pix')

# 注视点（“+”）
fixation = visual.TextStim(win=win, text='+', height=40, color='black')

# -----------------------------
# 3. 从文件夹中读取刺激图片
# -----------------------------
# 图片存放路径（请确保该文件夹内有至少8个图片文件，支持jpg和png格式）
stim_path = 'E:/@小脑损伤/case1_TianTan20250228/视觉感知/加工时间'
# 同时获取 jpg 和 png 格式图片
stim_files = glob.glob(os.path.join(stim_path, '*.jpg')) + glob.glob(os.path.join(stim_path, '*.png'))

# -----------------------------
# 4. 试次参数设置
# -----------------------------
# 定义刺激呈现时间列表（单位：秒），从短到长排列（可根据需要调整）
stim_durations = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
trial_durations = stim_durations * 3
random.shuffle(trial_durations)
# 使用 TrialHandler 生成试次（这里只重复一次，每个试次依次使用不同呈现时长）
trialList = [{'stim_duration': d} for d in trial_durations]
trials = data.TrialHandler(trialList=trialList, nReps=1, method='sequential')

# -----------------------------
# 5. 实验说明
# -----------------------------
instructionText = visual.TextStim(
    win=win,
    text=(
        "欢迎参加实验。\n\n"
        "本实验中，每个试次屏幕中央会出现一个刺激图像。\n"
        "刺激呈现后，请用纸和笔绘制你所看到的图像。\n"
        "绘图完成后请按空格键进入下一试次。\n\n"
        "按任意键开始实验。"
    ),
    color='black',
    wrapWidth=1000
)
instructionText.draw()
win.flip()
event.waitKeys()  # 等待被试按键开始实验

# -----------------------------
# 6. 实验主循环
# -----------------------------
trial_num = 0
for trial in trials:
    trial_num += 1
    stim_duration = trial['stim_duration']
    
    # 6.1 显示注视点 500ms
    fixation.draw()
    win.flip()
    core.wait(0.5)
    
     # 6.2 随机抽取一个图片作为刺激，并在屏幕中央显示
    chosen_img = random.choice(stim_files)
    stim = visual.ImageStim(win=win, image=chosen_img, pos=(0, 0))
    stim.draw()
    win.flip()
    core.wait(stim_duration)
    
    # 6.3 刺激消失，呈现空白屏幕 500ms
    win.flip()
    core.wait(0.5)
    
    # 6.4 显示绘图提示，让被试根据记忆在纸上绘制刺激图像
    drawText = visual.TextStim(
        win=win,
        text="请用纸和笔绘制你刚才看到的图像\n绘图完成后按空格键继续",
        color='black',
        wrapWidth=800
    )
    drawText.draw()
    win.flip()
    
    # 6.5 记录绘图反应时（从提示出现到按下空格键的时间）
    drawClock = core.Clock()  # 重置计时器
    event.waitKeys(keyList=['space'])
    rt = drawClock.getTime()
    
    # 6.6 保存本试次数据：试次号、刺激呈现时长、绘图反应时、所呈现图片文件名
    dataFile.write(f"{trial_num},{stim_duration},{rt},{os.path.basename(chosen_img)}\n")
    
# -----------------------------
# 7. 实验结束
# -----------------------------
thanks = visual.TextStim(win=win, text="实验结束，感谢参与！", color='black')
thanks.draw()
win.flip()
core.wait(2)

# 关闭数据文件和窗口，退出程序
dataFile.close()
win.close()
core.quit()