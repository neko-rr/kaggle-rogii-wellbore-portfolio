Topic #729554: Submission fails with "Notebook Threw Exception" although submission.csv is generated correctly
  Author: Angel R, Gadea L.
  Posted: 2026-07-26 01:21:40.037000
  Votes: -1  Comments: 1

Hello,

I am experiencing a submission issue in this competition.

My notebook executes successfully in the Kaggle environment and generates the submission file correctly.

Validation performed before submission:



submission.csv exists: True

Shape: (14151, 2)

Columns: ['id', 'tvt']

Null values: 0

Duplicate IDs: 0

IDs order matches sample_submission.csv: True


The final notebook output confirms that the file is created correctly:
SHAPE FINAL:
(14151, 2)

VALORES NULOS:
id 0
tvt 0

ARCHIVO GENERADO:
True

TAMAﾃ前:
462310 bytes

The final debug also confirms:
MODEL EXISTS:
True

SUBMISSION EXISTS:
True

However, after submitting the notebook, Kaggle reports:
Notebook Threw Exception

The submission log does not show a Python traceback. The last lines are:
[NbConvertApp] Converting notebook notebook.ipynb to notebook
[NbConvertApp] Writing 329407 bytes to notebook.ipynb
[NbConvertApp] Converting notebook notebook.ipynb to html
[NbConvertApp] Writing 612869 bytes to results.html

I also tested a minimal notebook that only creates a valid submission.csv file, and that submission was accepted successfully.

Could you please help identify what could be causing the evaluator to fail after the notebook execution completes?

Thank you.

Comments:
笏懌楳 PC Jimmmy (2026-07-26 02:06:55.837000) [+0]
笏・ The logs never show the submission failures.  The log your seeing is only the one generated when the 3 fake test wells get run.
笏・ 
笏・ Most of that type error is shape or memory error related to the fact...
