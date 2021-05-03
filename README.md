# Лабораторная работа №4.
**Цель лабораторной работы:**
Исследовать влияние различных техник аугментации
данных на процесс обучения нейронной сети на примере решения задачи классификации
Food-101 с использованием техники обучения Transfer Learning.

**Задачи:**
1. С использованием [1], техники обучения Transfer Learning [2] и оптимальной
политики изменения темпа обучения, определенной в ходе выполнения
лабораторной #3, обучить нейронную сеть EfficientNet-B0 (предварительно
обученную на базе изображений imagenet) для решения задачи классификации
изображений Food-101 с использованием следующих техник аугментации данных
[3]:  
* Случайное горизонтальное и вертикальное отображение [4]  
* Использование случайной части изображения [5]  
* Поворот на случайный угол [6]  

2.  Для каждой индивидуальной техники аугментации определить оптимальный набор
параметров.  

3. Обучить нейронную сеть с использованием оптимальных техник аугментации
данных 2a-с совместно.

**Замечания**: В данной лабораторной работе параметр BATCH_SIZE равен 32. Оптимальная политика изменения темпа обучения - cosine decay with restarts с параметрами: initial_learning_rate = 0.001, first_decay_steps = 5000, t_mul = 2.0, m_mul = 0.75.
## 1. С использованием [1], техники обучения Transfer Learning [2] и оптимальной политики изменения темпа обучения, определенной в ходе выполнения лабораторной #3, обучить нейронную сеть EfficientNet-B0 (предварительно обученную на базе изображений imagenet) для решения задачи классификации изображений Food-101 с использованием следующих техник аугментации данных [3]: Случайное горизонтальное и вертикальное отображение [4], Использование случайной части изображения [5], Поворот на случайный угол [6].
* **Графики обучения EfficientNetB0 с использованием аугментации данных RandomFlip**:  
   * График точности epoch_categorical_accuracy:
   <img src="./graphs/flip_categorical_accuracy.png">
   <img src="./graphs/flip_categorical_accuracy_legend.png">
 
   * График функции потерь epoch_loss:
   <img src="./graphs/flip_loss.png">
   <img src="./graphs/flip_loss_legend.png">
   
 * **Анализ полученных результатов**: Наивысшие значения метрики точности наблюдаются на графике с горизонтальным отображением (67.99%). Также на графике функции потерь горизонтального отображения наблюдаются наименьшие значения (1.194). По сравнению с базовой нейронной сетью, мы выйграли ~0.1% точности. На скорость сходимости данная аугментация данных не повлияла. Оптимальным параметром будет 'horizontal'.
   
 * **Визуализации данных после RandomFlip('horizontal')**:
 <img src="./graphs/flip_h_data.png">

 * **Визуализации данных после RandomFlip('vertical')**:
 <img src="./graphs/flip_v_data.png">

 * **Визуализации данных после RandomFlip('horizontal_and_vertical')**:
 <img src="./graphs/flip_hv_data.png">  
 
* **Графики обучения EfficientNetB0 с использованием аугментации данных RandomСrop**:  
   * График точности epoch_categorical_accuracy:
   <img src="./graphs/crop_categorical_accuracy.png">
   <img src="./graphs/crop_categorical_accuracy_legend.png">
 
   * График функции потерь epoch_loss:
   <img src="./graphs/crop_loss.png">
   <img src="./graphs/crop_loss_legend.png">
   
 * **Анализ полученных результатов**: Наивысшие значения метрики точности наблюдаются на графике с параметрами апскейла 300x260 (66.97%). Также на графике функции потерь данного апскейла наблюдаются наименьшие значения (1.239). Однако, по сравнению с базовой нейронной сетью, мы потеряли в точности ~0.85%. На скорость сходимости данная аугментация данных не повлияла. Оптимальным параметром будем считать 300x260.
   
 * **Визуализации данных после RandomCrop(для большей наглядности работы, отобразили для 300x300)**:
 <img src="./graphs/crop_data.png">
 
 
 * **Графики обучения EfficientNetB0 с использованием аугментации данных RandomRotation**:  
   Здесь по умолчанию параметр заполнения стоит reflect.
   * График точности epoch_categorical_accuracy:
   <img src="./graphs/rot_categorical_accuracy.png">
   <img src="./graphs/rot_categorical_accuracy_legend.png">
 
   * График функции потерь epoch_loss:
   <img src="./graphs/rot_loss.png">
   <img src="./graphs/rot_loss_legend.png">
   
 * **Анализ полученных результатов**: Наивысшие значения метрики точности наблюдаются на графике с параметром factor=0.01 (67.62%). Однако на графике функции потерь с параметром factor=0.04 наблюдаются наименьшие значения (1.209). Да и разница в точности между factor=0.01 и 0.04 всего 0.05%. В данном случае я выбрал параметр factor=0.04 как оптимальный, что соответствует границам угла поворота от -14.4 до 14.4 градусов. По сравнению с базовой нейронной сетью, мы потеряли в точности ~0.3%. На скорость сходимости данная аугментация данных не повлияла.
 
* **Графики обучения EfficientNetB0 с использованием аугментации данных RandomRotation(исследуем параметр заполнения fill_mode)**:
  Здесь параметр factor равен 0.04.
   * График точности epoch_categorical_accuracy:
   <img src="./graphs/rot_mode_categorical_accuracy.png">
   <img src="./graphs/rot_mode_categorical_accuracy_legend.png">
 
   * График функции потерь epoch_loss:
   <img src="./graphs/rot_mode_loss.png">
   <img src="./graphs/rot_mode_loss_legend.png">
