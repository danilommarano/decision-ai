import json
import pandas as pd

# Carregar arquivos
with open("data/json/prospects.json", "r", encoding='utf-8') as f:
    prospects = json.load(f)

with open("data/json/vagas.json", "r", encoding='utf-8') as f:
    jobs = json.load(f)

with open("data/json/applicants.json", "r", encoding='utf-8') as f:
    applicants = json.load(f)

# Criar lista para montar o DataFrame
registros = []

jobs_list = []
for job_id, data in jobs.items():
    informacoes = data.get("informacoes_basicas", {})
    perfil = data.get("perfil_vaga", {})
    beneficios = data.get("beneficios", {})

    registro = {
        "id_vaga": job_id,
        **informacoes,
        **perfil,
        **beneficios
    }

    jobs_list.append(registro)

df_job = pd.DataFrame(jobs_list)
df_job.to_csv("data/csv/vagas.csv", encoding='utf-8')

applicants_list = []
for applicant_id, data in applicants.items():
    infos_basicas = data.get("infos_basicas", {})
    informacoes_pessoais = data.get("informacoes_pessoais", {})
    informacoes_profissionais = data.get("informacoes_profissionais", {})
    formacao_e_idiomas = data.get("formacao_e_idiomas", {})
    cargo_atual = data.get("cargo_atual", {})
    cv_pt = data.get("cv_pt", {})
    cv_en = data.get("cv_en", {})

    registro = {
        "id_candidato": applicant_id,
        **infos_basicas,
        **informacoes_pessoais,
        **informacoes_profissionais,
        **formacao_e_idiomas,
        **cargo_atual,
        'cv_pt': cv_pt,
        'cv_en': cv_en,
    }

    applicants_list.append(registro)

df_applicant = pd.DataFrame(applicants_list)
df_applicant.to_csv("data/csv/candidatos.csv", encoding='utf-8')


prospects_list = []
for prospect_id, data in prospects.items():
    for prospect in data["prospects"]:
        registro = {
            "id_vaga": prospect_id,
            "titulo": data.get("titulo", None),
            "modalidade": data.get("modalidade", None),
            **prospect,
        }
        prospects_list.append(registro)

df_prospect = pd.DataFrame(prospects_list)
df_prospect.to_csv("data/csv/prospect.csv", encoding='utf-8')

df_merge1 = df_prospect.merge(df_job, on="id_vaga", how="left")
df_merge1["codigo"] = df_merge1["codigo"].astype(str)
df_applicant["id_candidato"] = df_applicant["id_candidato"].astype(str)
df_final = df_merge1.merge(df_applicant, left_on="codigo", right_on="id_candidato", how="left")
df_final.to_csv("data/final.csv", encoding='utf-8')
