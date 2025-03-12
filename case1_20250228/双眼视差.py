# -*- coding: utf-8 -*-
"""
双眼立体视觉测试实验程序（anaglyph 版）
利用随机点立体图测试2.5维深度加工能力
请被试佩戴红蓝眼镜观看（红眼滤片给左眼，蓝眼滤片给右眼）
"""

from psychopy import visual, core, event
import numpy as np
import random
import csv

# --------------------------
# 实验参数设置
# --------------------------
nDots = 500                # 每幅图中的点数
dotSize = 0.02             # 点的大小（单位：norm）
targetCenter = np.array([0.0, 0.0])  # 目标区域中心（单位：norm）
targetRadius = 0.3         # 目标区域半径（单位：norm）
fixationDuration = 0.5     # 注视点呈现时间（秒）
stimulusDuration = 0.3     # 刺激呈现时间（秒）
responseTimeout = 2.0      # 响应超时（秒）

# 条件设置：
# - target：有目标，右眼中目标区域的点偏移一定值（此处为0.05）
# - non-target：无目标，左右眼图像一致
conditions = [{'name': 'target', 'disparity': 0.05},
              {'name': 'non-target', 'disparity': 0.0}]
nTrialsPerCondition = 5
trialList = conditions * nTrialsPerCondition
random.shuffle(trialList)

# --------------------------
# 创建实验窗口（使用 stereo=True）
# --------------------------
win = visual.Window([800, 600], fullscr=False, stereo=True, units='norm', color=[0, 0, 0])
# 尝试设置 anaglyph 模式（部分版本可能不支持，该异常可以忽略）
try:
    win.stereoMode = 'anaglyph'
except Exception as e:
    print("设置 anaglyph 模式时出错：", e)

# --------------------------
# 创建各类刺激
# --------------------------
# 注视点与提示信息
fixation = visual.TextStim(win, text='+', height=0.1, color='white')
instruction = visual.TextStim(win, text='请佩戴红蓝眼镜并按空格键开始实验', height=0.07, color='white')
responsePrompt = visual.TextStim(win, text='请判断是否出现突出区域\n按 "1" 表示有，"2" 表示无',
                                 height=0.07, pos=(0, -0.8), color='white')

# 使用 DotStim 创建随机点刺激，不在初始化时传入 eye 参数
stim_left = visual.DotStim(win, nDots=nDots, dotSize=dotSize, color=[1, 1, 1],
                           fieldPos=(0, 0), fieldSize=(2, 2), dotLife=-1)
stim_right = visual.DotStim(win, nDots=nDots, dotSize=dotSize, color=[1, 1, 1],
                            fieldPos=(0, 0), fieldSize=(2, 2), dotLife=-1)
# 在创建后设置左右眼属性
stim_left.eye = 'left'
stim_right.eye = 'right'

# --------------------------
# 显示开始提示
# --------------------------
instruction.draw()
win.flip()
event.waitKeys(keyList=['space'])

# 用于保存实验数据
results = []
trialClock = core.Clock()

# --------------------------
# 试次循环
# --------------------------
for trial in trialList:
    # 生成随机点（均匀分布在 [-1, 1] 区间内）
    dots = np.random.uniform(-1, 1, (nDots, 2))
    # 计算每个点到目标中心的欧式距离
    distances = np.sqrt(np.sum((dots - targetCenter) ** 2, axis=1))
    targetMask = distances < targetRadius  # 标记目标区域内的点

    # 左眼图像保持不变
    dots_left = dots.copy()
    # 右眼图像：若为 target 条件，则在目标区域内的点进行水平偏移
    dots_right = dots.copy()
    current_disp = trial['disparity']
    dots_right[targetMask, 0] += current_disp  # x 方向偏移

    # 更新 DotStim 的点位置
    stim_left.dotsXY = dots_left
    stim_right.dotsXY = dots_right

    # 1. 注视阶段
    fixation.draw()
    win.flip()
    core.wait(fixationDuration)

    # 2. 刺激呈现阶段（同时绘制左右眼刺激）
    stim_left.draw()
    stim_right.draw()
    win.flip()
    core.wait(stimulusDuration)

    # 3. 响应阶段
    win.flip()  # 清屏
    responsePrompt.draw()
    win.flip()

    trialClock.reset()
    keys = event.waitKeys(maxWait=responseTimeout, keyList=['1', '2'], timeStamped=trialClock)
    if keys:
        key, rt = keys[0]
    else:
        key, rt = None, None

    # 判断正确性
    correctKey = '1' if trial['name'] == 'target' else '2'
    correct = (key == correctKey)

    # 保存本试次结果
    results.append({
        'trialType': trial['name'],
        'disparity': current_disp,
        'response': key,
        'correct': correct,
        'rt': rt
    })

    core.wait(0.5)

# --------------------------
# 实验结束，显示结束信息
# --------------------------
endText = visual.TextStim(win, text='实验结束，谢谢参与！', height=0.1, color='white')
endText.draw()
win.flip()
core.wait(2.0)

# 打印实验结果到控制台
print("实验结果:")
for res in results:
    print(res)

# 将结果写入 CSV 文件，Excel 可直接打开 CSV 文件
with open('results.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['trialType', 'disparity', 'response', 'correct', 'rt']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for res in results:
        writer.writerow(res)

win.close()
core.quit()
