import numpy as np
from psychopy import visual, event, core
import colorsys
import pandas as pd
import datetime

# 定义六种基本颜色的色调和名称：红、黄、绿、青、蓝、品红
hue_list = np.random.rand(8) 
# 定义标准刺激和目标刺激的初始饱和度条件
standard_list = [0.4, 0.6, 0.8]
target_init_list = [0.3, 0.6, 0.9]

# 定义眼别：左眼和右眼
eye_conditions = ["左", "右"]

# 创建 PsychoPy 窗口
win = visual.Window(size=(1000, 600), color=(1, 1, 1), units='norm')

# 用于存储试验结果的列表
results = []

brightness = 1.0  # 固定亮度

trial_counter = 1

# 构建所有试次的列表：每个试次包含颜色、标准刺激饱和度、目标刺激初始饱和度及眼别
trial_list = []
for i, hue in enumerate(hue_list):
    for std_val in standard_list:
        for target_init in target_init_list:
            for eye in eye_conditions:
                trial_list.append({
                    'color_index': i,
                    'hue': hue,
                    'standard_saturation': std_val,
                    'target_initial': target_init,
                    'eye_condition': eye
                })

# 随机打乱试次顺序
np.random.shuffle(trial_list)

# 依次执行每个试次
for trial in trial_list:
    hue = trial['hue']
    current_standard = trial['standard_saturation']
    target_init = trial['target_initial']
    eye = trial['eye_condition']
    
    # 目标刺激的初始饱和度
    target_saturation = target_init
    
    # 显示试验说明文字
    instructions = visual.TextStim(
        win,
        text=(f"Trial {trial_counter}/72:\n"
              f"使用你的 {eye}眼 进行判断\n"
              "请使用↑/↓键调整目标刺激（右侧）颜色\n"
              "使其与标准刺激（左侧）匹配，调整好后按回车确认"),
        pos=(-0.2, -0.5),
        color=(-1, -1, -1),
        height=0.08,
        wrapWidth=1.5
    )
    
    # 创建两个矩形刺激：标准刺激放在屏幕左侧，目标刺激放在屏幕右侧
    rect_standard = visual.Rect(win=win, width=0.6, height=0.6, pos=(-0.5, 0.3))
    rect_target = visual.Rect(win=win, width=0.6, height=0.6, pos=(0.5, 0.3))
    
    trial_active = True
    while trial_active:
        # 检测按键输入
        keys = event.getKeys()
        for key in keys:
            if key == 'up':
                target_saturation = min(target_saturation + 0.05, 1.0)
            elif key == 'down':
                target_saturation = max(target_saturation - 0.05, 0.0)
            elif key in ['return']:
                trial_active = False  # 按回车确认匹配
            elif key == 'escape':
                win.close()
                core.quit()
        
        # 计算标准刺激的颜色（采用当前标准饱和度）
        r_std, g_std, b_std = colorsys.hsv_to_rgb(hue, current_standard, brightness)
        rect_standard.fillColor = (r_std * 2 - 1, g_std * 2 - 1, b_std * 2 - 1)
        
        # 计算目标刺激的颜色（采用当前目标饱和度）
        r_tgt, g_tgt, b_tgt = colorsys.hsv_to_rgb(hue, target_saturation, brightness)
        rect_target.fillColor = (r_tgt * 2 - 1, g_tgt * 2 - 1, b_tgt * 2 - 1)
        
        # 绘制刺激与说明文字，并刷新窗口
        rect_standard.draw()
        rect_target.draw()
        instructions.draw()
        win.flip()
    
    # 保存本次试次结果
    results.append({
        'trial': trial_counter,
        'hue': hue,
        'standard_saturation': current_standard,
        'target_initial': target_init,
        'final_target_saturation': target_saturation,
        'eye_condition': eye
    })
    
    trial_counter += 1
    core.wait(0.5)

# 将试验结果保存到 Excel 文件中
df = pd.DataFrame(results)
date_str = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"experiment_results_{date_str}.xlsx"
df.to_excel(filename, index=False)
print("实验结果已保存")
win.close()
core.quit()
