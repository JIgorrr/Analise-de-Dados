import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pycountry

# Importando a base de dados:
df = pd.read_csv("ds_salaries.csv")

# region Tratando os dados:
data_scientist_titles = ['Data Scientist', 'Data Analyst', 'Data Modeler', 'Data Strategist', \
                         'Data Quality Analyst', 'Compliance Data Analyst', 'Data Architect', \
                         'Business Data Analyst', 'Applied Data Scientist', 'Staff Data Analyst', \
                         'Data Specialist', 'Financial Data Analyst', 'BI Developer', 'BI Analyst', \
                         'Data Science Consultant', 'Data Analytics Specialist', 'BI Data Analyst', \
                         'Insight Analyst', 'Big Data Architect', 'Product Data Analyst', \
                         'Data Analytics Consultant', 'Data Management Specialist', 'Data Operations Analyst', \
                         'Marketing Data Analyst', 'Power BI Developer', 'Product Data Scientist', \
                         'Cloud Data Architect', 'Staff Data Scientist', 'Finance Data Analyst']
engineer_titles = ['ML Engineer', 'Research Engineer', 'Analytics Engineer', 'Business Intelligence Engineer', \
                   'Machine Learning Engineer', 'Data Engineer', 'Computer Vision Engineer', \
                   'Applied Machine Learning Engineer', 'ETL Engineer', 'Data DevOps Engineer', \
                   'Big Data Engineer', 'BI Data Engineer', 'MLOps Engineer', 'Autonomous Vehicle Technician', \
                   'Cloud Database Engineer', 'Data Infrastructure Engineer', 'Software Data Engineer', \
                   'Data Operations Engineer', 'Machine Learning Infrastructure Engineer', 'Deep Learning Engineer', \
                   'Machine Learning Software Engineer', 'Computer Vision Software Engineer', 'Azure Data Engineer', \
                   'Marketing Data Engineer', 'Data Science Engineer', 'Machine Learning Research Engineer', \
                   'NLP Engineer', 'Data Analytics Engineer', 'Cloud Data Engineer', 'ETL Developer']
researcher_titles = ['Applied Scientist', 'Research Scientist', 'Machine Learning Researcher', \
                     'Machine Learning Scientist', 'Applied Machine Learning Scientist', 'Deep Learning Researcher', \
                     'Machine Learning Developer', '3D Computer Vision Researcher']
manager_titles = ['Principal Data Scientist', 'Data Analytics Manager', 'Head of Data', 'Data Science Manager', \
                  'Data Manager', 'Lead Data Analyst', 'Director of Data Science', 'Lead Data Scientist', \
                  'Data Science Lead', 'Head of Data Science', 'Data Analytics Lead', 'Data Lead', \
                  'Manager Data Management', 'Principal Machine Learning Engineer', 'Data Science Tech Lead', \
                  'Data Scientist Lead', 'Principal Data Architect', 'Machine Learning Manager', \
                  'Lead Machine Learning Engineer', 'Lead Data Engineer', 'Head of Machine Learning', \
                  'Principal Data Analyst', 'Principal Data Engineer']
AI_titles = ['AI Developer', 'AI Scientist', 'AI Programmer']


def group_job_title(job_title):
    if job_title in data_scientist_titles:
        return "Cientista de Dados"
    elif job_title in engineer_titles:
        return "Engenheiro"
    elif job_title in researcher_titles:
        return "Investigador"
    elif job_title in manager_titles:
        return "Gerente"
    elif job_title in AI_titles:
        return "Desenvolvedor IA"


def country_name(country_code):
    try:
        return pycountry.countries.get(alpha_2=country_code).name
    except:
        return 'other'


def experience_level_to_num(experience_level):
    if experience_level == 'EN':
        return 'Nível de Entrada'
    elif experience_level == 'MI':
        return 'Nível Intermediário'
    elif experience_level == 'SE':
        return 'Sênior'
    elif experience_level == 'EX':
        return 'Nível Executivo'


def work_year_to_num(work_year):
    if work_year == 2020:
        return 0
    elif work_year == 2021:
        return 1
    elif work_year == 2022:
        return 2
    elif work_year == 2023:
        return 3


def employment_type_to_num(employment_type):
    if employment_type == 'FL':
        return 'Freelancer'
    elif employment_type == 'CT':
        return 'Contratado'
    elif employment_type == 'PT':
        return 'Part Time'
    elif employment_type == 'FT':
        return 'Full Time'


def company_size_to_text(company_size):
    if company_size == 'S':
        return 'Empresa de Pequeno Porte'
    elif company_size == 'L':
        return 'Empresa de Grande Porte'
    elif company_size == 'M':
        return 'Empresa de Médio Porte'


df['job_category'] = df['job_title'].apply(group_job_title)
df['company_country'] = df['company_location'].apply(country_name)
df['employee_country'] = df['employee_residence'].apply(country_name)
df['experience_level'] = df['experience_level'].apply(experience_level_to_num)
df['work_year'] = df['work_year'].apply(work_year_to_num)
df['employment_type'] = df['employment_type'].apply(employment_type_to_num)
df['company_size'] = df['company_size'].apply(company_size_to_text)

job_category_counts = df.value_counts('job_category', normalize=True) * 100
salary_by_job_category = df.groupby('job_category', as_index=True)['salary_in_usd'].mean().sort_values()
salary_by_country = df.groupby('company_country', as_index=True)['salary_in_usd'].mean().sort_values()
salary_by_experience_level = df.groupby('experience_level', as_index=True)['salary_in_usd'].mean()
employee_by_total = df.groupby('employee_residence', as_index=True)['employee_residence'].count()
company_size_counts = df.groupby('company_size', as_index=True)['company_size'].count()

plt.figure(figsize=(10, 5))
plt.barh(job_category_counts.index, job_category_counts.values, color='blue')
plt.xlabel('% de empregos')
plt.ylabel('Categoria de empregos')
plt.suptitle('Porcentagem de categoria de emprego')

plt.figure(figsize=(10, 5))
sns.barplot(x=salary_by_job_category.index, y=salary_by_job_category.values * 1e-5, color='blue')
plt.ylabel('Salário Anual (100K)')
plt.xlabel('Categoria de empregos')
plt.suptitle('Média salarial por categoria de emprego')

plt.figure(figsize=(12, 6))
sns.barplot(x=salary_by_country.index, y=salary_by_country.values * 1e-5, color='blue')
plt.ylabel('Salário Anual (100K)')
plt.xlabel('Pais da Empresa')
plt.xticks(rotation=90)
plt.tight_layout()
plt.suptitle('Paises que pagam mais')

plt.figure(figsize=(10, 5))
sns.barplot(x=salary_by_experience_level.index, y=salary_by_experience_level.values * 1e-5, color='blue')
plt.ylabel('Salário Anual (100K)')
plt.xlabel('Nível de Experiência')
plt.suptitle('Média salarial por nível de experiência')

plt.figure(figsize=(12, 6))
sns.barplot(x=employee_by_total.index, y=employee_by_total.values, color='blue')
plt.ylabel('Quantidade')
plt.xlabel('Pais do Empregado')
plt.xticks(rotation=90)
plt.tight_layout()
plt.suptitle('Quantidade de funcionarios por pais')

labels = company_size_counts.index
sizes = company_size_counts.values
explode = (0.1, 0, 0)
cor = ['#FF0000', '#00008B', '#FF1493']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90, colors=cor )
ax1.axis('equal')
plt.suptitle("Porcentagem do porte das empresas na área tecnológica")
plt.show()
# endregion

if __name__ == '__main__':
    app.run_server(debug=True)
