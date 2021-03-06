# 评测方法

## I. 测试集
经过结构化的N份门诊病历。

---

## II. 评测指标
总体思路是比对门诊病历初诊疾病列表与算法输出疾病列表之间的相似度。设病例中的诊断结果为$\mathbb{D}$，设算法输出的疾病列表为$\hat{\mathbb{D}}$。这里我们认为$\mathbb{D}$是无序的，而$\hat{\mathbb{D}}$是有序的。设相似度的度量为$S(\cdot || \cdot) \in \mathbb{R}$。

### II-1. 以$\mathbb{D}$为标准评价$\hat{\mathbb{D}}$
#### II-1-(1) F1-Score & ROC
考虑算法的结果是否诊断到了疾病，是否有误诊。

$$S_{F1}(\mathbb{P}||\mathbb{D}) = \frac{2 \cdot precision \cdot recall}{precision + recall}$$

其中$\mathbb{P} \subset \hat{\mathbb{D}}$。子集的选择有以下几种方式：
1. Top $n$:
   - $\mathbb{P} = \{\hat{d} | \hat{d}的分数在前n个\}$
   - 这个指标的意义在于看$\hat{\mathbb{D}}$的绝对顺序是否合理，因为不论怀疑疾病的列表有多长，它都会忽略第$n$个之后的疾病
2. Top $p\%$:
   - $\mathbb{P} = \{\hat{d} | score(\hat{d}) > Percentile_{(1-p)}\}$
   - 这个指标的意义在于看$\hat{\mathbb{D}}$的相对顺序是否合理，因为随着怀疑疾病列表的增长以及高分疾病的增多，参评的列表也会随之变长，命中率自然会有所提高（当然，假阳性也会明显升高）
3. Above threshold $\theta$:
   - $\mathbb{P} = \{\hat{d} | score(\hat{d}) > \theta\}$
   - 这个指标的意义在于看疾病得分的绝对数值是否有很好的区分性

上述指标除了可以观测F1-Score以外，还可以对应地更改选择$\mathbb{P}$的参数，绘制ROC曲线，观察AUC。

这里需要说明实验的含义以及混淆矩阵的计算方式：
- **实验的含义：**
  - [x] 采样并不能穷尽症状集合的子集空间，也不是在其中进行完全的随机采样。因此输入数据的样本空间为所有可能在人类身上发生的症状组合，即所有具有实际医学意义的症状集合。
  - [x] 这些症状组合可以表达为$N$维向量，其中$N$为症状数量，每一个维度只有三个取值：$1, 0, -1$，分别表示“有”，“不确定”和“无”。则样本空间为整个向量空间的部分片段，在好的抽样方法下，可以做到在这个空间上的随机采样。
  - [x] 这个实验过程可以和人脸识别的评价实验做类比：
    - 人脸识别的样本空间也不是完整的二维图片空间，而是描绘人脸的那些图片；我们的评测中只抽取了具有实际医学意义的向量，而不是任意向量。
    - 人脸识别目标是识别面部图片对应的身份，而不在于识别图片中是否包含人脸；我们的算法目标在于鉴别患者的疾病，而不在于判断当前的症状是否具有医学意义（虽然我们可以认为算法寻找矛盾的过程就相当于鉴别是否具有医学意义，但严格来说这不算是诊断）。
  - [x] 例如$\{头痛^1，发热^{-1}，咳嗽^1\}$是在我们的样本空间中的（取值为0的症状省略）。而像$\{高血压^1，低血压^1\}$这样的向量不属于我们的样本空间。
- **混淆矩阵的计算方式：**
  - 由于算法输出的结果不是一维的数据点，不好直接判断单个采样的正确性；而如果把一份病例的数据单独拿出来计算F1再合并，则计算单个F1的数据点过少。计算混淆矩阵的方式需要做一点修改。
  - 设第$i$个样本得到的输出（Prediction）为$\hat{\mathbb{P}_i} = \{\hat{d}_{ij}\}$，答案为$\mathbb{D}_i = \{d_{ik}\}$，则比较$\hat{d}_{ij}$和$d_{ik}$可以得到一个小的混淆矩阵，即$TP_i, FP_i, TN_i, FN_i$。则整体的准确率和召回率为：
  - $$precision = \frac{\sum_i TP_i}{\sum_i (TP_i + FP_i)}$$
  - $$recall = \frac{\sum_i TP_i}{\sum_i (TP_i + FN_i)}$$
  - 这种计算方式既保留了结果与算法的相关性也解决了数据点过少的问题。

### II-2. 以$\hat{\mathbb{D}}$为标准评价$\mathbb{D}$
#### II-2-(1) Rank Score
该指标（$S_{Rank}(\mathbb{D}||\hat{\mathbb{D}})$）的设计目标是反映疾病评分的整体分布，它需要满足的性质如下：
1. $\mathbb{D}$在$\hat{\mathbb{D}}$中的排名靠前 $\propto S_{Rank}(\mathbb{D}||\hat{\mathbb{D}})$
2. $\mathbb{D}$中疾病的得分高 $\propto S_{Rank}(\mathbb{D}||\hat{\mathbb{D}})$
3. $\mathbb{D}$与$\hat{\mathbb{D}}$相似 $\propto S_{Rank}(\mathbb{D}||\hat{\mathbb{D}})$

$$S_{Rank}(\mathbb{D}||\hat{\mathbb{D}}) = ?$$

---

## III. 操作流程

### III-1. 挑选测试集
找出能够代表随机采样的门诊病历集合，数量不能少于100份。病例的获取可以考虑：
- [x] 将所有病例（包括住院病历）进行常见度的评分加权
- [x] 去医院门诊蹲点采样

### III-2. 流式运行诊断算法
- 先输入主诉，然后在规定回合数（如：$I=5$）内根据系统问题参考病例回答。回答遵循以下规则：
  - [ ] 在病例中记录为“有”的症状回答为：有
  - [ ] 在病例中记录为“无”的症状回答为：无
  - [ ] 没有在病例中记录的症状回答为：不确定
- 在交互过程中记录问诊流程。
- 最后的诊断结果按疾病评分从高到低记录，需要同时记录疾病名称和对应得分。
- 如果诊断失败，则需要记录UNSAT信息

### III-3. 批式运行诊断算法
- 将病例中记录的**除诊断结果以外的**所有信息一起作为主诉输入诊断算法。变量的置位遵循以下规则：
  - [ ] 在病例中记录为“有”的症状回答为：有
  - [ ] 在病例中记录为“无”的症状回答为：无
- 不进行交互，直接得出结果。
- 最后的诊断结果按疾病评分从高到低记录，需要同时记录疾病名称和对应得分。
- 如果诊断失败，则需要记录UNSAT信息

### III-4. 检验逻辑矛盾
- 将病例中记录的所有信息（**包括诊断结果**）一起作为主诉输入诊断算法。变量的置位遵循以下规则：
  - [ ] 在病例中记录为“有”的症状回答为：有
  - [ ] 在病例中记录为“无”的症状回答为：无
- 不进行交互，也无需记录诊断结果
- 如果诊断失败，则需要记录UNSAT信息

### III-5. 计算评价指标
根据III-2和III-3的结果计算II中的评价指标，分别归类绘制图表。
