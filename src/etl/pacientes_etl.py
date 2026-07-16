"""
ETL para dados de pacientes - Dashboard Hospitalar
Extrai, transforma e carrega dados de exemplo para o Power BI
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações
RANDOM_SEED = 42
NUM_PACIENTES = 1000
NUM_INTERNACOES = 5000

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Especialidades médicas
ESPECIALIDADES = [
    'Cardiologia', 'Ortopedia', 'Neurologia', 'Pediatria',
    'Oncologia', 'Gastroenterologia', 'Pneumologia', 'Nefrologia'
]

# Regiões
REGIOES = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']

def gerar_pacientes(n: int) -> pd.DataFrame:
    """Gera dataset anonimizado de pacientes"""

    pacientes = {
        'Id_Paciente': range(1, n + 1),
        'Idade': np.random.randint(1, 100, n),
        'Sexo': np.random.choice(['M', 'F'], n),
        'Regiao': np.random.choice(REGIOES, n),
        'Tipo_Sanguineo': np.random.choice(
            ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], n
        ),
        'Peso_kg': np.round(np.random.normal(70, 15, n), 1),
        'Altura_m': np.round(np.random.normal(1.68, 0.1, n), 2),
    }

    df = pd.DataFrame(pacientes)

    # Adicionar IMC
    df['IMC'] = np.round(
        df['Peso_kg'] / (df['Altura_m'] ** 2), 1
    )

    # Faixa etária
    df['Faixa_Etaria'] = pd.cut(
        df['Idade'],
        bins=[0, 12, 18, 60, 100],
        labels=['Criança', 'Adolescente', 'Adulto', 'Idoso']
    )

    return df

def gerar_internacoes(pacientes_df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Gera dataset de internações"""

    internacoes = []
    data_base = datetime(2024, 1, 1)

    for i in range(n):
        id_paciente = random.choice(pacientes_df['Id_Paciente'].tolist())
        paciente = pacientes_df[pacientes_df['Id_Paciente'] == id_paciente].iloc[0]

        # Data de entrada
        dias_offset = random.randint(0, 730)  # 2 anos
        data_entrada = data_base + timedelta(days=dias_offset)

        # Duração da internação (baseada em idade e especialidade)
        especialidade = random.choice(ESPECIALIDADES)
        if especialidade in ['Cardiologia', 'Neurologia', 'Oncologia']:
            duracao = random.randint(5, 30)
        elif especialidade in ['Ortopedia', 'Pediatria']:
            duracao = random.randint(1, 10)
        else:
            duracao = random.randint(2, 15)

        data_alta = data_entrada + timedelta(days=duracao)

        # Tempo de espera (em horas)
        tempo_espera = random.randint(0, 48)

        # Custo (baseado na especialidade e duração)
        custo_base = {
            'Cardiologia': 5000, 'Neurologia': 6000, 'Oncologia': 8000,
            'Ortopedia': 4000, 'Pediatria': 3000, 'Gastroenterologia': 3500,
            'Pneumologia': 4500, 'Nefrologia': 5500
        }
        custo = custo_base[especialidade] + (duracao * 500) + random.randint(-500, 500)

        # Readmissão (10% de chance)
        readmissao = 1 if random.random() < 0.10 else 0

        internacao = {
            'Id_Internacao': i + 1,
            'Id_Paciente': id_paciente,
            'Data_Entrada': data_entrada.strftime('%Y-%m-%d'),
            'Data_Alta': data_alta.strftime('%Y-%m-%d') if random.random() > 0.05 else None,
            'Dias_Internacao': duracao,
            'Tempo_Espera_Horas': tempo_espera,
            'Especialidade': especialidade,
            'Custo_Procedimento': round(custo, 2),
            'Readmissao_Flag': readmissao,
            'Id_Medico': random.randint(1, 50),
            'Leito': f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(101, 420)}",
        }

        internacoes.append(internacao)

    return pd.DataFrame(internacoes)

def gerar_medicos(n: int) -> pd.DataFrame:
    """Gera dataset de médicos"""

    medicos = {
        'Id_Medico': range(1, n + 1),
        'Nome': [f'Médico {i}' for i in range(1, n + 1)],
        'Especialidade_Principal': np.random.choice(ESPECIALIDADES, n),
        'CRM': [f'{random.randint(10000, 99999)}-SP' for _ in range(n)],
        'Ano_Formacao': np.random.randint(1980, 2024, n),
    }

    return pd.DataFrame(medicos)

def gerar_leitos() -> pd.DataFrame:
    """Gera dataset de leitos disponíveis"""

    leitos = []
    for unidade in ['UTI Adulto', 'UTI Pediátrica', 'Enfermaria A', 'Enfermaria B', 'Obstetrícia']:
        qtd_leitos = random.randint(20, 50)
        for i in range(qtd_leitos):
            leitos.append({
                'Id_Leito': f"{unidade[:3].upper()}{i+1:03d}",
                'Unidade': unidade,
                'Tipo': 'UTI' if 'UTI' in unidade else 'Enfermaria',
                'Quantidade_Leitos': qtd_leitos,
            })

    return pd.DataFrame(leitos).drop_duplicates(subset=['Id_Leito'])

def salvar_datasets():
    """Gera e salva todos os datasets"""

    print("Gerando pacientes...")
    pacientes = gerar_pacientes(NUM_PACIENTES)

    print("Gerando internações...")
    internacoes = gerar_internacoes(pacientes, NUM_INTERNACOES)

    print("Gerando médicos...")
    medicos = gerar_medicos(50)

    print("Gerando leitos...")
    leitos = gerar_leitos()

    # Salvar arquivos
    print("Salvando arquivos...")
    pacientes.to_csv('data/pacientes_sample.csv', index=False, encoding='utf-8')
    internacoes.to_csv('data/internacoes_sample.csv', index=False, encoding='utf-8')
    medicos.to_csv('data/medicos_sample.csv', index=False, encoding='utf-8')
    leitos.to_csv('data/leitos_sample.csv', index=False, encoding='utf-8')

    print("\n✅ Datasets gerados com sucesso!")
    print(f"  - Pacientes: {len(pacientes)} registros")
    print(f"  - Internações: {len(internacoes)} registros")
    print(f"  - Médicos: {len(medicos)} registros")
    print(f"  - Leitos: {len(leitos)} registros")

if __name__ == '__main__':
    salvar_datasets()