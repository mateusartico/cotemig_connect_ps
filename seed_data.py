#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de teste
"""
from app import create_app
from app.core.database_singleton import database
from app.core.factory import EntityFactoryProvider
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.monitoria_repository import MonitoriaRepository
from datetime import datetime, timedelta

def seed_database():
    """Popula o banco com dados de teste"""
    app = create_app()
    
    with app.app_context():
        # Limpar dados existentes
        database.drop_all()
        database.create_all()
        
        # Repositories
        usuario_repo = UsuarioRepository()
        disciplina_repo = DisciplinaRepository()
        monitoria_repo = MonitoriaRepository()
        
        print("Criando usuários...")
        
        # Admin
        admin = EntityFactoryProvider.create_entity('usuario',
            nome='Administrador',
            email='admin@cotemig.com.br',
            tipo='admin',
            senha='admin123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(admin)
        
        # Monitores
        monitor1 = EntityFactoryProvider.create_entity('usuario',
            nome='João Silva',
            email='joao.silva@cotemig.com.br',
            tipo='monitor',
            senha='monitor123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(monitor1)
        
        monitor2 = EntityFactoryProvider.create_entity('usuario',
            nome='Ana Costa',
            email='ana.costa@cotemig.com.br',
            tipo='monitor',
            senha='monitor123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(monitor2)
        
        # Alunos
        aluno1 = EntityFactoryProvider.create_entity('usuario',
            nome='Maria Santos',
            email='maria.santos@aluno.cotemig.com.br',
            tipo='aluno',
            senha='aluno123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(aluno1)
        
        aluno2 = EntityFactoryProvider.create_entity('usuario',
            nome='Pedro Oliveira',
            email='pedro.oliveira@aluno.cotemig.com.br',
            tipo='aluno',
            senha='aluno123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(aluno2)
        
        print("Criando disciplinas...")
        
        # Disciplinas
        disciplinas_data = [
            {'nome': 'Programação I', 'codigo': 'PROG1', 'categoria': 'Programação'},
            {'nome': 'Banco de Dados', 'codigo': 'BD1', 'categoria': 'Banco de Dados'},
            {'nome': 'Estruturas de Dados', 'codigo': 'ED1', 'categoria': 'Programação'},
            {'nome': 'Redes de Computadores', 'codigo': 'REDES1', 'categoria': 'Redes'},
            {'nome': 'Engenharia de Software', 'codigo': 'ES1', 'categoria': 'Engenharia'},
            {'nome': 'Matemática Discreta', 'codigo': 'MAT1', 'categoria': 'Matemática'},
        ]
        
        disciplinas = []
        for disc_data in disciplinas_data:
            disciplina = EntityFactoryProvider.create_entity('disciplina', **disc_data)
            disciplina_repo.save(disciplina)
            disciplinas.append(disciplina)
        
        print("Criando monitorias...")
        
        # Monitorias
        base_date = datetime.now() + timedelta(days=1)
        
        monitorias_data = [
            {
                'titulo': 'Introdução ao Python',
                'descricao': 'Monitoria básica de Python para iniciantes',
                'data_hora': base_date + timedelta(hours=1),
                'duracao': 90,
                'vagas_total': 15,
                'local': 'Lab 1',
                'tags': 'python,programacao,basico',
                'monitor_id': monitor1.id,
                'disciplina_id': disciplinas[0].id
            },
            {
                'titulo': 'SQL Avançado',
                'descricao': 'Consultas complexas e otimização de queries',
                'data_hora': base_date + timedelta(hours=3),
                'duracao': 120,
                'vagas_total': 12,
                'local': 'Lab 2',
                'tags': 'sql,banco,avancado',
                'monitor_id': monitor2.id,
                'disciplina_id': disciplinas[1].id
            },
            {
                'titulo': 'Algoritmos de Ordenação',
                'descricao': 'Implementação e análise de algoritmos de ordenação',
                'data_hora': base_date + timedelta(days=1, hours=2),
                'duracao': 90,
                'vagas_total': 10,
                'local': 'Lab 3',
                'tags': 'algoritmos,ordenacao,estruturas',
                'monitor_id': monitor1.id,
                'disciplina_id': disciplinas[2].id
            },
            {
                'titulo': 'Configuração de Redes',
                'descricao': 'Configuração básica de switches e roteadores',
                'data_hora': base_date + timedelta(days=2, hours=1),
                'duracao': 150,
                'vagas_total': 8,
                'local': 'Lab Redes',
                'tags': 'redes,configuracao,cisco',
                'monitor_id': monitor2.id,
                'disciplina_id': disciplinas[3].id
            },
            {
                'titulo': 'Padrões de Projeto',
                'descricao': 'Design Patterns mais utilizados na programação',
                'data_hora': base_date + timedelta(days=3, hours=2),
                'duracao': 120,
                'vagas_total': 20,
                'local': 'Auditório',
                'tags': 'padroes,design,software',
                'monitor_id': monitor1.id,
                'disciplina_id': disciplinas[4].id
            }
        ]
        
        for monitoria_data in monitorias_data:
            monitoria = EntityFactoryProvider.create_entity('monitoria', **monitoria_data)
            monitoria_repo.save(monitoria)
        
        print("✅ Banco de dados populado com sucesso!")
        print("\n📋 Usuários criados:")
        print("👤 Admin: admin@cotemig.com.br / admin123")
        print("👨‍🏫 Monitor 1: joao.silva@cotemig.com.br / monitor123")
        print("👨‍🏫 Monitor 2: ana.costa@cotemig.com.br / monitor123")
        print("👨‍🎓 Aluno 1: maria.santos@aluno.cotemig.com.br / aluno123")
        print("👨‍🎓 Aluno 2: pedro.oliveira@aluno.cotemig.com.br / aluno123")
        print(f"\n📚 {len(disciplinas)} disciplinas criadas")
        print(f"📅 {len(monitorias_data)} monitorias criadas")

if __name__ == '__main__':
    seed_database()