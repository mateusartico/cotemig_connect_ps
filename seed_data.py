#!/usr/bin/env python3

from app import create_app
from app.core.database_singleton import database
from app.core.factory import EntityFactoryProvider
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.monitoria_repository import MonitoriaRepository
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    
    with app.app_context():

        # Recria o banco
        database.drop_all()
        database.create_all()
        

        usuario_repo = UsuarioRepository()
        disciplina_repo = DisciplinaRepository()
        monitoria_repo = MonitoriaRepository()
        
        print("Criando usuários...")
        
        # essa conta é só pra teste
        admin = EntityFactoryProvider.create_entity('usuario',
            nome='Administrador',
            email='admin@cotemig.com.br',
            tipo='admin',
            senha='admin123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(admin)
        

        monitor1 = EntityFactoryProvider.create_entity('usuario',
            nome='Mateus Artico',
            email='monitor-mateusartico@cotemig.com.br',
            tipo='monitor',
            senha='monitor123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(monitor1)
        
        monitor2 = EntityFactoryProvider.create_entity('usuario',
            nome='Ana Elisa',
            email='monitor-anaelisa@cotemig.com.br',
            tipo='monitor',
            senha='monitor123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(monitor2)
        

        aluno1 = EntityFactoryProvider.create_entity('usuario',
            nome='Daniel',
            email='22301461@aluno.cotemig.com.br',
            tipo='aluno',
            senha='aluno123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(aluno1)
        
        aluno2 = EntityFactoryProvider.create_entity('usuario',
            nome='Giovanni',
            email='22302832@aluno.cotemig.com.br',
            tipo='aluno',
            senha='aluno123',
            verificado=True,
            ativo=True
        )
        usuario_repo.save(aluno2)
        
        print("Criando disciplinas...")
        

        disciplinas_data = [
            {'nome': 'Front End', 'codigo': 'FRONT', 'categoria': 'Design'},
            {'nome': 'Banco de Dados', 'codigo': 'BD1', 'categoria': 'Banco de Dados'},
            {'nome': 'Lógica de Programação', 'codigo': 'LOGP', 'categoria': 'Programação'},
            {'nome': 'Ambientes Computacionais', 'codigo': 'AMBCOM', 'categoria': 'Redes'},
            {'nome': 'Banco de Dados 2', 'codigo': 'BD2', 'categoria': 'Banco de Dados'},
            {'nome': 'Técnicas de Programação Avançada', 'codigo': 'TPA', 'categoria': 'Programação'},
            {'nome': 'Redes de Computadores', 'codigo': 'REDES', 'categoria': 'Redes'},
            {'nome': 'Programação Orientada a Objetos', 'codigo': 'POO', 'categoria': 'Programação'},
        ]
        
        disciplinas = []
        for disc_data in disciplinas_data:
            disciplina = EntityFactoryProvider.create_entity('disciplina', **disc_data)
            disciplina_repo.save(disciplina)
            disciplinas.append(disciplina)
        
        print("Criando monitorias...")
        

        # Monitorias para os próximos dias
        base_date = datetime.now() + timedelta(days=1)
        
        monitorias_data = [
            {
                'titulo': 'Monitoria Primeiro Ano',
                'descricao': 'Monitoria básica sobre lógica de programação em portugol',
                'data_hora': base_date + timedelta(hours=1),
                'duracao': 60,
                'vagas_total': 20,
                'local': 'Lab 1',
                'tags': 'portugol,programacao,basico',
                'monitor_id': monitor1.id,
                'disciplina_id': disciplinas[0].id
            },
            {
                'titulo': 'Monitoria Ajuda Pit',
                'descricao': 'Monitoria para ajudar os grupos a finalizarem o pit',
                'data_hora': base_date + timedelta(hours=3),
                'duracao': 70,
                'vagas_total': 50,
                'local': 'Lab 2',
                'tags': 'pit,banco,avancado',
                'monitor_id': monitor2.id,
                'disciplina_id': disciplinas[1].id
            }

        ]
        
        for monitoria_data in monitorias_data:
            monitoria = EntityFactoryProvider.create_entity('monitoria', **monitoria_data)
            monitoria_repo.save(monitoria)
        
        print("[OK] Banco de dados populado com sucesso!")
        print("\nUsuários criados:")
        print("Admin: admin@cotemig.com.br / admin123")
        print("Monitor 1: monitor-mateusartico@cotemig.com.br / monitor123")
        print("Monitor 2: monitor-anaelisa@cotemig.com.br / monitor123")
        print("Aluno 1: 22301461@aluno.cotemig.com.br / aluno123")
        print("Aluno 2: 22302832@aluno.cotemig.com.br / aluno123")
        print(f"\n[AVISO] {len(disciplinas)} disciplinas criadas")
        print(f"[AVISO] {len(monitorias_data)} monitorias criadas")

if __name__ == '__main__':
    seed_database()