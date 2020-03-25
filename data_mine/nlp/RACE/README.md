# RACE: Large-scale ReAding Comprehension Dataset From Examinations


Dataset description
-------------------

Collected from the English exams for middle and high school Chinese students
in the age range between 12 to 18, RACE consists of near 28,000 passages and
near 100,000 questions generated by human experts (English instructors), and
covers a variety of topics which are carefully designed for evaluating the
students’ ability in understanding and reasoning.

In particular, the proportion of questions that requires reasoning is much
larger in RACE than that in other benchmark datasets for reading
comprehension, and there is a significant gap between the performance of the
state-of-the-art models (43%) and the ceiling human performance (95%).


* [Paper](https://arxiv.org/pdf/1704.04683.pdf)
* [RACE baselines](https://github.com/qizhex/RACE_AR_baselines)
* [Leaderboard](http://www.qizhexie.com/data/RACE_leaderboard)


Question ID caveat
------------------

Some questions have the same ID in the original RACE dataset specification.
The IDs that are included in the provided files identify passages rather
than questions (e.g. `middle1548` represents a document that has
multiple questions associated with it - inheriting the same ID as the
document). We try to make the question IDs unique by appending a prefix
to the passage ID the question belongs to. For example, let's say that
the passage `middle1548` includes 3 questions. The questions will receive the
following IDs (always starting at 1):

1. `1-middle1548`
2. `2-middle1548`
3. `3-middle1548`